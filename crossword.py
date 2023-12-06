from cmu_graphics import *
import random
import math
import time
import tkinter as tk

def onAppStart(app):
    screenWidth = 700
    boardWidth = 400
    app.background = 'linen'
    app.rows = 10
    app.cols = 10
    app.boardLeft = (screenWidth - boardWidth) // 2
    app.boardTop = 60
    app.boardWidth = 400
    app.boardHeight = 400
    app.cellBorderWidth = 2
    app.selection = (0, 0)
    wordPool =  [
                "PERCY", "GREGOR", "CINDER", "EMMA", "MATILDA", "ALICE", "VIOLET", "KEVIN", "OSAMU", "AUSTEN", 
                "RIORDAN", "KAFKA", "DAHL", "CAMUS", "CIRCE", "MILLER", "ULYSSES", "HOLMES", "WATCHMEN", 
                "ISHIGURO", "CHBOKSY", "STEINBECK", "SALINGER", "CARROLL", "HOLES", "ATONEMENT", "CRESS", 
                "CORALINE", "ORWELL", "WILDE", "PERSUASION", "CARRIE", "DRACULA", "GATSBY"
                ]
    # CITATION: How to use random to select items in a list - https://www.geeksforgeeks.org/python-random-sample-function/ 
    app.words = random.sample(wordPool, 8)
    app.board = generateBoard(app.rows, app.cols, app.words)
    app.selectedCells = [] 
    app.wordLines = [] 
    app.wordBank = []
    app.wordFound = False

# CITATION: I used code under 5.3.3 of "Cell Selection" in CS Academy for hovering words.
def onMouseMove(app, mouseX, mouseY):
    selectedCell = getCell(app, mouseX, mouseY)
    if selectedCell != None:
      if selectedCell == app.selection:
          app.selection = selectedCell
      else:
          app.selection = selectedCell

# CITATION: I used some solver logic in http://www.krivers.net/15112-f18/notes/notes-wordsearch.html to help generate the board (theirs was hard-coded)
# CMU 15-112: Fundamentals of Programming and Computer Science, Class Notes: Understanding Word Search, Fall 18
def generateBoard(rows, cols, words): ###
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    board = [[' ' for _ in range(cols)] for _ in range(rows)] 
    for word in words:
        word = word.upper() # all words should be uppercase for consistency
        direction = random.choice([(0, 1), (1, 0)])  # random horizontal or vertical direction
        while True: 
            startRow = random.randint(0, rows - 1) # randomly chosen starting positions in the board's boundaries
            startCol = random.randint(0, cols - 1) 
            endRow = startRow + direction[0] * (len(word) - 1) # based on the starting position and direction of word
            endCol = startCol + direction[1] * (len(word) - 1)
            if 0 <= endRow < rows and 0 <= endCol < cols: 
                validPlacement = True
                for i in range(len(word)):
                    # must check if cell at calculated position on the board is not empty
                    # must also check if it's doesn't already contain the letter of the word that is going to be placed
                    if board[startRow + i * direction[0]][startCol + i * direction[1]] != ' ' and board[startRow + i * direction[0]][startCol + i * direction[1]] != word[i]:
                        validPlacement = False
                        break
                if validPlacement:
                    for i in range(len(word)):
                        # this will place the letter onto the board (by looping though each letter)
                        board[startRow + i * direction[0]][startCol + i * direction[1]] = word[i]
                    break
    # for the remaning empty spaces of the board, add a random letter from the alphabet
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == ' ':
                board[row][col] = random.choice(alphabet)
    return board

# CITATION: I used code under 5.3.2 of "Drawing a 2d Board" in CS Academy to build the base of my crossword
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

def drawBoardBorder(app):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
             fill=None, border='saddleBrown',
             borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    # CITATION: Cell Selection (5.3.3)
    color = 'tan' if (row, col) == app.selection else 'blanchedAlmond'
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='saddleBrown',
             borderWidth=app.cellBorderWidth)
    drawLabel(app.board[row][col], cellLeft + cellWidth/2, cellTop + cellHeight/2, size=15, font='Metamorphous', fill='black')

# CITATION: I used code under 5.3.3 of "Cell Selection" in CS Academy for selected words
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

