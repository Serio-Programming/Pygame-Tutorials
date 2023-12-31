# Platformer Tutorial
# From: https://coderslegacy.com/python/pygame-platformer-game-development/
# Python 3.9.6
# A program by Tyler Serio
# This program is a simple platformer video game made from following the above tutorial

# Import packages
import pygame
from pygame.locals import *
import random
import time

pygame.init() # Initializes pygame
vec = pygame.math.Vector2 # Variable, 2 for two dimensional

# Set constants
HEIGHT = 450 # Height of window
WIDTH = 400 # Width of window
ACC = 0.5 # Acceleration 
FRIC = -0.12 # Friction
FPS = 60 # Frames per second

FramePerSec = pygame.time.Clock() # Clock set up to later control frames per second

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

        # Define the position, velocity, acceleration
        self.pos = vec((10, 400)) # Define starting position
        self.vel = vec(0, 0) # First number is x acceleration/velocity, second is y
        self.acc = vec(0, 0) # First number is x acceleration/velocity, second is y

    # Define the move function that takes into account acceleration, velocity, friction on the x-axis
    def move(self):
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
            self.vel.y = -15

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

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

    def generateCoin(self):
        if (self.speed == 0):
            coins.add(Coin((self.rect.centerx, self.rect.centery - 50)))

# Define the coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        #self.surf = pygame.Surface((40, 40)) # Defines a surface
        #self.surf.fill((70, 90, 255)) # Fills surface with a color
        #self.rect.topleft = pos
        #self.rect = self.surf.get_rect()
        self.surf = pygame.Surface((20, 20)) # Defines a surface
        self.surf.fill((128, 255, 40)) # Fills surface with a color
        self.rect = self.surf.get_rect() # Defines starting position of object
        self.rect.topleft = pos

    def update(self):
        if self.rect.colliderect(P1.rect):
            P1.score += 5
            self.kill()

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
            p.rect.center = (random.randrange(0, WIDTH - width), random.randrange(-5, 0))
            C = check(p, platforms)
        p.generateCoin()
        platforms.add(p)
        all_sprites.add(p)

# Generate first platform and player
PT1 = platform() # Create a platform object
P1 = Player() # Create a player object

### Generate a platform that will always be close to the player in the beginning
##p = platform()
##p.rect.center = (random.randrange(0, WIDTH - 300), 350)

PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255, 0, 0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))

PT1.moving = False
PT1.point = False

## Sprites Groups and Game Loop ##
# Define the sprite group and add to it
all_sprites = pygame.sprite.Group() # Define a sprite group
all_sprites.add(PT1) # Add platform to sprite group
all_sprites.add(P1) # Add the player to the sprite group
platforms = pygame.sprite.Group() # Create platform group
platforms.add(PT1) # Add platform to group
coins = pygame.sprite.Group()
#platforms.add(p)
#all_sprites.add(p)

# Add randomized level generation
# This loop runs randomly between 4 and 8 times
# It generates platforms and adds them to the sprites/platforms group
for x in range(random.randint(4, 8)):
    C = True
    pl = platform()
    while C:
        pl = platform()
        C = check(pl, platforms)
    pl.generateCoin()
    platforms.add(pl)
    all_sprites.add(pl)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()

    # Start a game over screen if the player falls below the screen
    if P1.rect.top > HEIGHT:
        for entity in all_sprites:
            entity.kill()
            time.sleep(1)
            displaysurface.fill((255, 0, 0))
            pygame.display.update()
            time.sleep(1)
            pygame.quit()
            exit()

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
