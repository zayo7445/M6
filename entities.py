import pygame
import random


class Entity(pygame.sprite.Sprite):
    def __init__(self, position, width, height, speed, health):
        super().__init__()
        self.position = pygame.Vector2(position)
        self.width = width
        self.height = height
        self.speed = speed
        self.health = health
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(center=self.position)

    def update(self):
        self.rect.center = self.position

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()


class Enemy(Entity):
    def __init__(self, position, width, height, speed, health):
        super().__init__(position, width, height, speed, health)
        self.image.fill((255, 255, 255))

    def move(self):
        self.position.x -= self.speed

    def collision(self, player):
        return self.rect.colliderect(player.rect)


class Player(Entity):
    def __init__(self, position, width, height, speed, health):
        super().__init__(position, width, height, speed, health)
        self.image.fill((52, 235, 229))

    def move(self, keys):
        if keys[pygame.K_w] and self.position.y > 0:  # Move Upwards
            self.position.y -= self.speed
        if keys[pygame.K_s] and self.position.y < 1080 - self.height:  # Move Downwards
            self.position.y += self.speed
        if keys[pygame.K_d] and self.position.x < 1920 - self.width:  # Move Right
            self.position.x += self.speed
        if keys[pygame.K_a] and self.position.x > 0:  # Move Left
            self.position.x -= self.speed
