# TIE-02101: 13. Graafisen käyttöliittymän suunnitteleminen ja toteuttaminen (skaalautuva)
# Petrus Jussila

# The following program is a memory game.
# First the icons are covered by purple tiles
# which the user must click to discover icon beneath.
# Whenever the user clicks on a tile,
# the icon beneath will be revealed to the user.
# If the next click also reveals a icon and they match,
# the icons will stay up. If they don't match,
# the icons will be covered and miss counter will rise.

# Importing tkinter for gui
# Importing random for the shuffle for icons
# Importing os for restarting the program
from tkinter import *
from random import shuffle
from time import sleep
import os

tiles = []

# Insert 10 different .gif images into pictures[] which sizes are (70x70)
pictures = [
]

# The information of the rows and columns of the tiles.
# In this case 4 and 5 since there's 10 * 2 = 20 tiles.
# Also creates a miss counter for mistakes.
rows = 4
columns = 5
miss_counter = 0

# The lines (39-53) define the GUI
# from which the whole program operates on.
base = Tk()
base.title("Christmas memory game")
canvas = Canvas(base,height=340, width=700)
canvas.grid(row=0,column=0)
base.maxsize(height=340, width=700)
bgImg = PhotoImage(file="smth.gif")
canvas.create_image(340, 170, image=bgImg)
canvas.create_text(550,80,fill="white",font="Times 20",
                   text="Christmas themed")
canvas.create_text(550,110,fill="white",font="Times 20",
                   text="memory game")
canvas.create_text(550,160,fill="white",font="Times 20",
                   text="Match the icons to win!")
canvas.create_text(550,320,fill="white",font="Times 10",
                   text='Press "Esc" to quit.')
canvas.create_text(550,300,fill="white",font="Times 10",
                   text='Press "R" to restart.')

class Tile(object):
    def __init__(self, x, y, picture):
        """
        The program creates each tile to represent an object.
        :param x: The x-coordinate of the tile.
        :param y: The y-coordinate of the tile.
        :param picture: The picture the tile holds when "turned" over.
        """
        self.x = x
        self.y = y
        self.picture = picture

    def draw_face_down(self):
        """
        Creates a purple tile to hide under the icons.
        """
        self.box = canvas.create_rectangle(self.x, self.y, self.x + 70,
                                           self.y + 70, fill="#621FCA")
        self.isFaceUp = False

    def draw_face_up(self):
        """
        Deletes the purple tile and reveals the icon beneath.
        """
        canvas.delete(self.box)
        picture = PhotoImage(file=self.picture)
        canvas.create_image(self.x + 35, self.y + 35, image=picture)
        widget = Label(base, image=picture)
        widget.picture = picture
        self.isFaceUp = True

    def is_under_mouse(self, event):
        """
        Used to track whether the user's mouse is over an tile when clicked.
        """
        if(event.x > self.x and event.x < self.x + 70):
            if(event.y > self.y and event.y < self.y + 70):
                return True

# Creates an pair to each icon and then shuffles them.
shuffled_pictures = []
for picture in pictures:
    shuffled_pictures.append(picture)
    shuffled_pictures.append(picture)
shuffle(shuffled_pictures)

# Creates the icons and then calls the object
# to create the purple tiles in it's method.
for x in range(0,columns):
    for y in range(0,rows):
        tiles.append(Tile(x * 78 + 20, y * 78 + 10,
                          shuffled_pictures.pop()))

for i in range(len(tiles)):
    tiles[i].draw_face_down()

# Keeps track of which tiles are "flipped".
global flipped_tiles
flipped_tiles = []
flipped_per_turn = 0

def check_tiles():
    """
    Checks the two recently uncovered tiles whether they match or not.
    """
    if not(flipped_tiles[-1].picture == flipped_tiles[-2].picture):
        flipped_tiles[-1].draw_face_down()
        flipped_tiles[-2].draw_face_down()
        del flipped_tiles[-2:]
        global miss_counter
        global misses
        if miss_counter >= 1:
            canvas.delete(misses)
        miss_counter += 1
        misses = canvas.create_text(550, 260, fill="white", font="Times 20",
                                    text="Miss: " + str(miss_counter))
    else:
        base.bell()
        if len(flipped_tiles) == len(tiles):
            canvas.create_text(550, 230, fill="white", font="Times 20",
                               text="You win!")

def mouseclicked(event):
    """
    Flips a tile and if two have been flipped
    then it calls the function "check_tiles"
    """
    global flipped_tiles
    global flipped_per_turn
    for tile in tiles:
        if tile.is_under_mouse(event):
            if (not(tile.isFaceUp)):
                flipped_per_turn += 1
                tile.draw_face_up()
                flipped_tiles.append(tile)
                if flipped_per_turn == 2:
                    base.after(400, check_tiles)
                    flipped_per_turn = 0

def quit(event):
    """
    Ends the program.
    """
    base.destroy()

def reset(event):
    """
    Restarts the program.
    """
    python = sys.executable
    os.execl(python, python, *sys.argv)
    base.destroy()

def start():
    """
    Starts the program
    """
    base.mainloop()

# Key binds for the mouse1-button, Escape-button and r-key.

base.bind("<Button-1>", mouseclicked)
base.bind("<Escape>", quit)
base.bind("r", reset)

start()