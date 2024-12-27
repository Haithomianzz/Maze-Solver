from heapq import heappop, heappush
from typing import List, Set, Tuple, Dict, Union


def heuristic(node: Tuple[int, int], goal: Tuple[int, int]) -> int:
    """
    Computes the Manhattan heuristic for A* search.

    Parameters:
    - node (Tuple[int, int]): Current node coordinates.
    - goal (Tuple[int, int]): Goal node coordinates.

    Returns:
    - int: The Manhattan distance between the node and the goal.
    """
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])


def a_star(graph: Dict[Tuple[int, int], List[Tuple[int, int, int]]], start: Tuple[int, int], goal: Tuple[int, int]) -> Union[Tuple[List[Tuple[int, int]], int, Set[Tuple[int, int]]], Tuple[None, float, Set[Tuple[int, int]]]]:
    """
    Performs the A* search algorithm.

    Parameters:
    - graph (dict): The graph representing the maze.
    - start (Tuple[int, int]): The start node.
    - goal (Tuple[int, int]): The goal node.

    Returns:
    - Tuple[List[Tuple[int, int]], int, Set[Tuple[int, int]]]: Path, cost, and visited nodes.
    """
    # Initialization
    path, visited, open_set, s_costs, f_costs = {}, set(), [(0, start)], {start: 0}, {start: heuristic(start, goal)}

    while open_set:
        current = heappop(open_set)[1]  # Node with lowest f cost
        if current in visited: continue
        visited.add(current)
        if current == goal:
            return reconstruct_path(path, goal), s_costs[current], visited

        for neighbor_x, neighbor_y, weight in get_missing_neighbours(graph, current, visited):
            neighbor = (neighbor_x, neighbor_y)
            pathcost = s_costs[current] + weight
            if neighbor not in s_costs or pathcost < s_costs[neighbor]:
                path[neighbor] = current
                s_costs[neighbor] = pathcost
                f_costs[neighbor] = s_costs[neighbor] + heuristic(neighbor, goal)
                heappush(open_set, (f_costs[neighbor], neighbor))
    return None, float('inf'), visited


def dfs(graph: Dict[Tuple[int, int], List[Tuple[int, int, int]]], start: Tuple[int, int], goal: Tuple[int, int]) -> Union[Tuple[List[Tuple[int, int]], int, Set[Tuple[int, int]]], Tuple[None, float, Set[Tuple[int, int]]]]:
    """
    Performs Depth First Search (DFS).

    Parameters:
    - graph (dict): The graph representing the maze.
    - start (Tuple[int, int]): The start node.
    - goal (Tuple[int, int]): The goal node.

    Returns:
    - Tuple[List[Tuple[int, int]], int, Set[Tuple[int, int]]]: Path, cost, and visited nodes.
    """
    path, cost, visited, stack = {}, {start: 0}, set(), [(start, 0)]

    while stack:
        current, current_cost = stack.pop()
        if current in visited: continue
        visited.add(current)
        if current == goal:
            return reconstruct_path(path, goal), cost[current], visited

        for neighbor_x, neighbor_y, weight in get_missing_neighbours(graph, current, visited):
            neighbor = (neighbor_x, neighbor_y)
            total_cost = current_cost + weight
            if neighbor not in cost or total_cost < cost[neighbor]:
                path[neighbor] = current
                cost[neighbor] = total_cost
                stack.append((neighbor, total_cost))
    return None, float('inf'), visited


def dfs_biased(maze: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]) -> Union[Tuple[List[Tuple[int, int]], int, Set[Tuple[int, int]]], Tuple[None, float, Set[Tuple[int, int]]]]:
    """
    Performs Depth First Search (DFS) with bias towards the goal.

    Parameters:
    - maze (List[List[int]]): The maze grid.
    - start (Tuple[int, int]): The start node.
    - goal (Tuple[int, int]): The goal node.

    Returns:
    - Tuple[List[Tuple[int, int]], int, Set[Tuple[int, int]]]: Path, cost, and visited nodes.
    """
    path, cost, visited, stack = {}, {start: 0}, set(), [(start, 0)]

    while stack:
        current, current_cost = stack.pop()
        if current in visited: continue
        visited.add(current)
        if current == goal:
            return reconstruct_path(path, goal), cost[current], visited

        for neighbor_x, neighbor_y, weight in get_missing_neighbours_biased(current, goal, maze, visited):
            neighbor = (neighbor_x, neighbor_y)
            total_cost = current_cost + weight
            if neighbor not in cost or total_cost < cost[neighbor]:
                path[neighbor] = current
                cost[neighbor] = total_cost
                stack.append((neighbor, total_cost))
    return None, float('inf'), visited


def bfs(graph: Dict[Tuple[int, int], List[Tuple[int, int, int]]], start: Tuple[int, int], goal: Tuple[int, int]) -> Union[Tuple[List[Tuple[int, int]], int, Set[Tuple[int, int]]], Tuple[None, float, Set[Tuple[int, int]]]]:
    """
    Performs Breadth First Search (BFS).

    Parameters:
    - graph (dict): The graph representing the maze.
    - start (Tuple[int, int]): The start node.
    - goal (Tuple[int, int]): The goal node.

    Returns:
    - Tuple[List[Tuple[int, int]], int, Set[Tuple[int, int]]]: Path, cost, and visited nodes.
    """
    path, cost, visited, queue = {}, {start: 0}, set(), [(start, 0)]

    while queue:
        current, current_cost = queue.pop(0)
        if current in visited: continue
        visited.add(current)
        if current == goal:
            return reconstruct_path(path, current), cost[current], visited

        for neighbor_x, neighbor_y, weight in get_missing_neighbours(graph, current, visited):
            neighbor = (neighbor_x, neighbor_y)
            total_cost = current_cost + weight
            if neighbor not in cost or total_cost < cost[neighbor]:
                path[neighbor] = current
                cost[neighbor] = total_cost
                queue.append((neighbor, total_cost))
    return None, float('inf'), visited


