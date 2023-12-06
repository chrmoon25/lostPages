########## NOTES ##########
# Player sprite: https://kyunt.itch.io/purple-thief-player-animation-enemies-items
# Wall image: https://superwalrusland.com/ohr/issue26/pa/pixelart.html 
# Page sprite: https://pixeldungeon.fandom.com/wiki/Scroll_of_Mirror_Image 
# Portal gif: https://www.pinterest.com/pin/5770305765823550/ 
# Heart: https://tenor.com/search/pixel-heart-gifs
# Ghosts: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.deviantart.com%2Fandwise1121%2Fart%2FGhost-idle-892396700&psig=AOvVaw3eGvgNnC5_5xCprYBaPUS2&ust=1701499213399000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCJjN-dXQ7YIDFQAAAAAdAAAAABAD
# cite gif source (mike)
## FONTS: https://piazza.com/class/lkq6ivek5cg1bc/post/2217
## https://academy.cs.cmu.edu/docs/label
# game over: https://pngimg.com/image/83319

from cmu_graphics import *
from PIL import Image
import math
import random

# IMPORTED MODULES
# https://www.youtube.com/watch?v=CUFIjz_U7Mo 
# https://youtu.be/AAfy0-AWg-A?si=bg1AUZNPb0yGkCW4
import subprocess

# CITATION: I followed parts of a tutorial from "Tokyo EdTech" from YouTube - https://www.youtube.com/watch?v=inocKE13DEA&list=PLlEgNdBJEO-lNDJgg90fmfAq9RzORkQWP
# although they used turtle to help build their maze.
# Lists to store walls and collected pages
walls = []
pages = []
ghosts = []
# hearts = 3
portalPosition = []
levels = [""]
wallWidth = 24 
app.background = 'black'
app.won = False
app.lost = False

# Class to represent the walls (each little block)
class Pen():
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Player class
class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hearts = 3
        self.lastCollideTime = 0
        self.collideTime = 60
        self.pagesCollected = 0
        # self.move = False

    def loseHeart(self):
        self.hearts -= 1
    
    # Method to check the collision between the player and other objects in the maze
    # Includes pages and later on, enemies
    def isCollision(self, other):
        a = self.x - other.x
        b = self.y - other.y
        distance = math.sqrt((a**2) + (b**2))
        # Going with a distance of less than 5 (distance calculated with Py. Theorum)
        if distance < 6:
            return True
        else:
            return False
        
        
    def wallCollision(self, dx, dy, walls):
        new_x = self.x + dx
        new_y = self.y + dy

        # Check if any part of the player will collide with a wall
        player_left = new_x - 7  # player's left edge
        player_right = new_x + 7  #  player's right edge
        player_top = new_y - 10  #  player's top edge
        player_bottom = new_y + 10  #  player's bottom edge

        for wall_x, wall_y in walls:
            # Adjust the wall's sides considering its width (12 but 11 jsut in case)
            wall_left = wall_x - 11
            wall_right = wall_x + 11
            wall_top = wall_y - 11
            wall_bottom = wall_y + 11

            # Check for collision
            if (player_left < wall_right and player_right > wall_left and
                player_top < wall_bottom and player_bottom > wall_top):
                return False  # Collision detected, cannot move

        return True


    def move(self, dx, dy, walls):
        if self.wallCollision(dx, dy, walls):
            self.x += dx
            self.y += dy

        # No collisions detected, move to the new position

# Class to represent the pages (to be collected)
class Portal():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Page():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visible = True

    # Method to hide the pages when they are walked over
    # FIX THIS!!!
    def destroy(self):
        self.visible = False

