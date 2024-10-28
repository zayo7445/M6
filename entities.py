import particles
import math
import random
import pygame


class Entity(pygame.sprite.Sprite):
    group = pygame.sprite.Group()

    def __init__(self, position, speed, width, height, color, health):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(center=position)
        self.image.fill(color)

        self.velocity = pygame.Vector2(0, 0)
        self.speed = speed
        self.color = color
        self.health = health
        self.max_health = health

        self.surface = pygame.display.get_surface()

        Entity.group.add(self)

    def visible(self):
        return self.surface.get_rect().contains(self.rect)

    def collide(self, other):
        collides = pygame.sprite.spritecollide(self, other, False)
        if collides:
            self.on_collide(collides)

    def on_collide(self, collides):
        """Override in subclass"""
        pass

    def destroy(self):
        for _ in range(100):
            speed = random.uniform(1, 5)
            angle = random.uniform(0, 2 * math.pi)
            velocity = speed * math.cos(angle), speed * math.sin(angle)
            size = random.randint(5, 10)
            color = random.choice([
                (251, 191, 36),
                (249, 115, 22),
                (239, 68, 68),
                (127, 29, 29),
            ])
            particles.Burst(self.rect.center, velocity, size, color, 100)
        self.kill()

    def heal(self, health):
        self.health += health
        if self.health > self.max_health:
            self.health = self.max_health

    def take_damage(self, damage):
        for _ in range(3):
            speed = random.uniform(1, 5)
            angle = random.uniform(0, 2 * math.pi)
            velocity = speed * math.cos(angle), speed * math.sin(angle)
            size = random.randint(5, 10)
            color = self.color
            particles.Burst(self.rect.center, velocity, size, color, 100)
        self.health -= damage
        if self.health <= 0:
            self.destroy()

    def healthbar(self):
        if self.health < self.max_health:
            pygame.draw.rect(
                self.surface,
                (239, 68, 68),
                (self.rect.x, self.rect.bottom + 5, self.rect.width, 5),
            )
            pygame.draw.rect(
                self.surface,
                (34, 197, 94),
                (self.rect.x, self.rect.bottom + 5, self.rect.width * (self.health / self.max_health), 5),
            )

    def move(self):
        """Override in subclass"""
        pass

    def update(self):
        """Override in subclass"""
        pass


class Player(Entity):
    group = pygame.sprite.Group()

    def __init__(self, position, speed, width, height, color, health):
        super().__init__(position, speed, width, height, color, health)
        self.acceleration = 0.05 * speed
        self.friction = 0.05

        Player.group.add(self)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]: self.velocity.y -= self.acceleration
        if keys[pygame.K_s]: self.velocity.y += self.acceleration
        if keys[pygame.K_a]: self.velocity.x -= self.acceleration
        if keys[pygame.K_d]: self.velocity.x += self.acceleration

        if not (keys[pygame.K_w] or keys[pygame.K_s]):
            self.velocity.y *= (1 - self.friction)
        if not (keys[pygame.K_a] or keys[pygame.K_d]):
            self.velocity.x *= (1 - self.friction)

        if self.velocity.length() > self.speed:
            self.velocity.scale_to_length(self.speed)

        self.rect.move_ip(self.velocity)
        self.rect.clamp_ip(self.surface.get_rect())

    def laser(self):
        particles.Laser(
            position=(self.rect.right, self.rect.centery),
            velocity=(25, 0),
            width=50, height=5,
            color=self.color,
            other=Enemy.group,
            damage=10,
        )

    def rocket(self):
        particles.Rocket(
            position=(self.rect.right, self.rect.centery),
            velocity=(25, 0),
            width=50, height=5,
            color=self.color,
            other=Enemy.group,
            damage=1000,
        )

    def update(self):
        self.move()
        self.healthbar()


class Enemy(Entity):
    group = pygame.sprite.Group()

    def __init__(self, position, speed, width, height, color, health, other, damage):
        super().__init__(position, speed, width, height, color, health)
        self.other = other
        self.damage = damage
        self.velocity.x -= speed
        self.timer = random.randint(60, 180)

        Enemy.group.add(self)

    def move(self):
        self.rect.move_ip(self.velocity)

    def on_collide(self, collides):
        for other in collides:
            other.take_damage(self.damage)
        self.destroy()

    def laser(self):
        particles.Laser(
            position=(self.rect.left, self.rect.centery),
            velocity=(-25, 0),
            width=50, height=5,
            color=self.color,
            other=Player.group,
            damage=10,
        )

    def update(self):
        self.move()
        self.healthbar()
        self.collide(self.other)

        if self.timer <= 0:
            self.laser()
            self.timer = random.randint(60, 180)
        else:
            self.timer -= 1






