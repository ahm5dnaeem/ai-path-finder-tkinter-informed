import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import time
import random
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
                        textvariable=algorithm_var,
                        values=["Manhattan Distance", "Euclidean Distance"],
                        state="readonly")
dropdown_2.pack(side=tk.LEFT, padx=10)

# Select Button
def select_algorithm():
    selected = algorithm_var.get()
    return
select_btn = tk.Button(control_frame,
                       text="Select",
                       command=select_algorithm)
select_btn.pack(side=tk.LEFT)

info_label = tk.Label(root, text="Click the start box",
                      font=("Arial", 14))
info_label.pack(pady=10)

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


def printParent(parent, goal):
    maingoal = goal
    while parent.get(goal) != None:
        r,c = goal
        grid_cells[r][c].config(bg="Orange")
        root.update()
        root.after(200)
        goal = parent[goal]
    r,c = maingoal
    grid_cells[r][c].config(bg="Red")
    r,c = goal
    grid_cells[r][c].config(bg="Blue")



map_generation()
root.mainloop()
