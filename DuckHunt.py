from superwires import games, color
import pygame.display, pygame.mouse
from random import randint

# Setup game window
foreground = None

games.init(screen_width=640, screen_height=480, fps=60)
pygame.display.set_caption("Duck Hunt")








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