class Ghost():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = random.choice(['up', 'down', 'left', 'right'])



    def isCollision(self, other):
        a = self.x - other.x
        b = self.y - other.y
        distance = math.sqrt((a**2) + (b**2))
        # Going with a distance of less than 5 (distance calculated with Py. Theorum)
        if distance < 10:
            return True
        else:
            return False
        
        
    def move(self):
        dx, dy = 0, 0
        if self.direction == 'up':
            dy = 2
        if self.direction == 'down':
            dy = -2
        if self.direction == 'left':
            dx = -2
        if self.direction == 'right':
            dx = 2

        moveX = self.x + dx
        moveY = self.y + dy   

        if self.wallCollision(dx, dy, walls) and (moveX, moveY) not in portalPosition:
        # if self.wallCollision(dx, dy, walls):
            self.x += dx
            self.y += dy
        else:
           self.direction = random.choice(['up', 'down', 'left', 'right']) 

    
    def isClose(self, other):
        a = self.x - other.x
        b = self.y - other.y
        distance = math.sqrt((a**2) + (b**2))

        if distance <= 75:
            return True
        else:
            return False
        
    def wallCollision(self, dx, dy, walls):
        new_x = self.x + dx
        new_y = self.y + dy

        # Check if any part of the player will collide with a wall
        player_left = new_x - 12  # Adjust  player's left edge
        player_right = new_x + 12  # Adjust player's right edge
        player_top = new_y - 12  # Adjust player's top edge
        player_bottom = new_y + 12  # Adjust player's bottom edge

        for wall_x, wall_y in walls:
            # Adjust the wall's sides considering its width (12 but 11 jsut in case)
            wall_left = wall_x - 11
            wall_right = wall_x + 11
            wall_top = wall_y - 11
            wall_bottom = wall_y + 11

            # Check for collision
            if (player_left < wall_right and player_right > wall_left and
                player_top < wall_bottom and player_bottom > wall_top):
                return False  # Collision detected, cannot move

        return True

    # CITATION: Used for pathfinding with A*
    # https://en.wikipedia.org/wiki/A*_search_algorithm#:~:text=A*%20is%20an%20informed%20search,shortest%20time%2C%20etc.).
    # Used for variable names and pseudocode: https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
    # Understanding implementation (heuristic via manhattan distance), pseudocode: https://www.geeksforgeeks.org/a-search-algorithm/
    # Example tutorial: https://www.youtube.com/watch?time_continue=4&v=crDPaKwDnDY&embeds_referring_euri=https%3A%2F%2Fwww.google.com%2F&source_ve_path=MjM4NTE&feature=emb_title
    # Backtracking (?) for a* https://stackoverflow.com/questions/42884863/a-star-algorithm-understanding-the-f-g-h-scores

    def heuristic(self, a, b):
        # calculates manhattan distance between the ghost (start) and player (target)
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # this is my a* implementation 
    def AStar(self, start, target, walls):
        # toVisit is set of positions that are to be explored
        toVisit = {start}
        # visited is places alr visited
        visited = set()
        # helps to backtrack to make shortest distance
        stepBack = dict()

        # g will keep track of the actual cost from start position to any position (following best path)
        gScore = {start: 0}
        # f stores total estimated cost of the cheapest path (g), this is done by heuristic calculation
        # heuristic helps an algo find good choices basically (i just kept the function name the same)  
        fScore = {start: self.heuristic(start, target)}


        # while items in the toVisit path 
        while toVisit:
            current = None # lowest f
            currentfScore = 999999
            for position in toVisit:
                if fScore[position] < currentfScore:
                    current = position
                    currentfScore = fScore[position]

            # target is found
            if current == target:
                # make path
                path = []
                # current --> starting position
                while current in stepBack:
                    path.append(current)
                    current = stepBack[current]
                return path[::-1]  # reverse the path to get it from start to target

            toVisit.remove(current)
            visited.add(current)

            for neighbor in self.getNeighbors(current):
                if neighbor in visited or neighbor in walls: #skips
                    continue

                newgScore = gScore[current] + 1  # assuming each move cost is 1

                if newgScore < gScore.get(neighbor, 999999):
                    stepBack[neighbor] = current
                    gScore[neighbor] = newgScore
                    fScore[neighbor] = newgScore + self.heuristic(neighbor, target)
                    if neighbor not in toVisit:
                        toVisit.add(neighbor)

        return None  # no path found

    def getNeighbors(self, position):
        x, y = position
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return neighbors

    def chase(self, player):
        start = (self.x, self.y)
        target = (player.x, player.y)
        
        path = self.AStar(start, target, walls)
        
        if path:
            self.moveAlongPath(path, walls)


    def moveAlongPath(self, path, walls):
        if path:
            nextX, nextY = path[0]
            dx = nextX - self.x
            dy = nextY - self.y

            if self.wallCollision(dx, dy, walls):
                self.x = nextX
                self.y = nextY

            # Remove the first position as it's reached
            path.pop(0)

