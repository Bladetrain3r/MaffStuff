#!/usr/bin/env python3
"""Headless Collatz sphere renderer.

A corrected, offscreen sibling of ``collatz_GPU.py``.  The interactive viewer
derived each point's number from the *radius* of a point on a unit sphere.
Radius is 1.0 everywhere on a unit sphere, so all five million points carried
the same integer; at the default scale the number also exceeded the overflow
guard, every point failed the convergence test, and the window drew nothing.

Here the number comes from position *on* the surface, which is what makes the
picture a picture of something.  Two layouts:

``uv``       one integer per pixel of a rows x cols raster wrapped onto the
             sphere: longitude carries the low bits of n, latitude the high
             bits.  With cols a power of two the residue structure of the
             stopping time shows up as vertical banding.  Per-pixel, so there
             is no lattice and no moire.
``lattice``  the original Fibonacci-lattice point cloud, index -> number.

The Collatz iteration still runs on the GPU, now in fp64 so trajectory peaks
above 2^32 stay exact, and without the ad-hoc bit-pattern multipliers that
used to bend the numbers before they were plotted.

Requires an EGL-capable GPU; no display is needed.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np


COLLATZ_GLSL = """
// Colour channels for one starting value.  Returns false if the trajectory
// did not reach 1 within the iteration budget or left the exact-integer range.
bool collatz_measure(double n0, int max_iterations,
                     out float steps_out, out float expansion_out,
                     out float odd_fraction_out, out float first_pow2_out) {
    double cur = n0;
    double peak = n0;
    int steps = 0;
    int odd_steps = 0;
    int last_odd = -1;

    for (int i = 0; i < max_iterations; i++) {
        if (cur == 1.0lf) {
            steps_out = float(steps);
            expansion_out = log2(float(peak / n0));
            odd_fraction_out = steps > 0 ? float(odd_steps) / float(steps) : 0.0;
            // After the final 3n+1 the value only halves, so it is a power of
            // two: the step after the last odd step is the first power of two.
            first_pow2_out = float(last_odd + 1);
            return true;
        }
        double half_cur = cur * 0.5lf;
        if (floor(half_cur) == half_cur) {
            cur = half_cur;
        } else {
            last_odd = steps;
            odd_steps++;
            cur = 3.0lf * cur + 1.0lf;
        }
        steps++;
        if (cur > peak) peak = cur;
        if (cur > 9007199254740992.0lf) break;   // 2^53, fp64 exactness limit
    }
    return false;
}

// Polynomial fit to viridis: perceptually uniform and colour-blind safe.
vec3 viridis(float t) {
    t = clamp(t, 0.0, 1.0);
    const vec3 c0 = vec3(0.2777273272, 0.0054929071, 0.3340998053);
    const vec3 c1 = vec3(0.1050930431, 1.4040130949, 1.3843792057);
    const vec3 c2 = vec3(-0.3308618287, 0.2148069211, 0.0947605920);
    const vec3 c3 = vec3(-4.6342885944, -5.7991747143, -19.3324241195);
    const vec3 c4 = vec3(6.2283287818, 14.1799802812, 56.6905367889);
    const vec3 c5 = vec3(4.7763213735, -13.7451315979, -65.3532350885);
    const vec3 c6 = vec3(-5.4354456840, 4.6458234300, 26.3124352495);
    return c0 + t * (c1 + t * (c2 + t * (c3 + t * (c4 + t * (c5 + t * c6)))));
}

float channel(int mode, float steps, float expansion,
              float odd_fraction, float first_pow2,
              float lo, float hi) {
    float v;
    if (mode == 0)      v = steps;
    else if (mode == 1) v = expansion;
    else if (mode == 2) v = odd_fraction;
    else                v = first_pow2;
    return clamp((v - lo) / max(hi - lo, 1e-6), 0.0, 1.0);
}
"""

UV_VERTEX = """
#version 400 core
layout(location = 0) in vec2 corner;
out vec2 vNdc;
void main() {
    vNdc = corner;
    gl_Position = vec4(corner, 0.0, 1.0);
}
"""

UV_FRAGMENT = """
#version 400 core

in vec2 vNdc;
out vec4 fragColor;

