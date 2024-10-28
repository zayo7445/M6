import particles
import entities
import spawners
import random
import pygame


pygame.init()


def main():
    window = pygame.display.set_mode((1920, 1080))
    rect = window.get_rect()
    pygame.display.set_caption("Space Invaders")

    for _ in range(100):
        particles.Star(
            position=(random.randint(0, rect.width), random.randint(0, rect.height)),
            velocity=(random.uniform(-1, -5), 0),
            size=random.randint(1, 5),
            color=(255, 255, 255),
        )

    player = entities.Player((500, 500), 15, 50, 50, (59, 130, 246), 100)
    enemies = spawners.EnemySpawner(5000, 100, 3000)

    health = spawners.HealthSpawner(3e4, 0, 0)

    clock = pygame.time.Clock()
    dt = 0

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.laser()
                elif event.key == pygame.K_r:
                    player.rocket()

        window.fill((0, 0, 0))

        particles.Particle.group.draw(window)
        particles.Particle.group.update()

        entities.Entity.group.draw(window)
        entities.Entity.group.update()

        enemies.update(dt)
        health.update(dt)

        pygame.display.flip()
        dt = clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
