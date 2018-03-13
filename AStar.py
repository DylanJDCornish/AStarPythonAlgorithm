import tkinter as tk
import tkinter.font as tkFont
import unittest


class Node:
	# constructor
    def __init__(self, x, y, parent, finalCoordinates):
	# set variables and define them
        self.__coodinates = (x, y)
        self.__parent = parent
        self.__finalCoordinates = finalCoordinates

        if finalCoordinates:
			#  cheapest cost of the path from block
            self.__H = 4 * min(abs(finalCoordinates[0] - x),\
                               abs(finalCoordinates[1] - y)) +\
                10 * max(abs(finalCoordinates[0] - x),\
                         abs(finalCoordinates[1] - y))
        else:
            self.__H = 0

        if parent:
            self.__G = parent.getCost() +\
                       int(10 * ((parent.getYCoordinates() - y) ** 2 +\
                                 (parent.getXCoordinates() - x) ** 2) ** (1/2))
        else:
            self.__G = 0

		# A* equation
        self.__F = self.__G + self.__H

	# get the coordinates x and y 
    def getCoordinates(self):
        return self.__coodinates
    
	# get parent of current object    
    def getParent(self):
        return self.__parent

	 # get x coordinates
    def getXCoordinates(self):
        return self.__coodinates[0]
    
	# get y coordinates
    def getYCoordinates(self):
        return self.__coodinates[1]
	
	# heuristic function gets cheapest cost of the path
    def getHeuristic(self):
        return self.__H
		
	# gets cost from the start node to this node
    def getCost(self):
        return self.__G
		
	# estimate for the complete cost of travelling from the starting point 
    def getFitness(self):
        return self.__F

class Grid(tk.Canvas):
    def __init__(self, master, width, height, nodeSize):
		# constructor
        tk.Canvas.__init__(self, master,\
                           width=width*nodeSize,\
                           height=height*nodeSize)
		# set variables and define them
        self.__width = nodeSize * width
        self.__height = nodeSize * height
        self.__size = nodeSize
        self.__obstacles = []
        self.__grid = []
        self.__start = None
        self.__finalCoordinates = None

		# setting size of blocks to grid
        boundary = 1 if nodeSize > 1 else 0
        for i in range(width):
            for j in range(height):
                self.__grid.append(self.create_rectangle(\
                                    i * nodeSize + boundary,\
                                    j * nodeSize + boundary,\
                                    (i+1) * nodeSize - boundary,\
                                    (j+1) * nodeSize - boundary))

	# set colour of certain block
    def Colour(self, coodinates, colour):
        color_dict = {"route": "blue", "obstacle": "purple",\
                      "seeker": "black", "target": "red"}
        if 0 <= coodinates[0] < self.__width / self.__size and\
           0 <= coodinates[1] < self.__height / self.__size:
            tag = int(self.__height / self.__size) * coodinates[0] + coodinates[1] + 1
            self.itemconfig(tag, fill=color_dict[colour])
            self.update_idletasks()

	# user clicks grid sets as seeker
    def setStart(self, x, y):
        self.__start = Node(x, y, None, self.__finalCoordinates)
        self.Colour((x, y), "seeker")

    def getStart(self):
        return self.__start

	# user clicks grid sets as target
    def setFinalcoodinates(self, x, y):
        self.__finalCoordinates = (x, y)
        self.Colour((x, y), "target")

    def getFinalcoodinates(self):
        return self.__finalCoordinates

	# user clicks grid sets obstacles
    def setObstacle(self, coodinates, convert=False):
        coodinates = (coodinates[0], coodinates[1])                                        
        if convert:
            coodinates = self.gridCoodinates(coodinates)
        self.Colour(coodinates, "obstacle")
        self.__obstacles.append((coodinates[0], coodinates[1]))

    def getObstacles(self):
        return self.__obstacles

    def getSize(self):
        return self.__size

    def gridCoodinates(self, canvasCoodinates):
        return (int(canvasCoodinates[0] / self.__size),\
                int(canvasCoodinates[1] / self.__size))

    def canvasCoodinates(self, gridCoodinates):
        canvasCoodinates = []
        for coodinates in gridCoodinates:
            canvasCoodinates.append((coodinates[0] * self.__size,\
                                  coodinates[1] * self.__size))
        return canvasCoodinates

    def getDimensions(self):
        return (int(self.__width / self.__size),\
                int(self.__height / self.__size))

