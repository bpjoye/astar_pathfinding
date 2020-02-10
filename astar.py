import Tkinter as tk
from operator import attrgetter
import numpy as np

GRID_SIZE = 10

class Node():

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

####################################################################

def astar(maze, start, end):

    for row in maze:
        print(row)

    start_node = Node(None, start)
    end_node = Node(None, end)

    # Nodes to be evaluated
    open_nodes = [start_node]
    # Nodes that have already been evaluated
    closed_nodes = []


    # Loop until there are no more open nodes
    while len(open_nodes) > 0:
        
        # Get the open node with the smallest f value
        current_node = min(open_nodes, key=attrgetter('f'))
        # Remove that node from the open nodes
        open_nodes.remove(current_node)
        # Add that node to the closed nodes
        closed_nodes.append(current_node)

        # The end node has been found
        if current_node == end_node:
            path = []
            previous_node = current_node
            # Loop backwards through the parents to get the full path
            while previous_node is not None:
                path.append(previous_node.position)
                previous_node = previous_node.parent
            # Return the reversed path since we got it backwards
            return path[::-1]

        # Get the children for the current node
        children = []
        # Loop through all possible transformations to get the children
        for new_position in [(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,-1), (1,-1), (-1,1)]:

            transformed_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # The child node is out of bounds
            if transformed_position[0] > (len(maze)-1) or transformed_position[0] < 0 or transformed_position[1] > (len(maze[len(maze)-1])-1) or transformed_position[1] < 0:
                continue

            # The child node is a blocked node
            if maze[transformed_position[0]][transformed_position[1]] != 0:
                continue

            # Create the child node and append it to the open nodes list
            child_node = Node(current_node, transformed_position)
            children.append(child_node)

        # Loop through the child nodes for the current node
        for child_node in children:

            # Check if the child node is in the closed nodes list
            for closed_node in closed_nodes:
                # Check for equality with the node classes custom defined equality operator
                if child_node == closed_node:
                    # Continue to the next child if this one is closed
                    continue

            # Calculate the g, h and f values for the child node
            child_node.g = current_node.g + 1
            child_node.h = ((child_node.position[0] - end_node.position[0]) ** 2) + ((child_node.position[1] - end_node.position[1]) ** 2)
            child_node.f = child_node.g + child_node.h

            # Check if the node is already in the open nodes 
            for open_node in open_nodes:
                if child_node == open_node and child_node.g > open_node.g:
                    continue
            
            # Add the child node to the open nodes list
            open_nodes.append(child_node)

####################################################################

# Clicking a box
def on_click(i,j,event):
    color = "black"
    event.widget.config(bg=color)
    board[i][j] = color
    maze[i][j] = 1

####################################################################

# Clicking find path
def begin():
    drawgrid()
    print("finding path")
    path = astar(maze, start, end)

####################################################################

    print("plotting path")

    for i,row in enumerate(board):
        for j,column in enumerate(row):

            # Path color
            for x,y in path:
                if i == x and j == y:
                    L = tk.Label(gridframe,width=2,bg='blue', borderwidth=2)
        
            # Place the label
            L.grid(row=i,column=j)
            L.bind('<Button-1>',lambda e,i=i,j=j: on_click(i,j,e))

####################################################################

def drawgrid():

    for widget in gridframe.winfo_children():
        widget.destroy()

    for i,row in enumerate(maze):
        for j,column in enumerate(row):

            # Default color
            L = tk.Label(gridframe, width=2, bg='gray', borderwidth=2)

            # Start and end color
            if i == start[0] and j == start[1]:
                L = tk.Label(gridframe,width=2,bg='green', borderwidth=2) 
            elif i == end[0] and j == end[1]:
                L = tk.Label(gridframe,width=2,bg='red', borderwidth=2)

            # Place the label
            L.grid(row=i,column=j)
            L.bind('<Button-1>',lambda e,i=i,j=j: on_click(i,j,e))

####################################################################

def reset():

    board = [[None]*GRID_SIZE for _ in range(GRID_SIZE)]
    maze = np.zeros([GRID_SIZE, GRID_SIZE])

####################################################################

# start_input = input("Enter the starting coordinate 'x y': ")
# coords = [int(s) for s in start_input.split() if s.isdigit()]
# start = Node(coords[0],coords[1])

# start_input = input("Enter the ending coordinate 'x y': ")
# coords = [int(s) for s in start_input.split() if s.isdigit()]
# end = Node(coords[0],coords[1])
# start = Node(1,1)
# end = Node(10,10)

####################################################################

board = [[None]*GRID_SIZE for _ in range(GRID_SIZE)]
maze = np.zeros([GRID_SIZE, GRID_SIZE])
start = (0,0)
end = (7,6)


# Create the GUI
root = tk.Tk()

topframe = tk.Frame(root)
topframe.pack(side="top")

gridframe = tk.Frame(root)
gridframe.pack(side="bottom")

begin_button = tk.Button(topframe, text="Find path", command=begin)
begin_button.pack()

reset_button = tk.Button(topframe, text="Reset", command=reset)
reset_button.pack()

drawgrid()


root.mainloop()