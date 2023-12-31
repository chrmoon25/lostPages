# CITATIONS FOR GIFS/IMAGES:
# Ghosts: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.deviantart.com%2Fandwise1121%2Fart%2FGhost-idle-892396700&psig=AOvVaw3eGvgNnC5_5xCprYBaPUS2&ust=1701499213399000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCJjN-dXQ7YIDFQAAAAAdAAAAABAD
# "You Win": https://www.greekcomics.gr/forums/index.php?/profile/25133-tik/content/page/25/&type=forums_topic_post 
# Player: https://kyunt.itch.io/purple-thief-player-animation-enemies-items
# Pages: https://pixeldungeon.fandom.com/wiki/Scroll_of_Mirror_Image 
# Walls: https://superwalrusland.com/ohr/issue26/pa/pixelart.html 
# Portal: https://www.pinterest.com/pin/5770305765823550/ 
# Hearts: https://tenor.com/search/pixel-heart-gifs
# "Game Over": https://pngimg.com/image/83319

# CITATIONS FOR FONTS:
# https://fonts.google.com/specimen/Pixelify+Sans
# https://fonts.google.com/specimen/Metamorphous?query=meta 

# CITATIONS FOR COLORS/HOW TO UPLOAD FONTS:
# Colors - https://academy.cs.cmu.edu/docs/label
# Fonts - https://piazza.com/class/lkq6ivek5cg1bc/post/2217

from cmu_graphics import *
from PIL import Image
import math
import random
import subprocess

# CITATION: I followed parts of a tutorial from "Tokyo EdTech" on YouTube to help build the base of my maze
# https://www.youtube.com/watch?v=inocKE13DEA&list=PLlEgNdBJEO-lNDJgg90fmfAq9RzORkQWP
walls = []
pages = []
ghosts = []
portalPosition = []
levels = [""]
wallWidth = 24 
app.background = 'black'
app.won = False
app.lost = False

class Pen():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hearts = 3
        self.lastCollideTime = 0
        self.collideTime = 60
        self.pagesCollected = 0

    def loseHeart(self):
        self.hearts -= 1
    
    # method to check the collision between the player and other objects in the maze
    def isCollision(self, other):
        a = self.x - other.x
        b = self.y - other.y
        distance = math.sqrt((a**2) + (b**2))
        if distance < 6:
            return True
        else:
            return False
        
    def wallCollision(self, dx, dy, walls):
        new_x = self.x + dx
        new_y = self.y + dy

        # check if any part of the player will collide with a wall
        player_left = new_x - 7  
        player_right = new_x + 7 
        player_top = new_y - 10  
        player_bottom = new_y + 10   

        for wall_x, wall_y in walls:
            # adjusted the walls' sides considering its width of 24 (12 but 11 jsut in case)
            wall_left = wall_x - 11
            wall_right = wall_x + 11
            wall_top = wall_y - 11
            wall_bottom = wall_y + 11

            if (player_left < wall_right and player_right > wall_left and
                player_top < wall_bottom and player_bottom > wall_top):
                return False  # collision detected, can't move

        return True
    
    def move(self, dx, dy, walls):
        if self.wallCollision(dx, dy, walls):
            self.x += dx
            self.y += dy
        # no collisions detected, move to the new position

class Portal():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Page():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visible = True

    # method to hide the pages when they are walked over
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

        # adjusted this a little since ghost imgs are bigger than player
        player_left = new_x - 12  
        player_right = new_x + 12  
        player_top = new_y - 12  
        player_bottom = new_y + 12  

        for wall_x, wall_y in walls:
            wall_left = wall_x - 11
            wall_right = wall_x + 11
            wall_top = wall_y - 11
            wall_bottom = wall_y + 11

            if (player_left < wall_right and player_right > wall_left and
                player_top < wall_bottom and player_bottom > wall_top):
                return False  

        return True

    # CITATION: All links below were used for pathfinding with A* search algorithm
    # Backtracking -  https://stackoverflow.com/questions/42884863/a-star-algorithm-understanding-the-f-g-h-scores
    # Understanding g, h nodes and pseudocode - https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
    # Understanding implementation (heuristic via manhattan distance) and pseudocode - https://www.geeksforgeeks.org/a-search-algorithm/
    # Example tutorial - https://www.youtube.com/watch?time_continue=4&v=crDPaKwDnDY&embeds_referring_euri=https%3A%2F%2Fwww.google.com%2F&source_ve_path=MjM4NTE&feature=emb_title
    # Main source (provided by mentor) -  https://www.cs.cmu.edu/~112/notes/student-tp-guides/Pathfinding.pdf
    # https://en.wikipedia.org/wiki/A*_search_algorithm#:~:text=A*%20is%20an%20informed%20search,shortest%20time%2C%20etc.).
    def heuristic(self, a, b):
        # calculates manhattan distance between the ghost (start) and player (target)
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def AStar(self, start, target, walls):
        # set of positions to be explored
        toVisit = {start}
        # places already visited
        visited = set()
        # backtrack to make shortest distance
        stepBack = dict()

        # g will keep track of the actual cost from start position to any position (following best path)
        gScore = {start: 0}
        # f stores total estimated cost of the cheapest path (g), this is done by heuristic calculation
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
                if neighbor in visited or neighbor in walls: 
                    continue

                newgScore = gScore[current] + 1  # since each move is 1

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

            # remove the first position as it's reached
            path.pop(0)

