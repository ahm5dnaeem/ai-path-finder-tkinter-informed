import tkinter as tk
from tkinter import ttk
import time
root = tk.Tk()
root.title("Search Visualizer")

# ---------- USER INPUT ----------
rows = int(input("Enter rows: "))
cols = int(input("Enter cols: "))
# rows = 5
# cols = 5
board = [[0 for _ in range(cols)] for _ in range(rows)]
mode = "start"
start_pos = None
goal_pos = None

# ---------- TOP CONTROL FRAME ----------
control_frame = tk.Frame(root)
control_frame.pack(pady=10)

# Dropdown variable
algorithm_var = tk.StringVar()
algorithm_var.set("BFS")   # default

dropdown = ttk.Combobox(control_frame,
                        textvariable=algorithm_var,
                        values=["BFS", "DFS","UCS","DLS","IDDFS","Bidirectional"],
                        state="readonly")
dropdown.pack(side=tk.LEFT, padx=10)

# Select Button
def select_algorithm():
    selected = algorithm_var.get()
    print("Selected Algorithm:", selected)
    if selected == "BFS":
        parent = bfs(board, start_pos,goal_pos)
    elif selected == "DFS":
        parent = dfs(board,start_pos,goal_pos)
    elif selected == "UCS":
        parent = ucs(board,start_pos,goal_pos)
    elif selected == "DLS":
        limit = int(input("Enter Limit: "))
        parent = dls(board,start_pos,goal_pos, limit)
    elif selected == "IDDFS":
        parent = iddfs(board,start_pos,goal_pos)
    elif selected == "Bidirectional":
        parent = bidirectional(board,start_pos,goal_pos)
    printParent(parent, goal_pos)
select_btn = tk.Button(control_frame,
                       text="Select",
                       command=select_algorithm)
select_btn.pack(side=tk.LEFT)

info_label = tk.Label(root, text="Click the start box",
                      font=("Arial", 14))
info_label.pack(pady=10)

# ---------- GRID FRAME ----------
grid_frame = tk.Frame(root)
grid_frame.pack()

grid_cells = []

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
        info_label.config(text="Ready to run algorithm")
        mode = "done"

def dls(board, start, goal, limit):
    rows = len(board)
    cols = len(board[0])

    stack = [(start, 0)]  # (node, depth)
    visited = set()
    parent = {}

    while stack:
        current, depth = stack.pop()

        if current == goal:
            return parent

        if depth > limit:
            continue

        r, c = current
        grid_cells[r][c].config(bg="Yellow")
        root.update()
        root.after(200)

        visited.add(current)

        neighbors = [
            (r+1, c),
            (r-1, c),
            (r, c+1),
            (r, c-1),
            (r+1,c+1),
            (r-1,c-1)
        ]

        for nr, nc in neighbors:
            if 0 <= nr < rows and 0 <= nc < cols:
                if board[nr][nc] != 1 and (nr, nc) not in visited:
                    stack.append(((nr, nc), depth + 1))
                    parent[(nr, nc)] = current

                    grid_cells[nr][nc].config(bg="Gray")
                    root.update()
                    root.after(200)

    return None

def ucs(board, start, goal):
    rows = len(board)
    cols = len(board[0])

    frontier = []
    frontier.append((0, start))  # (cost, node)

    visited = set()
    parent = {}
    cost_so_far = {start: 0}

    while frontier:
        frontier.sort()
        cost, current = frontier.pop(0)

        if current == goal:
            break

        r, c = current
        grid_cells[r][c].config(bg="Yellow")
        root.update()
        root.after(200)

        visited.add(current)

        neighbors = [
            (r+1, c),
            (r-1, c),
            (r, c+1),
            (r, c-1),
            (r+1,c+1),
            (r-1,c-1)
        ]

        for nr, nc in neighbors:
            if 0 <= nr < rows and 0 <= nc < cols:
                new_cost = cost + 1

                if board[nr][nc] != 1 and (nr, nc) not in visited:
                    if (nr, nc) not in cost_so_far or new_cost < cost_so_far[(nr, nc)]:
                        cost_so_far[(nr, nc)] = new_cost
                        frontier.append((new_cost, (nr, nc)))
                        parent[(nr, nc)] = current

                        grid_cells[nr][nc].config(bg="Gray")
                        root.update()
                        root.after(200)

    return parent

