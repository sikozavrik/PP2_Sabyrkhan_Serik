import pygame
from ball import Ball

WIDTH, HEIGHT = 800, 600
FPS = 60


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Practice 09 - Moving Ball")
    clock = pygame.time.Clock()

    ball = Ball(x=WIDTH // 2, y=HEIGHT // 2, radius=25, step=20)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    ball.move(-1, 0, WIDTH, HEIGHT)
                elif event.key == pygame.K_RIGHT:
                    ball.move(1, 0, WIDTH, HEIGHT)
                elif event.key == pygame.K_UP:
                    ball.move(0, -1, WIDTH, HEIGHT)
                elif event.key == pygame.K_DOWN:
                    ball.move(0, 1, WIDTH, HEIGHT)

        screen.fill((255, 255, 255))
        ball.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()