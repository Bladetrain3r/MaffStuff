const size = 1000;
const canvas = document.getElementById('collatzCanvas');
const ctx = canvas.getContext('2d');
canvas.width = size;
canvas.height = size;

// Initialize grid (2D array or flat array)
let grid = new Int32Array(size * size);
// Initialize all to 0 except center
for (let i = 0; i < size * size; i++) {
  grid[i] = 0;
}
const center = (Math.floor(size/2) * size) + Math.floor(size/2);
grid[center] = 1000000; // seed value

function update() {
  const newGrid = new Int32Array(size * size);
  const imageData = ctx.createImageData(size, size);
  const data = imageData.data;

  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      const idx = y * size + x;
      const n = grid[idx];

      // Collatz update
      let f;
      if (n % 2 === 0) {
        f = n / 2;
      } else {
        f = 3 * n + 1;
      }

      newGrid[idx] = f;

      // Determine alive or dead
      // alive if f > n, dead if f < n
      const alive = (f > n);
      const color = alive ? 255 : 0;

      // Set pixel color: grayscale (color, color, color, 255)
      const pixelBase = idx * 4;
      data[pixelBase] = color;     // R
      data[pixelBase+1] = color;   // G
      data[pixelBase+2] = color;   // B
      data[pixelBase+3] = 255;     // A
    }
  }

  grid = newGrid;
  ctx.putImageData(imageData, 0, 0);

  requestAnimationFrame(update);
}

requestAnimationFrame(update);
