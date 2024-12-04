import ssd1306
import framebuf
from machine import I2C, Pin
import random
import time

def step(grid):
    """
    Computes one step of Conway's game of life on a toroidal 2D grid.
    Args:
        grid: 2D list representing the current grid state.
    Returns:
        2D list representing the next grid state.
    """
    height = len(grid)
    width = len(grid[0])
    new_grid = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            # Count live neighbors
            live_neighbors = sum(
                grid[(y + dy) % height][(x + dx) % width]
                for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                if not (dy == 0 and dx == 0)
            )

            # Apply Conway's Game of Life rules
            if grid[y][x] == 1 and live_neighbors in (2, 3):
                new_grid[y][x] = 1
            elif grid[y][x] == 0 and live_neighbors == 3:
                new_grid[y][x] = 1

    return new_grid

def init_grid(height, width):
    """
    Initializes a grid with random binary values.
    Args:
        height: Grid height.
        width: Grid width.
    Returns:
        2D list representing the grid.
    """
    return [[random.randint(0, 1) for _ in range(width)] for _ in range(height)]

def main():
    # I2C setup
    sda = Pin(0)
    scl = Pin(1)
    i2c = I2C(0, sda=sda, scl=scl, freq=400000)
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    
    # Grid setup
    width = 128
    height = 64
    grid = init_grid(height, width)

    frame_count = 0
    while True:
        t1 = time.ticks_ms()

        # Draw current state on the OLED
        display.fill(0)
        for y in range(height):
            for x in range(width):
                if grid[y][x] == 1:
                    display.pixel(x, y, 1)
        display.show()

        # Update the grid to the next state
        grid = step(grid)

        t2 = time.ticks_ms()
        frame_count += 1

        # Print frame time every 10 frames
        if frame_count == 10:
            print(f"Frame time: {time.ticks_diff(t2, t1)} ms")
            frame_count = 0

if __name__ == "__main__":
    main()
