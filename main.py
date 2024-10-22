import particles
import entities
import random
import pygame


pygame.init()


def main():
    window = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Space Invaders")

    for _ in range(100):
        particles.Star(
            position=(random.randint(0, window.get_width()), random.randint(0, window.get_height())),
            side=random.randint(1, 5),
            velocity=(random.uniform(-1.0, -3.0), 0),
            color=(255, 255, 255),
        )

    player = entities.Player(
        position=(200, window.get_height()//2),
        width=50,
        height=50,
        speed=10,
        color=(59, 130, 246),
        health=100,
    )
    enemy_spawner = entities.EnemySpawner(
        interval=5000,
        delta=100,
        minimum=1000
    )

    clock = pygame.time.Clock()
    dt = 0

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        window.fill((0, 0, 0))

        enemy_spawner.update(dt)

        particles.Particle.group.draw(window)
        particles.Particle.group.update()

        entities.Entity.group.draw(window)
        entities.Entity.group.update()

        pygame.display.flip()
        dt = clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