# Hard-coded maze (planning to add more levels in the future)
# Tried recursive backtracing but it was a mess so I'm sticking with hard-code right now

levelOne = [
    "XXXXXXXXXXXXXXXXXXXX",
    "X                X X",
    "X X   XXXXXXXX   X X",
    "X XXX      X     X X",
    "X     X  X X XX XX X",
    "XXXX  X XX X  G    X",
    "X  X  X  X XXXX X  X",
    "X  X XXXXX    X X  X",
    "X  X        X XXXXXX",
    "XX XXXXXXXXXX      X",
    "X  X   X    XXXX X X",
    "X    X   X     X X X",
    "XXXXXXXX X XXX X   X",
    "X X    X X  XX XXX X",
    "X   XX       X   X X",
    "X X  XXXXXXXGXX  X X",
    "X    X  X    X     X",
    "X XXXX  X XXXX XX XX",
    "X X    XX   X      X",
    "X X XXXX  XXXXXXXX X",
    "X X   X   XP   T X X",
    "X XXX X XXX XX TXX X",
    "X     X     X  TX  X",
    "XXXXXXXXXXXXXXXOXXXX",
]

# Add level one to the levels list
levels.append(levelOne)

# Function to set up the maze, including walls, player, and pages 
def setupMaze(level, app):
    maze = []
    # pages = []
    player = None
    portal = None
    mazeHeight = len(level)
    mazeWidth = len(level[0])
    # Center the maze on the 700 by 700 screen
    mazeX = (app.width - mazeWidth * 24) // 2 
    mazeY = (app.height - mazeHeight * 24) // 2 

    # heart = Heart(50, 50)

    # Maze dimensions - if the playing screen is 700 x 700 and the actual maze is 600 x 600...
    # Then we can fit around 24 blocks down and across
    for y in range(mazeHeight):
        for x in range(mazeWidth):
            character = level[y][x]
            screenX = mazeX + x * 24
            screenY = mazeY + y * 24

            # playerX = app.width//2
            # playerY = app.height//2

            # Each letter refers to it's maze letter counterpart
            if character == "X":
                pen = Pen(screenX, screenY)
                maze.append(pen)

                walls.append((screenX, screenY))
                # print was just a test to see if all x, y coords were being tracked
                # print(walls)

            if character == "P":
                player = Player(screenX, screenY)

            if character == "T":
                page = Page(screenX, screenY)
                maze.append(page)
                pages.append(page)

            if character == "G":
                ghost = Ghost(screenX, screenY)
                maze.append(ghost)
                ghosts.append(ghost)

            if character == "O":
                portal = Portal(screenX, screenY)
                # walls.append((screenX, screenY))
                portalPosition.append((screenX, screenY))
                
    return maze, player, page, ghost, portal

# def restartGame(app):
    # app.player = Player(50, 50) 
    # app.player.hearts = 3
    # app.player.pagesCollected = 0
    # app.player.lastCollideTime = 0
    # app.player.collideTime = 60
    
    # app.walls = []
    # app.pages = []
    # app.ghosts = [] 
    # app.portalPosition = []
 
 # app.paused or

