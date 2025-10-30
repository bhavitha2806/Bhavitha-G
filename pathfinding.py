import tkinter as tk
import heapq
import time

# Maze layout
# S = Start, G = Goal, # = Wall, . = Path
maze = [
    ['S', '.', '.', '#', '.', '.', '.'],
    ['#', '#', '.', '#', '.', '#', '.'],
    ['.', '.', '.', '.', '.', '#', '.'],
    ['.', '#', '#', '#', '.', '.', '.'],
    ['.', '.', '.', '#', '.', '#', 'G']
]

# Directions (Up, Down, Left, Right)
moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Start and Goal
start = (0, 0)
goal = (4, 6)

# Cell size
CELL_SIZE = 60

# Heuristic function (Manhattan Distance)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Greedy Best First Search Algorithm
def greedy_best_first_search(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    open_list = []
    heapq.heappush(open_list, (heuristic(start, goal), start))
    came_from = {}
    visited = set()

    while open_list:
        _, current = heapq.heappop(open_list)
        if current == goal:
            break

        visited.add(current)
        for move in moves:
            neighbor = (current[0] + move[0], current[1] + move[1])

            if (0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and
                maze[neighbor[0]][neighbor[1]] != "#" and neighbor not in visited):

                if neighbor not in [n for _, n in open_list]:
                    came_from[neighbor] = current
                    heapq.heappush(open_list, (heuristic(neighbor, goal), neighbor))

    # Reconstruct path
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return []
    path.append(start)
    path.reverse()
    return path

# Tkinter GUI setup
root = tk.Tk()
root.title("Pac-Man Pathfinding using GBFS")

canvas = tk.Canvas(root, width=700, height=400, bg="black")
canvas.pack()

# Draw the maze grid
def draw_maze():
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            x1, y1 = j * CELL_SIZE, i * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            color = "white"

            if maze[i][j] == "#":
                color = "gray"
            elif maze[i][j] == "S":
                color = "blue"
            elif maze[i][j] == "G":
                color = "red"
            else:
                color = "black"

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="white")

# Animate Pac-Man moving along the path
def animate_path(path):
    pacman = canvas.create_oval(0, 0, CELL_SIZE, CELL_SIZE, fill="yellow")
    for (i, j) in path:
        x = j * CELL_SIZE + CELL_SIZE / 2
        y = i * CELL_SIZE + CELL_SIZE / 2
        canvas.coords(pacman, x - 20, y - 20, x + 20, y + 20)
        root.update()
        time.sleep(0.4)
    canvas.create_text(350, 350, text="Goal Reached!", fill="white", font=("Arial", 16, "bold"))

# Run the visualization
def start_pathfinding():
    draw_maze()
    path = greedy_best_first_search(maze, start, goal)
    if path:
        animate_path(path)
    else:
        canvas.create_text(350, 350, text="No Path Found!", fill="red", font=("Arial", 16, "bold"))

# Start Button
start_button = tk.Button(root, text="Start Pathfinding", font=("Arial", 14), bg="green", fg="white", command=start_pathfinding)
start_button.pack(pady=10)

root.mainloop()




