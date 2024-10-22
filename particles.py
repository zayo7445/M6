import pygame


class Particle(pygame.sprite.Sprite):
    group = pygame.sprite.Group()
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

        Particle.group.add(self)

    def update(self):
        self.position += self.velocity
        self.rect.center = self.position


class Projectile(Particle):
    group = pygame.sprite.Group()
    def __init__(self, position, width, height, velocity, color, target, damage):
        super().__init__(position, width, height, velocity, color)
        self.target = target
        self.damage = damage
        self.window = pygame.display.get_surface()

        Projectile.group.add(self)

    def collision(self):
        collisions = pygame.sprite.spritecollide(self, self.target.group, False)
        if collisions:
            for target in collisions:
                target.take_damage(self.damage)
            self.kill()

    def update(self):
        super().update()
        self.collision()
        if self.position.x >= self.window.get_width():
            self.kill()


class Explosion(Particle):
    group = pygame.sprite.Group()
    def __init__(self, position, side, velocity, color, lifespan):
        super().__init__(position, side, side, velocity, color)
        self.lifespan = lifespan
        self.init_lifespan = lifespan
        self.init_side = side

        Explosion.group.add(self)

    def update(self):
        super().update()
        side = self.init_side * (self.lifespan / self.init_lifespan)
        self.image = pygame.transform.scale(self.image, (side, side))

        self.lifespan -= 1
        if self.lifespan <= 0:
            self.kill()


class Star(Particle):
    group = pygame.sprite.Group()
    def __init__(self, position, side, velocity, color):
        super().__init__(position, side, side, velocity, color)
        self.window = pygame.display.get_surface()

        Star.group.add(self)

    def update(self):
        super().update()
        if self.position.x <= 0:
            self.position.x = self.window.get_width()
