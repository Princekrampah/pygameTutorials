import pygame
import random
import math

# intantiate a pygame object
pygame.init

# create the game screen(width(x-value), height(y-value))
screen = pygame.display.set_mode((900, 600))


# set game window title
pygame.display.set_caption("Space Invader Game")

# load background image
background_img = pygame.image.load("./assets/background.jpg")

# load the window icon
win_icon = pygame.image.load("./assets/startup.png")
# set the window icon
pygame.display.set_icon(win_icon)



# add audio to the game
from pygame import mixer

mixer.init()

# add background music
mixer.music.load("./assets/backgroundTrack.mp3")
# play music in a loop by passing in -1
mixer.music.play(-1)

# shot sound
shot_sound = mixer.Sound("./assets/teleport.mp3")

# crash sound
crash_sound = mixer.Sound("./assets/shot.mp3")


# load player image
player_img = pygame.image.load("./assets/spaceship.png")
# 410 because we have to consider the size of the image as well
playerX = 410
playerY = 480
change_in_playerX = 0

# multiple enemies
enemy_img = []
enemyX = []
enemyY = []
change_in_enemyX = []
number_of_enemies = 4

for i in range(number_of_enemies):
    # load enemy image
    enemy_img.append(pygame.image.load("./assets/ufo.png"))
    # 410 because we have to consider the size of the image as well
    enemyX.append(random.randint(64, 836))
    enemyY.append(random.randint(64, 160))
    change_in_enemyX.append(0.4)


# buttet load up
bullet_img = pygame.image.load("./assets/bullet.png")
bulletY = 480
bulletX = 0
bullet_state = "loaded"
change_in_bulletY = 4

# score values
player_score = 0


# create score font
pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 32)
# font coordinates
fontX = 15
fontY = 15


# game over font
game_over_font = pygame.font.Font("freesansbold.ttf", 64)


def player(x, y):
    # draw player image onto screen
    screen.blit(player_img, (x, y))
    
def enemy(x, y, i):
    # draw player image onto screen
    screen.blit(enemy_img[i], (x, y))


def shot(x, y):
    global bullet_state
    bullet_state = "fired"
    # draw bullet on the screen
    screen.blit(bullet_img, (x, y))
    

def isCollided(bulletX, bulletY, enemyX, enemyY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    
    if distance < 30:
        return True
    else:
        return False
    
    
def display_score(x, y):
    # create an  image to blit to the screen
    score_img = font.render(f"Total Score: {str(player_score)}", True, (255, 255, 255))
    screen.blit(score_img, (x, y))
    

def game_over():
    # create an  image to blit to the screen
    game_over_img = game_over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(game_over_img, (430, 250))


running = True

# run an infinite loop, we put anything we want persistant
# in each frame of the game here
while running:
    # get list of all game events happening
    for game_event in pygame.event.get():
        # check if close btn pressed
        if game_event.type == pygame.QUIT:
            running = False

        # check if key has been pressed
        if game_event.type == pygame.KEYDOWN:
            # check out for the ESC key press 
            if game_event.key == pygame.K_ESCAPE:
                running = False
                
            # if left arrow is pressed
            if game_event.key == pygame.K_LEFT:
                change_in_playerX = -0.55
                
            if game_event.key == pygame.K_RIGHT:
                change_in_playerX = 0.55
                
            # this here is not going to display the bullet continuously
            # to do this, we need to put it inside of the infinite while loop
            if game_event.key == pygame.K_SPACE:
                # we can only fire a loaded bullet
                if bullet_state == "loaded":
                    shot_sound.play()
                    bulletX = playerX
                    shot(bulletX, bulletY)
            
        # check if keystroke has been released
        if game_event.type == pygame.KEYUP:
            if game_event.key == pygame.K_LEFT or game_event.key == pygame.K_RIGHT:
                change_in_playerX = 0
                
    
    # lets add a fill to the background(Background color)
    # this is basically going to be an RGB value
    # simply passing this, the color wont change
    # we need to update the screen
    screen.fill((0, 0, 0))
    screen.blit(background_img, (0, 0))
    
    # this should be call after the screen.fill() so that the player can
    # appear above the drawing and must be before the pygame.display.update()
    playerX += change_in_playerX
    
    # add some boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 836:
        # 900 - 64(size of img) = 836
        playerX = 836
        
        
        
    for i in range(number_of_enemies):
        
        # game over
        if enemyY[i] > 400:
            for j in range(number_of_enemies):
                enemyY[j] = -3000
            game_over()
            break
        
        # enemy movement
        enemyX[i] += change_in_enemyX[i]
        # add some boundaries
        if enemyX[i] <= 0:
            change_in_enemyX[i] = 0.4
            enemyY[i] += random.randint(0, 60)
        elif enemyX[i] >= 836:
            change_in_enemyX[i] = -0.4
            enemyY[i] += random.randint(0, 60)
            
        # Collision detection
        if isCollided(bulletX, bulletY, enemyX[i], enemyY[i]):
            crash_sound.play()
            bulletY = 480
            # reset the bullet for the next round of shot
            bullet_state = "loaded"
            
            player_score += 1
            print(player_score)
            # respound enemy to a random position, reduce the y-value from
            # 836 to 835
            enemyX[i] = random.randint(64, 835)
            enemyY[i] = random.randint(64, 160)
            
        enemy(enemyX[i], enemyY[i], i)        
        
    if bulletY <= 0:
        # move bullet back to spacecraft y-position
        bulletY = 480
        # reset the bullet for the next round of shot
        bullet_state = "loaded"
        
    if bullet_state == "fired":
        shot(bulletX, bulletY)
        # move bullet in upward direction
        bulletY -= change_in_bulletY
        
        

    
    player(playerX, playerY)
    # display the score here
    display_score(fontX, fontY)
    
    
    
    # update the screen to reflect color change
    # this is important for also player movements and the changes in the screen
    pygame.display.update()
    

pygame.quit()         
        
    