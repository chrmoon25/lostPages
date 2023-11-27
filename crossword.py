########## NOTES ##########
# FIX BORDER SELECTION WITH WORDS
# CHANGE FONT/BACKGROUND COLOR
# ADD TIMER AND LIVES
# ADD HINTS

from cmu_graphics import *
import random
import math

def onAppStart(app):
    app.rows = 8
    app.cols = 8
    app.boardLeft = 50
    app.boardTop = 75
    app.boardWidth = 400
    app.boardHeight = 400
    app.cellBorderWidth = 2
    app.selection = (0, 0)
    app.words = ["DOG", "CAT", "RAT", "HAT", "MAT", "BAT"]  # Words to find
    app.board = generateBoard(app.rows, app.cols, app.words)
    app.selectedCells = set() ###
    app.wordLines = [] ###
    app.timerDelay = 1000  ### 1 second delay
    app.elapsedTime = 0 ###
    app.cellTimer = None ###

# Cell selection
def onMouseMove(app, mouseX, mouseY):
    selectedCell = getCell(app, mouseX, mouseY)
    if selectedCell != None:
      if selectedCell == app.selection:
          app.selection = selectedCell
      else:
          app.selection = selectedCell

def onMousePress(app, mouseX, mouseY): ###
    selectedCell = getCell(app, mouseX, mouseY)
    if selectedCell != None:
        app.selection = selectedCell
        app.selectedCells.add(selectedCell)
        if app.cellTimer != None:
            app.timerDelay = 7000  # Set delay to 7 seconds for resetting color
            app.elapsedTime = 0
        else:
            app.cellTimer = True

# def timerTimeout(app): ###
#     if app.cellTimer:
#         app.elapsedTime += app.timerDelay
#         if app.elapsedTime >= 7000:
#             app.selectedCells = set()  # Reset selected cells after 7 seconds
#             app.cellTimer = None

def generateBoard(rows, cols, words):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    for word in words:
        word = word.upper()
        direction = random.choice([(0, 1), (1, 0)])  # Random horizontal or vertical direction
        while True:
            startRow = random.randint(0, rows - 1)
            startCol = random.randint(0, cols - 1)
            endRow = startRow + direction[0] * (len(word) - 1)
            endCol = startCol + direction[1] * (len(word) - 1)
            if 0 <= endRow < rows and 0 <= endCol < cols:
                validPlacement = True
                for i in range(len(word)):
                    if board[startRow + i * direction[0]][startCol + i * direction[1]] != ' ' \
                            and board[startRow + i * direction[0]][startCol + i * direction[1]] != word[i]:
                        validPlacement = False
                        break
                if validPlacement:
                    for i in range(len(word)):
                        board[startRow + i * direction[0]][startCol + i * direction[1]] = word[i]
                    break
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == ' ':
                board[row][col] = random.choice(alphabet)
    return board

# CITATION: I used code under 5.3.2 of "Drawing a 2d Board" in CS Academy to build the base of my crossword.
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

def drawBoardBorder(app):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
             fill=None, border='black',
             borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    # Cell selection
    color = 'cyan' if (row, col) == app.selection else None
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)
    drawLabel(app.board[row][col], cellLeft + cellWidth/2, cellTop + cellHeight/2, size=15)

# def drawWordLines(app): ###
#     for line in app.wordLines:
#         startRow, startCol, endRow, endCol = line
#         startCellX, startCellY = getCellLeftTop(app, startRow, startCol)
#         endCellX, endCellY = getCellLeftTop(app, endRow, endCol)
#         cellWidth, cellHeight = getCellSize(app)
#         drawLine(startCellX + cellWidth / 2, startCellY + cellHeight / 2,
#                  endCellX + cellWidth / 2, endCellY + cellHeight / 2,
#                  width=5, fill='green')

def drawSelectedCell(app, cell): ####
    row, col = cell
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    color = 'yellow' if cell in app.selectedCells else None
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)
    drawLabel(app.board[row][col], cellLeft + cellWidth / 2, cellTop + cellHeight / 2, size=15)

# Cell selection
def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
      return (row, col)
    else:
      return None

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def redrawAll(app):
    # drawLabel('Word Search Game', 300, 30, size=16)
    drawBoardBorder(app)
    drawBoard(app)
    # drawWordLines(app)
    for cell in app.selectedCells:
        drawSelectedCell(app, cell)

def main():
    runApp(width=500, height=500)

main()
