import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
from typing import List, Tuple, Set, Optional

def visualize(maze: List[List[int]], path: Optional[List[Tuple[int, int]]] = None, seen: Optional[Set[Tuple[int, int]]] = None, cost: int = 0, label: str = "Maze Initialization", DPI: int = 800) -> None:
    """
    Visualizes the maze with the given path and visited nodes.

    Parameters:
    - maze (List[List[int]]): The maze grid.
    - path (Optional[List[Tuple[int, int]]]): The path from start to goal.
    - seen (Optional[Set[Tuple[int, int]]]): Set of visited nodes.
    - cost (int): The total cost of the path.
    - label (str): The algorithm used for pathfinding.
    - DPI (int): The resolution of the output image.
    """
    cmap = {
        'unvisited': '#808080',
        'visited': 'blue',
        'path': 'lime',
        'obstacle': 'black',
        'start': 'yellow',
        'goal': 'red'
    }
    height, width = len(maze), len(maze[0])
    fig, axis = plt.subplots()
    fig.patch.set_facecolor('black')
    fig.set_dpi(DPI)

    start = path[0] if path else None
    end = path[-1] if path else None

    for y in range(height):
        for x in range(width):
            if (x, y) == start:
                color = cmap['start']
            elif (x, y) == end:
                color = cmap['goal']
            else:
                if path and (x, y) in path:  # if the cell is in the path
                    color = cmap['path']
                elif seen and (x, y) in seen:  # if the cell has been visited
                    color = cmap['visited']
                elif maze[y][x] == '#':  # if the cell is an obstacle
                    color = cmap['obstacle']
                else:  # if the cell has not been visited
                    color = cmap['unvisited']
            rect = plt.Rectangle((x, height - y - 1), 1, 1, facecolor=color)
            axis.add_patch(rect)

    # Set the axis limits
    axis.set_xlim(0, width)
    axis.set_ylim(0, height)

    # Set the ticks at Dynamic intervals
    tick_interval = int(max(width, height) / 10)
    axis.set_xticks(np.arange(0, width + 1, tick_interval))
    axis.set_yticks(np.arange(0, height + 1, tick_interval))

    # Optionally, add grid lines for better visualization
    axis.grid(visible=True, which='both', color='white', linestyle='--', linewidth=0.5)

    # Set axis labels (customize if needed)
    axis.set_xlabel(
        (f"Cost: {cost} Steps: {len(path)} " if path else "") +
        (f"Seen: {len(seen)} " if seen else "") +
        f"Size: {width}x{height}",
        color='white', fontsize=15
    )
    axis.set_aspect('equal', adjustable='box')
    plt.title(label, color='white', fontsize=20, pad=20)

    # Create solutions directory if it doesn't exist
    os.makedirs('solutions', exist_ok=True)

    # Generate a unique filename with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    filename = f"solutions/{label}_{timestamp}.svg".replace(' ', '_')

    if (path): fig.savefig(filename, format='svg')
    plt.show()