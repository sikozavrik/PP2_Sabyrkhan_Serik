from collections import deque
import pygame


class PaintCanvas:
    def __init__(self, width: int, height: int, bg_color=(255, 255, 255)):
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.surface = pygame.Surface((width, height))
        self.surface.fill(bg_color)

    def draw_pencil(self, start: tuple[int, int], end: tuple[int, int], color, thickness: int) -> None:
        pygame.draw.line(self.surface, color, start, end, thickness)

    def draw_line(self, start: tuple[int, int], end: tuple[int, int], color, thickness: int) -> None:
        pygame.draw.line(self.surface, color, start, end, thickness)

    def draw_line_preview(
        self, target: pygame.Surface, start: tuple[int, int], end: tuple[int, int], color, thickness: int
    ) -> None:
        pygame.draw.line(target, color, start, end, thickness)

    def flood_fill(self, x: int, y: int, new_color: tuple[int, int, int]) -> None:
        if not (0 <= x < self.width and 0 <= y < self.height):
            return

        target_color = self.surface.get_at((x, y))[:3]
        new_rgb = new_color[:3]
        if target_color == new_rgb:
            return

        queue = deque([(x, y)])
        visited = {(x, y)}

        while queue:
            cx, cy = queue.popleft()
            if self.surface.get_at((cx, cy))[:3] != target_color:
                continue

            self.surface.set_at((cx, cy), new_rgb)

            for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))

    def draw_text(self, pos: tuple[int, int], text: str, color, font: pygame.font.Font) -> None:
        if not text:
            return
        img = font.render(text, True, color)
        self.surface.blit(img, pos)