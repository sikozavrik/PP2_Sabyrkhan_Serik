from pathlib import Path
import pygame
from player import MusicPlayer

WIDTH, HEIGHT = 700, 350
FPS = 30


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Practice 09 - Music Player")
    font = pygame.font.SysFont(None, 32)
    small_font = pygame.font.SysFont(None, 24)
    clock = pygame.time.Clock()

    base_dir = Path(__file__).resolve().parent
    player = MusicPlayer(base_dir / "music")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_n:
                    player.next_track()
                elif event.key == pygame.K_b:
                    player.prev_track()
                elif event.key == pygame.K_q:
                    running = False

        # Если трек доиграл сам, обновим статус
        if player.is_playing and not pygame.mixer.music.get_busy():
            player.is_playing = False

        screen.fill((28, 30, 38))

        if not player.tracks:
            msg = font.render("No audio files in music/ folder", True, (240, 120, 120))
            screen.blit(msg, (50, 120))
        else:
            track_name = player.current_track.name
            status = "Playing" if player.is_playing else "Stopped"
            pos = player.get_position_sec()

            lines = [
                font.render(f"Track {player.index + 1}/{len(player.tracks)}: {track_name}", True, (245, 245, 245)),
                font.render(f"Status: {status} | Pos: {pos:.1f}s", True, (140, 220, 160)),
                small_font.render("[P] Play   [S] Stop   [N] Next   [B] Back   [Q] Quit", True, (190, 195, 210)),
            ]
            for i, surf in enumerate(lines):
                screen.blit(surf, (50, 60 + i * 65))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()