import pygame
import math


class Bullet:
    def __init__(self, x, y, angle):
        self.original_image = pygame.image.load('пуля3.png').convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (5, 5))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel = 10
        self.angle = angle
        self.dx = self.vel * math.cos(math.radians(angle))
        self.dy = -self.vel * math.sin(math.radians(angle))

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self, window):
        window.blit(self.image, self.rect)

    def check_collision(self, obstacles, enemies):
        for obstacle in obstacles:
            if obstacle.color != (85, 170, 255):  # BLUE
                if self.rect.colliderect(obstacle.rect):
                    self.dx = 0
                    self.dy = 0
                    return True
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemies.remove(enemy)
                return True

        return False

class Bullet_enemy(Bullet):
    pass


