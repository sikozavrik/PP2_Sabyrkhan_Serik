from datetime import datetime
from pathlib import Path
import pygame


class MickeyClock:
    def __init__(self, center: tuple[int, int], hand_image_path: Path):
        self.center = center
        raw_hand = pygame.image.load(str(hand_image_path)).convert_alpha()

        # Правая рука = минуты, левая рука = секунды
        self.minute_hand = pygame.transform.smoothscale(raw_hand, (70, 170))
        self.second_hand = pygame.transform.smoothscale(
            pygame.transform.flip(raw_hand, True, False), (55, 210)
        )

    @staticmethod
    def get_angles() -> tuple[float, float, int, int]:
        now = datetime.now()
        minute = now.minute % 60
        second = now.second % 60

        # Положительный угол в Pygame поворачивает против часовой стрелки
        minute_angle = -((minute + second / 60.0) * 6.0)
        second_angle = -(second * 6.0)
        return minute_angle, second_angle, minute, second

    def draw(self, surface: pygame.Surface) -> None:
        minute_angle, second_angle, minute, second = self.get_angles()

        # Циферблат
        pygame.draw.circle(surface, (245, 245, 245), self.center, 230)
        pygame.draw.circle(surface, (30, 30, 35), self.center, 230, 4)

        # Минутная стрелка (правая рука)
        rot_min = pygame.transform.rotate(self.minute_hand, minute_angle)
        rect_min = rot_min.get_rect(center=self.center)
        surface.blit(rot_min, rect_min)

        # Секундная стрелка (левая рука)
        rot_sec = pygame.transform.rotate(self.second_hand, second_angle)
        rect_sec = rot_sec.get_rect(center=self.center)
        surface.blit(rot_sec, rect_sec)

        # Центральная точка
        pygame.draw.circle(surface, (20, 20, 20), self.center, 8)

        # Цифровое отображение минут и секунд
        font = pygame.font.SysFont(None, 36)
        label = font.render(f"{minute:02d}:{second:02d}", True, (20, 20, 20))
        surface.blit(label, label.get_rect(center=(self.center[0], self.center[1] + 265)))