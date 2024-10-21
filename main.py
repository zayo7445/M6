import particles
import pygame
from entities import *
pygame.init()


def main():
    window = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Space Invaders")

    stars = pygame.sprite.Group(particles.Star(window) for _ in range(100))

    player = Player(position=(100, 100), width=100, height=50, speed=5, health=150)
    players = pygame.sprite.Group(player)

    enemy = Enemy(position=(1600, 500), width=50, height=40, speed=6, health=200)
    enemies = pygame.sprite.Group(enemy)

    projectiles = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    clock = pygame.time.Clock()
    run: bool = True
    while run:
        window.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pos_x = player.position.x + player.width
                    pos_y = player.position.y + player.height/2
                    projectiles.add(particles.Projectile(window, (pos_x, pos_y)))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    projectiles.add(particles.Projectile(window, event.pos))
                elif event.button == 3:
                    explosions.add(particles.Explosion(100, event.pos) for _ in range(50))

        keys = pygame.key.get_pressed()
        player.move(keys)

        stars.update()
        stars.draw(window)

        players.draw(window)
        players.update()

        enemies.draw(window)
        enemies.update()
        enemy.move()

        projectiles.update()
        projectiles.draw(window)

        explosions.update()
        explosions.draw(window)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()