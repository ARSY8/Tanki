import pygame
import threading
import time

# Игровые настройки
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Игровые объекты
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

# Игровая логика
def game_loop():
    # Инициализация Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pygame Game")
    clock = pygame.time.Clock()

    # Создание игровых объектов
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Игровой цикл
    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Обновление игровых объектов
        all_sprites.update()

        # Запуск отрисовки в отдельном потоке
        draw_thread = threading.Thread(target=draw_game, args=(screen, all_sprites))
        draw_thread.start()
        draw_thread.join()

        # Ограничение частоты кадров
        clock.tick(FPS)

    # Завершение Pygame
    pygame.quit()

def draw_game(screen, all_sprites):
    # Очистка экрана
    screen.fill((255, 255, 255))

    # Отрисовка игровых объектов
    all_sprites.draw(screen)

    # Обновление экрана
    pygame.display.flip()

# Запуск игры в отдельном потоке
game_thread = threading.Thread(target=game_loop)
game_thread.start()

