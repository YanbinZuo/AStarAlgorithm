# Name: Yanbin Zuo
# date: 9/5/2021

import pygame
from queue import PriorityQueue

# first, need to intialize the pygame
# REMEMBER: MUST HAVE THIS LINE, AND IT HAS TO BE FIRST
pygame.init()

WIDTH = 800
ROWS = 50
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm") 

# some RGB colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (118, 128, 128)
TURQUOISE = (64, 224, 208)

# we will fill windows with spot, so make a Spot class
# every spot object is a square containing its own index, width and color
# the index x, y is different with the toturial, but I think mine is more clear
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        # NOTICE: here could be mixed up
        # x related to col
        # y related to row
        self.x = col * width
        self.y = row * width
        self.color = YELLOW
        self.neighbors = []

    # may change this to x, y
    def get_pos(self):
        return self.row, self.col
    
    def is_close(self):
        return self.color == RED  
    
    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    
    def reset(self):
        self.color = YELLOW
    
    def make_closed(self):
        self.color = RED
    
    def make_open(self):
        self.color = GREEN
    
    def make_barrier(self):
        self.color = BLACK
    
    def make_start(self):
        self.color = ORANGE
    
    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE
    
    # draw a square spot on the window
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    def update_neighbors(self, grid):
        self.neighbors = []        
        # up
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row-1][self.col])
        # down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): 
            self.neighbors.append(grid[self.row+1][self.col])
        # left
        if self.col > 0 and not grid[self.row][self.col-1].is_barrier():
            self.neighbors.append(grid[self.row][self.col-1])
        # right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].is_barrier():
            self.neighbors.append(grid[self.row][self.col+1])

    def __lt__(self, other):
        return False


# function purpose: use a list of lists to store spots
# Parameters:
# rows: total rows in Windows (ROWS)
# width: length of Windows (WIDTH)
# return: a 2d array to store spots
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid

# function to draw the grid lines
def draw_gridLines(win, width, rows):
    gap = width // rows
    for i in range(rows):
        # draw horizontal line
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        # draw vertical line
        pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, width))

# function to draw everything to the window
def draw(win, width, rows, grid):
    # fill the window with white color background
    win.fill(WHITE)
    # draw the spot
    # this will draw all the spot fill in the window with spot color 
    # this will cover the white background color
    for row in grid:
        for spot in row:
            spot.draw(win)    
            
    # finally draw the grid line on the top of others
    draw_gridLines(win, width, rows)

    # REMEMBER: ALWAYS NEED TO UPDATE the window for every new draw
    pygame.display.update()
    
# get the position when clicked the mouse
def get_clicked_position(pos, width, rows):
    gap = width // rows
    x, y = pos
    row = y // gap
    col = x // gap
    return row, col


# heuristic function
# p1, p2 are positions
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)

# draw: taking an argument which is draw, which is a function that is going to call
def aStartAlgorithm(draw, grid, start, end):
    # draw = lambda: print("hello")
    # draw()

    # hash table, or dictionary in python
    # keeping track of where are we came from, keep track the path
    came_from = {}

    # if f value is same, we use count value for the second number of 
    # the priority queue sort
    count = 0

    # hashtable to store g_score and f_score
    g_score = {spot: float("inf") for row in grid for spot in row}
    """
    same as:
    for row in grid:
        for spot in row:
            g_score[spot] = float("inf")
    """
    f_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score[start] = g_score[start] + h(start.get_pos(), end.get_pos())

    open_set = PriorityQueue()
    # put the start spot to the priority queue
    open_set.put((f_score[start], count, start))
    
    while not open_set.empty():
        # hit the x button to quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
         
        current = open_set.get()[2]

        # draw path(purple)
        if current == end:
            while current in came_from:
                current = came_from[current]
                current.make_path()
                draw()
            # mark the start and end points
            start.make_start()
            end.make_end()
            return True
        
        temp_g_score = g_score[current] + 1
        for neighbor in current.neighbors:
            if temp_g_score < g_score[neighbor]:
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = g_score[neighbor] + h(neighbor.get_pos(), end.get_pos())
                came_from[neighbor] = current
                count += 1
                open_set.put((f_score[neighbor], count, neighbor))
                neighbor.make_open()
        
        if current != start:
            current.make_closed()
   
        draw()
        
    return False


def main(win, width, rows):     
    grid = make_grid(rows, width)    
    start = None
    end = None
    run = True
    while run:
        draw(win, width, rows, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # left click of mouse
            if pygame.mouse.get_pressed()[0]:
                """
                https://www.pygame.org/docs/
                pygame.mouse.get_pos()
                    get the mouse cursor position
                    get_pos() -> (x, y)
                    Returns the x and y position of the mouse cursor. 
                    The position is relative to the top-left corner of the display.
                """
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, width, rows)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != start and spot != end:
                    spot.make_barrier()
            
            # right click of mouse
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, width, rows)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    # call A* algorithm
                    # pass draw function as an argument to aStartAlgorithm function
                    # inside aStartAlgorithm function, we can call draw function directly
                    aStartAlgorithm(lambda: draw(win, width, rows, grid), grid, start, end)
                
                # press c to clear everything
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(rows, width)

    # exit the pygame window after the loop
    pygame.quit()


main(WIN, WIDTH, ROWS)


"""
note: lambda function (anonymous function)
x = lambda: print("hello")   --> same as 
x = def func():
    print("hello")

x()  --> class x() will call the print function
"""
