########## NOTES ##########
# Player sprite: https://kyunt.itch.io/purple-thief-player-animation-enemies-items
# Book sprite: https://wifflegif.com/gifs/706281-pixel-art-spell-gif
# Wall image: https://superwalrusland.com/ohr/issue26/pa/pixelart.html 
# Page sprite: https://pixeldungeon.fandom.com/wiki/Scroll_of_Mirror_Image 
# Potion sprites: https://wiki.hypixel.net/Potions
# Portal gif: https://www.pinterest.com/pin/5770305765823550/ 
# Ghosts: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.deviantart.com%2Fandwise1121%2Fart%2FGhost-idle-892396700&psig=AOvVaw3eGvgNnC5_5xCprYBaPUS2&ust=1701499213399000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCJjN-dXQ7YIDFQAAAAAdAAAAABAD
# cite gif source (mike)
# 

from cmu_graphics import *
from PIL import Image
import math
import random
# import time


# CITATION: I followed parts of a tutorial from "Tokyo EdTech" from YouTube - https://www.youtube.com/watch?v=inocKE13DEA&list=PLlEgNdBJEO-lNDJgg90fmfAq9RzORkQWP
# although they used turtle to help build their maze.
# Lists to store walls and collected pages
walls = []
pages = []
ghosts = []
levels = [""]
wallWidth = 24 
app.background = 'black'

# Class to represent the walls (each little block)
class Pen():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # self.color = 'white'

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
        if distance < 6:
            return True
        else:
            return False
        
    def wallCollision(self, dx, dy, walls):
        new_x = self.x + dx
        new_y = self.y + dy

        # Check if any part of the player will collide with a wall
        player_left = new_x - 7  # Adjust  player's left edge
        player_right = new_x + 7  # Adjust player's right edge
        player_top = new_y - 10  # Adjust player's top edge
        player_bottom = new_y + 10  # Adjust player's bottom edge

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
        self.visible = True

class Page():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visible = True
        self.gold = 100

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
        self.gold = 25
        self.direction = random.choice(['up', 'down', 'left', 'right'])


    def move(self):
        dx, dy = 0, 0
        if self.direction == 'up':
            dy = 2
        if self.direction == 'down':
            dy = -2
        if self.direction == 'left':
            dx = -2
            # fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
        if self.direction == 'right':
            dx = 2

        
        # moveX = self.x + dx
        # moveY = self.y + dy

        if self.wallCollision(dx, dy, walls):
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

    
    # def chase(self, player):
    #     start = (self.x, self.y)
    #     target = (player.x, player.y)

    #     print(start)
    #     print(target)
        
    #     path = self.BFS(start, target, walls) 
    #     # make the path 

    #     self.moveAlongPath(path)
    #     # move along the path

    # def BFS(self, start, target, walls):
    #     pass

    # Inside the Ghost class

    def heuristic(self, a, b):
        # Calculate the heuristic (Manhattan distance)
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def AStar(self, start, target, walls):
        open_set = {start}
        closed_set = set()
        came_from = dict()

        g_score = {start: 0}
        f_score = {start: self.heuristic(start, target)}

        while open_set:
            current = None
            current_f_score = float('inf')
            for position in open_set:
                if f_score[position] < current_f_score:
                    current = position
                    current_f_score = f_score[position]

            if current == target:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]  # Reverse the path to get it from start to target

            open_set.remove(current)
            closed_set.add(current)

            for neighbor in self.get_neighbors(current):
                if neighbor in closed_set or neighbor in walls:
                    continue

                tentative_g_score = g_score[current] + 1  # Assuming each move cost is 1

                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, target)
                    if neighbor not in open_set:
                        open_set.add(neighbor)

        return None  # If no path found

    def get_neighbors(self, position):
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
            next_x, next_y = path[0]
            dx = next_x - self.x
            dy = next_y - self.y

            if self.wallCollision(dx, dy, walls):
                self.x = next_x
                self.y = next_y

            # Remove the first position as it's reached
            path.pop(0)
    # CITATION: Used for pathfinding with BFS
    # https://www.cs.cmu.edu/~112/notes/student-tp-guides/Pathfinding.pdf
    # https://en.wikipedia.org/wiki/Breadth-first_search 
    # https://favtutor.com/blogs/breadth-first-search-python
    # refine this part more 