uniform float aspect;
uniform float tan_half_fov;
uniform float camera_distance;
uniform mat3 inv_rotation;
uniform double number_start;
uniform double number_stride;
uniform int cols;
uniform int rows;
uniform int max_iterations;
uniform int color_mode;
uniform int exclude_multiples_of_three;
uniform float range_lo;
uniform float range_hi;
uniform vec3 background;

const float PI = 3.14159265358979;

__COLLATZ__

void main() {
    vec3 origin = vec3(0.0, 0.0, camera_distance);
    vec3 dir = normalize(vec3(vNdc.x * aspect * tan_half_fov,
                              vNdc.y * tan_half_fov,
                              -1.0));

    float b = dot(origin, dir);
    float c = dot(origin, origin) - 1.0;
    float disc = b * b - c;
    if (disc < 0.0) { fragColor = vec4(background, 1.0); return; }

    float t = -b - sqrt(disc);
    if (t < 0.0) { fragColor = vec4(background, 1.0); return; }

    vec3 hit = origin + t * dir;          // world space, unit length
    vec3 obj = normalize(inv_rotation * hit);

    float v = acos(clamp(obj.y, -1.0, 1.0)) / PI;
    float u = atan(obj.z, obj.x) / (2.0 * PI) + 0.5;

    int row = clamp(int(v * float(rows)), 0, rows - 1);
    int col = clamp(int(u * float(cols)), 0, cols - 1);
    double n0 = number_start + double(row * cols + col) * number_stride;

    if (exclude_multiples_of_three == 1) {
        double third = n0 / 3.0lf;
        if (floor(third) == third) { fragColor = vec4(background, 1.0); return; }
    }

    float steps, expansion, odd_fraction, first_pow2;
    if (!collatz_measure(n0, max_iterations, steps, expansion,
                         odd_fraction, first_pow2)) {
        fragColor = vec4(background, 1.0);
        return;
    }

    float shade = channel(color_mode, steps, expansion, odd_fraction,
                          first_pow2, range_lo, range_hi);
    vec3 colour = viridis(shade);

    // Gentle diffuse term so the ball reads as a ball without eating the ramp.
    vec3 light = normalize(vec3(-0.4, 0.6, 0.9));
    float lambert = max(dot(hit, light), 0.0);
    colour *= 0.62 + 0.38 * lambert;

    fragColor = vec4(colour, 1.0);
}
"""

LATTICE_VERTEX = """
#version 400 core

layout(location = 0) in float index;

uniform mat4 mvp;
uniform float point_count;
uniform float point_size;
uniform double number_start;
uniform double number_stride;
uniform int max_iterations;
uniform int color_mode;
uniform int exclude_multiples_of_three;
uniform float range_lo;
uniform float range_hi;

out float vShade;

const float GOLDEN_ANGLE = 2.39996322972865332;

__COLLATZ__

void main() {
    float phi = acos(1.0 - 2.0 * (index + 0.5) / point_count);
    float theta = GOLDEN_ANGLE * index;
    float s = sin(phi);
    vec3 pos = vec3(cos(theta) * s, sin(theta) * s, cos(phi));

    // The fix: the number comes from the index, not from the radius.
    double n0 = number_start + double(index) * number_stride;

    bool drop = false;
    if (exclude_multiples_of_three == 1) {
        double third = n0 / 3.0lf;
        if (floor(third) == third) drop = true;
    }

    float steps, expansion, odd_fraction, first_pow2;
    if (drop || !collatz_measure(n0, max_iterations, steps, expansion,
                                 odd_fraction, first_pow2)) {
        gl_Position = vec4(0.0, 0.0, -100.0, 1.0);
        gl_PointSize = 0.0;
        vShade = 0.0;
        return;
    }

    vShade = channel(color_mode, steps, expansion, odd_fraction,
                     first_pow2, range_lo, range_hi);
    gl_Position = mvp * vec4(pos, 1.0);
    gl_PointSize = point_size;
}
"""

LATTICE_FRAGMENT = """
#version 400 core
in float vShade;
out vec4 fragColor;

__COLLATZ__

