import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import heapq
import time
import random
from datetime import datetime
from unittest import result
root = tk.Tk()
root.title("Search Visualizer")

# ---------- USER INPUT ----------
# rows = int(input("Enter rows: "))
# cols = int(input("Enter cols: "))
# rows = 5
# cols = 5
board = []
mode = "start"
start_pos = None
goal_pos = None
density = tk.DoubleVar()
execution_time = 0
nodes_expanded = 0
path_cost = 0

# ---------- TOP CONTROL FRAME ----------
control_frame = tk.Frame(root)
control_frame.pack(pady=10)

# Dropdown variable
algorithm_var = tk.StringVar()
algorithm_var.set("A* Search")   # default
heuristic_var = tk.StringVar()
heuristic_var.set("Manhattan Distance")   # default

dropdown_1 = ttk.Combobox(control_frame,
                        textvariable=algorithm_var,
                        values=["A* Search", "Greedy Best First Search"],
                        state="readonly")
dropdown_1.pack(side=tk.LEFT, padx=10)
dropdown_2 = ttk.Combobox(control_frame,
                        textvariable=heuristic_var,
                        values=["Manhattan Distance", "Euclidean Distance"],
                        state="readonly")
dropdown_2.pack(side=tk.LEFT, padx=10)

# Select Button
def select_algorithm():
    selected = algorithm_var.get()
    dynamic_map_with_obstacles(density.get())
    root.update()
    info_label.config(text=f"Running {selected}...")
    root.after(500)
    if selected == "A* Search":
        print("A* Search selected")
        a_star_search()
    elif selected == "Greedy Best First Search":
        print("Greedy Best First Search selected")
        greedy_best_first_search()
    return
select_btn = tk.Button(control_frame,
                       text="Select",
                       command=select_algorithm)
select_btn.pack(side=tk.LEFT)

info_label = tk.Label(root, text="Click the start box",
                      font=("Arial", 14))
info_label.pack(pady=10)

execution_time_label = tk.Label(root, text="Execution Time: N/A",
                                font=("Arial", 12))
execution_time_label.pack()
nodes_expanded_label = tk.Label(root, text="Nodes Expanded: N/A",
                                font=("Arial", 12))
nodes_expanded_label.pack()
path_cost_label = tk.Label(root, text="Path Cost: N/A",
                                font=("Arial", 12))
path_cost_label.pack()


# ---------- GRID FRAME ----------

grid_cells = []  # To store cell references for easy access
def map_generation():
    rows = tk.simpledialog.askinteger("Input", "Enter number of rows:", parent=root, minvalue=1)
    cols = tk.simpledialog.askinteger("Input", "Enter number of columns:", parent=root, minvalue=1)
    global density
    obstacles_density = tk.Scale(root,variable=density,from_=0, to=1, resolution=0.05, orient=tk.HORIZONTAL, label="Obstacles Density")
    obstacles_density.pack(pady=10)
    global board
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if (i, j) != start_pos and (i, j) != goal_pos:
                if random.random() < density.get():
                    board[i][j] = 1  # Mark as obstacle
    grid_frame = tk.Frame(root)
    grid_frame.pack()
    for i in range(rows):
        row_list = []
        for j in range(cols):
            cell = tk.Label(grid_frame,
                            width=6,
                            height=3,
                            bg="white",
                            borderwidth=1,
                            relief="solid",text=f"({i},{j})")
            cell.grid(row=i, column=j)
            cell.bind("<Button-1>",
                    lambda event, r=i, c=j: on_cell_click(event, r, c))
            row_list.append(cell)
        grid_cells.append(row_list)
    
def dynamic_map_with_obstacles(density):
    global board
    for i in range(len(board)):
        for j in range(len(board[0])):
            if (i, j) != start_pos and (i, j) != goal_pos:
                if random.random() < density:
                    board[i][j] = 1  # Mark as obstacle
                    grid_cells[i][j].config(bg="Black")
                else:
                    board[i][j] = 0  # Clear obstacle
                    grid_cells[i][j].config(bg="white")
def on_cell_click(event, r, c):
    global mode, start_pos, goal_pos

    if mode == "start":
        start_pos = (r, c)
        grid_cells[r][c].config(bg="Blue")
        board[r][c] = 2
        info_label.config(text="Click the goal box")
        mode = "goal"

    elif mode == "goal":
        # Prevent selecting same cell as start
        if (r, c) == start_pos:
            return

        goal_pos = (r, c)
        # print("Goal position set to:", goal_pos)
        grid_cells[r][c].config(bg="Green")
        board[r][c] = 3
        info_label.config(text="Ready to run algorithm, click to add/remove obstacles",font=("Arial", 11))
        mode = "obstacles"
    elif mode == "obstacles":
        # Toggle obstacle
        if board[r][c] == 0:
            board[r][c] = 1
            grid_cells[r][c].config(bg="Black")
        elif board[r][c] == 1:
            board[r][c] = 0
            grid_cells[r][c].config(bg="white")


