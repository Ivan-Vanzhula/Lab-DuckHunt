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
# Name.........: Game
# Description..: Will spawn ducks/check for pause
# Syntax.......: Game()
# ==========================================
class Game(games.Sprite):
    """ Duck Spawner Class """
    image = games.load_image("Sprites/spawner.png")

    # State of Game
    paused = False  # True when game is paused
    over = False  # True when game is over
    started = False  #

    scoreLabel = games.Text(value="0", size=25, left=500, y=428, color=color.white)
    ducksShotLabel = games.Text(value="0", size=30, x=70, y=418, color=color.white)

    def __init__(self):
        super(Game, self).__init__(image=Game.image, x=0, y=0)

        # Label for total points
        games.screen.add(self.scoreLabel)
        games.screen.add(self.ducksShotLabel)

        # Instructions Labels
        self.instructions = games.Text(value="Shoot as many ducks as possible in 30 seconds!", size=35, x=320, y=100, color=color.white)
        self.instructions2 = games.Text(value="Press \"P\" to pause", size=35, x=320, y=140, color=color.white)
        self.instructions3 = games.Text(value="Press \"R\" to restart", size=35, x=320, y=180, color=color.white)

        games.screen.add(self.instructions)
        games.screen.add(self.instructions2)
        games.screen.add(self.instructions3)

        # Paused Game Sprite
        self.paused = games.Sprite(image=games.load_image("Sprites/paused.png"), x=320, y=240, dx=0, dy=0)

        # Final Results Labels
        self.results = games.Text(value="", size=35, x=320, y=100, color=color.white)  # How many ducks were hit
        self.results2 = games.Text(value="", size=35, x=320, y=140, color=color.white)  # Accuracy

        # Counters to delay events
        self.spawnCounter = 0
        self.menuCounter = 0

        self.keyDelay = 0
        self.keyDelayStart = False

        # Game state flag
        self.playing = False  # Set to true after instructions go away

        # Create the timer for the game
        self.gameTimer = Clock()
        games.screen.add(self.gameTimer)

        # Set initial game state
        Game.started = False  # True when game is started
        Game.paused = False  # True when game is paused
        Game.over = False  # True when game is over

        # Create the settings menu
        self.settingMenu = Menu()
        self.settingMenu.open()

        # Reset game scores
        GameScores.reset_score()
        Game.update_score_labels()

    def spawn(self):
        """ Spawn a duck """
        # Generate a random colored duck
        new_duck = Duck(randint(1, 3))

        # Increment total ducks spawned
        GameScores.totalDucks += 1

        # Add the duck to the screen
        games.screen.add(new_duck)

    def update(self):
        # Check if the game is over and display results
        if Game.over and GameScores.totalShots > 0:
            # Reset the menu counter and set playing to False
            self.menuCounter = 0
            self.playing = False
            Game.over = True

            # Show results
            self.results.value = "You hit " + str(GameScores.ducksHit) + " of " + str(GameScores.totalDucks) + " ducks!"
            self.results2.value = "Accuracy: " + str(
                int((int(GameScores.ducksHit) / GameScores.totalShots) * 100)) + "%"

            # Add the result texts to the game screen
            games.screen.add(self.results)
            games.screen.add(self.results2)

    @staticmethod
    def update_score_labels():
        """ Update the score labels """
        Game.scoreLabel.value = GameScores.score
        Game.ducksShotLabel.value = GameScores.ducksHit
        Game.scoreLabel.left = 500

    @staticmethod
    def update_score(points):
        """ Update The Game Score """
        # Update score and total ducks hit
        GameScores.score += points
        GameScores.ducksHit += 1

        # Update score labels
        Game.update_score_labels()

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