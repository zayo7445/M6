import particles
import sounds
import random
import pygame


audio = sounds.Audio.get_instance()

audio.load_sfx("laser", "assets/laser.mp3")
audio.load_sfx("rocket", "assets/rocket.mp3")
audio.load_sfx("explosion", "assets/explosion.mp3")
audio.load_sfx("dead", "assets/dead.mp3")
audio.load_sfx("heal", "assets/heal.mp3")
audio.load_sfx("damage", "assets/damage.mp3")


class Cooldown:
    """Cooldown for periodic events."""
    def __init__(self, time):
        self.cooldown = time
        self.timer = 0

    @property
    def ready(self):
        """Checks if the cooldown period has elapsed."""
        return self.timer <= 0

    def reset(self):
        """Resets the cooldown timer to the initial time."""
        self.timer = self.cooldown

    def update(self, dt):
        """Updates the cooldown timer."""
        if self.timer > 0:
            self.timer -= dt


class Entity(pygame.sprite.Sprite):
    """A base class for a rudimentary game entity."""
    group = pygame.sprite.Group()

    def __init__(self, surface, position, speed, width, height, color, health, image=None):
        super().__init__()
        if image:
            self.image = image
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill(color)

        self.rect = self.image.get_rect(center=position)

        self.surface = surface
        self.viewport = surface.get_rect()
        self.buffer = self.viewport.inflate(self.rect.width * 2, self.rect.height * 2)

        self.speed = speed
        self.color = color
        self.health = health
        self.max_health = health

        self.velocity = pygame.Vector2(0, 0)

        Entity.group.add(self)

    @property
    def visible(self):
        """Checks if the viewport and buffer area contains the entity."""
        return self.buffer.contains(self.rect)

    def move(self):
        """Moves the entity based on its velocity."""
        self.rect.move_ip(self.velocity)

    def collide(self, other):
        """Checks for collisions with another group of sprites."""
        collides = pygame.sprite.spritecollide(self, other, False)
        if collides:
            self.on_collide(collides)

    def on_collide(self, collides):
        """Called upon collision. Override in subclass."""
        pass

    def destroy(self):
        """Destroys the entity with a particle burst effect."""
        audio.play_sfx("explosion")
        particles.Burst.create(
            surface=self.surface,
            position=self.rect.center,
            num=100,
        )
        self.kill()

    def take_damage(self, damage):
        """Reduces the health of the entity by a specified amount and triggers destruction."""
        audio.play_sfx("damage")
        particles.Burst.create(
            surface=self.surface,
            position=self.rect.center,
            num=3,
            color=self.color,
        )
        self.health -= damage
        if self.health <= 0:
            self.destroy()

    def heal(self, health):
        """Restores health of the entity by a specified amount."""
        audio.play_sfx("heal")
        self.health += health
        if self.health > self.max_health:
            self.health = self.max_health

    def healthbar(self):
        """Draws a health bar below the entity if health is not full."""
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

    def update(self, dt):
        """Updates the state of the entity. Override in subclass."""
        pass


class Player(Entity):
    """A class for the player."""
    group = pygame.sprite.Group()

    def __init__(self, surface, position, speed, width, height, color, health, image=None, controller=None):
        super().__init__(surface, position, speed, width, height, color, health, image)
        self.other = Enemy.group
        self.controller = controller

        self.acceleration = 0.05 * speed
        self.friction = 0.05

        self.cooldown = {
            "laser": Cooldown(0.1),
            "rocket": Cooldown(5),
        }

        Player.group.add(self)

    def move(self):
        """Handles player movement for both keyboard and controller."""
        super().move()
        self.rect.clamp_ip(self.viewport)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.velocity.y -= self.acceleration
        if keys[pygame.K_s]:
            self.velocity.y += self.acceleration
        if keys[pygame.K_a]:
            self.velocity.x -= self.acceleration
        if keys[pygame.K_d]:
            self.velocity.x += self.acceleration

        if self.controller:
            axis_x = self.controller.get_axis(0)
            axis_y = self.controller.get_axis(1)
            self.velocity.x += axis_x * self.acceleration
            self.velocity.y += axis_y * self.acceleration

        axis_x, axis_y = 0, 0

        if not (keys[pygame.K_w] or keys[pygame.K_s] or abs(axis_y)):
            self.velocity.y *= (1 - self.friction)
        if not (keys[pygame.K_a] or keys[pygame.K_d] or abs(axis_x)):
            self.velocity.x *= (1 - self.friction)

        if self.velocity.length() > self.speed:
            self.velocity.scale_to_length(self.speed)

    def laser(self):
        """Fires a laser if the cooldown has elapsed."""
        if self.cooldown.get("laser").ready:
            audio.play_sfx("laser")
            if self.controller:
                self.controller.rumble()
            particles.Laser(
                surface=self.surface,
                position=self.rect.center,
                velocity=(25, 0),
                width=50, height=5,
                color=self.color,
                other=self.other,
                damage=15,
            )
            self.cooldown.get("laser").reset()

    def rocket(self):
        """Fires a rocket if the cooldown has elapsed."""
        if self.cooldown.get("rocket").ready:
            audio.play_sfx("rocket")
            if self.controller:
                self.controller.rumble()
            particles.Rocket(
                surface=self.surface,
                position=self.rect.center,
                velocity=(25, 0),
                width=50, height=5,
                color=self.color,
                other=self.other,
                damage=100,
            )
            self.cooldown.get("rocket").reset()

    def destroy(self):
        super().destroy()
        audio.play_sfx("dead")

    def update(self, dt):
        """Updates the state of the player."""
        self.move()
        self.healthbar()
        self.cooldown.get("laser").update(dt)
        self.cooldown.get("rocket").update(dt)


class Enemy(Entity):
    """A class for enemies."""
    group = pygame.sprite.Group()

    def __init__(self, surface, position, speed, width, height, color, health, damage, image=None):
        super().__init__(surface, position, speed, width, height, color, health, image)
        self.damage = damage
        self.other = Player.group

        self.velocity.x -= speed
        self.cooldown = {
            "laser": Cooldown(random.randint(1, 3)),
        }

        Enemy.group.add(self)

    def on_collide(self, collides):
        """Handles actions upon collision."""
        for other in collides:
            other.take_damage(self.damage)
        self.destroy()

    def laser(self):
        """Fires a laser if the cooldown has elapsed."""
        if self.cooldown.get("laser").ready:
            audio.play_sfx("laser")
            particles.Laser(
                surface=self.surface,
                position=self.rect.center,
                velocity=(-25, 0),
                width=50, height=5,
                color=self.color,
                other=self.other,
                damage=self.damage,
            )
            self.cooldown.get("laser").cooldown = random.randint(1, 3)
            self.cooldown.get("laser").reset()

    def update(self, dt):
        """Updates the state of the enemy."""
        self.move()
        self.collide(self.other)
        self.healthbar()

        self.cooldown.get("laser").update(dt)
        self.laser()

        if not self.visible:
            for other in self.other:
                other.take_damage(self.damage)
            self.kill()
