import particles
import pygame


pygame.init()


def main():
    window = pygame.display.set_mode((2560, 1440))
    pygame.display.set_caption("Space Invaders")

    stars = pygame.sprite.Group(particles.Star(window) for _ in range(100))

    enemies = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    clock = pygame.time.Clock()
    run: bool = True
    while run:
        window.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    projectiles.add(particles.Projectile(window, event.pos))
                elif event.button == 3:
                    explosions.add(particles.Explosion(100, event.pos) for _ in range(50))


        stars.update()
        stars.draw(window)

        projectiles.update()
        projectiles.draw(window)

        explosions.update()
        explosions.draw(window)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()