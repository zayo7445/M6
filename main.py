import particles
import entities
import spawners
import controllers
import sounds
import os
import random
import pygame


os.environ["SDL_JOYSTICK_HIDAPI_PS5_RUMBLE"] = "1"

pygame.init()


def main():
    """Main function for the game loop."""
    window = pygame.display.set_mode((1920, 1080))
    viewport = window.get_rect()
    pygame.display.set_caption("Space Invaders")

    audio = sounds.Audio()

    audio.load_music("assets/music.mp3")
    audio.play_music()

    controller = controllers.Controller()

    for _ in range(100):
        particles.Star(
            surface=window,
            position=(random.randint(0, viewport.width), random.randint(0, viewport.height)),
            velocity=(random.uniform(-7, -3), 0),
            side=random.randint(1, 5),
            color=(255, 255, 255),
        )

    player = entities.Player(
        surface=window,
        position=(viewport.width // 10, viewport.height // 2),
        speed=15,
        width=64, height=64,
        color=(59, 130, 246),
        health=100,
        image=pygame.image.load("assets/player.png").convert_alpha(),
        controller=controller,
    )
    enemies = spawners.EnemySpawner(
        surface=window,
        interval=5,
        delta=0.2,
        minimum=3,
    )
    health = spawners.HealthSpawner(
        surface=window,
        interval=15,
        delta=0,
        minimum=0,
    )

    clock = pygame.time.Clock()
    dt = 0

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if player.alive():
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:
                        player.laser()
                    elif event.button == 1:
                        player.rocket()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.laser()
                    elif event.key == pygame.K_r:
                        player.rocket()

        window.fill((0, 0, 0))

        enemies.update(dt)
        health.update(dt)

        particles.Particle.group.draw(window)
        particles.Particle.group.update(dt)

        entities.Entity.group.draw(window)
        entities.Entity.group.update(dt)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

    pygame.quit()


if __name__ == "__main__":
    main()