# putting this here for reference - https://favtutor.com/blogs/breadth-first-search-python
    


# Hard-coded maze (planning to add more levels in the future)
# Tried recursive backtracing but it was a mess so I'm sticking with hard-code right now

levelOne = [
    "XXXXXXXXXXXXXXXXXXXX",
    "XP                 X",
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
    "X    X  X    X     X",
    "X XXXX TX XXXX XX XX",
    "X X    XX   X      X",
    "X X XXXX  XXXXXXXX X",
    "X X   X   X   X    X",
    "X XXX X XXX X XXXX X",
    "X     X     X   X  X",
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
                
    return maze, player, page, ghost, portal


def onKeyHold(app, keys):
    dx, dy = 0, 0
    if 'up' in keys or 'w' in keys:
        dy = -5
    elif 'down' in keys or 's' in keys:
        dy = 5
    elif 'left' in keys or 'a' in keys:
        dx = -5
    elif 'right' in keys or 'd' in keys:
        dx = 5

    # Multiply by the step size you want to move
    # dx *= stepSize
    # dy *= stepSize

    app.player.move(dx, dy, walls)

def onAppStart(app):
    app.counter = 0
    app.framesPerStep = 5
    # app.steps = 1000
    app.maze, app.player, app.page, app.ghost, app.portal = setupMaze(levels[1], app) 

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
    
    pageGif = Image.open('/Users/jiynmn/Desktop/15-112/lostPages/assets/scroll.gif')
    app.pageSpriteList = []
    for frame in range(pageGif.n_frames):
        pageGif.seek(frame)
        fr = pageGif.resize((20, 20))  # Resize to 24x24 pixels
        cmu_image = CMUImage(fr)
        app.pageSpriteList.append(cmu_image)

    portalGif = Image.open('/Users/jiynmn/Desktop/15-112/lostPages/assets/portal.gif')
    app.portalSpriteList = []
    for frame in range(portalGif.n_frames):
        portalGif.seek(frame)
        fr = portalGif.resize((40, 40))  # Resize to 24x24 pixels
        cmu_image = CMUImage(fr)
        app.portalSpriteList.append(cmu_image)
    
    wallImage = Image.open('/Users/jiynmn/Desktop/15-112/lostPages/assets/wall.jpg')
    app.wallSprite = CMUImage(wallImage.resize((24, 24))) 

    print(app.playerSpriteList)
    print(app.ghostSpriteList)
    print(app.pageSpriteList)
    print(app.portalSpriteList)


    app.spriteCounter = 0
    app.stepsPerSecond = 500

def onStep(app):
    # app.moveSpeed = 5
    #Set spriteCounter to next frame

    app.counter += 1
    if app.counter % app.framesPerStep == 0:
        app.spriteCounter = (app.spriteCounter + 1) % len(app.playerSpriteList)
    

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

    
    # Check collision between player and pages, and add gold if collision is made
    # Hiding feature not working at the moment
    for page in pages:
        if app.player.isCollision(page):
            app.player.gold += page.gold
            print("Player Gold: {}".format(app.player.gold))
            page.destroy()
            pages.remove(page) # Each page is a one time instance (100 gold only one time)
    
    for ghost in ghosts:
        ghost.move()

        if app.player.isCollision(ghost):
            print("YOU DIED!!!")

        if ghost.isClose(app.player):
            print("ghost is CLOSE!")
            ghost.chase(app.player)
 

    

def main():
    runApp(width=700, height=700)

if __name__ == '__main__':
    main()