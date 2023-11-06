# Platformer Practice
# Python 3.9.6
# A program by Tyler Serio
# A program for testing out platformer game mechanics, menus, gameplay, etc.

# Import packages
import pygame
from pygame.locals import *
import random
import time

pygame.init() # Initializes pygame
pygame.mixer.init() # Initializes mixer module (for sounds)
vec = pygame.math.Vector2 # Variable, 2 for two dimensional

# Set constants
HEIGHT = 450 # Height of window
WIDTH = 400 # Width of window
ACC = 0.5 # Acceleration 
FRIC = -0.12 # Friction
FPS = 60 # Frames per second
FramePerSec = pygame.time.Clock() # Clock set up to later control frames per second

###
# Define sound lists up top here
###

# Create display surface
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT)) # Display surface
pygame.display.set_caption("Game") # Window caption

# Define the player class
class Player(pygame.sprite.Sprite):
    def __init__(self): # Self represents the object of the class itself
        super().__init__() # Super gives access to parent class methods/properties
        self.surf = pygame.Surface((30, 30)) # Defines a surface
        self.surf.fill((128, 255, 40)) # Fills surface with a color
        self.rect = self.surf.get_rect() # Defines starting position of object
        self.jumping = False
        self.score = 0
        self.jumpsound = pygame.mixer.Sound("cartoon-jump-6462.mp3")
        self.feather = False # Feather powerup related
        self.feathertime = 0 # Feather powerup related

        # Define the position, velocity, acceleration
        self.pos = vec((10, 400)) # Define starting position
        self.vel = vec(0, 0) # First number is x acceleration/velocity, second is y
        self.acc = vec(0, 0) # First number is x acceleration/velocity, second is y

    # Define the move function that takes into account acceleration, velocity, friction on the x-axis
    def move(self):
        if self.feather == True:
            self.acc = vec(0, 0.1)
            if self.feathertime < 0:
                self.feathertime = 0
                self.feather = False
        else:
            self.acc = vec(0, 0.5)

        pressed_keys = pygame.key.get_pressed() # Get which keys are pressed

        if pressed_keys[K_LEFT]: # If the left key is pressed
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]: # If the right key is pressed
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC # Acceleration is velocity and friction
        self.vel += self.acc # Adding velocity from acceleration
        self.pos += self.vel + 0.5 * self.acc # Moving position using velocity/acceleration

        if self.pos.x > WIDTH: # If position of player is outside screen on right
            self.pos.x = 0 # Move player to left side of screen
        if self.pos.x < 0: # If position of player is outside screen on left
            self.pos.x = WIDTH # Move player to right side of screen

        self.rect.midbottom = self.pos

    # Define the jump method
    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            if self.feather == True: # Feather powerup related
                self.vel.y = -8
                self.feathertime -= 1 # Feather powerup related
                if self.feathertime < 0:
                    self.feathertime = 0
                    self.feather = False
                    self.vel.y = -15
            else:
                self.vel.y = -15
            jumpsound = self.jumpsound
            pygame.mixer.Sound.play(jumpsound).set_volume(0.25)

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
            # Change how this works when Boost powerup is active

    # Define the update method that checks for collisions with platforms
    def update(self):
        hits = pygame.sprite.spritecollide(self, platforms, False) # Define a variable using the spritecollide function. Checks if sprite of first parameters has collided with sprite/sprites of second parameter. Final parameter is "do you want this (player) sprite deleted? Usually False
        if self.vel.y > 0: # This makes sure velocity is not zero unless there is already some initial velocity
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:
                        hits[0].point = False
                        self.score += 1
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False
            
