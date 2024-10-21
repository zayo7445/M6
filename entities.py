import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, position, width, height, speed, health):
        super().__init__()
        self.position = pygame.Vector2(position)
        self.width = width
        self.height = height
        self.speed = speed
        self.health = health

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=self.position)

    def update(self):
        self.rect = self.position


class Enemy(Entity):
    def init(self, position, width, height, speed, health):
        super().init(position, width, height, speed, health)
        self.image.fill((255, 255, 255))

    def create(self):
        help


class Player(Entity):
    def init(self, position, width, height, speed, health):
        super().init(position, width, height, speed, health)
        self.image.fill((255, 255, 255))

    def move(self, keys):
        if keys[pygame.K_w] and self.position.y > 0:
            self.position.y -= self.speed
        if keys[pygame.K_s] and self.position.y < 1080 - self.height:
            self.position.y += self.speed
        if keys[pygame.K_d] and self.position.x < 1920 - self.width:
            self.position.x += self.speed
        if keys[pygame.K_a] and self.position.x > 0:
            self.position.x -= self.speed