# implementation of the A* function
def AStar(Grid):

	# set variable as seeker from method
    openNeighbours = [Grid.getStart()]
	
	# set variable as target from method
    openList = [openNeighbours[0].getCoordinates()]
    closedNeighbours = []
    closedList = []
	
	# get dimensions of grid
    gridWidth = Grid.getDimensions()[0]
    gridHeight = Grid.getDimensions()[1]

    obstaclesCoodinates = Grid.getObstacles()

    finalCoordinates = Grid.getFinalcoodinates()
    startCoodinates = Grid.getStart().getCoordinates()

    current = openNeighbours[0]
    coodinates = current.getCoordinates()
	
	# while loop implmenting A*
    while len(openNeighbours) > 0:

        for dx in range(-1, 2):
            for dy in range(-1, 2):

                x = coodinates[0] + dx
                y = coodinates[1] + dy
				
				# checks surrounding neighbours
                if (x, y) not in openList and\
                    (x, y) not in closedList and\
                    (x, y) not in obstaclesCoodinates and\
                    (x, y-dy) not in obstaclesCoodinates and\
                    (x-dx, y) not in obstaclesCoodinates and\
                    0 <= x < gridWidth and 0 <= y < gridHeight:

                    newBlock = Node(x, y, current, finalCoordinates)
                    newCoodinates = (x, y)

                    openNeighbours.append(newBlock)
                    openList.append(newCoodinates)

                    if newCoodinates == finalCoordinates:
                        return newBlock

        try:
            neighbour = openNeighbours[0]

        except:
            break
			
		# works for empty []
        for block in openNeighbours[1:]: 

            if block.getFitness() < neighbour.getFitness():
                neighbour = block

        current = neighbour
        coodinates = current.getCoordinates()

        closedNeighbours.append(current)
        closedList.append(coodinates)

        index = openList.index(coodinates)
        openNeighbours.remove(openNeighbours[index])
        openList.remove(openList[index])

    return None

# method displays the route
def start(Grid):

    start.set_off = False

    def begin(Grid=Grid):

        if not start.set_off:
            
            end = AStar(Grid)
            route = []

            finalCoordinates = Grid.getFinalcoodinates()
            startCoodinates = Grid.getStart().getCoordinates()
            
            while end:
                route.append(end.getCoordinates())
                end = end.getParent()
				
				# display route when found using the coordinates
                for coodinates in route:
                    if coodinates != finalCoordinates and coodinates != startCoodinates:
                        Grid.Colour(coodinates, "route")
                    
        start.set_off = True

    return begin

def wrapSquares(Grid):

    def setSquares(event, Grid=Grid):
        
        if not start.set_off:
            x, y = Grid.gridCoodinates((event.x, event.y))
            
            if not Grid.getStart():
                Grid.setStart(x, y)
            elif not Grid.getFinalcoodinates():
                Grid.setFinalcoodinates(x, y)
            elif Grid.gridCoodinates((x, y)) not in Grid.getObstacles():
                Grid.setObstacle((x, y))

    return setSquares

if __name__ == "__main__":

    root = tk.Tk()
	
	# set title
    root.title("A Star Search - Dylan Cornish")

	# set size of grid
    Grid = Grid(root, 25, 25, 20)
    Grid.pack()
    mFunction = wrapSquares(Grid)
	
	# set buttons
    Grid.bind("<B1-Motion>", mFunction)
    Grid.bind("<Button-1>", mFunction)
	# button initiates start function when clicked
    button = tk.Button(root, text="Begin Search", command=start(Grid))
    button.pack()

    tk.mainloop()
	
class assertTest(unittest.TestCase):

    def assertTest(self):
        self.assertTrue(True)
		
class gridTest(unittest.TestCase):

    def testGrid(self):
        self.assertEqual(AStar(Grid), getCoordinates)

class nodeTest(unittest.TestCase):

    def testNode(self):
        self.assertEqual(Node(finalCoordinates, 10,10))

class obstacleTest(unittest.TestCase):

    def testObstacle(self):
        self.assertEqual(Grid.setObstacle(coodinates, 20,20))		

class startTest(unittest.TestCase):

    def testStart(self):
        self.assertEqual(start(Grid)(end, AStar(Grid)))	
		
if __name__ == '__main__':
    unittest.main()
