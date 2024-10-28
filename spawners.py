import particles
import entities
import random
import pygame


class Spawner:
    def __init__(self, interval, delta, minimum):
        self.interval = interval
        self.delta = delta
        self.minimum = minimum
        self.timer = 0

        self.surface = pygame.display.get_surface()

    def spawn(self):
        """Override in subclass"""
        pass

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.interval:
            self.spawn()
            self.timer = 0
            if self.delta > 0:
                self.interval = max(self.minimum, self.interval - self.delta)


class HealthSpawner(Spawner):
    def __init__(self, interval, delta, minimum):
        super().__init__(interval, delta, minimum)

    def spawn(self):
        particles.Health(
            position=(self.surface.get_width(), random.randint(10, self.surface.get_height() - 10)),
            velocity=(random.uniform(-7, -3), 0),
            size=20,
            color=(34, 197, 94),
            other=entities.Player.group,
            health=random.randint(25,75),
        )


class EnemySpawner(Spawner):
    def __init__(self, interval, delta, minimum):
        super().__init__(interval, delta, minimum)

    def spawn(self):
        entities.Enemy(
            position=(self.surface.get_width(), random.randint(25, self.surface.get_height() - 25)),
            speed=random.uniform(3, 7),
            width=50, height=50,
            color=(239, 68, 68),
            health=random.randint(50, 100),
            other=entities.Player.group,
            damage=10,
        )