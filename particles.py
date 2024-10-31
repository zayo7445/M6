import math
import random
import pygame


class Particle(pygame.sprite.Sprite):
    """A base class for creating particle effects."""
    group = pygame.sprite.Group()

    def __init__(self, surface, position, velocity, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=position)

        self.surface = surface
        self.viewport = surface.get_rect()
        self.buffer = self.viewport.inflate(self.rect.width * 2, self.rect.height * 2)
        self.velocity = pygame.Vector2(velocity)
        self.color = color

        Particle.group.add(self)

    @property
    def visible(self):
        """Checks if the viewport and buffer area contains the particle."""
        return self.buffer.contains(self.rect)

    def move(self):
        """Moves the particle based on its velocity."""
        self.rect.move_ip(self.velocity)

    def collide(self, other):
        """Checks for collisions with another group of sprites."""
        collides = pygame.sprite.spritecollide(self, other, False)
        if collides:
            self.on_collide(collides)

    def on_collide(self, collides):
        """Called upon collision. Override in subclass."""
        pass

    def update(self, dt):
        """Updates the state of the entity. Override in subclass."""
        pass


class Burst(Particle):
    """A class for creating burst particle effects."""
    group = pygame.sprite.Group()

    def __init__(self, surface, position, velocity, side, color, lifespan):
        super().__init__(surface, position, velocity, side, side, color)
        self.side = side
        self.lifespan = lifespan
        self.life = lifespan

        Burst.group.add(self)

    @classmethod
    def create(cls, surface, position, num, **kwargs):
        """A class method to create a default burst effect."""
        for _ in range(num):
            speed = random.uniform(1, 5)
            angle = random.uniform(0, 2 * math.pi)
            props = {
                "surface": surface,
                "position": position,
                "velocity": (speed * math.cos(angle), speed * math.sin(angle)),
                "side": random.randint(5, 10),
                "color": random.choice([
                    (251, 191, 36),
                    (249, 115, 22),
                    (239, 68, 68),
                    (127, 29, 29),
                ]),
                "lifespan": 100,
            }
            if kwargs:
                props.update(kwargs)
            cls(**props)

    def move(self):
        """Moves the particle based on its velocity with random movements."""
        super().move()
        self.velocity += (random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))

    def decay(self):
        """Reduces the life of the particle."""
        self.life -= 1
        if self.life <= 0:
            self.kill()

    def transform(self):
        """Scales the particle down and updates position."""
        side = self.side * (self.life / self.lifespan)
        self.image = pygame.transform.scale(self.image, (side, side))
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, dt):
        """Updates the state of the entity."""
        self.move()
        self.decay()
        self.transform()
        if not self.visible:
            self.kill()


class Projectile(Particle):
    """A class for creating projectiles."""
    group = pygame.sprite.Group()

    def __init__(self, surface, position, velocity, width, height, color, damage, other):
        super().__init__(surface, position, velocity, width, height, color)
        self.damage = damage
        self.other = other

        Projectile.group.add(self)

    def on_collide(self, collides):
        """Called upon collision."""
        for other in collides:
            other.take_damage(self.damage)
        self.kill()

    def update(self, dt):
        """Updates the state of the projectile."""
        self.move()
        self.collide(self.other)
        if not self.visible:
            self.kill()


class Laser(Projectile):
    """A class for creating laser projectiles."""
    def __init__(self, surface, position, velocity, width, height, color, damage, other):
        super().__init__(surface, position, velocity, width, height, color, damage, other)


class Rocket(Projectile):
    """A class for creating rocket projectiles."""
    def __init__(self, surface, position, velocity, width, height, color, damage, other):
        super().__init__(surface, position, velocity, width, height, color, damage, other)

    def on_collide(self, collides):
        """Called upon collision. Creates a burst particle effect."""
        super().on_collide(collides)
        Burst.create(
            surface=self.surface,
            position=(self.rect.left, self.rect.centery),
            num=1000,
        )

    def update(self, dt):
        """Updates the state of the rocket projectile. Creates a trail effect."""
        super().update(dt)
        Burst.create(
            surface=self.surface,
            position=(self.rect.left, self.rect.centery),
            num=5,
        )


class Star(Particle):
    """A class for creating a star particle. Used for starry background with parallax effect."""
    group = pygame.sprite.Group()

    def __init__(self, surface, position, velocity, side, color):
        super().__init__(surface, position, velocity, side, side, color)

    def move(self):
        """Moves the star from right to left and repositions on the right side when they exit the viewport"""
        super().move()
        if not self.visible:
            self.rect.left = self.viewport.width

    def update(self, dt):
        """Updates the state of the star particle."""
        self.move()


class Health(Particle):
    """A health particle that restores health to entities upon collision."""
    group = pygame.sprite.Group()

    def __init__(self, surface, position, velocity, side, color, health, other):
        super().__init__(surface, position, velocity, side, side, color)
        self.health = health
        self.other = other

        Health.group.add(self)

    def on_collide(self, collides):
        """Heals collided entities and creates a small burst effect on collection."""
        for other in collides:
            other.heal(self.health)
        self.kill()
        Burst.create(
            surface=self.surface,
            position=(self.rect.left, self.rect.centery),
            num=10,
            color=self.color,
        )

    def update(self, dt):
        """Updates the state of the health particle."""
        self.move()
        self.collide(self.other)
        if not self.visible:
            self.kill()