def onMousePress(app, mouseX, mouseY):
    if app.won or app.lost:
        labelWidth = 150
        labelHeight = 45
        
        labelX = (app.width - labelWidth) // 2
        labelY = (app.height - labelHeight) // 2 + 75
        
        if labelX < mouseX < labelX + labelWidth and labelY < mouseY < labelY + labelHeight:
            # app.paused = False
            app.won = False
            app.lost = False
            app.maze, app.player, app.page, app.ghost, app.portal = setupMaze(levels[1], app) 
            # restartGame(app)


def onKeyHold(app, keys):
    dx, dy = 0, 0
    if app.paused == False:
        if 'up' in keys or 'w' in keys:
            dy = -5
        elif 'down' in keys or 's' in keys:
            dy = 5
        elif 'left' in keys or 'a' in keys:
            dx = -5
        elif 'right' in keys or 'd' in keys:
            dx = 5

    app.player.move(dx, dy, walls)

def processGif(filePath, width, height):
    gif = Image.open(filePath)
    spriteList = []
    
    for frame in range(gif.n_frames):
        gif.seek(frame)
        resizedFrame = gif.resize((width, height))
        cmu_image = CMUImage(resizedFrame)
        spriteList.append(cmu_image)
    
    return spriteList

def onAppStart(app):
    global paused
    app.paused = False
    app.counter = 0
    app.framesPerStep = 5
    app.spriteCounter = 0
    app.stepsPerSecond = 300
    app.maze, app.player, app.page, app.ghost, app.portal = setupMaze(levels[1], app) 

    app.playerSpriteList = processGif('/Users/jiynmn/Desktop/15-112/lostPages/assets/sprite.gif', 24, 24)
    app.ghostSpriteList = processGif('/Users/jiynmn/Desktop/15-112/lostPages/assets/ghost.gif', 20, 20)
    app.pageSpriteList = processGif('/Users/jiynmn/Desktop/15-112/lostPages/assets/scroll.gif', 20, 20)
    app.portalSpriteList = processGif('/Users/jiynmn/Desktop/15-112/lostPages/assets/portal.gif', 40, 40)
    app.heartSpriteList = processGif('/Users/jiynmn/Desktop/15-112/lostPages/assets/heart.gif', 28, 28)
        
    wallImage = Image.open('/Users/jiynmn/Desktop/15-112/lostPages/assets/wall.jpg')
    app.wallSprite = CMUImage(wallImage.resize((24,24))) 

    # gameOver = Image.open('/Users/jiynmn/Desktop/15-112/lostPages/assets/gameOver1.png')
    gameOver = Image.open('/Users/jiynmn/Desktop/15-112/lostPages/assets/gameOver.png')
    app.gameOver = CMUImage(gameOver) 

    youWin = Image.open('/Users/jiynmn/Desktop/15-112/lostPages/assets/youWin.png')
    app.youWin = CMUImage(youWin.resize((330, 220)))

def onStep(app):
    if app.paused == False:
        app.counter += 1
        if app.counter % app.framesPerStep == 0:
            app.spriteCounter = (app.spriteCounter + 1) % len(app.playerSpriteList)

        app.player.lastCollideTime += 1
        for ghost in ghosts:
            if (app.player.isCollision(ghost) and app.player.lastCollideTime >= app.player.collideTime):
                app.player.loseHeart()
                app.player.lastCollideTime = 0

        if app.player.hearts <= 0:
            app.lost = True
        
        if app.player.pagesCollected == 3 and app.player.isCollision(app.portal):
            app.won = True