void main() {
    vec2 d = gl_PointCoord - vec2(0.5);
    if (dot(d, d) > 0.25) discard;
    fragColor = vec4(viridis(vShade), 1.0);
}
"""

MODE_NAMES = {0: "stopping time", 1: "expansion log2(peak/n)",
              2: "odd-step fraction", 3: "first power of two"}


def perspective(fovy_deg, aspect, near, far):
    f = 1.0 / math.tan(math.radians(fovy_deg) / 2.0)
    m = np.zeros((4, 4), dtype="f4")
    m[0, 0] = f / aspect
    m[1, 1] = f
    m[2, 2] = (far + near) / (near - far)
    m[2, 3] = (2.0 * far * near) / (near - far)
    m[3, 2] = -1.0
    return m


def look_at(eye, target, up):
    eye, target, up = (np.array(v, dtype="f8") for v in (eye, target, up))
    f = target - eye
    f /= np.linalg.norm(f)
    s = np.cross(f, up)
    s /= np.linalg.norm(s)
    u = np.cross(s, f)
    m = np.eye(4, dtype="f4")
    m[0, :3], m[1, :3], m[2, :3] = s, u, -f
    m[:3, 3] = -m[:3, :3] @ eye
    return m


def rotation_y(radians):
    c, s = math.cos(radians), math.sin(radians)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]], dtype="f8")


def rotation_x(radians):
    c, s = math.cos(radians), math.sin(radians)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]], dtype="f8")


def to_mat4(m3):
    m = np.eye(4, dtype="f4")
    m[:3, :3] = m3
    return m


def reference_measures(numbers, mode):
    """Vectorised CPU measurement; normalises the ramp and cross-checks the GPU."""
    current = numbers.astype(np.int64).copy()
    steps = np.zeros(len(numbers), dtype=np.int64)
    odd_steps = np.zeros(len(numbers), dtype=np.int64)
    peak = numbers.astype(np.int64).copy()
    last_odd = np.full(len(numbers), -1, dtype=np.int64)

    active = current != 1
    while active.any():
        cur = current[active]
        odd = (cur & 1).astype(bool)
        idx = np.flatnonzero(active)
        odd_idx = idx[odd]
        last_odd[odd_idx] = steps[odd_idx]
        odd_steps[odd_idx] += 1
        cur = np.where(odd, 3 * cur + 1, cur >> 1)
        current[active] = cur
        peak[active] = np.maximum(peak[active], cur)
        steps[active] += 1
        active = current != 1

    if mode == 0:
        return steps.astype(np.float64)
    if mode == 1:
        return np.log2(peak / numbers)
    if mode == 2:
        return np.where(steps > 0, odd_steps / np.maximum(steps, 1), 0.0)
    return (last_odd + 1).astype(np.float64)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--layout", choices=("uv", "lattice"), default="uv")
    p.add_argument("--cols", type=int, default=2048, help="uv: longitude cells (use a power of two)")
    p.add_argument("--rows", type=int, default=1024, help="uv: latitude cells")
    p.add_argument("--points", type=int, default=2_000_000, help="lattice: point count")
    p.add_argument("--start", type=int, default=1)
    p.add_argument("--stride", type=int, default=1)
    p.add_argument("--frames", type=int, default=1)
    p.add_argument("--width", type=int, default=1920)
    p.add_argument("--height", type=int, default=1080)
    p.add_argument("--supersample", type=int, default=2)
    p.add_argument("--point-size", type=float, default=1.6)
    p.add_argument("--max-iterations", type=int, default=1200)
    p.add_argument("--tilt", type=float, default=16.0)
    p.add_argument("--distance", type=float, default=2.55)
    p.add_argument("--percentile", type=float, default=1.0,
                   help="clip the colour ramp at this percentile from each end")
    p.add_argument("--exclude-multiples-of-three", action="store_true",
                   help="drop n divisible by 3: the values no trajectory ever enters")
    p.add_argument("--color-mode", type=int, default=0, choices=(0, 1, 2, 3))
    p.add_argument("--out", type=Path, default=Path("frames"))
    p.add_argument("--prefix", default="collatz")
    args = p.parse_args()

    import moderngl
    from PIL import Image

    count = args.rows * args.cols if args.layout == "uv" else args.points
    last = args.start + (count - 1) * args.stride
    sample_idx = np.linspace(0, count - 1, min(count, 250_000), dtype=np.int64)
    sample_n = args.start + sample_idx * args.stride
    measures = reference_measures(sample_n, args.color_mode)
    lo = float(np.percentile(measures, args.percentile))
    hi = float(np.percentile(measures, 100.0 - args.percentile))
    print(f"range: n in [{args.start}, {last}] step {args.stride}  ({count} values)")
    print(f"colour: {MODE_NAMES[args.color_mode]}  "
          f"p{args.percentile:g}={lo:.3f}  p{100 - args.percentile:g}={hi:.3f}  "
          f"min={measures.min():.3f} max={measures.max():.3f}")

    ctx = moderngl.create_standalone_context(backend="egl", require=400)
    print(f"gpu: {ctx.info['GL_RENDERER']}")

    ss = max(1, args.supersample)
    rw, rh = args.width * ss, args.height * ss
    colour_tex = ctx.texture((rw, rh), 4)
    depth = ctx.depth_renderbuffer((rw, rh))
    fbo = ctx.framebuffer(color_attachments=[colour_tex], depth_attachment=depth)
    fbo.use()
    ctx.viewport = (0, 0, rw, rh)
    background = (0.043, 0.047, 0.058)

    if args.layout == "uv":
        prog = ctx.program(vertex_shader=UV_VERTEX,
                           fragment_shader=UV_FRAGMENT.replace("__COLLATZ__", COLLATZ_GLSL))
        quad = np.array([-1, -1, 3, -1, -1, 3], dtype="f4")
        vao = ctx.vertex_array(prog, [(ctx.buffer(quad.tobytes()), "2f", "corner")])
        prog["aspect"].value = rw / rh
        prog["tan_half_fov"].value = math.tan(math.radians(45.0) / 2.0)
        prog["camera_distance"].value = args.distance
        prog["cols"].value = args.cols
        prog["rows"].value = args.rows
        prog["background"].value = background
    else:
        ctx.enable(moderngl.DEPTH_TEST | moderngl.PROGRAM_POINT_SIZE)
        prog = ctx.program(vertex_shader=LATTICE_VERTEX.replace("__COLLATZ__", COLLATZ_GLSL),
                           fragment_shader=LATTICE_FRAGMENT.replace("__COLLATZ__", COLLATZ_GLSL))
        indices = np.arange(args.points, dtype="f4")
        vao = ctx.vertex_array(prog, [(ctx.buffer(indices.tobytes()), "1f", "index")])
        prog["point_count"].value = float(args.points)
        prog["point_size"].value = args.point_size * ss

    prog["number_start"].value = float(args.start)
    prog["number_stride"].value = float(args.stride)
    prog["max_iterations"].value = args.max_iterations
    prog["color_mode"].value = args.color_mode
    prog["exclude_multiples_of_three"].value = 1 if args.exclude_multiples_of_three else 0
    prog["range_lo"].value = lo
    prog["range_hi"].value = hi

    proj = perspective(45.0, rw / rh, 0.1, 100.0)
    view = look_at((0.0, 0.0, args.distance), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0))
    tilt = rotation_x(math.radians(args.tilt))

    args.out.mkdir(parents=True, exist_ok=True)
    for frame in range(args.frames):
        angle = 2.0 * math.pi * frame / max(1, args.frames)
        rot = tilt @ rotation_y(angle)
        if args.layout == "uv":
            prog["inv_rotation"].write(np.ascontiguousarray(rot.T, dtype="f4").tobytes())
        else:
            prog["mvp"].write(np.ascontiguousarray((proj @ view @ to_mat4(rot)).T, dtype="f4").tobytes())

        fbo.clear(*background, 1.0)
        vao.render(mode=moderngl.TRIANGLES if args.layout == "uv" else moderngl.POINTS)

        image = Image.frombytes("RGBA", (rw, rh), fbo.read(components=4))
        image = image.transpose(Image.FLIP_TOP_BOTTOM).convert("RGB")
        if ss > 1:
            image = image.resize((args.width, args.height), Image.LANCZOS)
        path = args.out / f"{args.prefix}_{frame:03d}.png"
        image.save(path, optimize=True)
        print(f"  frame {frame + 1}/{args.frames} -> {path}")


if __name__ == "__main__":
    main()
