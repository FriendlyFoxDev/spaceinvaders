import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Creates the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.png")

# Background Sounds
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Speeds
enemy_speed = 0.2
player_speed = 0.3
bullet_speed = 1

# Player
player_img = pygame.image.load("player.png")
player_x = 370
player_y = 480
player_x_change = 0

# Enemy
enemyImg = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("alien.png"))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(enemy_speed)
    enemy_y_change.append(40)

# Laser
laser_img = pygame.image.load("bullet.png")
bullet_y_change = bullet_speed
bullet_x = 0
bullet_y = player_y
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

text_x = 10
text_y = 10

# Game Over Text
over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(laser_img, (x + 16, y + 10))


def is_collision(e_x, e_y, b_x, b_y):
    distance = math.sqrt(math.pow(e_x - b_x, 2) + math.pow(e_y - b_y, 2))
    if distance < 27:
        return True
    else:
        return False


# Game Loop that break when running = False
running = True
while running:
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -player_speed
            if event.key == pygame.K_RIGHT:
                player_x_change = player_speed
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    player_x += player_x_change

    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    for i in range(num_of_enemies):

        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break

        enemy_x[i] += enemy_x_change[i]

        if enemy_x[i] <= 0:
            enemy_x_change[i] = enemy_speed
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -enemy_speed
            enemy_y[i] += enemy_y_change[i]

        # Collision
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)

    # Bullet Movement
    if bullet_y == -32:
        bullet_state = "ready"
        bullet_y = player_y
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
