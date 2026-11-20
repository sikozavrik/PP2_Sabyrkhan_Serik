from pathlib import Path
import pygame
from clock import MickeyClock

WIDTH, HEIGHT = 600, 620
FPS = 10  # Достаточно для обновления каждую секунду и плавного движения стрелок


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Practice 09 - Mickey's Clock")
    clock_fps = pygame.time.Clock()

    base_dir = Path(__file__).resolve().parent
    hand_path = base_dir / "images" / "mickey_hand.png"
    mickey_clock = MickeyClock(center=(WIDTH // 2, 270), hand_image_path=hand_path)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((220, 225, 235))
        mickey_clock.draw(screen)
        pygame.display.flip()
        clock_fps.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()