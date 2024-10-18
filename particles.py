import math
import random
import pygame


class Particle(pygame.sprite.Sprite):
    def __init__(self, position, width, height, velocity, color):
        super().__init__()
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.width = width
        self.height = height
        self.color = color

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=self.position)

    def update(self):
        self.position += self.velocity
        self.rect.center = self.position


class Projectile(Particle):
    def __init__(self, surface, position):
        velocity: tuple = (25, 0)
        width: int = 50
        height: int = 5
        color: tuple = (37, 99, 235)
        super().__init__(position, width, height, velocity, color)
        self.surface = surface

    def update(self):
        super().update()
        if self.position.x >= self.surface.get_width():
            self.kill()


class Explosion(Particle):
    def __init__(self, lifespan, position):
        speed = random.uniform(1.0, 5.0)
        angle = random.uniform(0.0, 2 * math.pi)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        velocity = (vx, vy)
        width = random.randint(5, 10)
        height = width
        color = random.choice([
            (251, 191, 36),
            (249, 115, 22),
            (239, 68, 68),
            (127, 29, 29),
        ])
        super().__init__(position, width, height, velocity, color)
        self.lifespan = lifespan

    def update(self):
        super().update()
        self.width = max(0.0, self.width - 0.1)
        self.height = self.width
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.lifespan -= 1
        if self.lifespan <= 0:
            self.kill()


class Star(Particle):
    def __init__(self, surface):
        position = (random.randint(0, surface.get_width()), random.randint(0, surface.get_height()))
        velocity = (random.uniform(-1.0, -3.0), 0)
        width = random.randint(1, 5)
        height = width
        color = (255, 255, 255)
        super().__init__(position, width, height, velocity, color)
        self.surface = surface

    def update(self):
        super().update()
        if self.position.x <= 0:
            self.position.x = self.surface.get_width()



