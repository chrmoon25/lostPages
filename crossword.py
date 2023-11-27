########## NOTES ##########
# FIX BORDER SELECTION WITH WORDS
# CHANGE FONT/BACKGROUND COLOR
# ADD TIMER AND LIVES
# ADD HINTS
# ORGANIZE INTO CLASSES
# CENTER PLACEMENT

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
    ############################################################################
    app.words = ["dog", "CAT", "RAT", "HAT", "MAT", "BAT"]  # Words to find (test practice, will use txt later on)
    app.board = generateBoard(app.rows, app.cols, app.words)
    app.selectedCells = [] ###
    app.wordLines = [] ###

# Cell selection (5.3.3)
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
        app.selectedCells.append(selectedCell)
        print(app.selectedCells)

def redrawAll(app):
    drawBoardBorder(app)
    drawBoard(app)
    drawWordLines(app)
    for cell in app.selectedCells:
        drawSelectedCell(app, cell)

# CITATION: I used some solver logic in http://www.krivers.net/15112-f18/notes/notes-wordsearch.html to help with generating the board (theirs was hard-coded).
# (CMU 15-112: Fundamentals of Programming and Computer Science, Class Notes: Understanding Word Search, Fall 18)
def generateBoard(rows, cols, words): ###
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    board = [[' ' for _ in range(cols)] for _ in range(rows)] 
    for word in words:
        word = word.upper() # All words should be uppercase for consistency
        direction = random.choice([(0, 1), (1, 0)])  # Random horizontal or vertical direction
        while True: # To find valid placement on the board
            startRow = random.randint(0, rows - 1) # Randomly chosen starting positions in the board's boundaries
            startCol = random.randint(0, cols - 1) # Same goes for over here
            endRow = startRow + direction[0] * (len(word) - 1) # Calculated based on the starting position and direction of word
            endCol = startCol + direction[1] * (len(word) - 1)
            # Word should fit within the boundaries of the board, if it does, the placement returns True
            if 0 <= endRow < rows and 0 <= endCol < cols: 
                validPlacement = True
                for i in range(len(word)):
                    # must check if cell at calculated position on the board is not empty
                    # must also check if it's doesn't already contain the letter of the word that is going to be placed
                    if board[startRow + i * direction[0]][startCol + i * direction[1]] != ' ' and board[startRow + i * direction[0]][startCol + i * direction[1]] != word[i]:
                        validPlacement = False
                        # exit loop bc placement direction for this word is not valid
                        break
                # this is the opposite, meaning the placement is valid
                if validPlacement:
                    for i in range(len(word)):
                        # this will place the letter onto the board (by looping though each letter)
                        board[startRow + i * direction[0]][startCol + i * direction[1]] = word[i]
                    # next word!
                    break
    # after everything is done, for the remaning empty spaces of the board, add a random letter from the alphabet
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
    # Cell selection (5.3.3)
    color = 'cyan' if (row, col) == app.selection else None
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)
    drawLabel(app.board[row][col], cellLeft + cellWidth/2, cellTop + cellHeight/2, size=15)

# CITATION: I used code under 5.3.3 of "Cell Selection" in CS Academy for selected words.
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

################################################################################

def drawSelectedCell(app, cell): ####
    row, col = cell
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    # This is similar to the drawCell function, but we check if the cell is in the list so it stays yellow
    color = 'yellow' if cell in app.selectedCells else None
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)
    drawLabel(app.board[row][col], cellLeft + cellWidth / 2, cellTop + cellHeight / 2, size=15)

def drawWordLines(app):
    selected_word = ''.join([app.board[row][col] for (row, col) in app.selectedCells])
    # TEST - erase later
    print(selected_word)
    if selected_word in app.words:
        print("WORD FOUND")
        # Draw a stikethrough - so far words found returns correctly
        # This is only for one word though
        # Make a list for found words, then reset

def main():
    runApp(width=500, height=500)

main()