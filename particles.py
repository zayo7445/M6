import math
import random
import pygame


class Particle(pygame.sprite.Sprite):
    group = pygame.sprite.Group()

    def __init__(self, position, velocity, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(center=position)
        self.image.fill(color)

        self.velocity = pygame.Vector2(velocity)
        self.color = color

        self.surface = pygame.display.get_surface()

        Particle.group.add(self)

    def move(self):
        self.rect.move_ip(self.velocity)

    def visible(self):
        return self.surface.get_rect().contains(self.rect)

    def collide(self, other):
        collides = pygame.sprite.spritecollide(self, other, False)
        if collides:
            self.on_collide(collides)

    def on_collide(self, collides):
        """Override in subclass"""
        pass

    def update(self):
        """Override in subclass"""
        pass


class Burst(Particle):
    group = pygame.sprite.Group()

    def __init__(self, position, velocity, size, color, lifespan):
        super().__init__(position, velocity, size, size, color)
        self.size = size
        self.lifespan = lifespan
        self.life = lifespan

        Burst.group.add(self)

    def resize(self):
        size = self.size * (self.life / self.lifespan)
        self.image = pygame.transform.scale(self.image, (size, size))

    def move(self):
        super().move()
        self.velocity += (random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))

    def update(self):
        self.move()
        self.resize()
        self.life -= 1
        if self.life <= 0 or not self.visible():
            self.kill()


class Projectile(Particle):
    group = pygame.sprite.Group()

    def __init__(self, position, velocity, width, height, color, other, damage):
        super().__init__(position, velocity, width, height, color)
        self.other = other
        self.damage = damage

        Projectile.group.add(self)

    def on_collide(self, collides):
        for other in collides:
            other.take_damage(self.damage)
            self.kill()

    def update(self):
        self.move()
        self.collide(self.other)
        if not self.visible():
            self.kill()


class Laser(Projectile):
    def __init__(self, position, velocity, width, height, color, other, damage):
        super().__init__(position, velocity, width, height, color, other, damage)


class Rocket(Projectile):
    def __init__(self, position, velocity, width, height, color, other, damage):
        super().__init__(position, velocity, width, height, color, other, damage)

    def propel(self):
        for _ in range(3):
            speed = random.uniform(1, 5)
            angle = random.uniform(0, 2 * math.pi)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            Burst(
                position=(self.rect.left, self.rect.centery),
                velocity=velocity,
                size=random.randint(5, 10),
                color=random.choice([
                    (251, 191, 36),
                    (249, 115, 22),
                    (239, 68, 68),
                    (127, 29, 29),
                ]),
                lifespan=100,
            )

    def on_collide(self, collides):
        super().on_collide(collides)
        for _ in range(500):
            speed = random.uniform(1, 5)
            angle = random.uniform(0, 2 * math.pi)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            Burst(
                position=self.rect.center,
                velocity=velocity,
                size=random.randint(5, 10),
                color=random.choice([
                    (251, 191, 36),
                    (249, 115, 22),
                    (239, 68, 68),
                    (127, 29, 29),
                ]),
                lifespan=100,
            )

    def update(self):
        super().update()
        self.propel()


class Star(Particle):
    group = pygame.sprite.Group()

    def __init__(self, position, velocity, size, color):
        super().__init__(position, velocity, size, size, color)

    def update(self):
        self.move()
        if self.rect.right <= 0:
            self.rect.left = self.surface.get_rect().width


class Health(Particle):
    def __init__(self, position, velocity, size, color, other, health):
        super().__init__(position, velocity, size, size, color)
        self.other = other
        self.health = health

    def burst(self):
        for _ in range(10):
            speed = random.uniform(1, 5)
            angle = random.uniform(0, 2 * math.pi)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            Burst(
                position=self.rect.center,
                velocity=velocity,
                size=random.randint(5, 10),
                color=self.color,
                lifespan=100,
            )

    def on_collide(self, collides):
        for other in collides:
            self.burst()
            other.heal(self.health)
            self.kill()

    def update(self):
        self.move()
        self.collide(self.other)

