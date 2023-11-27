########## NOTES ##########
# FIX PLACEMENT (when screen is adjusted)
# ADD MORE LEVELS
# ADD POWERUPS?
# CHANGE COLORS/IMGS
# ADD SMOOTH MOVEMENT

from cmu_graphics import *
import math

# CITATION: I followed parts of a tutorial from "Tokyo EdTech" from YouTube - https://www.youtube.com/watch?v=inocKE13DEA&list=PLlEgNdBJEO-lNDJgg90fmfAq9RzORkQWP
# although they used turtle to help build their maze.
# Lists to store walls and collected pages
walls = []
pages = []
levels = [""]
app.background = 'black'

# Class to represent the walls (each little block)
class Pen():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = 'white'
    
# Class to represent the pages (to be collected)
class Page():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = 'yellow'
        self.gold = 100
        self.visible = True
    
    # Method to hide the pages when they are walked over
    def hide(self):
        self.visible = False
    
# Player class
class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = 'blue'
        self.gold = 0
    
    # Method to check the collision between the player and other objects in the maze
    # Includes pages and later on, enemies
    def isCollision(self, other):
        a = self.x - other.x
        b = self.y - other.y
        distance = math.sqrt((a**2) + (b**2))
        # Going with a distance of less than 5 (distance calculated with Py. Theorum)
        if distance < 5:
            return True
        else:
            return False

    # Each of the four methods below demonstrate character movement
    def moveUp(self):
        # MoveX isn't actually that necessary here but I added it just in case
        moveX = self.x
        moveY = self.y - 24
        # Checks if the move is legal by not being on the x, y coords of any white block
        # If the move is legal, actually do it
        # This pattern is the same for other directions
        if (moveX, moveY) not in walls:
            self.x = moveX
            self.y = moveY
    
    def moveDown(self):
        moveX = self.x 
        moveY = self.y + 24
        if (moveX, moveY) not in walls:
            self.x = moveX
            self.y = moveY
    
    def moveLeft(self):
        moveX = self.x - 24
        moveY = self.y 
        if (moveX, moveY) not in walls:
            self.x = moveX
            self.y = moveY
    
    def moveRight(self):
        moveX = self.x + 24
        moveY = self.y 
        if (moveX, moveY) not in walls:
            self.x = moveX
            self.y = moveY

# Hard-coded maze (planning to add more levels in the future)
# Tried recursive backtracing but it was a mess so I'm sticking with hard-code right now
levelOne = [
    "XXXXXXXXXXXXXXXXXXXX",
    "XPXXXXXX        XXXX",
    "X XXXXXX  XXXX  XXXX",
    "X     XX  XXXX  XXXX",
    "X     XX  XXXX  XXXX",
    "XXXX  XX  XX      XX",
    "XXXX  XX  XX      XX",
    "XXXX  XX  XXXXX  XXX",
    "X  X        XXX  XXX",
    "X  X  XXXXXXXXXXXXXX",
    "X        XXXXXXXXXXX",
    "X           XXXXXTXX",
    "XXXXXXXX    XXXXX  X",
    "XXXXXXXXXX  XXXXX  X",
    "XXX    XXX         X",
    "XXX    XXX         X",
    "X                  X",
    "X         XXXXXXXXXX",
    "XXXXXX    XXXXXXXXXX",
    "X    XXX  XXXXXXXXXX",
    "XXX  XXX           X",
    "X                  X",
    "X   XXXXXXXXXXXX  XX",
    "XXXXXXXXXXXXXXXX  XX",
]

# Add level one to the levels list
levels.append(levelOne)

# Function to set up the maze, including walls, player, and pages 
def setupMaze(level, app):
    maze = []
    # pages = []
    player = None
    mazeHeight = len(level)
    mazeWidth = len(level[0])
    # Center the maze on the 700 by 700 screen
    mazeX = (app.width - mazeWidth * 24) // 2 
    mazeY = (app.height - mazeHeight * 24) // 2 

    # Maze dimensions - if the playing screen is 700 x 700 and the actual maze is 600 x 600...
    # Then we can fit around 24 blocks down and across
    for y in range(mazeHeight):
        for x in range(mazeWidth):
            character = level[y][x]
            screenX = mazeX + x * 24
            screenY = mazeY + y * 24
    
    # Hardd-coding the position
    # maze = []
    # for y in range(len(level)):
    #     for x in range(len(level[y])):
    #         character = level[y][x]
    #         screenX = 100 + (x * 24)
    #         screenY = 600 - (y * 24)

            # Each letter refers to it's maze letter counterpart
            # X is the walls
            # P is the player (starting at the upper left hand screen)
            # T is the page (treasure) - this still needs some revision
            if character == "X":
                pen = Pen(screenX, screenY)
                maze.append(pen)

                walls.append((screenX, screenY))
                # print was just a test to see if all x, y coords were being tracked
                print(walls)

            if character == "P":
                player = Player(screenX, screenY)

            if character == "T":
                page = Page(screenX, screenY)
                pages.append(page)
    return maze, player, page

# Player movement according to keys
def onKeyPress(app, key):
    if key == 'up' or key == 'w':
        app.player.moveUp()
    elif key == 'down' or key == 's':
        app.player.moveDown()
    elif key == 'left' or key == 'a':
        app.player.moveLeft()
    elif key == 'right' or key == 'd':
        app.player.moveRight()

def onAppStart(app):
    app.maze, app.player, pages = setupMaze(levels[1], app) 

def redrawAll(app):
    for item in app.maze + [app.player]:
        if isinstance(item, Pen):
            drawRect(item.x, item.y, 20, 20, fill=item.color, border=item.color)
        elif isinstance(item, Player):
            drawRect(item.x, item.y, 20, 20, fill=item.color, border='black')
        elif isinstance(item, Page):
            if item.visible:
                drawRect(item.x, item.y, 10, 10, fill=item.color, border='black')
    
    # Check collision between player and pages, and add gold if collision is made
    # Hiding feature not working at the moment
    for page in pages:
        if app.player.isCollision(page):
            app.player.gold = page.gold
            print("Player Gold: {}".format(app.player.gold))
            page.hide()

def main():
    runApp(width=700, height=700)

if __name__ == '__main__':
    main()