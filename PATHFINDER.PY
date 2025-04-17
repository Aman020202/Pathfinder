import tkinter as tk
from tkinter import messagebox
from collections import deque
import heapq
import time
import networkx as nx
import matplotlib.pyplot as plt

# Extended graph with intermediate and international cities
graph = {
    'Delhi': {'Mumbai': 1400, 'Lucknow': 550, 'Jaipur': 280},
    'Mumbai': {'Delhi': 1400, 'Bangalore': 980, 'Ahmedabad': 530, 'Dubai': 2000},
    'Lucknow': {'Delhi': 550, 'Patna': 600, 'Kolkata': 980},
    'Patna': {'Lucknow': 600, 'Kolkata': 600},
    'Kolkata': {'Lucknow': 980, 'Patna': 600, 'Chennai': 1670},
    'Bangalore': {'Mumbai': 980, 'Chennai': 350, 'Hyderabad': 570},
    'Chennai': {'Bangalore': 350, 'Kolkata': 1670, 'Hyderabad': 630},
    'Hyderabad': {'Bangalore': 570, 'Chennai': 630, 'Nagpur': 500},
    'Nagpur': {'Hyderabad': 500, 'Ahmedabad': 850, 'Bhopal': 360},
    'Ahmedabad': {'Mumbai': 530, 'Nagpur': 850, 'Jaipur': 670},
    'Jaipur': {'Delhi': 280, 'Ahmedabad': 670, 'Bhopal': 600},
    'Bhopal': {'Nagpur': 360, 'Jaipur': 600},
    'Dubai': {'Mumbai': 2000, 'London': 5500},
    'London': {'Dubai': 5500, 'New York': 5600},
    'New York': {'London': 5600, 'San Francisco': 4700},
    'San Francisco': {'New York': 4700}
}

# UCS Algorithm
def ucs(graph, start, goal):
    visited = set()
    queue = [(0, start, [])]
    while queue:
        cost, node, path = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)
        path = path + [node]
        if node == goal:
            return path
        for neighbor, weight in graph.get(node, {}).items():
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight, neighbor, path))
    return []

# BFS Algorithm
def bfs(graph, start, goal):
    visited = set()
    queue = deque([start])
    parent = {start: None}
    while queue:
        node = queue.popleft()
        if node == goal:
            break
        for neighbor in graph.get(node, {}):
            if neighbor not in parent:
                parent[neighbor] = node
                queue.append(neighbor)
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent.get(current)
    path.reverse()
    return path if path and path[0] == start else []

# DFS Algorithm
def dfs(graph, start, goal):
    stack = [start]
    parent = {start: None}
    visited = set()
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        if node == goal:
            break
        for neighbor in graph.get(node, {}):
            if neighbor not in parent:
                parent[neighbor] = node
                stack.append(neighbor)
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent.get(current)
    path.reverse()
    return path if path and path[0] == start else []

# Visualize graph
def visualize_graph(path=None):
    G = nx.Graph()
    
    for city, neighbors in graph.items():
        for neighbor, distance in neighbors.items():
            G.add_edge(city, neighbor, weight=distance)
    
    pos = nx.spring_layout(G, seed=42)
    edge_labels = nx.get_edge_attributes(G, 'weight')

    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000)
    nx.draw_networkx_labels(G, pos, font_size=10)
    nx.draw_networkx_edges(G, pos, width=2)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    if path and len(path) > 1:
        edge_list = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=edge_list, edge_color='red', width=4)

    plt.title("Graph Visualization with Path" if path else "City Graph")
    plt.axis('off')
    plt.show()

# Run algorithm and show results
def run_algorithm():
    start = start_var.get()
    end = end_var.get()
    algo = algo_var.get()

    if start not in graph or end not in graph:
        messagebox.showerror("Error", "Invalid start or end city")
        return

    start_time = time.perf_counter()

    if algo == "BFS":
        path = bfs(graph, start, end)
    elif algo == "DFS":
        path = dfs(graph, start, end)
    elif algo == "UCS":
        path = ucs(graph, start, end)
    else:
        messagebox.showerror("Error", "Please select a valid algorithm")
        return

    end_time = time.perf_counter()

    if not path or path[0] != start:
        messagebox.showinfo("Result", "No path found")
        return

    total_cost = 0
    for i in range(len(path) - 1):
        total_cost += graph[path[i]][path[i + 1]]

    execution_time = (end_time - start_time) * 1_000_000  # microseconds

    messagebox.showinfo(
        "Result",
        f"Shortest Path: {path}\nTotal Cost: {total_cost} km\nExecution Time: {execution_time:.4f} microseconds"
    )

    visualize_graph(path)

# GUI Design
root = tk.Tk()
root.title("Shortest Path Finder (BFS, DFS, UCS)")
root.geometry("500x350")
root.config(bg="#f0f4f7")

tk.Label(root, text="Select Start City:", bg="#f0f4f7", font=("Arial", 12)).pack()
start_var = tk.StringVar(root)
start_menu = tk.OptionMenu(root, start_var, *graph.keys())
start_menu.config(bg="white", fg="black", font=("Arial", 11), highlightthickness=0)
start_menu.pack()

tk.Label(root, text="Select End City:", bg="#f0f4f7", font=("Arial", 12)).pack()
end_var = tk.StringVar(root)
end_menu = tk.OptionMenu(root, end_var, *graph.keys())
end_menu.config(bg="white", fg="black", font=("Arial", 11), highlightthickness=0)
end_menu.pack()

tk.Label(root, text="Select Algorithm:", bg="#f0f4f7", font=("Arial", 12)).pack()
algo_var = tk.StringVar(root)
algo_menu = tk.OptionMenu(root, algo_var, "BFS", "DFS", "UCS")
algo_menu.config(bg="white", fg="black", font=("Arial", 11), highlightthickness=0)
algo_menu.pack()

tk.Button(root, text="Show Graph", command=lambda: visualize_graph(), bg="#2196F3", fg="white",
          font=("Arial", 12, "bold"), activebackground="#1976D2", activeforeground="white").pack(pady=5)

tk.Button(root, text="Find Shortest Path", command=run_algorithm, bg="#4CAF50", fg="white",
          font=("Arial", 12, "bold"), activebackground="#388E3C", activeforeground="white").pack(pady=10)

root.mainloop()
