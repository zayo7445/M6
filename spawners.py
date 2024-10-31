import entities
import particles
import random
import pygame


class Spawner:
    """A base class to spawn objects."""
    def __init__(self, surface, interval, delta, minimum):
        """Initialize a Spawner instance."""
        self.surface = surface
        self.viewport = surface.get_rect()
        self.interval = interval
        self.delta = delta
        self.minimum = minimum
        self.timer = 0

    def spawn(self):
        """Spawns the object. Override in subclass."""
        pass

    def update(self, dt):
        """Updates the spawner, triggering a spawn if the interval has elapsed and decreases the interval."""
        self.timer += dt
        if self.timer >= self.interval:
            self.spawn()
            self.timer = 0
            if self.delta > 0:
                self.interval = max(self.minimum, self.interval - self.delta)


class HealthSpawner(Spawner):
    """A class for spawning health particles at regular intervals."""
    def __init__(self, surface, interval, delta, minimum):
        super().__init__(surface, interval, delta, minimum)

    def spawn(self):
        """Spawns a health particle with random health value."""
        particles.Health(
            surface=self.surface,
            position=(self.viewport.width, random.randint(10, self.viewport.height - 10)),
            velocity=(random.uniform(-7, -3), 0),
            side=20,
            color=(34, 197, 94),
            health=random.randint(25, 75),
            other=entities.Player.group,
        )


class EnemySpawner(Spawner):
    """A class for spawning enemies at regular intervals."""
    def __init__(self, surface, interval, delta, minimum):
        super().__init__(surface, interval, delta, minimum)

        self.images = {
            "red": pygame.image.load("assets/enemy_red.png"),
            "yellow": pygame.image.load("assets/enemy_yellow.png"),
            "green": pygame.image.load("assets/enemy_green.png")
        }

        self.types = [
            {
                "image": self.images.get("red"),
                "color": (239, 68, 68),
                "speed": 7,
                "health": 100,
                "damage": 12,
            },
            {
                "image": self.images.get("yellow"),
                "color": (251, 191, 36),
                "speed": 5,
                "health": 75,
                "damage": 10,
            },
            {
                "image": self.images.get("green"),
                "color": (34, 197, 94),
                "speed": 3,
                "health": 50,
                "damage": 8,
            },
        ]

    def spawn(self):
        props = random.choice(self.types)
        entities.Enemy(
            surface=self.surface,
            position=(self.viewport.width, random.randint(25, self.viewport.height - 25)),
            width=50, height=50,
            **props
        )