def heuristic(a, b, type="Manhattan Distance"):
    if type == "Manhattan Distance":
        print("Manhattan Distance selected")
        print(f"Calculating Manhattan distance between {a} and {b}")
        print(f"Horizontal distance: {abs(a[0] - b[0])}, Vertical distance: {abs(a[1] - b[1])}")
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    elif type == "Euclidean Distance":
        print("Euclidean Distance selected")
        print(f"Calculating Euclidean distance between {a} and {b}")
        print(f"Horizontal distance: {a[0] - b[0]}, Vertical distance: {a[1] - b[1]}")
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

def get_neighbors(pos):
    neighbors = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dr, dc in directions:
        nr, nc = pos[0] + dr, pos[1] + dc
        if 0 <= nr < len(board) and 0 <= nc < len(board[0]) and board[nr][nc] != 1:
            neighbors.append((nr, nc))
    return neighbors


    
def greedy_best_first_search():
    queue = []
    # print("Calculating heuristic for start position:", start_pos)
    heapq.heappush(queue, (heuristic(start_pos, goal_pos, heuristic_var.get()), start_pos))
    parent = {start_pos: None} 
    visited = set()
    execution_time = 0
    execution_time_label.config(text=f"Execution Time: {execution_time:.4f} seconds")
    current_time = datetime.now()
    nodes_expanded = 0
    while queue:
        execution_time = datetime.now() - current_time
        execution_time_label.config(text=f"Execution Time: {execution_time.total_seconds():.4f} seconds")
        _, current = heapq.heappop(queue)
        if current in visited:
            continue
        visited.add(current)
        nodes_expanded_label.config(text=f"Nodes Expanded: {len(visited)}")
        nodes_expanded += 1
        grid_cells[current[0]][current[1]].config(bg="Yellow")
        root.update()
        root.after(200)
        if current == goal_pos:
            print("Goal found!")
            printParent(parent, goal_pos)
            return
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                parent[neighbor] = current
                heapq.heappush(queue, (heuristic(neighbor, goal_pos, heuristic_var.get()), neighbor))

def a_star_search():
    queue = []
    # print("Calculating heuristic for start position:", start_pos)
    # print("Goal position:", goal_pos)
    # print("Selected heuristic:", heuristic_var.get())
    # heuristic(start_pos, goal_pos, heuristic_var.get())
    # print(heuristic(start_pos, goal_pos, heuristic_var.get()))
    heapq.heappush(queue, (0 + heuristic(start_pos, goal_pos, heuristic_var.get()), 0, start_pos))
    parent = {start_pos: None}
    g_cost = {start_pos: 0}
    visited = set()
    execution_time = 0
    execution_time_label.config(text=f"Execution Time: {execution_time:.4f} seconds")
    current_time = datetime.now()
    nodes_expanded = 0
    while queue:
        execution_time = datetime.now() - current_time
        execution_time_label.config(text=f"Execution Time: {execution_time.total_seconds():.4f} seconds")
        _, current_g, current = heapq.heappop(queue)
        if current in visited:
            continue
        visited.add(current)
        grid_cells[current[0]][current[1]].config(bg="Yellow")
        root.update()
        root.after(200)
        nodes_expanded_label.config(text=f"Nodes Expanded: {len(visited)}")
        nodes_expanded += 1
        if current == goal_pos:
            print("Goal found!")
            printParent(parent, goal_pos)
            return
        for neighbor in get_neighbors(current):
            tentative_g = current_g + 1
            if neighbor not in visited or tentative_g < g_cost.get(neighbor, float('inf')):
                parent[neighbor] = current
                g_cost[neighbor] = tentative_g
                f_cost = tentative_g + heuristic(neighbor, goal_pos, heuristic_var.get())
                heapq.heappush(queue, (f_cost, tentative_g, neighbor))
def printParent(parent, goal):
    maingoal = goal
    path_cost = 0
    while parent.get(goal) != None:
        r,c = goal
        grid_cells[r][c].config(bg="Orange")
        root.update()
        root.after(200)
        goal = parent[goal]
        path_cost += 1
    path_cost_label.config(text=f"Path Cost: {path_cost}")
    r,c = maingoal
    grid_cells[r][c].config(bg="Red")
    r,c = goal
    grid_cells[r][c].config(bg="Blue")



map_generation()
root.mainloop()
