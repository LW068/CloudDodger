import pygame
import random
import sys
import os
from pygame import mixer

#Initializing pygame / sound mixer for custom audio clips 
pygame.init()
mixer.init()

# Setting Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
INVISIBLE = (0, 0, 0, 1)

# Stores Highscore / converts to integer number / File Reader
try:
    with open("high_score.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    high_score = 0

# Player properties and dimensions / Intializng Betty's positon on screen
player_width = 100 # Set to 100 pixels 
player_height = 100 # set to 100 pixels 
player_health = 100  # Setting player health to 100%
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height

# Hitbox adjustment for Player / Collison detection area for player / setting pixels
player_hitbox_offset_x = 30 # Offset the hitbox by 30 pixels Horizontally
player_hitbox_offset_y = 30 # Offset the hitbox by 30 pixels Vertically
player_hitbox_width = player_width - player_hitbox_offset_x
player_hitbox_height = player_height - player_hitbox_offset_y

#Timer Font size / Dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Timer")
font_path = "fonts/press-start-2p.regular.ttf"  # Custom TTF file name
font = pygame.font.Font(font_path, 18)

# Set up clock / Controls game frame rate and track elapsed game time
clock = pygame.time.Clock()

# Define timer function / converting milliseconds to seconds /draw to screen
def draw_timer(screen, elapsed_time, x, y, font, color):
    timer_text = font.render(f"SCORE: {int(elapsed_time // 1000)}", True, color)
    screen.blit(timer_text, (x + 80, y))

# Starting point for elapsed timer
timer_start = pygame.time.get_ticks()

# Draws a health bar with an outline and filled portion based on the current health percentage of Betty.
def draw_health_bar(screen, health, x, y, width, height, color):
    health_percentage = max(0, min(1, health / 100))
    # Drawing health bar outline
    pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height), 2)
    pygame.draw.rect(
        screen,
        color,
        (x + 2,
         y + 2,
         (width - 4) * health_percentage,
            height - 4))  # Drawing health bar filled
    
# Game Score / Current Score Font
font = pygame.font.Font(font_path, 11)
# Create a font for the health percentage
percentage_font = pygame.font.Font(font_path, 15)
    # Displays the health value as a percentage on the screen using a specified font and color.
def draw_health_percentage(screen, health, x, y, font, color):
    health_percentage_text = font.render(f"{health}%", True, color) # < creating the % SIGN
    screen.blit(health_percentage_text, (x, y))

# Cloud Properties and Dimensions / Setting to the specified pixels
cloud_width = 100 # Set to 100 pixels
cloud_height = 50 # Set to 50 pixels
cloud_list = [] # Initalizing an empty list / storing cloud positions
cloud_speed = 10 # Well says itself

for i in range(5):  # Loop that iterates 5 times / creating 5 clouds
    cloud_x = random.randint(0, WIDTH - cloud_width) # Generating random clouds spawning but only within Game Window
    cloud_y = random.randint(-500, 0)
    cloud_list.append([cloud_x, cloud_y])

# Seahorse properties and dimensions / setting pixels
seahorse_width = 100 # Set to 100 pixels
seahorse_height = 100 # Set to 100 pixels
seahorse_list = [] # Initalizing an empty list / storing seahorse positions
seahorse_speed = 8 # Well says itself

for i in range(1): # Generates Seahorses for Extra Health Boost
    seahorse_x = random.randint(0, WIDTH - cloud_width) # Generating random seahorses spawning but only within Game Window
    seahorse_y = random.randint(-500, 0)
    seahorse_list.append([seahorse_x, seahorse_y]) # append the seahorse to empty list

# Main Menu Page
screen = pygame.display.set_mode((WIDTH, HEIGHT))
gamemenu_image1 = pygame.image.load('graphics/menuscreen/MenuScreen1.png')
gamemenu_image1 = pygame.transform.scale(gamemenu_image1, (WIDTH, HEIGHT))
gamemenu_image2 = pygame.image.load('graphics/menuscreen/MenuScreen2.png')
gamemenu_image2 = pygame.transform.scale(gamemenu_image2, (WIDTH, HEIGHT))

# Main Menu Start button and Game Title
start_text = font.render("START", True, WHITE)
start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)

# image loader
betty_image = pygame.image.load('graphics/betty.png')
end_image1 = pygame.image.load('graphics/endscreen/end_screen1.png')
end_image2 = pygame.image.load('graphics/endscreen/end_screen2.png')
spaceimage = pygame.image.load('graphics/spaceimage.png')
cloud_image = pygame.image.load('graphics/cloudimage.png')
cloud_image2 = pygame.image.load('graphics/cloudimage2.png')
betty_left_image = pygame.image.load('graphics/bettyleft.png')
betty_right_image = pygame.image.load('graphics/bettyright.png')
betty_default_image = pygame.image.load("graphics/betty.png")
seahorse_image = pygame.image.load('graphics/seahorse.png')
start_button_image = pygame.image.load('graphics/startbutton.GIF')

