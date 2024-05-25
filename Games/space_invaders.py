# filename: space_invaders.py

import pygame
import sys
import random
from pygame.locals import *

# Game constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PLAYER_SPEED = 5
BULLET_SPEED = 10
INVADER_SPEED = 2
INVADER_DROP_SPEED = 10
INVADER_SHOOT_CHANCE = 0.01
PLAYER_BULLET_LIMIT = 3
INVADER_BULLET_LIMIT = 10

# Initialize Pygame
pygame.init()

# Set up some variables
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Set up game objects
player = pygame.Rect(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 60, 50, 50)
bullets = []
invaders = [pygame.Rect(x, y, 40, 40) for x in range(100, WINDOW_WIDTH - 100, 50) for y in range(50, 200, 50)]
invader_bullets = []

# Game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE and len(bullets) < PLAYER_BULLET_LIMIT:
                bullets.append(pygame.Rect(player.centerx, player.top, 10, 20))

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[K_LEFT] and player.left > 0:
        player.left -= PLAYER_SPEED
    if keys[K_RIGHT] and player.right < WINDOW_WIDTH:
        player.right += PLAYER_SPEED

    # Bullet movement
    for bullet in bullets:
        bullet.top -= BULLET_SPEED
    bullets = [bullet for bullet in bullets if bullet.bottom > 0]

    # Invader movement
    for invader in invaders:
        invader.left += INVADER_SPEED
        if invader.right > WINDOW_WIDTH or invader.left < 0:
            INVADER_SPEED = -INVADER_SPEED
            for invader in invaders:
                invader.top += INVADER_DROP_SPEED
        if random.random() < INVADER_SHOOT_CHANCE and len(invader_bullets) < INVADER_BULLET_LIMIT:
            invader_bullets.append(pygame.Rect(invader.centerx, invader.bottom, 10, 20))

    # Invader bullet movement
    for bullet in invader_bullets:
        bullet.top += BULLET_SPEED
    invader_bullets = [bullet for bullet in invader_bullets if bullet.top < WINDOW_HEIGHT]

    # Collision detection
    for bullet in bullets:
        if bullet.collidelist(invaders) != -1:
            bullets.remove(bullet)
            del invaders[bullet.collidelist(invaders)]
    if player.collidelist(invader_bullets) != -1:
        pygame.quit()
        sys.exit()

    # Drawing
    window.fill((0, 0, 0))
    pygame.draw.rect(window, (0, 255, 0), player)
    for bullet in bullets:
        pygame.draw.line(window, (255, 255, 255), bullet.midtop, bullet.midbottom)
    for invader in invaders:
        pygame.draw.circle(window, (255, 0, 0), invader.center, invader.width // 2)
    for bullet in invader_bullets:
        pygame.draw.line(window, (255, 255, 255), bullet.midtop, bullet.midbottom)
    pygame.display.update()

    # Cap the frame rate
    clock.tick(60)
