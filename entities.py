import particles
import math
import random
import pygame


class Entity(pygame.sprite.Sprite):
    group = pygame.sprite.Group()
    def __init__(self, position, width, height, speed, color, health):
        super().__init__()
        self.position = pygame.Vector2(position)
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.health = health

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=self.position)

        Entity.group.add(self)

    def explode(self):
        for _ in range(50):
            speed = random.uniform(1.0, 5.0)
            angle = random.uniform(0.0, 2 * math.pi)
            velocity = (math.cos(angle) * speed - self.speed, math.sin(angle) * speed)
            side = random.randint(5, 10)
            color = random.choice([
                (251, 191, 36),
                (249, 115, 22),
                (239, 68, 68),
                (127, 29, 29),
            ])
            particles.Explosion(
                position=self.position,
                side=side,
                velocity=velocity,
                color=color,
                lifespan=100,
            )

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.explode()
            self.kill()


class Player(Entity):
    group = pygame.sprite.Group()
    def __init__(self, position, width, height, speed, color, health):
        super().__init__(position, width, height, speed, color, health)
        self.window = pygame.display.get_surface()

        Player.group.add(self)

    def move(self):
        direction = pygame.Vector2(0, 0)

        keys = pygame.key.get_pressed()
        key_mapping = {
            pygame.K_w: (0, -1),
            pygame.K_s: (0, 1),
            pygame.K_a: (-1, 0),
            pygame.K_d: (1, 0),
        }
        for key, (dx, dy) in key_mapping.items():
            if keys[key]:
                direction.x += dx
                direction.y += dy

        if direction.length() > 0:
            direction.scale_to_length(self.speed)
            self.position += direction

        self.rect.center = self.position
        self.rect.clamp_ip(self.window.get_rect())
        self.position = pygame.Vector2(self.rect.center)


    def shoot(self):
        particles.Projectile(
            position=(self.position.x + self.width//2, self.position.y),
            width=50,
            height=5,
            velocity=(25, 0),
            color=self.color,
            target=Enemy,
            damage=10,
        )

    def update(self):
        self.move()


class Enemy(Entity):
    group = pygame.sprite.Group()
    def __init__(self, position, width, height, speed, color, health, target, damage):
        super().__init__(position, width, height, speed, color, health)
        self.target = target
        self.damage = damage
        Enemy.group.add(self)

    def collision(self):
        collisions = pygame.sprite.spritecollide(self, self.target.group, False)
        if collisions:
            for target in collisions:
                target.take_damage(self.damage)
            self.explode()
            self.kill()

    def move(self):
        self.position.x -= self.speed
        self.rect.center = self.position

    def update(self):
        self.collision()
        self.move()


class EnemySpawner:
    def __init__(self, interval, delta, minimum):
        self.interval = interval
        self.delta = delta
        self.minimum = minimum
        self.window = pygame.display.get_surface()
        self.timer = 0

    def spawn_enemy(self):
        Enemy(
            position=(self.window.get_width(), random.randint(50, self.window.get_height() - 50)),
            width=50,
            height=50,
            speed=random.randint(3, 7),
            color=(239, 68, 68),
            health=random.randint(50, 100),
            target=Player,
            damage=10,
        )

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.interval:
            self.spawn_enemy()
            self.timer = 0
            self.interval = max(self.minimum, self.interval - self.delta)
