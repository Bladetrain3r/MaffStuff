import math
import sys
import os
import json
import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class CollatzSphereVisualizer:
    def __init__(self, config_path='collatz_sphere_config.json'):
        # Load configuration
        try:
            with open(config_path, 'r') as config_file:
                self.config = json.load(config_file)
        except FileNotFoundError:
            print(f"Config file {config_path} not found, using defaults")
            self.config = {
                "width": 1280,
                "height": 1280,
                "max_iterations": 320,
                "resolution": 0.015,
                "camera": {
                    "initial_position": [0, 0, -10],
                    "initial_rotation": [30, 0, 0],
                    "auto_rotate": {
                        "enabled": False,
                        "speed_x": 0.5,
                        "speed_y": 0.5
                    }
                },
                "color": {
                    "max_power_norm": 64.0,
                    "max_value_norm": 32.0,
                    "value_weight": 0.6,
                    "z_weight": 0.5,
                    "step_weight": 1.0
                }
            }
        
        # Initialize visualization parameters
        self.scale = self.config.get('scale', 40.0)
        self.max_iterations = self.config['max_iterations']
        self.resolution = self.config['resolution']
        
        # Color mapping parameters
        self.color_params = self.config.get('color', {
            'max_power_norm': 64.0,
            'max_value_norm': 32.0,
            'value_weight': 0.6,
            'z_weight': 0.5,
            'step_weight': 1.0
        })
        
        # Camera settings
        self.camera_pos = self.config['camera'].get('initial_position', [0, 0, -10])
        self.rotation = self.config['camera'].get('initial_rotation', [30, 0, 0])
        
        # Auto-rotation settings
        auto_rotate = self.config['camera'].get('auto_rotate', {})
        self.auto_rotate = auto_rotate.get('enabled', False)
        self.auto_rotate_speed = [
            auto_rotate.get('speed_x', 0.5),
            auto_rotate.get('speed_y', 0.5)
        ]
        
        # Performance optimization
        self.cache = {}
        self.points = None
        self.colors = None
        
        # Pygame and OpenGL setup
        pygame.init()
        display = (self.config.get('width', 1280), self.config.get('height', 1280))
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Collatz 3D Sphere Visualization")

    def is_power_of_two(self, n):
        return n > 0 and (n & (n - 1)) == 0

    def calculate_stopping_time(self, n):
        if n in self.cache:
            return self.cache[n]
            
        if n < 1:
            return None
            
        steps = 0
        current = n
        max_value = n
        power_two_steps = 0
        seen = set()
        first_power = None
        
        while not self.is_power_of_two(current) and steps < self.max_iterations and current not in seen:
            seen.add(current)
            if current % 2 == 0:
                current //= 2
            else:
                current = 3 * current + 1
                max_value = max(max_value, current)
            steps += 1
        
        if self.is_power_of_two(current):
            first_power = current
            power_two_steps = int(math.log2(current))
        
        result = {
            'steps': steps,
            'power_steps': power_two_steps,
            'max_value': max_value,
            'converged': self.is_power_of_two(current),
            'first_power': first_power
        }
        
        self.cache[n] = result
        return result

    def get_color(self, result, z_coord):
        if not result or not result['converged']:
            return (0.2, 0.2, 0.2)
            
        # Normalize values
        steps_norm = min(1.0, result['steps'] / self.max_iterations)
        value_norm = min(1.0, math.log2(result['max_value']) / self.color_params['max_value_norm'])
        z_norm = (z_coord + 1) / 2
        
        # Default coloring
        return (
            steps_norm,
            value_norm * 0.5 + z_norm * 0.5,
            (1.0 - steps_norm) * z_norm
        )

    def generate_points(self):
        points = []
        colors = []
        
        print("Generating points...")
        total_points = int((2 * np.pi / self.resolution) * (np.pi / self.resolution))
        points_generated = 0
        
        for theta in np.arange(0, 2*np.pi, self.resolution):
            for phi in np.arange(0, np.pi, self.resolution):
                x = math.sin(phi) * math.cos(theta)
                y = math.sin(phi) * math.sin(theta)
                z = math.cos(phi)
                
                # Map spherical coordinates to a number
                n = self._map_to_number(x, y, z)
                result = self.calculate_stopping_time(n)
                color = self.get_color(result, z_coord=z)
                
                if result and result['converged']:
                    points.append((x, y, z))
                    colors.append(color)
                
                points_generated += 1
                if points_generated % 1000 == 0:
                    print(f"Progress: {points_generated}/{total_points} points ({(points_generated/total_points)*100:.1f}%)")
        
        print("Point generation complete!")
        return np.array(points, dtype=np.float32), np.array(colors, dtype=np.float32)

    def _map_to_number(self, x, y, z):
        r = math.sqrt(x*x + y*y + z*z)
        
        # Base mapping with some variation
        base_number = int(r * math.pow(2, self.scale))
        
        # Optional: Add some pattern-based adjustments
        patterns = {
            '101': 1.1,    # L-type harbor pattern
            '111': 0.9,    # Mersenne-like pattern
            '1010': 1.05,  # Alternating pattern
        }
        
        # Apply pattern-based adjustments
        for pattern, factor in patterns.items():
            if self._has_bit_pattern(base_number, pattern):
                base_number = int(base_number * factor)
        
        return max(1, base_number)

    def _has_bit_pattern(self, n, pattern):
        """Check if number contains specific binary pattern."""
        bin_str = bin(n)[2:]  # Convert to binary, remove '0b' prefix
        return pattern in bin_str

    def init_gl(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_POINT_SMOOTH)
        glPointSize(2.0)
        
        print("Generating points...")
        self.points, self.colors = self.generate_points()
        print(f"Generated {len(self.points)} points")

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Apply camera position
        glTranslatef(*self.camera_pos)
        
        # Apply rotations
        glRotatef(self.rotation[0], 1, 0, 0)  # Pitch
        glRotatef(self.rotation[1], 0, 1, 0)  # Yaw
        glRotatef(self.rotation[2], 0, 0, 1)  # Roll
        
        # Render points
        glBegin(GL_POINTS)
        for point, color in zip(self.points, self.colors):
            glColor3fv(color)
            glVertex3fv(point)
        glEnd()
        
        pygame.display.flip()

    def reshape(self, width, height):
        if height == 0:
            height = 1
            
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width/height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def run(self):
        self.init_gl()
        self.reshape(self.config.get('width', 1280), self.config.get('height', 1280))
        
        print("\nControls:")
        print("  Arrow keys: Rotate")
        print("  Page Up/Down: Zoom in/out")
        print("  A: Toggle auto-rotation")
        print("  R: Reset view")
        print("  Q or ESC: Quit")
        
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_r:
                        # Reset to initial configuration
                        self.camera_pos = self.config['camera'].get('initial_position', [0, 0, -10])
                        self.rotation = self.config['camera'].get('initial_rotation', [30, 0, 0])
                    elif event.key == pygame.K_PAGEUP:
                        self.camera_pos[2] += 1
                    elif event.key == pygame.K_PAGEDOWN:
                        self.camera_pos[2] -= 1
                    elif event.key == pygame.K_a:
                        self.auto_rotate = not self.auto_rotate
            
            # Handle rotation
            if self.auto_rotate:
                self.rotation[0] += self.auto_rotate_speed[0]
                self.rotation[1] += self.auto_rotate_speed[1]
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.rotation[1] -= 2
                if keys[pygame.K_RIGHT]:
                    self.rotation[1] += 2
                if keys[pygame.K_UP]:
                    self.rotation[0] -= 2
                if keys[pygame.K_DOWN]:
                    self.rotation[0] += 2
            
            self.display()
            clock.tick(60)
        
        pygame.quit()

def create_default_config():
    """Create a default configuration file if it doesn't exist."""
    default_config = {
        "width": 1280,
        "height": 1280,
        "max_iterations": 320,
        "resolution": 0.015,
        "scale": 40.0,
        "camera": {
            "initial_position": [0, 0, -10],
            "initial_rotation": [30, 0, 0],
            "auto_rotate": {
                "enabled": False,
                "speed_x": 0.5,
                "speed_y": 0.5
            }
        },
        "color": {
            "max_power_norm": 64.0,
            "max_value_norm": 32.0,
            "value_weight": 0.6,
            "z_weight": 0.5,
            "step_weight": 1.0
        }
    }
    
    config_path = 'collatz_sphere_config.json'
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=4)
        print(f"Created default configuration file: {config_path}")

def main():
    # Create default config if it doesn't exist
    create_default_config()
    
    # Initialize and run the visualization
    viz = CollatzSphereVisualizer()
    viz.run()

if __name__ == "__main__":
    main()