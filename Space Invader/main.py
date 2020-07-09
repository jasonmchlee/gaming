import random
import pygame
import math
from pygame import mixer


# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.jpg")

# Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1)


# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("rocket.png")
pygame.display.set_icon(icon)

# PLAYER
playerImg = pygame.image.load("player.png")
playerX = 370  # coordinates - half of width
playerY = 480  # coordinates - close to max height of 600
playerX_change = 0


# player function
def player(x, y):
    screen.blit(playerImg, (x, y))  # to draw image onto the screen using the player coordinates


# ENEMY
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("spaceship.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)  # move it down by 40 pixels

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
over_font = pygame.font.Font("freesansbold.ttf", 64)


# location of score
testX = 10
testY = 10

def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x,y))

# Game Over Text
def  game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# enemy function
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # to draw image onto the screen using the player coordinates


# BULLET

# Ready - can't see bullet on screen. Fire - bullet is moving
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480  # same level as space ship
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


# bullet function
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"  # in motion
    screen.blit(bulletImg, (x + 16, y + 10))  # make sure bullet appears in center of bullet


# collision function
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# GAME LOOP
running = True
while running:

    # RGB - Red, Green, Blue values to implement screen color
    screen.fill((0, 0, 0))

    # background image
    screen.blit(background, (0, 0))

    # all events in the game
    for event in pygame.event.get():

        # create an event to quit if it is exited then break while loop
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:

            # increase coordinate when key is pressed
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5

            # fire bullet
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":  # checks if bullet is already on the screen
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    # get the current x coordinate of space ship
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)  # calls the function and creates bullet

        # releasing the key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # PLAYER MOVEMENT
    playerX += playerX_change  # increment the change

    # setting boundaries for the space ship
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # ENEMY MOVEMENT
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000 # bring enemies below the screen

            # When 1 enemy reaches 440 pixels and display game over text
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]  # increment the change

        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # COLLISION
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480  # reset to original
            bullet_state = 'ready'
            score_value += 1
            print(score_value)

            # respawn the enemy in original random location
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # BULLET MOVEMENT
    # shooting several bullets
    if bulletY <= 0:
        bulletY = 480  # reset state
        bullet_state = "ready"

    # keep it presistent in the game by including in while loop
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)  # calling the function. We draw the player ontop of the screen fill.
    show_score(testX, testY)
    pygame.display.update()  # update the screen each time
