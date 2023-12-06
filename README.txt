PROJECT DESCRIPTION:
--------------------------------------------------------------------------------
The name of my project is Lost Pages. It is a maze-based game where the player 
is in a “magical library” and must collect all the pages in the maze to escape. 
To collect the pages, the player must solve word puzzles. The puzzles are word 
searches that are themed after my favorite books (including their characters 
and authors). 

HOW TO RUN THE PROJECT:
--------------------------------------------------------------------------------
To run the project, go to the terminal and simply run the path of the main 
lostPages.py file. I personally run it through my computer by typing in the 
command, "python3 /Users/jiynmn/Desktop/15-112/lostPages/lostPages.py". You 
will need to replace /Users/jiynmn/Desktop/15-112/lostPages/lostPages.py 
with the location of the file. It is important to check that all the 
necessary assets for the program are in the folder. 

Since all of my assets and sub-files were loaded locally, you will need to 
replace their paths with wherever the lostPages folder is located on your 
computer. For example, when I loaded the gif for the main player, I used 
'/Users/jiynmn/Desktop/15-112/lostPages/assets/sprite.gif'. This is the 
same for the crossword file. When the player collides with a page in the 
game, it uses subprocess to open the file. You will need to replace this 
file destination for wherever you store the crossword.py file.

The "post-MVP" libraries I use in my code are subprocess (to open files) and 
tkinter (to close windows). Since these are part of the general Python library, 
no external installation is required, as long as the user as python3 up to date.

For fonts, I used the Google Fonts "Metamorphous" and "Pixelify Sans." To upload 
these fonts so that I could use them in my project, I added them to my Font Book 
(on Mac). I did this by going to Font Book > File > Add Fonts to Current User, 
then uploading the folder. If you are on Windows, you can add these fonts in 
Control Panel > Appearance and Personalization > Fonts.


*** There are no shortcut commands
*** All assets and fonts are provided in the submission
