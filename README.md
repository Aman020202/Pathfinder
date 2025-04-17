This project allows users to find the shortest path between two cities using three popular search algorithms: Breadth-First Search (BFS), Depth-First Search (DFS), and Uniform Cost Search (UCS). The user can select a starting city, an ending city, and an algorithm to calculate the shortest path. The system visualizes the cities and the shortest path found, along with the total distance and execution time.

Features:

Graph Representation: A graph of cities is created with cities connected by roads, each road having a specific distance.
Algorithms Implemented:
BFS (Breadth-First Search): A simple algorithm that explores all neighbors at the present depth before moving on to nodes at the next depth level.
DFS (Depth-First Search): An algorithm that explores as far as possible along a branch before backtracking.
UCS (Uniform Cost Search): A search algorithm that expands the least cost node, ensuring the shortest path is found.
Graph Visualization: Visualizes the city graph and highlights the shortest path using NetworkX and Matplotlib.
GUI Interface: Developed using Tkinter, users can select the starting city, ending city, and algorithm from a graphical interface.
Requirements:

Python 3.x
Tkinter (for GUI)
Matplotlib (for graph visualization)
NetworkX (for graph management and drawing)
heapq (for priority queue in UCS)
