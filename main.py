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
    for i in range(num_enemies):
        while True:
            x = random.randint(50 * 3, WIDTH - 50)
            y = random.randint(50 * 3, HEIGHT - 50)
            enemy = EnemyTank(x, y)
            if not any(enemy.rect.colliderect(obstacle.rect) for obstacle in obstacles + enemies):
                enemies.append(enemy)
                break
    return enemies


def draw_text(window, text, size, color, x, y):
    font = pygame.font.SysFont(None, size)
    label = font.render(text, True, color)
    window.blit(label, (x, y))


def start_screen():
    run = True
    while run:
        WIN.fill(WHITE)
        draw_text(WIN, "Press Enter to Start", 50, BLACK, WIDTH // 2 - 150, HEIGHT // 2 - 50)
        draw_text(WIN, "Press ESC to Quit", 30, BLACK, WIDTH // 2 - 100, HEIGHT // 2 + 10)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def game_over_screen(message, rounds_won):
    run = True
    while run:
        WIN.fill(WHITE)
        draw_text(WIN, message, 50, BLACK, WIDTH // 2 - 200, HEIGHT // 2 - 50)
        draw_text(WIN, f"Rounds Won: {rounds_won}", 30, BLACK, WIDTH // 2 - 100, HEIGHT // 2 + 10)
        draw_text(WIN, "Press Enter to Restart", 30, BLACK, WIDTH // 2 - 150, HEIGHT // 2 + 50)
        draw_text(WIN, "Press ESC to Quit", 30, BLACK, WIDTH // 2 - 100, HEIGHT // 2 + 90)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def main():
    clock = pygame.time.Clock()

    while True:
        start_screen()  # Показываем экран начала игры

        round_num = 1
        rounds_won = 0

        while round_num <= 7:
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

            # Количество врагов теперь соответствует номеру раунда
            enemies = create_enemies(round_num, obstacles + [tank])

            # создаём экземпляр A* в которм будет хранится матрица которая описывает поле 
            astar = AStar(WIDTH, HEIGHT, Tank.size)

            # заполняем пматрицу препятствиями 
            astar.save_obstacles(obstacles)

            round_quit_flag = False
            player_lost = False  # Новый флаг для отслеживания поражения игрока

            while not round_quit_flag:
                clock.tick(60)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    tank.process_key_event(event)

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            new_bullet = Bullet(tank.rect.centerx, tank.rect.centery, tank.get_angle())
                            bullets.append(new_bullet)

                tank.move()

                if tank.check_collision(obstacles + enemies):
                    tank.stop()

                for enemy in enemies:
                    enemy.move(lambda: astar.bfs(tank, enemy))
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
                        player_lost = True  # Устанавливаем флаг поражения игрока
                        round_quit_flag = True
                        break

                if len(enemies) == 0:  # Проверяем, остались ли враги
                    round_quit_flag = True
                    rounds_won += 1  # Увеличиваем количество выигранных раундов
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

                pygame.display.update()
                clock.tick(60)

            if player_lost:  # Если игрок проиграл, показываем экран поражения
                game_over_screen("You Lost!", rounds_won)
                break

            round_num += 1  # Переходим к следующему раунду

        # Если прошли все раунды, показываем экран победы
        if round_num > 7:
            game_over_screen("You Won!", rounds_won)

if __name__ == "__main__":
    main()
