# Platformer Tutorial
# From: https://coderslegacy.com/python/pygame-platformer-game-development/
# Python 3.9.6
# A program by Tyler Serio
# This program is a simple platformer video game made from following the above tutorial

##### Setting the Foundation #####
## Initalization and Constants ##
# Import packages
import pygame
from pygame.locals import *
import random

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

## Player and Platform Classes ##
# Define the player class
class Player(pygame.sprite.Sprite):
    def __init__(self): # Self represents the object of the class itself
        super().__init__() # Super gives access to parent class methods/properties
        self.surf = pygame.Surface((30, 30)) # Defines a surface
        self.surf.fill((128, 255, 40)) # Fills surface with a color
        self.rect = self.surf.get_rect() # Defines starting position of object
        self.jumping = False

        # Define the position, velocity, acceleration
        self.pos = vec((10, 385)) # Define starting position
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
        hits = pygame.sprite.spritecollide(P1, platforms, False) # Define a variable using the spritecollide function. Checks if sprite of first parameters has collided with sprite/sprites of second parameter. Final parameter is "do you want this (player) sprite deleted? Usually False
        if P1.vel.y > 0: # This makes sure velocity is not zero unless there is already some initial velocity
            if hits:
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

def plat_gen():
    while len(platforms) < 9:
        width = random.randrange(50, 100)
        p = platform()
        p.rect.center = (random.randrange(0, WIDTH - width), random.randrange(-50, 0))
        platforms.add(p)
        all_sprites.add(p)
   
PT1 = platform() # Create a platform object
P1 = Player() # Create a player object

PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255, 0, 0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))

## Sprites Groups and Game Loop ##
# Define the sprite group and add to it
all_sprites = pygame.sprite.Group() # Define a sprite group
all_sprites.add(PT1) # Add platform to sprite group
all_sprites.add(P1) # Add the player to the sprite group
platforms = pygame.sprite.Group() # Create platform group
platforms.add(PT1) # Add platform to group

# Add randomized level generation
# This loop runs randomly between 4 and 8 times
# It generates platforms and adds them to the sprites/platforms group
for x in range(random.randint(4, 8)):
    pl = platform()
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

    print(P1.jumping)

    if P1.rect.top <= HEIGHT / 3: # Moves screen up when player is a third of the way up
        P1.pos.y += abs(P1.vel.y) 
        for plat in platforms: # Update the position of all platforms
            plat.rect.y += abs(P1.vel.y)# Add Player's velocity for all platforms
            if plat.rect.top >= HEIGHT:
                plat.kill() # Destroy platforms below the screen

    displaysurface.fill((0, 0, 0))

    P1.move() # Call player movement method every loop
    P1.update() # Call player update method
    plat_gen() # Generate platforms when there are fewer on the screen

    for entity in all_sprites: # For all sprites
        displaysurface.blit(entity.surf, entity.rect) # Blit to surface

    pygame.display.update() # Push all changes to screen and update it
    FramePerSec.tick(FPS) # Tick function used on clock object limits refresh to 60 FPS

## Implementing Movement ## 
# Changes were made in the Player class and Game Loop

##### Gravity and Jumping #####
## Implementing Gravity
# Changed self.acc in player class to vec(0, 0.5)
# This adds a constant downward movement
# Add collision detection
# Changes were made


