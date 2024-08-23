# Import additional modules
import pgzrun
import pygame
# import time
import random

# Set size of overall game window
WIDTH = 1000
HEIGHT = 600
# Variables for animating background color
blue = 130
blue_forward = True
# Ground
ground_color = 0, 0, 139
ground = Rect((0, 580), (1000, 20))
# Player
ninja = Actor('jumper-1', (WIDTH/2, HEIGHT/2))
ninja_x_velocity = 0
ninja_y_velocity = 0
gravity = 1
jumping = False
jumped = False
allow_x = True
timer = []
# Platforms
platform_01 = pygame.Rect((450, 500), (100, 10))  # Platform in center of screen
platform_02 = pygame.Rect((300, 400), (100, 10))  # . Moving out left
platform_03 = pygame.Rect((600, 400), (100, 10))  # . Moving out right
platform_04 = pygame.Rect((200, 300), (100, 10))  # . . Moving out left
platform_05 = pygame.Rect((700, 300), (100, 10))  # . . Moving out right
platform_06 = pygame.Rect((100, 200), (100, 10))  # . . . Moving out left
platform_LT_x = 200  # Starting x position of left moving platform
platform_RT_x = 700  # Starting x position of right moving platform
platform_LT = pygame.Rect((platform_LT_x, 200), (100, 10))  # Left moving platform
platform_RT = pygame.Rect((platform_RT_x, 200), (100, 10))  # Right moving platform
platform_07 = pygame.Rect((800, 200), (100, 10))  # . . . Moving out right
platform_08 = pygame.Rect((0, 100), (100, 10))  # Top far left
platform_09 = pygame.Rect((900, 100), (100, 10))  # Top far right
# Used to define all walkable surfaces
platforms = [ground, platform_01, platform_02, platform_03, platform_04,
             platform_05, platform_06, platform_07, platform_08, platform_09,
             platform_LT, platform_RT]
# Variables to track direction of moving platforms
platform_LT_leftDir = True
platform_RT_leftDir = False
# Gems
diamond_x = [950, 50, 850, 150, 750, 250, 650, 350, 500]
diamond_y = [70, 70, 170, 170, 270, 270, 370, 370, 470]
diamond_xy = random.randint(0, 8)
gem = Actor('diamond_s', (diamond_x[diamond_xy], diamond_y[diamond_xy]))
points = 0
# Music
pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.init()
pygame.mixer.quit()
pygame.mixer.init(22050, -16, 2, 1024)
sounds.ninja_music.play(-1)


def draw():
    # This is our function for drawing things on screen

    # We need to set these variables for global use, or the changes only stay
    # within this function
    global platform_LT, platform_RT
    # Paints the entire game window in our 'animatable' blue
    screen.fill((173, 216, blue))
    # Overlays an image (with alpha) that is exact size of game window
    screen.blit('skyline_large', (0, 0))
    # Dynamically updates position of platforms for drawing them moving
    platform_LT = Rect((platform_LT_x, 200), (100, 10))  # Left moving platform
    platform_RT = Rect((platform_RT_x, 200), (100, 10))  # Right  platform
    platforms[10] = platform_LT
    platforms[11] = platform_RT
    # Draws all walkable surfaces by iterating through 'platforms' list
    for i in platforms:
        screen.draw.filled_rect(i, ground_color)
    # Draws the Actor we set up at start
    ninja.draw()
    gem.draw()
    screen.draw.text('Loot:', center=(50, 540), fontsize=40, shadow=(1, 1), color=(255, 255, 255), scolor='#202020')
    screen.draw.text(str(points), center=(45, 570), fontsize=40, shadow=(1, 1), color=(255, 255, 255), scolor='#202020')

def update():
    # This is our game loop

    # Run animation code defined below
    background_color_fade()
    # Moves platforms
    platform_mover()
    # Moves player
    ninja_move()


