import random
import pygame


from bullet import Bullet_enemy



class Tank:

    size = (50, 50)
    image = 'tank.png'

    def __init__(self, x, y):
        self.original_image = pygame.image.load(self.image).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel = 5
        self.angle = 0
        self.direction = None
        self.speed_x = 0
        self.speed_y = 0


    def draw(self, window):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        window.blit(rotated_image, rotated_rect)

    def move(self):
        self.speed_x = 0
        self.speed_y = 0
        if self.direction == "up":
            self.speed_y = -self.vel
            self.angle = 90
        elif self.direction == "down":
            self.speed_y = self.vel
            self.angle = 270
        elif self.direction == "left":
            self.speed_x = -self.vel
            self.angle = 180
        elif self.direction == "right":
            self.speed_x = self.vel
            self.angle = 0
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def process_key_event(self, event):
        if event.type == pygame.KEYDOWN:
            if not self.direction:
                if event.key == pygame.K_UP:
                    self.direction = "up"
                elif event.key == pygame.K_DOWN:
                    self.direction = "down"
                elif event.key == pygame.K_LEFT:
                    self.direction = "left"
                elif event.key == pygame.K_RIGHT:
                    self.direction = "right"
            else:
                if event.key == pygame.K_UP:
                    self.direction = "up"
                elif event.key == pygame.K_DOWN:
                    self.direction = "down"
                elif event.key == pygame.K_LEFT:
                    self.direction = "left"
                elif event.key == pygame.K_RIGHT:
                    self.direction = "right"
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP and self.direction == "up":
                self.direction = None
            elif event.key == pygame.K_DOWN and self.direction == "down":
                self.direction = None
            elif event.key == pygame.K_LEFT and self.direction == "left":
                self.direction = None
            elif event.key == pygame.K_RIGHT and self.direction == "right":
                self.direction = None

    def get_angle(self):
        return self.angle

    def check_collision(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                return True
        return False
    
    def center(self):
        return self.rect.center
    
    def stop(self):
        self.rect.x -= self.speed_x
        self.rect.y -= self.speed_y



class EnemyTank(Tank):

    size = (50, 50)
    image = 'Enemy_tank.png'
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.target = None
        self.change_interval = 400
        self.last_change_time = pygame.time.get_ticks() - 500000005
        self.last_shot_time = pygame.time.get_ticks()
        self.shot_interval = 500

    def move(self, lambda_bfs):
        directions = ["up", "down", "left", "right"]
        current_time = pygame.time.get_ticks()

        if current_time - self.last_change_time > self.change_interval:
            self.direction = lambda_bfs()
            self.last_change_time = current_time  # Обновляем время последнего изменения
        super().move()
       

    def check_collision(self, obstacles):
        return super().check_collision([i for i in obstacles if i != self])
    
    def check_kill(self, tank, obstacles):
        speed_cors = [self.speed_y, self.speed_x]
        if sum(speed_cors) == 0:
            return False
        cors_tank = list(tank.rect.center)
        cors_self = list(self.rect.center)
        # astar = lambda : astar.check_kill(speed_cors, cors_self, cors_tank)
        if speed_cors[0] > speed_cors[1]:
            speed_cors.reverse()
            cors_tank.reverse()
            cors_self.reverse()
        speed = speed_cors[1]
        if abs(cors_tank[0] - cors_self[0]) * 2 > tank.rect.width:
            return False
        if (cors_tank[1] > cors_self[1])  == (speed > 0):
            bullet = Bullet_enemy(self.rect.centerx, self.rect.centery, self.angle)
            count_ = 0
            while not bullet.check_collision(obstacles, []):
                count_ += 1
                if count_ > 1000:
                    break
                if bullet.check_collision([], [tank]):
                    return True
                bullet.move()
            return False
            
    def check_shot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shot_interval:
            self.last_shot_time = current_time  # Обновляем время последнего изменения
            return True
        return False
