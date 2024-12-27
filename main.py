from maze_solver.maze import create_maze
from maze_solver.algorithms import a_star, dfs, bfs, create_graph, dfs_biased
from maze_solver.visualization import visualize
import matplotlib.pyplot as plt
DPI: int = 800 # Lower DPI if workloads are too high
# Close ALL open plots

def main() -> None:
    """Main function to run the maze solver application."""
    while True:  # while the user does not enter valid dimensions
        try:
            w, l = int(input("Enter the width of the maze: ")), int(input("Enter the height of the maze: "))
            if w <= 0 or l <= 0:  # if the dimensions are invalid
                print("Invalid dimensions. Please enter valid dimensions.")
                continue
            break  # break the loop if valid dimensions are entered
        except (TypeError, ValueError):
            print("Invalid dimensions. Please enter valid dimensions.")
            continue

    maze = create_maze(w, l)  # create the maze
    print("Printing the maze...")
    try:
        visualize(maze, label="Maze Initialization", DPI=DPI)  # visualize the maze
    except ImportError:
        print("Please install matplotlib to visualize the maze.")
        return

    while True:  # while the user does not enter valid start and end points
        try:
            x, y = int(input("Enter the x coordinate of the start point: ")), int(input("Enter the y coordinate of the start point: "))
            if not 0 <= x < len(maze[0]) or not 0 <= y < len(maze) or maze[y][x] == '#':
                print("Invalid start point. Please select a valid start point.")
                continue
            start = (x, y)  # set the start point

            x, y = int(input("Enter the x coordinate of the end point: ")), int(input("Enter the y coordinate of the end point: "))
            if not 0 <= x < len(maze[0]) or not 0 <= y < len(maze) or maze[y][x] == '#':
                print("Invalid end point. Please select valid points.")
                continue
            end = (x, y)  # set the end point
            break
        except (TypeError, ValueError):
            print("Please select valid points.")
            continue

    graph = create_graph(maze)  # create the graph

    # Run and visualize Depth-First Search
    solution, cost, seen = dfs(graph, start, end)
    visualize(maze, solution, seen, cost, "Depth-First Search", DPI)
    print("Printing the DFS Solution...")

    # Run and visualize Biased Depth-First Search
    solution, cost, seen = dfs_biased(maze, start, end)
    visualize(maze, solution, seen, cost, "Biased Depth-First Search", DPI)
    print("Printing the Biased DFS Solution...")

    # Run and visualize Breadth-First Search
    solution, cost, seen = bfs(graph, start, end)
    visualize(maze, solution, seen, cost, "Breadth-First Search", DPI)
    print("Printing the BFS Solution...")

    # Run and visualize A* Search
    solution, cost, seen = a_star(graph, start, end)
    visualize(maze, solution, seen, cost, "A-Star Search", DPI)
    print("Printing the A* Search Solution...")

    print("All solutions have been printed.")
    print()
    print("Reminder: Close the plots to avoid unnecessary memory usage.")
if __name__ == '__main__':
    main()