# Scale Images to specified pixel dimensions
start_button_image = pygame.transform.scale(start_button_image, (150, 150))
seahorse_image = pygame.transform.scale(seahorse_image, (200, 200))
betty_image = pygame.transform.scale(betty_image, (100, 100))
betty_left_image = pygame.transform.scale(betty_left_image, (100, 100))
betty_right_image = pygame.transform.scale(betty_right_image, (100, 100))
cloud_image = pygame.transform.scale(cloud_image, (cloud_width, cloud_height))
cloud_image2 = pygame.transform.scale(cloud_image2, (cloud_width, cloud_height))
betty_default_image = pygame.transform.scale(betty_default_image, (100, 100))
end_image1 = pygame.transform.scale(end_image1, (WIDTH, HEIGHT))
end_image2 = pygame.transform.scale(end_image2, (WIDTH, HEIGHT))


# Sound Loader 
bettydead_sound = mixer.Sound('audios/bettydead_sound.mp3')

menu = True # initalizing menu variable and setting the value to True / controls menu display
running = False # Initalizing running variable and setting value to False / controls game loop
game_started = False  # Initializing game_started variable and setting value to False
background_counter = 0
button_counter = 0
FPS = 60
while menu: # As long as it is set to true, it will control the menu events
    for event in pygame.event.get(): # Iterating through all the events in the event queues
        if event.type == pygame.QUIT: # Checks if window is closed
            menu = False # if the window closes then set the menu to False to close application

        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos): # Checks if mouse clicks on start button
                running = True
                menu = False
                game_started = True  # Set game_started to True
                timer_start = pygame.time.get_ticks()  # Set timer_start when the game starts


    high_score_text = font.render(f"HIGH SCORE: {high_score}", True, WHITE)
    high_score_rect = high_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 5))
    screen.blit(high_score_text, high_score_rect)

    # Draw Main Menu Screen
    background_counter += 1
    if background_counter % 32 < 16: # half the time
        screen.blit(gamemenu_image1, (0, 0))
    else: # half the time
        screen.blit(gamemenu_image2, (0, 0))

    pygame.display.flip()
    clock.tick(FPS)

# Default Cloud list
cloud_list = [] # Intializing empty list for storing cloud positions
for i in range(5): # Creates positions for the 5 clouds
    cloud_x = random.randint(0, WIDTH - cloud_width) # Spawns the cloud within the screen x axis
    cloud_y = random.randint(-500, 0) # spawns the clouds above which is y axis off screen
    cloud_list.append([cloud_x, cloud_y]) # appends the created cloud to the cloud list

# Seahorse list
seahorse_list = [] # intializes empty list for storing seahorse positions
for i in range(1): # creates positions for 1 seahorse
    seahorse_x = random.randint(0, WIDTH - seahorse_width) # spawns the seahorse within the screen x axis
    seahorse_y = random.randint(-500 , 0 ) # spawns the seahorse above which is y axis off screen
    seahorse_list.append([seahorse_x, seahorse_y]) # appends the created seahorse to the seahorse list

# Set up player
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height

# Collisions between player and clouds
def check_collision(player, cloud):
    player_hitbox = pygame.Rect(player[0] + player_hitbox_offset_x // 2, player[1] + player_hitbox_offset_y // 2, player_hitbox_width, player_hitbox_height)
    cloud_rect = pygame.Rect(cloud[0], cloud[1], cloud_width, cloud_height)
    return player_hitbox.colliderect(cloud_rect)

# Collison between Player and Seahorse 
def check_collision_seahorse(player, seahorse):
    player_hitbox = pygame.Rect(player[0] + player_hitbox_offset_x // 2, player[1] + player_hitbox_offset_y //2, player_hitbox_width, player_hitbox_height)
    seahorse = pygame.Rect(seahorse[0], seahorse[1], seahorse_width, seahorse_height)
    return player_hitbox.colliderect(seahorse)


# Set up Game Over text
game_over_text = font.render("", True, RED)
game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))

music_path = 'audios/gamemusic.mp3'

if os.path.isfile(music_path):
    try:
        mixer.music.load(music_path)
        mixer.music.play(-1)
    except pygame.error:
        pass

# Displays last high score from txt file
def draw_high_score(screen, high_score, x, y, font, color):
    high_score_text = font.render(f"HIGH SCORE: {int(high_score)}", True, color)
    screen.blit(high_score_text, (x, y))

