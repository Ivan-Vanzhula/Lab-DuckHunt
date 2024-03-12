from superwires import games, color
import pygame.display, pygame.mouse
from random import randint

# Setup game window
foreground = None

games.init(screen_width=640, screen_height=480, fps=60)
pygame.display.set_caption("Duck Hunt")


# CLASS ====================================
# Name.........: Menu
# Description..: Create menu/contain settings
# Syntax.......: Menu()
# ==========================================
class Menu(games.Sprite):
    duckSpeed = 1  # Default speed of ducks

    def __init__(self):
        # Load menu images
        mainMenu = games.load_image("Sprites/Main_menu.png", transparent=False)
        settingMenu = games.load_image("Sprites/Settings_menu.png", transparent=False)

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
        self.pointer = games.Sprite(image=self.pointerImage, x=490 + 640, y=239)

        # Create crosshair sprite for settings menu
        self.crosshair = Cursor()

        # Add crosshair to the screen
        games.screen.add(self.crosshair)

    def tick(self):
        # Handle menu interactions
        if Cursor.clicked and not self.moveCounter:
            match self.activeMenu:
                # Main menu interactions
                case 0:
                    if 389 > Cursor.xPos > 251 and 162 > Cursor.yPos > 116:
                        Game.started = True  # Start the game
                        self.close()  # Close the menu
                    elif 389 > Cursor.xPos > 251 and 262 > Cursor.yPos > 216:
                        self.activeMenu = 1  # Switch to settings menu

                        self.moveCounter = 20  # Start menu transition
                        self.moveDirection = -1
                # Settings menu interactions
                case 1:
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
        self.timer = games.Text(value="0:30", size=50, x=300, y=435, color=color.white)
        games.screen.add(self.timer)

        self.clockCount = 0
        self.seconds = 30

        # Sound For Last 10 Seconds
        self.sound = games.load_sound("Sounds/beep.wav")

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
