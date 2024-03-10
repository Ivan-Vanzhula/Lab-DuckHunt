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