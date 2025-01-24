import tkinter as tk
import random
from collections import deque
from sdffs import create_maze

def find_path_bfs(maze):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    start, exit = (1, 1), (len(maze) - 2, len(maze[0]) - 2)
    queue = deque([start])
    visited = {start}
    parent = {}

    while queue:
        x, y = queue.popleft()
        if (x, y) == exit:
            path = []
            while (x, y) in parent:
                path.append((x, y))
                x, y = parent[(x, y)]
            return [(1, 1)] + path[::-1]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0 and (nx, ny) not in visited:
                queue.append((nx, ny))
                visited.add((nx, ny))
                parent[(nx, ny)] = (x, y)

    return []

class Maze:
    def __init__(self, grid):
        self.grid = grid

    def can_move_to(self, x, y):
        if 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0]):
            return self.grid[x][y] == 0
        return False

class MazeVisualizer:
    def __init__(self, maze, path):
        self.maze = maze
        self.path = path
        self.cell_size = 30
        self.window = tk.Tk()
        self.window.title("Bludiště")
        self.canvas = tk.Canvas(
            self.window,
            width=len(maze.grid[0]) * self.cell_size,
            height=len(maze.grid) * self.cell_size,
        )
        self.canvas.pack()
        self.robot_icon = None

    def draw_maze(self):
        for i, row in enumerate(self.maze.grid):
            for j, cell in enumerate(row):
                color = "black" if cell == 1 else "white"
                if (i, j) == (len(self.maze.grid) - 2, len(self.maze.grid[0]) - 2):
                    color = "green"
                self.canvas.create_rectangle(
                    j * self.cell_size,
                    i * self.cell_size,
                    (j + 1) * self.cell_size,
                    (i + 1) * self.cell_size,
                    fill=color,
                    outline="gray",
                )

    def draw_robot(self, x, y):
        if self.robot_icon:
            self.canvas.delete(self.robot_icon)
        self.robot_icon = self.canvas.create_oval(
            y * self.cell_size + 5,
            x * self.cell_size + 5,
            (y + 1) * self.cell_size - 5,
            (x + 1) * self.cell_size - 5,
            fill="red",
        )

    def animate_robot(self):
        for x, y in self.path:
            if self.maze.can_move_to(x, y):
                self.draw_robot(x, y)
                self.window.update()
                self.window.after(400)

    def show(self):
        self.draw_maze()
        if self.path:
            self.animate_robot()
        else:
            print("Žádná cesta")
        self.window.mainloop()

if __name__ == "__main__":
    width, height = 21, 21
    grid = create_maze(width, height)
    maze = Maze(grid)
    path = find_path_bfs(grid)

    visualizer = MazeVisualizer(maze, path)
    visualizer.show()