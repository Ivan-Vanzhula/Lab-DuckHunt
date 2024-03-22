from superwires import games, color
import pygame.display
import pygame.mouse
from random import randint

# Setup game window
foreground = None

games.init(screen_width=640, screen_height=480, fps=60)
pygame.display.set_caption('Duck Hunt')


# Exception class for restarting the game
class RestartException(Exception):
    def __init__(self):
        super().__init__('')  # Initialize the exception with an empty message


# CLASS ====================================
# Name.........: Menu
# Description..: Create menu/contain settings
# Syntax.......: Menu()
# ==========================================
class Menu(games.Sprite):
    duckSpeed = 1  # Default speed of ducks

    def __init__(self):
        # Load menu images
        mainMenu = games.load_image('Sprites/Main_menu.png', transparent=False)
        settingMenu = games.load_image('Sprites/Settings_menu.png',
                                       transparent=False)

        # Combine menu images into one surface
        self.joinedMenu = pygame.Surface((1280, 480))
        self.joinedMenu.blit(mainMenu, (0, 0))
        self.joinedMenu.blit(settingMenu, (640, 0))

        # Initialize the sprite with the combined menu image
        super(Menu, self).__init__(image=self.joinedMenu, x=640, y=240)

        # Initialize menu state variables
        self.activeMenu = 0  # 0 for main menu, 1 for settings menu

        self.moveDirection = -1  # Direction to move when changing menu
        self.moveCounter = 0  # Counter for smooth menu transitions

        # Create pointer sprite
        self.pointerImage = pygame.Surface((30, 30)).convert_alpha()
        self.pointerImage.fill((255, 255, 255, 0))
        pygame.draw.circle(self.pointerImage, (0, 0, 0), (15, 15), 14)
        self.pointer = games.Sprite(image=self.pointerImage,
                                    x=490 + 640, y=239)

        # Create crosshair sprite for settings menu
        self.crosshair = Cursor()

        # Add crosshair to the screen
        games.screen.add(self.crosshair)

    def tick(self):
        # Handle menu interactions
        if Cursor.clicked and not self.moveCounter:
            # Main menu interactions
            if self.activeMenu == 0:
                if 389 > Cursor.xPos > 251 and 162 > Cursor.yPos > 116:
                    Game.started = True  # Start the game
                    self.close()  # Close the menu
                elif 389 > Cursor.xPos > 251 and 262 > Cursor.yPos > 216:
                    self.activeMenu = 1  # Switch to settings menu

                    self.moveCounter = 20  # Start menu transition
                    self.moveDirection = -1
            # Settings menu interactions
            elif self.activeMenu == 1:
                if 386 > Cursor.xPos > 253 and 340 > Cursor.yPos > 296:
                    self.activeMenu = 0  # Switch back to main menu

                    self.moveCounter = 20  # Start menu transition
                    self.moveDirection = 1
                elif 128 > Cursor.yPos > 88:
                    # Handle crosshair selection
                    if 110 > Cursor.xPos > 70:
                        self.crosshair.set_image(Cursor.images[0])
                    elif 206 > Cursor.xPos > 166:
                        self.crosshair.set_image(Cursor.images[1])
                    elif 303 > Cursor.xPos > 263:
                        self.crosshair.set_image(Cursor.images[2])
                    elif 400 > Cursor.xPos > 360:
                        self.crosshair.set_image(Cursor.images[3])
                elif 254 > Cursor.yPos > 224:
                    # Handle duck speed selection
                    if 430 > Cursor.xPos > 400:
                        Menu.duckSpeed = 0.5
                        self.pointer.x = 415
                    elif 505 > Cursor.xPos > 475:
                        Menu.duckSpeed = 1
                        self.pointer.x = 490
                    elif 580 > Cursor.xPos > 550:
                        Menu.duckSpeed = 1.5
                        self.pointer.x = 565

        # Update menu position during menu transitions
        if self.moveCounter:
            self.x += 32 * self.moveDirection
            self.pointer.x += 32 * self.moveDirection
            self.moveCounter -= 1

    def open(self):
        # Add menu and pointer to the screen
        games.screen.add(self)
        games.screen.add(self.pointer)

    def close(self):
        # Start the game and remove menu and pointer from the screen
        Game.started = True
        games.screen.remove(self)
        games.screen.remove(self.pointer)


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
# Name.........: Duck
# Description..: Class for a duck
# Syntax.......: Duck()
# ==========================================
class Duck(games.Sprite):
    """ Duck Class """

    def __init__(self, duck_type):
        # Colors Available
        colors = [3, 'black', 'blue', 'red']
        duck_color = colors[duck_type]

        # Sprites for the Duck
        self.flyRight = [3, games.load_image('Sprites/' + duck_color + '/duck1.png'),
                         games.load_image('Sprites/' + duck_color + '/duck2.png'),
                         games.load_image('Sprites/' + duck_color + '/duck3.png')]

        self.flyStraightRight = [3, games.load_image('Sprites/' + duck_color + '/duck4.png'),
                                 games.load_image('Sprites/' + duck_color + '/duck5.png'),
                                 games.load_image('Sprites/' + duck_color + '/duck6.png')]

        self.flyLeft = [3, games.load_image('Sprites/' + duck_color + '/duck7.png'),
                        games.load_image('Sprites/' + duck_color + '/duck8.png'),
                        games.load_image('Sprites/' + duck_color + '/duck9.png')]

        self.flyStraightLeft = [3, games.load_image('Sprites/' + duck_color + '/duck10.png'),
                                games.load_image('Sprites/' + duck_color + '/duck11.png'),
                                games.load_image('Sprites/' + duck_color + '/duck12.png')]

        self.die = [3, games.load_image('Sprites/' + duck_color + '/duckDie1.png'),
                    games.load_image('Sprites/' + duck_color + '/duckDie2.png'),
                    games.load_image('Sprites/' + duck_color + '/duckDie3.png')]

        # Initialize Duck Sprite At Random X-Location
        super(Duck, self).__init__(image=self.flyRight[1], x=randint(10, 470),
                                   y=350, dx=0, dy=-1 * Menu.duckSpeed)

        # Point Values Based On Duck Color
        point_values = {'blue': 25, 'red': 50, 'black': 75}

        # Direction Constants
        self.RIGHT = 1
        self.LEFT = 2

        # Duck Variables
        self.alive = True
        self.direction = randint(1, 2)
        self.straight = False  # True if duck is flying straight
        self.points = point_values[duck_color]

        # Animation Frames
        self.frames = [4,
                       self.flyRight[2],
                       self.flyRight[3],
                       self.flyRight[2],
                       self.flyRight[1]]

        # Points above the duck's head when it's shot
        self.deathScore = games.Text(value=str(self.points), size=25,
                                     x=self.x, y=self.top - 5,
                                     color=color.white)

        # Animation Variables
        self.dieDelay = 0  # Delay Duck Falling
        self.continueDeath = False
        self.animationCount = 0
        self.frame = 1  # What frame of the animation?
        self.directionCount = 0

        # Set velocity based on direction
        if self.direction == self.RIGHT:
            self.dx = .5 * Menu.duckSpeed

        else:
            self.dx = -.5 * Menu.duckSpeed

    def change_direction(self):
        """ Decide to change duck's direction """
        random_number = randint(1, 340)

        if random_number % 5 == 0:
            # Switch the duck's direction
            if self.direction == self.RIGHT:
                self.direction = self.LEFT
                self.dx = -.5 * Menu.duckSpeed

            else:
                self.direction = self.RIGHT
                self.dx = .5 * Menu.duckSpeed

        # Decide if it will fly straight or not
        random_number = randint(1, 340)

        if random_number % 5 == 0:
            # Change duck to straight or up
            self.straight = not self.straight

    def update(self):
        if not Game.paused and not Game.over:
            # Check if the duck is alive
            if self.alive:
                # Duck is alive
                if self.bottom < 0 or self.right < 0 or self.left > 640:
                    # Duck is off the screen, destroy
                    self.destroy()

                # Check if the duck should try and change directions
                if self.directionCount < 100:
                    self.directionCount += 1

                else:
                    self.change_direction()
                    self.directionCount = 0

                # Check if the duck is going straight and change velocity
                if self.straight:
                    self.dy = 0

                    if self.direction == self.RIGHT:
                        self.dx = 1 * Menu.duckSpeed

                    else:
                        self.dx = -1 * Menu.duckSpeed

                else:
                    # Duck is flying upwards
                    self.dy = -1 * Menu.duckSpeed

                # Update the animation frames based on duck's velocity
                if not self.alive:
                    self.frames = [2, self.die[2], self.die[3]]

                elif self.direction == self.RIGHT:
                    if self.straight:
                        self.frames = [
                            4, self.flyStraightRight[2],
                            self.flyStraightRight[3],
                            self.flyStraightRight[2],
                            self.flyStraightRight[1]]

                    else:
                        self.frames = [
                            4, self.flyRight[2], self.flyRight[3],
                            self.flyRight[2], self.flyRight[1]]

                elif self.direction == self.LEFT:
                    if self.straight:
                        self.frames = [
                            4, self.flyStraightLeft[2],
                            self.flyStraightLeft[3], self.flyStraightLeft[2],
                            self.flyStraightLeft[1]]

                    else:
                        self.frames = [
                            4, self.flyLeft[2], self.flyLeft[3],
                            self.flyLeft[2], self.flyLeft[1]]

                if self.frame > self.frames[0]:
                    self.frame = 1

                # Check for mouse clicks
                if Cursor.isShotAllowed:
                    # Prevent the shooting of a duck that's behind the tree
                    if not (Cursor.xPos in range(150, 240) and Cursor.yPos in range(220, 390)):
                        # Check if the mouse was over the duck
                        if Cursor.xPos in range(self.left, self.right) and Cursor.yPos in range(self.top, self.bottom):
                            # Duck was shot - Kill it
                            self.shot()

            else:
                # Duck is Dead, Destroy once it hits the ground
                if self.bottom > 370:
                    self.destroy()

    def tick(self):
        """ Tick Method """
        # Tick only if game is not paused
        if not Game.paused:
            if not self.alive:
                # This will display the point value above the head
                # and when it's done the duck will start to fall
                if self.dieDelay > 50 and not self.continueDeath:
                    self.dy = 1

                    self.continueDeath = True
                    self.frame = 1
                    games.screen.remove(self.deathScore)

                elif not self.continueDeath:
                    self.dieDelay += 1

            # This elif will help birds continue to fly
            # At the correct angle and direction after resuming from a pause
            elif (self.dx == 0) and (self.dy < 0):
                if not self.straight:
                    if self.direction == self.RIGHT:
                        self.dx = .5

                    else:
                        self.dx = -.5

            # Update the Duck's animation
            self.update_animation()

        elif Game.paused:
            # Game is Paused - Freeze the duck
            self.dx = 0
            self.dy = 0

    def shot(self):
        """ Kill the duck """
        Game.update_score(self.points)

        self.alive = False  # Set the duck to dead

        self.set_image(self.die[1])  # Replace with starting death animation

        self.frame = 1
        self.animationCount = 0

        # Freeze the duck
        self.dx = 0
        self.dy = 0

        # Display score above ducks head
        self.deathScore.x = self.x
        self.deathScore.y = self.top - 10

        games.screen.add(self.deathScore)

    def update_animation(self):
        self.animationCount += 1

        # Change animation for falling dead duck
        if not self.alive:
            if self.animationCount >= 17:
                if self.continueDeath:
                    self.dy = 2

                    # Advance the Death Animation
                    frames = [2, self.die[3], self.die[2]]

                    self.set_image(frames[self.frame])

                    self.frame += 1

                    # Make Sure the frame stays within the correct range
                    if self.frame > frames[0]:
                        self.frame = 1
                self.animationCount = 0

        # Change animation for duck that's not dead
        else:
            if self.animationCount >= 17 / Menu.duckSpeed:
                if self.frame > self.frames[0]:
                    self.frame = 1

                self.set_image(self.frames[self.frame])

                self.frame += 1

                if self.frame > self.frames[0]:
                    self.frame = 1

                # Reset the animation counter
                self.animationCount = 0


