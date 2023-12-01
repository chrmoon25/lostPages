########## NOTES ##########
# Player sprite: https://kyunt.itch.io/purple-thief-player-animation-enemies-items
# Book sprite: https://wifflegif.com/gifs/706281-pixel-art-spell-gif
# Wall image: https://superwalrusland.com/ohr/issue26/pa/pixelart.html 
# Page sprite: https://pixeldungeon.fandom.com/wiki/Scroll_of_Mirror_Image 
# Potion sprites: https://wiki.hypixel.net/Potions
# Ghosts: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.deviantart.com%2Fandwise1121%2Fart%2FGhost-idle-892396700&psig=AOvVaw3eGvgNnC5_5xCprYBaPUS2&ust=1701499213399000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCJjN-dXQ7YIDFQAAAAAdAAAAABAD
# cite gif source (mike)

# FIX PLACEMENT (when screen is adjusted)
# ADD MORE LEVELS
# ADD POWERUPS?
# CHANGE COLORS/IMGS
# ADD SMOOTH MOVEMENT
# FIX OVERLAY WITH PLAYER

from cmu_graphics import *
from PIL import Image
import math
import random

# CITATION: I followed parts of a tutorial from "Tokyo EdTech" from YouTube - https://www.youtube.com/watch?v=inocKE13DEA&list=PLlEgNdBJEO-lNDJgg90fmfAq9RzORkQWP
# although they used turtle to help build their maze.
# Lists to store walls and collected pages
walls = []
pages = []
ghosts = []
levels = [""]
app.background = 'black'

# Class to represent the walls (each little block)
class Pen():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # self.color = 'white'

# Class to represent the pages (to be collected)
class Page():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gold = 100
        self.visible = True

    # Method to hide the pages when they are walked over
    # FIX THIS!!!
    def destroy(self):
        self.visible = False
        # self.x = 2000
        # self.y = 2000

class Ghost():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gold = 100
    
    # def redrawAll(self):
    #     if self.visible:
    #         drawRect(self.x, self.y, 10, 10, fill=self.color)
    
# Player class
class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = 'blue'
        self.gold = 0
        # self.move = False
    
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
    "XXXX  XX  XX  G   XX",
    "XXXX  XX  XX      XX",
    "XXXX  XX  XXXXX  XXX",
    "X  X        XXX TXXX",
    "X  X  XXXXXXXXXXXXXX",
    "X     G  XXXXXXXXXXX",
    "X           XXXXXTXX",
    "XXXXXXXX    XXXXX  X",
    "XXXXXXXXXX  XXXXX  X",
    "XXX    XXX         X",
    "XXX    XXX  G      X",
    "X                  X",
    "X         XXXXXXXXXX",
    "XXXXXX    XXXXXXXXXX",
    "XT   XXX  XXXXXXXXXX",
    "XXX  XXX           X",
    "X       G          X",
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

            playerX = app.width//2
            playerY = app.height//2

            # Each letter refers to it's maze letter counterpart
            # X is the walls
            # P is the player (starting at the upper left hand screen)
            # T is the page (treasure) - this still needs some revision
            if character == "X":
                pen = Pen(screenX, screenY)
                maze.append(pen)

                walls.append((screenX, screenY))
                # print was just a test to see if all x, y coords were being tracked
                # print(walls)

            if character == "P":
                player = Player(playerX, playerY)

            if character == "T":
                page = Page(screenX, screenY)
                maze.append(page)
                pages.append(page)

            if character == "G":
                ghost = Ghost(screenX, screenY)
                maze.append(ghost)
                ghosts.append(ghost)
                
    return maze, player, page, ghost

# Player movement according to keys
def onKeyHold(app, keys):
    if 'up' in keys or 'w' in keys:
        app.player.moveUp()
    elif 'down' in keys or 's' in keys:
        app.player.moveDown()
    elif 'left' in keys or 'a' in keys:
        app.player.moveLeft()
    elif 'right' in keys or 'd' in keys:
        app.player.moveRight()

def onAppStart(app):
    app.maze, app.player,app.page, app.ghost = setupMaze(levels[1], app) 

    playerGif = Image.open('/Users/jiynmn/Desktop/15-112/lostPages/assets/sprite.gif')
    app.playerSpriteList = []
    for frame in range(playerGif.n_frames):
        #Set the current frame
        playerGif.seek(frame)
        #Resize the image
        fr = playerGif.resize((24, 24))
        #Flip the image
        # fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
        #Convert to CMUImage
        fr = CMUImage(fr)
        #Put in our sprite list
        app.playerSpriteList.append(fr)

    ghostGif = Image.open('/Users/jiynmn/Desktop/15-112/lostPages/assets/ghost.gif')
    app.ghostSpriteList = []
    for frame in range(ghostGif.n_frames):
        #Set the current frame
        ghostGif.seek(frame)
        #Resize the image
        fr = ghostGif.resize((20, 20))
        #Flip the image
        # fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
        #Convert to CMUImage
        fr = CMUImage(fr)
        #Put in our sprite list
        app.ghostSpriteList.append(fr)
    
    pageGif = Image.open('/Users/jiynmn/Desktop/15-112/lostPages/assets/scroll.gif')
    app.pageSpriteList = []
    for frame in range(pageGif.n_frames):
        pageGif.seek(frame)
        fr = pageGif.resize((20, 20))  # Resize to 24x24 pixels
        cmu_image = CMUImage(fr)
        app.pageSpriteList.append(cmu_image)
    
    wallImage = Image.open('/Users/jiynmn/Desktop/15-112/lostPages/assets/wall.jpg')
    app.wallSprite = CMUImage(wallImage.resize((24, 24))) 

    print(app.playerSpriteList)
    print(app.ghostSpriteList)
    print(app.pageSpriteList)


    app.spriteCounter = 0
    app.stepsPerSecond = 5

def onStep(app):
    #Set spriteCounter to next frame
    app.spriteCounter = (app.spriteCounter + 1) % len(app.playerSpriteList)




    

def redrawAll(app):
    for item in app.maze + [app.player] + [app.page] + [app.ghost]:
        if isinstance(item, Pen):
            drawImage(app.wallSprite, item.x, item.y, align = 'center')
            # drawRect(item.x, item.y, 20, 20, fill=item.color, border=item.color)
        elif isinstance(item, Player):
            # drawImage(app.spriteList[app.spriteCounter], item.x, item.y)
            drawImage(app.playerSpriteList[app.spriteCounter], item.x, item.y, align = 'center')
            # drawRect(item.x, item.y, 20, 20, fill=item.color, border='black')
        elif isinstance(item, Ghost):
            # drawImage(app.spriteList[app.spriteCounter], item.x, item.y)
            drawImage(app.ghostSpriteList[app.spriteCounter], item.x, item.y, align = 'center')
        elif isinstance(item, Page) and item.visible: #do I need this argument?
            drawImage(app.pageSpriteList[app.spriteCounter], item.x, item.y, align = 'center')
            # drawImage(app.playerSpriteList[app.spriteCounter], item.x, item.y, align = 'center')
            # drawRect(item.x, item.y, 20, 20, fill=item.color, border='black')
    
    # Check collision between player and pages, and add gold if collision is made
    # Hiding feature not working at the moment
    for page in pages:
        if app.player.isCollision(page):
            app.player.gold += page.gold
            print("Player Gold: {}".format(app.player.gold))
            page.destroy()
            pages.remove(page) # Each page is a one time instance (100 gold only one time)

def main():
    runApp(width=700, height=700)

if __name__ == '__main__':
    main()