def drawSelectedCell(app, cell): 
    row, col = cell
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    # This is similar to the drawCell function, but we check if the cell is in the list so it stays filled
    color = 'tan' if cell in app.selectedCells else None
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='saddleBrown',
             borderWidth=app.cellBorderWidth)
    drawLabel(app.board[row][col], cellLeft + cellWidth / 2, cellTop + cellHeight / 2, size=15, font='Metamorphous', fill='black')

### Citation (5.3.3) ends here

def drawLineThroughWord(app, startRow, startCol, endRow, endCol):
    cellWidth, cellHeight = getCellSize(app)
    startX = app.boardLeft + startCol * cellWidth + cellWidth / 2
    startY = app.boardTop + startRow * cellHeight + cellHeight / 2
    endX = app.boardLeft + endCol * cellWidth + cellWidth / 2
    endY = app.boardTop + endRow * cellHeight + cellHeight / 2
    drawLine(startX, startY, endX, endY, lineWidth=3, fill='fireBrick') 

def checkAndUpdateWord(app):
    selectedWord = ''.join([app.board[row][col] for (row, col) in app.selectedCells])
    if selectedWord in app.words:
        app.wordBank.append(selectedWord)
        app.selectedWordCoords = app.selectedCells[:]  # store word coordinates for drawing
        lineCoords = tuple(app.selectedWordCoords[0] + app.selectedWordCoords[-1])
        # translates to (x1, y1, x2, y2)
        app.wordLines.append(lineCoords)
        app.wordFound = True 
    else:
        startTime(app) 

    # CITATION: How to close a window with tkinter - https://www.geeksforgeeks.org/how-to-close-a-window-in-tkinter/#:~:text=To%20close%20a%20tkinter%20window%2C%20we%20can%20use%20the%20destroy,with%20the%20main%20tkinter%20window.
    if len(app.wordBank) == len(app.words):
        root = tk.Tk()  
        root.destroy()
    
def drawLinesThroughWords(app):
    lines = []
    for lineCoords in app.wordLines:
        startRow, startCol, endRow, endCol = lineCoords
        # draw the line and append the line coordinates to the list
        drawLineThroughWord(app, startRow, startCol, endRow, endCol)
        lines.append(lineCoords)

def drawWordBank(app):
    wordSpacing = (600 - 200) // 4
    # ensures even spacing
    textStartY = 600
    textStartX = 200

    for i in range(len(app.words)):
        # we want 4 words across
        drawLabel(app.words[i], textStartX + (i % 4) * wordSpacing, textStartY + (i // 4) * 30,
                  size=12, font='Metamorphous', fill='black')

def startTime(app):
    app.timerDelay = 3000  # 3 seconds
    app.startTime = time.time()

def onMousePress(app, mouseX, mouseY):
    selectedCell = getCell(app, mouseX, mouseY)
    if selectedCell != None:
        app.selection = selectedCell
        app.selectedCells.append(selectedCell)
        checkAndUpdateWord(app)

def onStep(app):
    # CITATION: To check for attributes - https://pythonhow.com/how/know-if-an-object-has-an-attribute/#:~:text=To%20check%20if%20an%20object,True%2C%20otherwise%20it%20returns%20False.
    if hasattr(app, 'startTime'):
        elapsedTime = time.time() - app.startTime
        if elapsedTime >= app.timerDelay / 1000:  # convert timerDelay to seconds
            app.selectedCells = []  # clear selected cells after the time delay
            del app.startTime  # remove the timer start time attribute
            app.timerDelay = None 
            
def redrawAll(app):
    drawBoard(app)
    for cell in app.selectedCells:
        drawSelectedCell(app, cell)
    drawBoardBorder(app)
    drawLinesThroughWords(app)
    drawWordBank(app)
    drawLabel('find all the words to collect the page!', 350, 30, size = 15, font = 'Pixelify Sans SemiBold', fill = 'saddleBrown')
    drawLabel('words must be selected in the right order!', 350, 480, size = 15, font = 'Pixelify Sans SemiBold', fill = 'saddleBrown')
    drawLabel('if you mess up, wait 3 seconds for the app to deselect.', 350, 500, size = 15, font = 'Pixelify Sans SemiBold', fill = 'saddleBrown')
    drawLabel('WORD BANK', 350, 550, size=17, font = 'Pixelify Sans SemiBold', fill = 'saddleBrown')

def main():
    runApp(width=700, height=700)

main()