# CLASS ====================================
# Name.........: Game
# Description..: Will spawn ducks/check for pause
# Syntax.......: Game()
# ==========================================
class Game(games.Sprite):
    """ Duck Spawner Class """
    image = games.load_image('Sprites/spawner.png')

    # State of Game
    paused = False  # True when game is paused
    over = False  # True when game is over
    started = False  #

    scoreLabel = games.Text(
        value='0', size=25, left=500, y=428, color=color.white)
    ducksShotLabel = games.Text(
        value='0', size=30, x=70, y=418, color=color.white)

    def __init__(self):
        super(Game, self).__init__(image=Game.image, x=0, y=0)

        # Label for total points
        games.screen.add(self.scoreLabel)
        games.screen.add(self.ducksShotLabel)

        # Instructions Labels
        self.instructions = games.Text(
            value='Shoot as many ducks as possible in 30 seconds!',
            size=35, x=320, y=100, color=color.white)

        self.instructions2 = games.Text(value='Press "P" to pause', size=35,
                                        x=320, y=140, color=color.white)
        self.instructions3 = games.Text(value='Press "R" to restart',
                                        size=35, x=320, y=180,
                                        color=color.white)

        games.screen.add(self.instructions)
        games.screen.add(self.instructions2)
        games.screen.add(self.instructions3)

        # Paused Game Sprite
        self.paused = games.Sprite(image=games.load_image(
            'Sprites/paused.png'),
            x=320, y=240, dx=0, dy=0)

        # Final Results Labels
        # How many ducks were hit
        self.results = games.Text(value='', size=35,
                                  x=320, y=100, color=color.white)
        # Accuracy
        self.results2 = games.Text(value='', size=35,
                                   x=320, y=140, color=color.white)

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
            self.results.value = 'You hit ' + str(GameScores.ducksHit) + ' of ' + str(GameScores.totalDucks) + ' ducks!'
            self.results2.value = 'Accuracy: ' + str(
                int((int(GameScores.ducksHit)
                    / GameScores.totalShots) * 100)) + '%'

            # Add the result texts to the game screen
            games.screen.add(self.results)
            games.screen.add(self.results2)

    def restart(self):
        # Raise an exception to restart the game
        raise RestartException

    def tick(self):
        if self.started:
            if self.started and self.playing and not Game.paused and not Game.over:
                # Keep counting until the duck spawner should spawn a new duck
                self.spawnCounter += 1

                if self.spawnCounter >= 75:
                    self.spawn()
                    self.spawnCounter = 0

            elif not Game.paused and not Game.over and self.started:
                # Keep counting until the menu should disappear
                if self.menuCounter >= 250:
                    # Remove instructions
                    games.screen.remove(self.instructions)
                    games.screen.remove(self.instructions2)
                    games.screen.remove(self.instructions3)
                    self.menuCounter = 0
                    self.playing = True
                    self.gameTimer.start_clock()

                else:
                    self.menuCounter += 1

                # Keep the final results until they should disappear
                if self.menuCounter >= 500:
                    # Destroy the game instance and exit
                    self.destroy()
                    exit()

                else:
                    self.menuCounter += 1

            # Check for the pause button to be pressed
            if games.keyboard.is_pressed(games.K_p) and not Game.over:
                if self.keyDelay == 0:
                    # Pause or unpause the game
                    Game.paused = not Game.paused
                    self.keyDelayStart = True

                    # Display the pause sprite if on pause, remove if not
                    if Game.paused:
                        games.screen.add(self.paused)
                        games.screen.add(self.instructions)

                    else:
                        # Keep mouse at position
                        # it was in when it paused to avoid cheating
                        pygame.mouse.set_pos(Cursor.xPos, Cursor.yPos)

                        # Remove pause label and instructions
                        games.screen.remove(self.paused)
                        games.screen.remove(self.instructions)

            # Check if the 'R' key is pressed
            # and it wasn't pressed in the previous tick
            if games.keyboard.is_pressed(games.K_r):
                self.restart()  # Restart the game
                return

            # Exit game if Escape button was pressed
            if games.keyboard.is_pressed(games.K_ESCAPE):
                exit()

        # Advance the keyboard delay
        if self.keyDelayStart:
            if self.keyDelay > 10:
                self.keyDelay = 0
                self.keyDelayStart = False

            else:
                self.keyDelay += 1

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

    images = [games.load_image(f'Sprites/Cursors/Cursor_{i}.png')
              for i in range(1, 5)]

    def __init__(self):
        """ Cursor Initializer """

        super(Cursor, self).__init__(
            image=self.images[0], x=games.mouse.x, y=games.mouse.y)

        self.mouseClicked = False
        self.mouseCounter = 0

        # Load gunshot sound
        self.gunShotSound = games.load_sound('Sounds/shot.wav')

    def update(self):
        # Keep the sprite at the same x and y location as the mouse
        self.x = Cursor.xPos
        self.y = Cursor.yPos

        # Remove and read to put on top of any birds
        games.screen.remove(self)
        games.screen.add(self)

    def tick(self):
        """ Check For Mouse Click """
        if not Game.paused and not Game.over:
            # Check if the mouse was clicked
            if games.mouse.is_pressed(0) and not Cursor.clicked:
                Cursor.clicked = True
                Cursor.isShotAllowed = True
                self.gunShotSound.play()

                if Game.started:
                    GameScores.totalShots += 1

            # Avoid repeated mouse clicks
            if Cursor.clicked:
                if not games.mouse.is_pressed(0):
                    Cursor.clicked = False
                    Cursor.isShotAllowed = False
                    self.mouseCounter = 0
                else:
                    if self.mouseCounter == 1:
                        self.mouseCounter = 0
                        Cursor.isShotAllowed = False
                    else:
                        self.mouseCounter = 1

            # Update cursor position
            Cursor.xPos = games.mouse.x
            Cursor.yPos = games.mouse.y

            # Bring the tree and grass in front of all the ducks
            if Game.started:
                games.screen.remove(foreground)
                games.screen.add(foreground)
            self.update()


