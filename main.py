import time
import random
import sys
import pygame

from bullet import Bullet, Bullet_enemy
from tanks import EnemyTank, Tank
from obstacle import Obstacle
from AStar import AStar

pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tanks")

WHITE = (255, 255, 255)
GREEN = (51, 102, 0)
BROWN = (240, 230, 140)
BLUE = (85, 170, 255)
BLACK = (0, 0, 0)

BACKGROUND_IMAGE = pygame.image.load('фонтрава10.png').convert()
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (800, 800))


def draw_landscape(window):
    window.blit(BACKGROUND_IMAGE, (0, 0))


def create_enemies(num_enemies, obstacles):
    enemies = []
    for _ in range(num_enemies):
        while True:
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)
            enemy = EnemyTank(x, y)
            if not any(enemy.rect.colliderect(obstacle.rect) for obstacle in obstacles + enemies):
                enemies.append(enemy)
                break
    return enemies


def main():
    clock = pygame.time.Clock()
    run = True

    tank = Tank(50, 50)
    bullets = []

    obstacles = [
        Obstacle(0, 0, 800, 5, BLACK),
        Obstacle(0, 0, 5, 800, BLACK),
        Obstacle(795, 0, 5, 800, BLACK),
        Obstacle(0, 795, 800, 5, BLACK),
        Obstacle(100, 100, 150, 20, BROWN),
        Obstacle(350, 100, 100, 20, BROWN),
        Obstacle(550, 100, 150, 20, BROWN),
        Obstacle(100, 100, 20, 150, BROWN),
        Obstacle(100, 350, 20, 100, BROWN),
        Obstacle(100, 550, 20, 150, BROWN),
        Obstacle(100, 680, 150, 20, BROWN),
        Obstacle(350, 680, 100, 20, BROWN),
        Obstacle(550, 680, 150, 20, BROWN),
        Obstacle(680, 100, 20, 150, BROWN),
        Obstacle(680, 350, 20, 100, BROWN),
        Obstacle(680, 550, 20, 150, BROWN),
        Obstacle(200, 200, 150, 20, BROWN),
        Obstacle(450, 200, 150, 20, BROWN),
        Obstacle(200, 200, 20, 150, BROWN),
        Obstacle(200, 450, 20, 150, BROWN),
        Obstacle(200, 580, 150, 20, BROWN),
        Obstacle(450, 580, 150, 20, BROWN),
        Obstacle(580, 200, 20, 150, BROWN),
        Obstacle(580, 450, 20, 150, BROWN),
        Obstacle(300, 300, 200, 200, BLUE)   
    ]

    enemies = create_enemies(5, obstacles + [tank])
    astar = AStar(WIDTH, HEIGHT, Tank.size)
    astar.save_obstacles(obstacles)
    quit_flag = False
    # Создание объекта Clock
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            tank.process_key_event(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    new_bullet = Bullet(tank.rect.centerx, tank.rect.centery, tank.get_angle())
                    bullets.append(new_bullet)

        tank.move()

        if tank.check_collision(obstacles + enemies):
            tank.stop()

        for enemy in enemies:
            enemy.move(lambda : astar.bfs(tank, enemy))
            if enemy.check_collision(obstacles + enemies + [tank]):
                enemy.stop()
        for enemy in enemies:
            if enemy.check_kill(tank, obstacles) and enemy.check_shot():
                new_bullet = Bullet_enemy(enemy.rect.centerx, enemy.rect.centery, enemy.angle)
                bullets.append(new_bullet)
        for bullet in bullets:
            if type(bullet) == Bullet and bullet.check_collision(obstacles, enemies):
                bullets.remove(bullet)
            if type(bullet) == Bullet_enemy and bullet.check_collision(obstacles, []):
                bullets.remove(bullet)
            if type(bullet) == Bullet_enemy and bullet.check_collision([], [tank]):
                bullets.remove(bullet)
                # print(bullet, bullet.angle)
                quit_flag = True
                break
        if quit_flag: 
            break

        draw_landscape(WIN)

        bullets = [bullet for bullet in bullets if
                   bullet.rect.right > 0 and bullet.rect.left < WIDTH and bullet.rect.bottom > 0 and bullet.rect.top < HEIGHT]

        for obstacle in obstacles:
            obstacle.draw(WIN)

        for enemy in enemies:
            enemy.draw(WIN)

        tank.draw(WIN)

        for bullet in bullets:
            bullet.draw(WIN)
            bullet.move()

        # Ограничение частоты кадров до 60 FPS
        # clock.tick(60)
        pygame.display.update()


    # pygame.quit()
    # sys.exit()


if __name__ == "__main__":
    main()
