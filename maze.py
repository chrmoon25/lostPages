########## NOTES ##########
# FIX PLACEMENT (when screen is adjusted)
# ADD MORE LEVELS
# ADD POWERUPS?
# CHANGE COLORS/IMGS

from cmu_graphics import *

app.background = 'black'

class Pen():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = 'white'

levels = [""]
levelOne = [
    "XXXXXXXXXXXXXXXXXXXX",
    "X XXXXXX        XXXX",
    "X XXXXXX  XXXX  XXXX",
    "X     XX  XXXX  XXXX",
    "X     XX  XXXX  XXXX",
    "XXXX  XX  XX      XX",
    "XXXX  XX  XX      XX",
    "XXXX  XX  XXXXX  XXX",
    "X  X        XXX  XXX",
    "X  X  XXXXXXXXXXXXXX",
    "X        XXXXXXXXXXX",
    "X           XXXXX XX",
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

levels.append(levelOne)

def setupMaze(level, app):
    maze = []
    mazeHeight = len(level)
    mazeWidth = len(level[0])
    mazeX = (app.width - mazeWidth * 24) // 2  # Calculate X offset for centering
    mazeY = (app.height - mazeHeight * 24) // 2  # Calculate Y offset for centering

    for y in range(mazeHeight):
        for x in range(mazeWidth):
            character = level[y][x]
            screenX = mazeX + x * 24
            screenY = mazeY + y * 24
    
    # maze = []
    # for y in range(len(level)):
    #     for x in range(len(level[y])):
    #         character = level[y][x]
    #         screenX = 100 + (x * 24)
    #         screenY = 600 - (y * 24)

            if character == "X":
                pen = Pen(screenX, screenY)
                maze.append(pen)
    return maze

def onAppStart(app):
    app.maze = setupMaze(levels[1], app)

def redrawAll(app):
    for pen in app.maze:
        drawRect(pen.x, pen.y, 20, 20, fill=pen.color, border=pen.color)

def main():
    runApp(width=700, height=700)

if __name__ == '__main__':
    main()