levelOne = [
    "XXXXXXXXXXXXXXXXXXXX",
    "XP               X X",
    "X X   XXXXXXXX   X X",
    "X XXX      X     X X",
    "X     X  X X XX XX X",
    "XXXX  X XX X  G    X",
    "X TX  X  X XXXX X  X",
    "X  X XXXXX    X X TX",
    "X  X        X XXXXXX",
    "XX XXXXXXXXXX      X",
    "X  X   X    XXXX X X",
    "X    X   X     X X X",
    "XXXXXXXX X XXX X   X",
    "X X    X X  XX XXX X",
    "X   XX       X   X X",
    "X X  XXXXXXXGXX  X X",
    "X    X TX    X     X",
    "X XXXX  X XXXX XX XX",
    "X X    XX   X      X",
    "X X XXXX  XXXXXXXX X",
    "X X   X   X      X X",
    "X XXX X XXX XX  XX X",
    "X     X     X   X  X",
    "XXXXXXXXXXXXXXXOXXXX",
]
levels.append(levelOne)

def setupMaze(level, app):
    maze = []
    player = None
    portal = None
    mazeHeight = len(level)
    mazeWidth = len(level[0])
    # center the maze 
    mazeX = (app.width - mazeWidth * 24) // 2 
    mazeY = (app.height - mazeHeight * 24) // 2 

    # maze dimensions - if the playing screen is 700 x 700 and the actual maze is 600 x 600...
    # then we can fit around 24 blocks down and across
    for y in range(mazeHeight):
        for x in range(mazeWidth):
            character = level[y][x]
            screenX = mazeX + x * 24
            screenY = mazeY + y * 24

            if character == "X":
                pen = Pen(screenX, screenY)
                maze.append(pen)
                walls.append((screenX, screenY))

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
                portalPosition.append((screenX, screenY))
                
    return maze, player, page, ghost, portal

def onMousePress(app, mouseX, mouseY):
    if app.won or app.lost:
        labelWidth = 150
        labelHeight = 45
        
        labelX = (app.width - labelWidth) // 2
        labelY = (app.height - labelHeight) // 2 + 75
        
        # allows player to restart game
        if labelX < mouseX < labelX + labelWidth and labelY < mouseY < labelY + labelHeight:
            app.won = False
            app.lost = False
            app.maze, app.player, app.page, app.ghost, app.portal = setupMaze(levels[1], app) 

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
    # CITATION: Gif demo (from lecture 11/21)
    # https://piazza.com/class/lkq6ivek5cg1bc/post/2231
    gif = Image.open(filePath)
    spriteList = []
    
    for frame in range(gif.n_frames):
        gif.seek(frame)
        resizedFrame = gif.resize((width, height))
        cmu_image = CMUImage(resizedFrame)
        spriteList.append(cmu_image)
    return spriteList

def onAppStart(app):
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

    gameOver = Image.open('/Users/jiynmn/Desktop/15-112/lostPages/assets/gameOver.png')
    app.gameOver = CMUImage(gameOver) 

    youWin = Image.open('/Users/jiynmn/Desktop/15-112/lostPages/assets/youWin.png')
    app.youWin = CMUImage(youWin.resize((330, 220)))

def onStep(app):
    # gifs
    if app.paused == False:
        app.counter += 1
        if app.counter % app.framesPerStep == 0:
            app.spriteCounter = (app.spriteCounter + 1) % len(app.playerSpriteList)

        # timer buffer (the isCollision method is sensitive and we don't want to rapidly lose all hearts)
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
        elif isinstance(item, Page) and item.visible: 
            drawImage(app.pageSpriteList[app.spriteCounter], item.x, item.y, align = 'center')
        elif isinstance(item, Portal):
            drawImage(app.portalSpriteList[app.spriteCounter], item.x, item.y, align = 'center')

    pageText = f"pages collected: {app.player.pagesCollected}/3"
    textX = app.width - 610
    textY = 25
    drawLabel(pageText, textX, textY, fill = 'white', size = 15, font = 'Pixelify Sans SemiBold')

    heartSpacing = 30  
    heartX = app.width - 25  
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
            # CITATION: I used the videos below to help me run my crossword.py in this file using subprocess
            # https://www.youtube.com/watch?v=CUFIjz_U7Mo 
            # https://youtu.be/AAfy0-AWg-A?si=bg1AUZNPb0yGkCW4
            subprocess.Popen(['python3', '/Users/jiynmn/Desktop/15-112/lostPages/crossword.py'])
            page.destroy()
            app.player.pagesCollected += 1
            pages.remove(page) 

    if app.player.pagesCollected != 3 and app.player.isCollision(app.portal):
        pageText = 'you have not collected all the pages!'
        textX = 350
        textY = 660
        drawLabel(pageText, textX, textY, fill = 'red', bold = True, size = 14, font = 'Pixelify Sans SemiBold')

    for ghost in ghosts:
        if app.paused == False:
            ghost.move()
        if ghost.isClose(app.player):
            ghost.chase(app.player)

def main():
    runApp(width=700, height=700)

if __name__ == '__main__':
    main()