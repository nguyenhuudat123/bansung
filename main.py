import pygame
import math
import random
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((900, 600))

# background
background = pygame.image.load('background.png')
mixer.music.load('background1.wav')
mixer.music.play(-1)

# title and logo
pygame.display.set_caption('micro battle')
icon = pygame.image.load('icon_ai.png')
pygame.display.set_icon(icon)

# player 1
policeImg = pygame.image.load('police.png')
policeX = 50
policeY = 200
policeY_change = 0.1

# player 2
terroristImg = pygame.image.load("terrorist.png")
terroristX = 800
terroristY = 200
terroristY_change = 0.1

# ready: cant see bullet ( nạp đạn)
# fire: bắn

# bullet_police
bullet_policeImg = pygame.image.load('bullet_police.png')
bullet_policeX = 50
bullet_policeY = 0
bullet_policeX_change = 0.5
bullet_policeY_change = 0
bullet_police_state = "ready"

# bullet_terrorist
bullet_terroristImg = pygame.image.load('bullet_terrorist.png')
bullet_terroristX = 850
bullet_terroristY = 0
bullet_terroristX_change = 0.5
bullet_terroristY_change = 0
bullet_terrorist_state = "ready"

# score
score_value_police = 0
score_value_terrorist = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# end game
end_font = pygame.font.Font('freesansbold.ttf', 40)


def police(x, y):
    screen.blit(policeImg, (x, y))


def terrorist(x, y):
    screen.blit(terroristImg, (x, y))


def fire_bullet_police(x, y):
    global bullet_police_state
    bullet_police_state = "fire"
    screen.blit(bullet_policeImg, (x + 25, y + 25))


def fire_bullet_terrorist(x, y):
    global bullet_terrorist_state
    bullet_terrorist_state = "fire"
    screen.blit(bullet_terroristImg, (x + 25, y + 25))


def isCollision(pX, pY, bX, bY):
    distance = math.sqrt((math.pow(pX - bX, 2) + math.pow(pY - bY, 2)))
    if distance <= 34.17:
        return True
    else:
        return False


def show_score(x, y):
    score = font.render("Score: " + str(score_value_police) + ' - ' + str(score_value_terrorist), True, (255, 0, 255))
    screen.blit(score, (x, y))


def end_game_text():
    end_text = end_font.render("END GAME", True, (0, 128, 0))
    screen.blit(end_text, (400, 270))


# game loop
running = True
while running:
    screen.fill((0, 0, 128))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keystroke is pressed, check
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                policeY_change = -policeY_change * 2
            if event.key == pygame.K_w:
                if bullet_police_state is "ready":
                    bulletSound = mixer.Sound('short.wav')
                    bulletSound.play()
                    bullet_policeY = policeY
                    fire_bullet_police(bullet_policeX, bullet_policeY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                policeY_change = policeY_change * 2

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:
                terroristY_change = -terroristY_change * 2
            if event.key == pygame.K_p:
                if bullet_terrorist_state is "ready":
                    bulletSound = mixer.Sound('short.wav')
                    bulletSound.play()
                    bullet_terroristY = terroristY
                    fire_bullet_terrorist(bullet_terroristX, bullet_terroristY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                terroristY_change = terroristY_change * 2

    # boundary
    if policeY <= 0:
        policeY_change = 0.1
    elif policeY >= 600 - 64:
        policeY_change = -0.1

    if terroristY <= 0:
        terroristY_change = 0.1
    elif terroristY >= 600 - 64:
        terroristY_change = -0.1

    policeY += policeY_change
    terroristY += terroristY_change

    # check collision
    collision_police = isCollision(terroristX, terroristY, bullet_policeX, bullet_policeY)
    if collision_police:
        bullet_policeX = 50
        bullet_police_state = "ready"
        score_value_police += 1
        hit_sound = mixer.Sound('hit.wav')
        hit_sound.play()

    collision_terrorist = isCollision(policeX, policeY, bullet_terroristX, bullet_terroristY)
    if collision_terrorist:
        bullet_terroristX = 800
        bullet_terrorist_state = "ready"
        score_value_terrorist += 1
        hit_sound = mixer.Sound('hit.wav')
        hit_sound.play()

    # bullet
    if bullet_policeX >= 900:
        bullet_policeX = 50
        bullet_police_state = "ready"

    if bullet_police_state is "fire":
        fire_bullet_police(bullet_policeX, bullet_policeY)
        bullet_policeX += bullet_policeX_change

    if bullet_terroristX <= 0:
        bullet_terroristX = 800
        bullet_terrorist_state = "ready"

    if bullet_terrorist_state is "fire":
        fire_bullet_terrorist(bullet_terroristX, bullet_terroristY)
        bullet_terroristX -= bullet_policeX_change

    show_score(textX, textY)
    police(policeX, policeY)
    terrorist(terroristX, terroristY)
    pygame.display.update()

    if score_value_police >= 5 or score_value_terrorist >= 5:
        end_text = end_font.render("END GAME", True, (0, 128, 0))
        screen.blit(end_text, (400, 270))