# Start Game loop / constantly updating 
while running:
    for event in pygame.event.get(): # Iterates through all event queues
        if event.type == pygame.QUIT:
            running = False # Closes out the Betty Dodger Game if a quit is detected 

    keys = pygame.key.get_pressed() # Gathers all current actions of the key binds that get touched by player

    if keys[pygame.K_RIGHT]: # If Pressed the Betty right image Will render
        player_x += 10 # Moves Betty 5 pixels to the right
        betty_image = betty_right_image # Renders the Betty image to appear
    elif keys[pygame.K_LEFT]: # If pressed the Betty Left Image will render
        player_x += -10 # Moves Betty 5 pixels to the left
        betty_image = betty_left_image # Renders the Betty image to appear
    else:
        betty_image = betty_default_image # If no keys are being touched
        screen.blit(betty_image, (player_x, player_y)) # Renders the Default Betty Image

    # Timer related code
    elapsed_time = pygame.time.get_ticks() - timer_start if game_started else 0

    pygame.display.flip()  # Update the display
    clock.tick(FPS)  # Limit the frame rate 
    
    player_x = max(0, min(player_x, WIDTH - player_width)) # Prevents Betty from going off screen

    # In Game Background Filler
    LIGHT_BLUE = (173, 216, 230)
    screen.fill(LIGHT_BLUE)
    
    # Calculates the time as soon as Game Starts
    elapsed_time = pygame.time.get_ticks() - timer_start
    draw_timer(screen, elapsed_time, WIDTH - 200, 10, font, RED) # Displays the Timer in Game

    # Render and Displays the high score
    draw_high_score(screen, high_score, WIDTH - 450, 10, font, BLUE)

    #High Score
    with open("high_score.txt", "w") as file:
        file.write(str(high_score))

    # Health Percentage Font
    percentage_font = pygame.font.Font(font_path, 12)

    draw_health_bar(screen, player_health, 10, 5, 200, 20, (0, 255, 0))  # Draw health bar
    player_health = min(player_health, 100) # Make sure health doesn't exceed 100% on health bar
    draw_health_percentage(screen, player_health, 10 + 200 // 2.2 - 15, 10, percentage_font, (0, 0, 0))
    # Health bar drawn + outline

    # Iterating through each cloud in list, increment the coordinates, reset coordinates at random coordinates at top screen
    for cloud in cloud_list: # Iterates through each cloud in the cloud list
        cloud[1] += cloud_speed # increases the y coordinate to make the cloud move vertically downwards 
        if cloud[1] > HEIGHT: # checks if it is vertically greater than the screen height / cloud moved off screen 
            cloud[0] = random.randint(0, WIDTH - cloud_width) # Resets the cloud positions at top of screen at random coordinates
            cloud[1] = random.randint(-500, 0) # Does same thing line above

        screen.blit(cloud_image, (cloud[0], cloud[1])) # Draws cloud image to screen
    # Darker Cloud Spawns 30 Seconds in game
    if elapsed_time >= 30000:  # 30 seconds * 1000 milliseconds
        current_cloud_image = cloud_image2
    else:
        current_cloud_image = cloud_image

    screen.blit(current_cloud_image, (cloud[0], cloud[1])) # Draws the clouds on screen

    # Iterates through loop / draws seahorse image to screen
    for seahorse in seahorse_list: # iterates through each seahorse in the list
        seahorse[1] += seahorse_speed # increases the y coordinates to make the seahorse move vertically downwards
        if seahorse[1] > HEIGHT: # checks if it is vertically greater than the window screen / seahorse moved off screen
            seahorse[0] = random.randint(0, WIDTH - cloud_width) # resets the seahorse positions at top of screen at random coordinates
            seahorse[1] = random.randint(-500, 0) # Does the same thing line above
            
        screen.blit(seahorse_image, (seahorse[0], seahorse[1])) # Draws the seahorse image on screen

    # Check for collision between Clouds and Betty
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for cloud in cloud_list:
        cloud_rect = pygame.Rect(cloud[0], cloud[1], cloud_width, cloud_height)
        if check_collision(player_rect, cloud_rect):
            player_health -= 3  # Decrease player health by 10

    if player_health <= 0: # if Betty's health is less than equal to 0 then hit the stop on the mixer and play death sound
        mixer.music.stop() # Stop theme music playing instantly
        bettydeath_sound = mixer.Sound('audios/bettydead_sound.mp3')
        bettydeath_sound.play() # When Betty's health hits 0%
        running = False  # End the game if player health reaches 0% Health

    # Players High score
    current_score = int(elapsed_time // 1000)
    if current_score > high_score: # checks to see the if current score is greater than high score
        high_score = current_score

    # Checks for collison between Betty and Seahorse
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for seahorse in seahorse_list:
        seahorse_rect = pygame.Rect(seahorse[0], seahorse[1], seahorse_width, seahorse_height)
        if check_collision_seahorse(player_rect, seahorse_rect):
            player_health += 1 # Increasing Betty's health when collided

    screen.blit(betty_image, (player_x, player_y)) # Draws to screen

    pygame.display.flip()
    clock.tick(FPS)

def game_over_screen():
    restart_button = pygame.Surface((200, 70), pygame.SRCALPHA)
    restart_button_rect = restart_button.get_rect(center=(WIDTH // 2, HEIGHT // 2.7))
    restart_text = font.render("", True, WHITE)

    background_counter = 0  # Line to initialize the counter for screen flickering

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    return True

        background_counter += 1  # Update the counter            

        # Flicker the game over background using the counter
        if background_counter % 32 < 16:
            screen.blit(end_image1, (0, 0))
        else:
            screen.blit(end_image2, (0, 0))

        screen.blit(game_over_text, game_over_rect)
        screen.blit(restart_button, restart_button_rect)

        pygame.display.flip()
        clock.tick(FPS)

# Show the "Game Over" screen
restart = game_over_screen()

if restart:
    # If the player chose to restart, run the script again
    os.execv(sys.executable, ['python'] + sys.argv)
else:
    pygame.quit()
