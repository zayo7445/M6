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





