import pygame


class Ball:
    def __init__(self, x: int, y: int, radius: int = 25, step: int = 20):
        self.x = x
        self.y = y
        self.radius = radius
        self.step = step
        self.color = (220, 30, 30)

    def move(self, dx: int, dy: int, screen_width: int, screen_height: int) -> None:
        new_x = self.x + dx * self.step
        new_y = self.y + dy * self.step

        # Игнорируем ход, если шар выходит за границы окна
        if new_x - self.radius < 0 or new_x + self.radius > screen_width:
            return
        if new_y - self.radius < 0 or new_y + self.radius > screen_height:
            return

        self.x = new_x
        self.y = new_y

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)