import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def bidirectional_bfs(graph, start, goal):
    if start == goal:
        return [start]
    
    
    frontier_start = {start}
    frontier_goal = {goal}
    
    
    parents_start = {start: None}
    parents_goal = {goal: None}
    
    while frontier_start and frontier_goal:
        
        next_frontier_start = set()
        for node in frontier_start:
            for neighbor in graph.neighbors(node):
                if neighbor not in parents_start:
                    parents_start[neighbor] = node
                    next_frontier_start.add(neighbor)
                    
                    
                    if neighbor in frontier_goal:
                        return reconstruct_path(parents_start, parents_goal, neighbor)
        frontier_start = next_frontier_start
        

        next_frontier_goal = set()
        for node in frontier_goal:
            for neighbor in graph.neighbors(node):
                if neighbor not in parents_goal:
                    parents_goal[neighbor] = node
                    next_frontier_goal.add(neighbor)
                    
                    
                    if neighbor in frontier_start:
                        return reconstruct_path(parents_start, parents_goal, neighbor)
        frontier_goal = next_frontier_goal
    
    return None  # No path found

def reconstruct_path(parents_start, parents_goal, meeting_point):
    
    path_from_start = []
    current = meeting_point
    while current is not None:
        path_from_start.append(current)
        current = parents_start[current]
    
    
    path_from_goal = []
    current = meeting_point
    while current is not None:
        path_from_goal.append(current)
        current = parents_goal[current]
    
    return list(reversed(path_from_start)) + path_from_goal[1:]


def bfs(graph, start, goal):
    queue = deque([start])
    visited = {start: None}
    
    while queue:
        node = queue.popleft()
        if node == goal:
            return reconstruct_single_path(visited, goal)
        
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited[neighbor] = node
                queue.append(neighbor)
    
    return None

def dfs(graph, start, goal):
    stack = [start]
    visited = {start: None}
    
    while stack:
        node = stack.pop()
        if node == goal:
            return reconstruct_single_path(visited, goal)
        
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited[neighbor] = node
                stack.append(neighbor)
    
    return None

def reconstruct_single_path(parents, goal):
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parents[current]
    return list(reversed(path))


def visualize_graph(graph, path=None):
    pos = nx.spring_layout(graph)  
    
    plt.figure(figsize=(8, 6))
    
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)
    
    if path:
        edges_in_path = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(graph, pos, edgelist=edges_in_path, edge_color='red', width=2)
    
    plt.title("Graph Visualization")
    plt.show()


if __name__ == "__main__":
   #  sample graph representing a city map
    G = nx.Graph()
    
    edges = [
        ('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'),
        ('C', 'E'), ('D', 'F'), ('E', 'F'), ('F', 'G')
    ]
    
    G.add_edges_from(edges)
    
    start_node = 'A'
    goal_node = 'G'
    
    print("Bi-directional BFS Path:", bidirectional_bfs(G, start_node, goal_node))
    print("Standard BFS Path:", bfs(G, start_node, goal_node))
    print("DFS Path:", dfs(G, start_node, goal_node))
    
    visualize_graph(G, bidirectional_bfs(G, start_node, goal_node))