def ninja_move():
    # This sets the players movement characteristics

    # We need to set these variables for global use, or the changes only stay
    # within this function
    global ninja_x_velocity, ninja_y_velocity, gravity, jumping, jumped, allow_x, timer, points, diamond_xy
    # Facing forwards
    if ninja_x_velocity == 0 and not jumped:
        ninja.image = 'jumper-1'
    # Gravity
    if collision_check():
        gravity = 1
        ninja.y -= 1
        allow_x = True
        timer = []
    if not collision_check():
        ninja.y += gravity
        if gravity <= 20:
            gravity += 0.5
        timer.append(pygame.time.get_ticks())
        if len(timer) > 5 and not jumped:
            allow_x = False
            ninja.image = 'jumper-up'
            if len(timer) > 20:
                ninja.image = 'jumper-fall'
                if len(timer) > 30:
                    ninja.image = 'jumper-fall2'
        # print(timer)
    # Left and right player movement
    if (keyboard.left) and allow_x:
        if (ninja.x > 40) and (ninja_x_velocity > -8):
            ninja_x_velocity -= 2
            ninja.image = 'jumper-left'
            if (keyboard.left) and jumped:
                ninja.image = 'jumper-jleft'
    if (keyboard.right) and allow_x:
        if (ninja.x < 960) and (ninja_x_velocity < 8):
            ninja_x_velocity += 2
            ninja.image = 'jumper-right'
            if (keyboard.right) and jumped:
                ninja.image = 'jumper-jright'
    ninja.x += ninja_x_velocity
    print(allow_x)
    # Player velocity
    if ninja_x_velocity > 0:
        ninja_x_velocity -= 1
    if ninja_x_velocity < 0:
        ninja_x_velocity += 1
    if ninja.x < 50 or ninja.x > 950:
        ninja_x_velocity = 0
    # Player jump
    if (keyboard.up) and collision_check() and not jumped:
        jumping = True
        jumped = True
        clock.schedule_unique(jumped_recently, 0.5)
        ninja.image = 'jumper-up'
        ninja_y_velocity = 95
    if jumping and ninja_y_velocity > 25:
        ninja_y_velocity = ninja_y_velocity - ((100 - ninja_y_velocity)/2)
        # print(ninja_y_velocity)
        ninja.y -= ninja_y_velocity/3  # Jump height
    else:
        ninja_y_velocity = 0
        jumping = False
    # Gem collision
    if ninja.colliderect(gem):
        points += 1
        old_diamond_xy = diamond_xy
        diamond_xy = random.randint(0, 8)
        while old_diamond_xy == diamond_xy:
            diamond_xy = random.randint(0, 8)
        gem.x = diamond_x[diamond_xy]
        gem.y = diamond_y[diamond_xy]


def platform_mover():
    # This code moves the two platorms in and then out at same time

    # We need to set these variables for global use, or the changes only stay
    # within this function
    global platform_LT_x, platform_RT_x, platform_LT_leftDir, platform_RT_leftDir
    # When True, will move left platform until it reaches 400, then it will
    # move back other direction
    if platform_LT_leftDir:
        platform_LT_x += 2
        if platform_LT_x == 400:
            platform_LT_leftDir = False
        if ninja.colliderect(platform_LT):
            ninja.x += 2
    else:
        platform_LT_x -= 2
        if platform_LT_x == 200:
            platform_LT_leftDir = True
        if ninja.colliderect(platform_LT):
            ninja.x -= 2
    # When False, will move right platform until it reaches 500, then it will
    # move back other direction
    if platform_RT_leftDir:
        platform_RT_x += 2
        if platform_RT_x == 700:
            platform_RT_leftDir = False
        if ninja.colliderect(platform_RT):
            ninja.x += 2
    else:
        platform_RT_x -= 2
        if platform_RT_x == 500:
            platform_RT_leftDir = True
        if ninja.colliderect(platform_RT):
            ninja.x -= 2


def collision_check():
    collide = False
    for i in platforms:
        if ninja.colliderect(i):
            collide = True
    return collide


def jumped_recently():
    global jumped
    jumped = False


def background_color_fade():
    # This code cycles varaible up and then back down, changing the numeric
    # value of blue in RGB color

    # We need to set these variables for global use, or the changes only stay
    # within this function
    global blue, blue_forward
    # As long as we're on our way up and less than max blue value, add one to
    # value of blue
    if blue < 255 and blue_forward:
        blue += 1
    else:
        blue_forward = False
    # Same functionality on way down to lowest value we set
    if blue > 130 and not blue_forward:
        blue -= 1
    else:
        blue_forward = True


pgzrun.go()