# Define the platform class
class platform(pygame.sprite.Sprite):
    def __init__(self): # Self represents the object of the class itself
        super().__init__() # Super gives access to parent class methods/properties
        self.surf = pygame.Surface((random.randint(50, 100), 12)) # Defines a surface
        self.surf.fill((0, 255, 0)) # Fills surface with a color
        #self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 10)) # Defines starting position of object
        self.rect = self.surf.get_rect(center = (random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 30))) # Randomly assign width of platform
        self.speed = random.randint(-1, 1)
        
        self.moving = True
        self.point = True

    def move(self):
        hits = self.rect.colliderect(P1.rect)
        if self.moving == True:
            self.rect.move_ip(self.speed, 0)
            if hits:
                P1.pos += (self.speed, 0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH

    def generateItem(self):
        if (self.speed == 0):
            chance = random.randint(1, 5)
            if chance == 5:
                coins.add(Powerup((self.rect.centerx, self.rect.centery - 50)))
            else:
                coins.add(Coin((self.rect.centerx, self.rect.centery - 50)))

# Define the coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.surf = pygame.Surface((20, 20)) # Defines a surface
        self.surf.fill((128, 255, 40)) # Fills surface with a color
        self.rect = self.surf.get_rect() # Defines starting position of object
        self.rect.topleft = pos

    def update(self):
        if self.rect.colliderect(P1.rect):
            P1.score += 5
            self.kill()

# Define the powerup class
class Powerup(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.surf = pygame.Surface((20, 20)) # Defines a surface
        self.rect = self.surf.get_rect() # Defines starting position of object
        self.rect.topleft = pos

        types = ["boost", "feather"]
        self.var = types[random.randint(0, len(types) - 1)]
        print(self.var)
        if self.var == "boost":
            self.surf.fill((200, 200, 200)) # Fills surface with a color
            sounds = ["vine-boom-162668.mp3", "ohoh-yeh-91690.mp3", "heavy-cineamtic-hit-166888.mp3", "shouting-yeah-7043.mp3", "hq-explosion-6288.mp3", "man-scream-121085.mp3"]
            self.jumpsound = pygame.mixer.Sound(sounds[random.randint(0, len(sounds)-1)])
        if self.var == "feather":
            self.surf.fill((100, 150, 220)) # Fills surface with a color

    def update(self):
        if self.rect.colliderect(P1.rect):
            P1.score += 5
            self.kill()
            if self.var == "boost":
                P1.vel.y = -35
                P1.jumping = True
                pygame.mixer.Sound.play(self.jumpsound)
            if self.var == "feather":
                P1.feather = True
                P1.feathertime = 5

# Define button class
class button(pygame.sprite.Sprite):
    def __init__(self, msg, x, y, posx, posy, action): # Self represents the object of the class itself
        super().__init__() # Super gives access to parent class methods/properties
        self.msg = msg
        self.surf = pygame.Surface((x, y)) # Defines a surface
        self.surf.fill((12, 12, 255)) # Fills surface with a color
        self.rect = self.surf.get_rect(center = (x/2, y/2))
        self.rect.topleft = (posx, posy)
        self.font = pygame.font.SysFont("Verdana", 20)
        self.action = action
        g = self.font.render(str(self.msg), True, (100, 100, 100))
        displaysurface.blit(self.surf, self.rect)
        displaysurface.blit(g, (posx + (x/4), posy + (y/4)))

# Define the function to check if a platform collides with a platform
def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform, groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 15) and (abs(platform.rect.bottom - entity.rect.top) < 15):
                return True
        C = False
        return C
                
# Define function to generate platforms
def plat_gen():
    while len(platforms) < 7:
        width = random.randrange(50, 100)
        p = platform()
        C = True
        while C:
            p = platform()
            p.rect.center = (random.randrange(0, WIDTH - width), random.randrange(-15, 0))
            C = check(p, platforms)
        p.generateItem()
        platforms.add(p)
        all_sprites.add(p)

# Define the game over menu
def game_over_menu():
    sounds = ["oh-gah-82730.mp3", "no-and-grunts-82716.mp3", "homemadeoof-47509.mp3", "aww-8277.mp3", "angel-ahhh-102549.mp3", "dishes-fall-and-crash-117075.mp3", "falling-143024.mp3", "falling-down-stairs-88067.mp3", "falling-down-stairs-v1-mixed-36001.mp3", "girl-oh-no-150550.mp3", "no-luck-too-bad-disappointing-sound-effect-112943.mp3", "splash-4-46870.mp3", "splash-6213.mp3", "whygod-36270.mp3", "falling-143024.mp3", "thud-82914.mp3", "monkey-128368.mp3", "thump-105302.mp3", "dishes-fall-and-crash-117075.mp3", "punch-6-166699.mp3"]
    gameoversound = pygame.mixer.Sound(sounds[random.randint(0, len(sounds)-1)])
    pygame.mixer.Sound.play(gameoversound)
    continuebttn = button("Continue", 200, 50, 100, 100, "continue")
    mainmenubttn = button("Main Menu", 200, 50, 100, 200, "mainmenu")
    quitbttn = button("Quit", 200, 50, 100, 300, "quit")
    bttns = pygame.sprite.Group()
    bttns.add(continuebttn)
    bttns.add(mainmenubttn)
    bttns.add(quitbttn)
    death = 1
    while death == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for x in bttns:
                    if x.rect.collidepoint(event.pos):
                        if x.action == "quit":
                            pygame.mixer.quit()
                            pygame.quit()
                            exit()
                        if x.action == "continue":
                            print("continue")
                            death = 0
                        if x.action == "mainmenu":
                            print("mainmenu")
                            global part
                            part = 1
                            death = 0
        bttns.update()
        pygame.display.update()
        FramePerSec.tick(FPS)
    for x in bttns:
        x.kill()
    displaysurface.fill((0, 0, 0))
    pygame.display.update()

# Define the main menu
def main_menu():
    music = pygame.mixer.Sound("cottagecore-17463.mp3")
    musicchannel = pygame.mixer.Channel(0)
    musicchannel.play(music, loops = -1)
    newbttn = button("New Game", 200, 50, 100, 50, "newgame")
    continuebttn = button("Continue", 200, 50, 100, 150, "continue")
    optionsbttn = button("Options", 200, 50, 100, 250, "options")
    quitbttn = button("Quit", 200, 50, 100, 350, "quit")
    bttns = pygame.sprite.Group()
    bttns.add(newbttn)
    bttns.add(continuebttn)
    bttns.add(optionsbttn)
    bttns.add(quitbttn)
    mainmenu = 1
    while mainmenu == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for x in bttns:
                    if x.rect.collidepoint(event.pos):
                        if x.action == "quit":
                            print("quit")
                            pygame.mixer.quit()
                            pygame.quit()
                            exit()
                        if x.action == "newgame":
                            print("newgame")
                            global part
                            part = 2
                            mainmenu = 0
                        if x.action == "continue":
                            print("continue")
                        if x.action == "options":
                            print("options")
        bttns.update()
        pygame.display.update()
        FramePerSec.tick(FPS)
    for x in bttns:
        x.kill()
    displaysurface.fill((0, 0, 0))
    start_new()
    generate()
    pygame.display.update()
    musicchannel.stop()

def options_menu():
    soundbttn = button("Sound", 200, 50, 100, 100, "sound")
    while optionsmenu == 1:
        bttns.update()
        pygame.display.update()
        FramePerSec.tick(FPS)
    for x in bttns:
        x.kill()
    displaysurface.fill(0, 0, 0)
    pygame.display.update()

def game_menu():
    continuebttn = button("Continue", 200, 50, 100, 100, "continue")
    optionsbttn = button("Options", 200, 50, 100, 200, "options")
    quitbttn = button("Quit", 200, 50, 100, 300, "quit")
    bttns = pygame.sprite.Group()
    bttns.add(continuebttn)
    bttns.add(optionsbttn)
    bttns.add(quitbttn)
    gamemenu = 1
    while gamemenu == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gamemenu = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                for x in bttns:
                    if x.rect.collidepoint(event.pos):
                        if x.action == "quit":
                            print("quit")
                            pygame.mixer.quit()
                            pygame.quit()
                            exit()
                        if x.action == "options":
                            print("options")
                        if x.action == "continue":
                            print("continue")
                            gamemenu = 0
        
        bttns.update()
        pygame.display.update()
        FramePerSec.tick(FPS)
    for x in bttns:
        x.kill()
    displaysurface.fill((0, 0, 0))
    pygame.display.update()  

global platforms, coins, all_sprites
platforms = pygame.sprite.Group()
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

global P1, PT1, PPRime
PT1 = platform() # Create a platform object
P1 = Player() # Create a player object
PPrime = platform()
PPrime.surf = pygame.Surface((75, 12))
PPrime.surf.fill((255, 0, 0))
PPrime.rect = PPrime.surf.get_rect(center = (75, 300))
PPrime.moving = False
PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255, 0, 0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
PT1.moving = False
PT1.point = False
all_sprites.add(PT1) # Add platform to sprite group
all_sprites.add(P1) # Add the player to the sprite group
platforms.add(PT1) # Add platform to group
all_sprites.add(PPrime)
platforms.add(PPrime)

def start_new():
    global platforms, coins, all_sprites
    platforms = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    print(len(all_sprites))

    global P1, PT1, PPrime
    PT1 = platform() # Create a platform object
    PPrime = platform()
    P1 = Player() # Create a player object
    PT1.surf = pygame.Surface((WIDTH, 20))
    PT1.surf.fill((255, 0, 0))
    PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
    PT1.moving = False
    PPrime.surf = pygame.Surface((75, 12))
    PPrime.surf.fill((255, 0, 0))
    PPrime.rect = PPrime.surf.get_rect(center = (75, 300))
    PPrime.moving = False
    PT1.point = False
    all_sprites.add(PT1) # Add platform to sprite group
    all_sprites.add(P1) # Add the player to the sprite group
    platforms.add(PT1) # Add platform to group
    all_sprites.add(PPrime)
    platforms.add(PPrime)

# Add randomized level generation
# This loop runs randomly between 4 and 8 times
# It generates platforms and adds them to the sprites/platforms group
def generate():
    for x in range(random.randint(4, 8)):
        C = True
        pl = platform()
        while C:
            pl = platform()
            C = check(pl, platforms)
        pl.generateItem()
        platforms.add(pl)
        all_sprites.add(pl)

# Game Loop
def game_loop():
    global part
    part = 1
    while True:
        if part == 1:
            main_menu()

        while part == 2:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.mixer.quit()
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_menu()
                    if event.key == pygame.K_SPACE:
                        P1.jump()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        P1.cancel_jump()

            # Start a game over screen if the player falls below the screen
            if P1.rect.top > HEIGHT:
                print(P1.rect.top)
                time.sleep(1)
                #    entity.kill()
                    #time.sleep(1)
                for entity in coins:
                    entity.kill()
                for entity in platforms:
                    entity.kill()
                displaysurface.fill((255, 0, 0))
                pygame.display.update()
                game_over_menu()
                if part == 1:
                    break
                else:
                    start_new()
                    generate()
                    PT11 = platform() # Create a platform object
                    PT11.surf = pygame.Surface((WIDTH, 20))
                    PT11.surf.fill((255, 0, 0))
                    PT11.rect = PT11.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))

                    PT11.moving = False
                    PT11.point = False
                    all_sprites.add(PT11)
                    platforms.add(PT11)
                    P1.pos = vec((10, 400))
                    P1.vel = vec(0, 0) # First number is x acceleration/velocity, second is y
                    P1.acc = vec(0, 0)

            if P1.rect.top <= HEIGHT / 3: # Moves screen up when player is a third of the way up
                P1.pos.y += abs(P1.vel.y) 
                for plat in platforms: # Update the position of all platforms
                    plat.rect.y += abs(P1.vel.y)# Add Player's velocity for all platforms
                    if plat.rect.top >= HEIGHT:
                        plat.kill() # Destroy platforms below the screen
                for coin in coins:
                    coin.rect.y += abs(P1.vel.y)
                    if coin.rect.top >= HEIGHT:
                        coin.kill()

            plat_gen() # Generate platforms when there are fewer on the screen

            displaysurface.fill((0, 0, 0)) # Fill the screen with the color black

            f = pygame.font.SysFont("Verdana", 20) # Font for the score at the top of the screen
            g = f.render(str(P1.score), True, (123, 255, 0)) # Render score at top of screen
            displaysurface.blit(g, (WIDTH/2, 10)) # Blit score to display surface
            if P1.feathertime > 0:
                fg = f.render(str(P1.feathertime), True, (123, 255, 0)) # Render feather uses at top of screen
                displaysurface.blit(fg, (WIDTH/2 + 50, 10)) # Blit score to display surface

            
            P1.move() # Call player movement method every loop
            P1.update() # Call player update method every loop
            
            for entity in platforms: # For every platform in the group of platforms
                 entity.move() # Move the platform

            for coin in coins:
                displaysurface.blit(coin.surf, coin.rect)
                coin.update()
                 
            for entity in all_sprites: # For all sprites
                displaysurface.blit(entity.surf, entity.rect) # Blit to surface
               

            pygame.display.update() # Push all changes to screen and update it
            FramePerSec.tick(FPS) # Tick function used on clock object limits refresh to 60 FPS
game_loop()
