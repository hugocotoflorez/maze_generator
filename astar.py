import math
from queue import PriorityQueue

# Creating a shortcut for pair
Pair = tuple[int, int]

# Creating a shortcut for pair with priority
pPair = tuple[float, Pair]


# A function to check if a given cell is valid
def isValid(row: int, col: int, ROW: int, COL: int) -> bool:
    return 0 <= row < ROW and 0 <= col < COL


# A function to check if a given cell is unblocked
def isUnBlocked(grid: list[list[int]], row: int, col: int) -> bool:
    return grid[row][col] == 0


# A function to check if the destination cell has been reached
def isDestination(row: int, col: int, dest: Pair) -> bool:
    return row == dest[0] and col == dest[1]


# A function to calculate the 'h' heuristics
def calculateHValue(row: int, col: int, dest: Pair) -> float:
    return math.sqrt((row - dest[0]) ** 2 + (col - dest[1]) ** 2)


# A function to trace the path from source to destination
def tracePath(cellDetails: list[list[dict]], dest: Pair):
    row, col = dest
    path = []
    while not (cellDetails[row][col]['parent_i'] == row and cellDetails[row][col]['parent_j'] == col):
        path.append((row, col))
        temp_row, temp_col = cellDetails[row][col]['parent_i'], cellDetails[row][col]['parent_j']
        row, col = temp_row, temp_col
    path.append((row, col))
    path.reverse()

    return path


# A function to find the shortest path using A* Search Algorithm
def aStarSearch(grid: list[list[int]], src: Pair, dest: Pair):
    ROW, COL = len(grid), len(grid[0])
    # If the source is out of range
    if not isValid(src[0], src[1], ROW, COL):
        print("Source is invalid")
        return

    # If the destination is out of range
    if not isValid(dest[0], dest[1], ROW, COL):
        print("Destination is invalid")
        return

    # Either the source or the destination is blocked
    if not isUnBlocked(grid, src[0], src[1]):
        print("Source is blocked")
        return
    
    if not isUnBlocked(grid, dest[0], dest[1]):
        print("Destination is blocked")
        return

    # If the destination cell is the same as the source cell
    if isDestination(src[0], src[1], dest):
        print("We are already at the destination")
        return

    # Initialize the cell details
    cellDetails = [[{'f': math.inf, 'g': math.inf, 'h': math.inf, 'parent_i': -1, 'parent_j': -1}
                    for _ in range(COL)] for _ in range(ROW)]

    # Initialize the starting cell
    i, j = src[0], src[1]
    cellDetails[i][j]['f'] = 0.0
    cellDetails[i][j]['g'] = 0.0
    cellDetails[i][j]['h'] = 0.0
    cellDetails[i][j]['parent_i'] = i
    cellDetails[i][j]['parent_j'] = j

    # Create an open list to store the cells yet to be visited
    openList = PriorityQueue()
    openList.put((0.0, (i, j)))

    # Initialize a boolean value to check if the destination is reached
    foundDest = False

    # Process cells until the open list is empty or the destination is reached
    while not openList.empty():
        p = openList.get()
        i, j = p[1]

        # Add the current cell to the closed list
        cellDetails[i][j]['isClosed'] = True

        # Generate the 8 successors of the current cell
        successors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in successors:
            newRow, newCol = i + dx, j + dy

            # Check if the successor cell is valid
            if isValid(newRow, newCol, ROW, COL):

                # If the destination cell is reached
                if isDestination(newRow, newCol, dest):
                    cellDetails[newRow][newCol]['parent_i'] = i
                    cellDetails[newRow][newCol]['parent_j'] = j
                    
                    foundDest = True
                    return tracePath(cellDetails, dest)

                # If the successor cell is unblocked and not on the closed list
                if isUnBlocked(grid, newRow, newCol) and not cellDetails[newRow][newCol].get('isClosed',False):
                    gNew = cellDetails[i][j]['g'] + 1.0
                    hNew = calculateHValue(newRow, newCol, dest)
                    fNew = gNew + hNew

                    # If the cell is not in the open list or the new path is shorter
                    if cellDetails[newRow][newCol]['f'] == math.inf or cellDetails[newRow][newCol]['f'] > fNew:
                        openList.put((fNew, (newRow, newCol)))

                        # Update the cell details
                        cellDetails[newRow][newCol]['f'] = fNew
                        cellDetails[newRow][newCol]['g'] = gNew
                        cellDetails[newRow][newCol]['h'] = hNew
                        cellDetails[newRow][newCol]['parent_i'] = i
                        cellDetails[newRow][newCol]['parent_j'] = j

    # When the destination cell is not found and the open list is empty
    if not foundDest:
        print("Failed to find the Destination Cell")