def reconstruct_path(came_from: Dict[Tuple[int, int], Tuple[int, int]], current: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Reconstructs the path from the start node to the goal node.

    Args:
        came_from (dict): A dictionary where the keys are nodes and the values are the nodes
                          that led to them in the search process.
        current (tuple): The current node (goal node).

    Returns:
        list: A list of nodes representing the path from start to goal.
    """
    path = []  # Initialize an empty path list.
    while current in came_from:  # While there are nodes to backtrack.
        path.append(current)  # Add the current node to the path.
        current = came_from[current]  # Backtrack to the previous node.

    # Return the reversed path, starting from the start node.
    return [current] + path[::-1]


def get_missing_neighbours(graph: Dict[Tuple[int, int], List[Tuple[int, int, int]]], node: Tuple[int, int], visited: Set[Tuple[int, int]]) -> List[Tuple[int, int, int]]:
    """
    Returns the neighbors of a node that have not been visited.

    Parameters:
    - graph (Dict[Tuple[int, int], List[Tuple[int, int, int]]]): The graph representing the maze.
    - node (Tuple[int, int]): The current node.
    - visited (Set[Tuple[int, int]]): Set of visited nodes.

    Returns:
    - List[Tuple[int, int, int]]: List of unvisited neighbors.
    """
    return [(n_x, n_y, weight) for n_x, n_y, weight in graph[node] if (n_x, n_y) not in visited]


def get_missing_neighbours_biased(node: Tuple[int, int], goal: Tuple[int, int], maze: List[List[int]], visited: Set[Tuple[int, int]]) -> List[Tuple[int, int, int]]:
    """
    Returns the biased neighbors of a node that have not been visited.

    Parameters:
    - node (Tuple[int, int]): The current node.
    - goal (Tuple[int, int]): The goal node.
    - maze (List[List[int]]): The maze grid.
    - visited (Set[Tuple[int, int]]): Set of visited nodes.

    Returns:
    - List[Tuple[int, int, int]]: List of unvisited biased neighbors.
    """
    return [(n_x, n_y, weight) for n_x, n_y, weight in get_neighbors_biased(node[0], node[1], maze, goal) if (n_x, n_y) not in visited]


def get_neighbors(x: int, y: int, maze: List[List[int]]) -> List[Tuple[int, int, int]]:
    """
    Returns a list of non-obstacle neighbors for a given cell in the maze.

    Parameters:
    - x (int): The x-coordinate of the cell.
    - y (int): The y-coordinate of the cell.
    - maze (List[List[int]]): The maze grid.

    Returns:
    - List[Tuple[int, int, int]]: A list of tuples representing the neighboring cells and their weights.
    """
    height, width = len(maze), len(maze[0])
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]  # Fixed order: up, left, down, right
    return [(x + dx, y + dy, maze[y + dy][x + dx]) for dx, dy in directions if 0 <= y + dy < height and 0 <= x + dx < width and maze[y + dy][x + dx] != '#']


def get_neighbors_biased(x: int, y: int, maze: List[List[int]], goal: Tuple[int, int]) -> List[Tuple[int, int, int]]:
    """
    Returns a list of biased non-obstacle neighbors for a given cell in the maze.

    Parameters:
    - x (int): The x-coordinate of the cell.
    - y (int): The y-coordinate of the cell.
    - maze (List[List[int]]): The maze grid.
    - goal (Tuple[int, int]): The goal node coordinates.

    Returns:
    - List[Tuple[int, int, int]]: A list of tuples representing the neighboring cells and their weights.
    """
    height, width = len(maze), len(maze[0])
    directions = [(0, -1) if y <= goal[1] else (0, 1), (-1, 0) if x <= goal[0] else (1, 0), (0, 1) if y <= goal[1] else (0, -1), (1, 0) if x <= goal[0] else (-1, 0)]
    if x == goal[0]:
        directions[2], directions[3] = directions[3], directions[2]
    return [(x + dx, y + dy, maze[y + dy][x + dx]) for dx, dy in directions if 0 <= y + dy < height and 0 <= x + dx < width and maze[y + dy][x + dx] != '#']


def create_graph(maze: List[List[int]]) -> Dict[Tuple[int, int], List[Tuple[int, int, int]]]:
    """
    Create a graph representation of the maze.

    Args:
        maze (List[List[int]]): The 2D maze grid where each cell represents a node.

    Returns:
        Dict[Tuple[int, int], List[Tuple[int, int, int]]]: A dictionary where each key is a node (x, y) and the value is a list of tuples
                                                           representing the neighboring nodes and their weights.
    """
    return {(x, y): get_neighbors(x, y, maze) for y in range(len(maze)) for x in range(len(maze[0])) if maze[y][x] != '#'}