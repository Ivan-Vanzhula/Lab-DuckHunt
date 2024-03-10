from superwires import games, color
import pygame.display, pygame.mouse
from random import randint

# Setup game window
foreground = None

games.init(screen_width=640, screen_height=480, fps=60)
pygame.display.set_caption("Duck Hunt")

# CLASS ====================================
# Name.........: GameScores
# Description..: Will store game scores
# Syntax.......: GameScores()
# ==========================================
class GameScores:
    score = 0  # Current game score
    ducksHit = 0  # Number of ducks hit
    totalShots = 0  # Total number of shots taken
    totalDucks = 0  # Total number of ducks spawned

    @staticmethod
    def reset_score():
        """ Reset the game scores """
        GameScores.score = 0
        GameScores.ducksHit = 0
        GameScores.totalShots = 0
        GameScores.totalDucks = 0

# CLASS ====================================
# Name.........: Cursor
# Description..: Sets mouse to the crosshair
# Syntax.......: Cursor()
# ==========================================
class Cursor(games.Sprite):
    """ Cursor Object """
    clicked = False
    isShotAllowed = False

    xPos = games.mouse.x
    yPos = games.mouse.y

    images = [games.load_image(f"Sprites/Cursors/Cursor_{i}.png") for i in range(1, 5)]

    def __init__(self):
        """ Cursor Initializer """

        super(Cursor, self).__init__(image=self.images[0], x=games.mouse.x, y=games.mouse.y)

        self.mouseClicked = False
        self.mouseCounter = 0

        # Load gunshot sound
        self.gunShotSound = games.load_sound("Sounds/shot.wav")

    def update(self):
        # Keep the sprite at the same x and y location as the mouse
        self.x = Cursor.xPos
        self.y = Cursor.yPos

        # Remove and read to put on top of any birds
        games.screen.remove(self)
        games.screen.add(self)


# FUNCTION ==================================
# Name.........: Main
# Description..: Will start the game
# Syntax.......: main()
# ==========================================
def main():
    global foreground  # Declare 'foreground' as a global variable

    while True:
        foreground = games.Sprite(image=games.load_image("Sprites/foreground.png"), left=1, bottom=390)
        games.screen.background = games.load_image("Sprites/background.png", transparent=False)

        # Add the foreground sprite to the screen
        games.screen.add(foreground)
        # Hide the mouse cursor
        games.mouse.is_visible = False


# Start!
main()