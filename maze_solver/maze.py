import random
from typing import List, Tuple, Set, Optional

def create_maze(width: int, height: int, obstacle_percentage: float = 0.2, weighted_percentage: float = 0.1) -> List[List[int]]:
    """
    Creates a maze with random obstacles and weighted cells.

    Parameters:
    - width (int): Width of the maze.
    - height (int): Height of the maze.
    - obstacle_percentage (float): Percentage of cells to be obstacles.
    - weighted_percentage (float): Percentage of cells to be weighted.
    - seed (int): Seed for random number generation.

    Returns:
    - List[List[int]]: The generated maze.
    """
    return [['#' if random.random() < obstacle_percentage else (random.randint(2, 5) if random.random() < weighted_percentage else 1) for _ in range(width)] for _ in range(height)]


def print_maze(maze: List[List[int]], path: Optional[List[Tuple[int, int]]] = None, seen: Optional[Set[Tuple[int, int]]] = None) -> None:
    """
    Prints the maze with path and visited nodes.

    Parameters:
    - maze (List[List[int]]): The maze to print.
    - path (Optional[List[Tuple[int, int]]]): The path taken to reach the goal.
    - seen (Optional[Set[Tuple[int, int]]]): Set of visited nodes.
    """
    for y, row in enumerate(maze):
        formatted_row = [
            '⬛' if cell == '#' and seen is not None else '🟩' if path and (x, y) in path else '🟦' if seen and (x, y) in seen else '⬜' for x, cell in enumerate(row)]
        print(''.join(formatted_row))