def redrawAll(app):

    for item in app.maze + [app.player] + [app.page] + [app.ghost] + [app.portal]:
        if isinstance(item, Pen):
            drawImage(app.wallSprite, item.x, item.y, align = 'center')
        elif isinstance(item, Player):
            drawImage(app.playerSpriteList[app.spriteCounter], item.x, item.y, align = 'center')
        elif isinstance(item, Ghost):
            drawImage(app.ghostSpriteList[app.spriteCounter], item.x, item.y, align = 'center')
        elif isinstance(item, Page) and item.visible: #do I need this argument?
            drawImage(app.pageSpriteList[app.spriteCounter], item.x, item.y, align = 'center')
        elif isinstance(item, Portal):
            drawImage(app.portalSpriteList[app.spriteCounter], item.x, item.y, align = 'center')

    pageText = f"pages collected: {app.player.pagesCollected}/3"
    textX = app.width - 610
    textY = 25
    ## ADD CITATION FOR THIS DSIFHSPFHE*W(HF*(OHDSUILFNDJSLNFDKSLNFJKLDSNJFK))
    drawLabel(pageText, textX, textY, fill = 'white', size = 15, font = 'Pixelify Sans SemiBold')


    heartSpacing = 30  # Adjust this value to manage the spacing between hearts
    heartX = app.width - 25  # Starting x-coordinate for hearts
    heartY = 25
    
    for i in range(app.player.hearts):
        newHeartX = heartX - (i * heartSpacing)
        drawImage(app.heartSpriteList[app.spriteCounter], newHeartX, heartY, align='center')

    if app.lost == True:
        drawRect(0, 0, app.width, app.height, fill='black')

        labelText = 'click to try again!'
        labelWidth = 200
        labelHeight = 50
        
        labelX = (app.width - labelWidth) // 2
        labelY = (app.height - labelHeight) // 2 + 85
        
        drawImage(app.gameOver, labelX + labelWidth // 2, 290, align = 'center')
        drawRect(labelX, labelY, labelWidth, labelHeight, fill='darkRed', border = 'red', borderWidth = 3)
        drawLabel(labelText, labelX + labelWidth // 2, labelY + labelHeight // 2, fill='red', align='center', size = 20, font = 'Pixelify Sans SemiBold')

    if app.won == True:
        drawRect(0, 0, app.width, app.height, fill='black')

        labelText = 'click to play again!'
        labelWidth = 200
        labelHeight = 50
        
        labelX = (app.width - labelWidth) // 2
        labelY = (app.height - labelHeight) // 2 + 85
        
        drawImage(app.youWin, labelX + labelWidth // 2, 290, align = 'center')
        drawRect(labelX, labelY, labelWidth, labelHeight, fill='darkGreen', border = 'limeGreen', borderWidth = 3)
        drawLabel(labelText, labelX + labelWidth // 2, labelY + labelHeight // 2, fill='limeGreen', align='center', size = 20, font = 'Pixelify Sans SemiBold')

    for page in pages:
        if app.player.isCollision(page):
            subprocess.Popen(['python3', '/Users/jiynmn/Desktop/15-112/lostPages/crossword.py'])
            page.destroy()
            app.player.pagesCollected += 1
            pages.remove(page) # Each page is a one time instance (100 gold only one time)

    if app.player.pagesCollected != 3 and app.player.isCollision(app.portal):
        pageText = 'you have not collected all the pages!'
        ### FIX THIS IODEHWIQODEJWIQODJE
        textX = 350
        textY = 660
        # fontPath = '/Users/jiynmn/Desktop/15-112/lostPages/assets/PixelifySans-Medium.ttf'
        # gameFont = ImageFont.truetype(fontPath, size=13)
        drawLabel(pageText, textX, textY, fill = 'red', bold = True, size = 14, font = 'Pixelify Sans SemiBold')

    for ghost in ghosts:
        if app.paused == False:
            ghost.move()

        if ghost.isClose(app.player):
            ghost.chase(app.player)


# app.player.hearts = 3
    # app.player.pagesCollected = 0
    # app.player.lastCollideTime = 0
    # app.player.collideTime = 60
    
    # app.walls = []
    # app.pages = []
    # app.ghosts = [] 
    # app.portalPosition = []


def main():
    runApp(width=700, height=700)

if __name__ == '__main__':
    main()