def dfs(board, start, goal):
    rows = len(board)
    cols = len(board[0])

    stack = []
    stack.append(start)

    visited = set()
    visited.add(start)

    parent = {}

    while stack:
        current = stack.pop()

        if current == goal:
            break

        r, c = current
        grid_cells[r][c].config(bg="Yellow")
        root.update()
        root.after(200)

        neighbors = [
            (r+1, c),
            (r-1, c),
            (r, c+1),
            (r, c-1),
            (r+1,c+1),
            (r-1,c-1)
        ]

        for nr, nc in neighbors:
            if 0 <= nr < rows and 0 <= nc < cols:
                if board[nr][nc] != 1 and (nr, nc) not in visited:
                    stack.append((nr, nc))
                    visited.add((nr, nc))
                    parent[(nr, nc)] = current

                    grid_cells[nr][nc].config(bg="Gray")
                    root.update()
                    root.after(200)

    return parent
def iddfs(board, start, goal):
    max_depth = rows * cols

    for depth in range(max_depth):
        result = dls(board, start, goal, depth)
        if result is not None:
            return result

    return None
def bidirectional(board, start, goal):
    rows = len(board)
    cols = len(board[0])

    q_start = [start]
    q_goal = [goal]

    visited_start = {start}
    visited_goal = {goal}

    parent_start = {}
    parent_goal = {}

    while q_start and q_goal:

        # Expand from start
        current = q_start.pop(0)
        r, c = current

        grid_cells[r][c].config(bg="Yellow")
        root.update()
        root.after(200)

        neighbors = [
            (r+1, c),
            (r-1, c),
            (r, c+1),
            (r, c-1),
            (r+1,c+1),
            (r-1,c-1)
        ]

        for nr, nc in neighbors:
            if 0 <= nr < rows and 0 <= nc < cols:
                node = (nr, nc)

                if node in visited_goal:
                    print("Meeting Point:", node)
                    return parent_start, parent_goal

                if board[nr][nc] != 1 and node not in visited_start:
                    q_start.append(node)
                    visited_start.add(node)
                    parent_start[node] = current

                    grid_cells[nr][nc].config(bg="Gray")
                    root.update()
                    root.after(200)

        # Expand from goal
        current = q_goal.pop(0)
        r, c = current

        grid_cells[r][c].config(bg="Pink")
        root.update()
        root.after(200)

        for nr, nc in neighbors:
            if 0 <= nr < rows and 0 <= nc < cols:
                node = (nr, nc)

                if node in visited_start:
                    print("Meeting Point:", node)
                    return parent_start, parent_goal

                if board[nr][nc] != 1 and node not in visited_goal:
                    q_goal.append(node)
                    visited_goal.add(node)
                    parent_goal[node] = current

                    grid_cells[nr][nc].config(bg="Orange")
                    root.update()
                    root.after(200)

    return None

def bfs(board, start, goal):
    rows = len(board)
    cols = len(board[0])

    queue = []
    queue.append(start)

    visited = set()
    visited.add(start)

    parent = {}

    while queue:
        current = queue.pop(0)
        
        if current == goal:
            break

        r, c = current
        grid_cells[r][c].config(bg="Yellow")
        root.update()
        root.after(200)   
        neighbors = [
            (r+1, c),
            (r-1, c),
            (r, c+1),
            (r, c-1),
            (r+1,c+1),
            (r-1,c-1)
        ]

        for nr, nc in neighbors:
            if 0 <= nr < rows and 0 <= nc < cols:
                if board[nr][nc] != 1 and (nr, nc) not in visited:
                    queue.append((nr, nc))
                    grid_cells[nr][nc].config(bg="Gray")
                    root.update()
                    root.after(200)
                    visited.add((nr, nc))
                    parent[(nr, nc)] = current

    return parent


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



root.mainloop()