# CLASS ====================================
# Name.........: Clock
# Description..: Displays the clock object on the screen
# Syntax.......: Clock()
# ==========================================
class Clock(games.Sprite):
    """ Class for displaying the Clock """
    def __init__(self):
        super(Clock, self).__init__(image=Game.image, x=0, y=0)

        # Timer Display
        self.timer = games.Text(
            value='0:30', size=50, x=300, y=435, color=color.white)
        games.screen.add(self.timer)

        self.clockCount = 0
        self.seconds = 30

        # Sound For Last 10 Seconds
        self.sound = games.load_sound('Sounds/beep.wav')

        self.started = False

    # Start the clock
    def start_clock(self):
        self.started = True

    def update(self):
        # Check if clock has run out of time
        if self.seconds <= 0:
            self.started = False
            Game.over = True
            games.mouse.is_visible = True  # Show mouse

        # Change the clock's color to red when it gets down to the last minute
        if self.seconds <= 10:
            self.timer.color = color.red

        # Keep the clock in the same position
        self.timer.left = 280

    # Update the Clock's Label
    def update_clock(self):
        label = '0:'

        if self.seconds < 10:
            label += '0' + str(self.seconds)

        else:
            label += str(self.seconds)

        # Play sound on final 10 seconds
        if self.seconds < 11:
            self.sound.play()

        # Update The Clock's Label
        self.timer.value = label

    # Perform the Clock countdown
    def tick(self):
        # Only Do Countdown if not paused and playing the game
        if self.started and not Game.paused:
            if self.clockCount >= 100:
                self.seconds -= 1

                # Show the new time on the clock
                self.update_clock()

                self.clockCount = 1

            else:
                self.clockCount += 1


# FUNCTION ==================================
# Name.........: Main
# Description..: Will start the game
# Syntax.......: main()
# ==========================================
def main():
    global foreground  # Declare 'foreground' as a global variable

    while True:
        foreground = games.Sprite(
            image=games.load_image('Sprites/foreground.png'),
            left=1, bottom=390)

        games.screen.background = games.load_image(
            'Sprites/background.png', transparent=False)

        # Add the foreground sprite to the screen
        games.screen.add(foreground)
        # Hide the mouse cursor
        games.mouse.is_visible = False

        # Create the game instance
        game = Game()

        # Add the game instance to the screen
        games.screen.add(game)

        try:
            # Run the game loop
            games.screen.mainloop()
        except RestartException:
            # Handle game restart exception

            # Get all objects currently on the screen
            all_objects = games.screen.get_all_objects()

            # Remove all objects from the screen
            while len(all_objects) > 0:
                games.screen.remove(all_objects[0])

            # Delete game timer and game instance to restart game
            del game.gameTimer
            del game.settingMenu
            del game


if __name__ == '__main__':
    # Start!
    main()
