import math
from datetime import datetime
from pathlib import Path

import pygame

# Tools that are drawn by dragging from point a to point b
SHAPES = ("line", "rect", "square", "circle", "right_triangle", "equilateral_triangle", "rhombus")


def draw_shape(surf, tool, a, b, color, size):
    """Draw one shape from point a to point b. `size` is the brush thickness."""
    (x1, y1), (x2, y2) = a, b
    if tool == "line":
        pygame.draw.line(surf, color, a, b, size)
        pygame.draw.circle(surf, color, a, size // 2)  # round ends, no gaps
        pygame.draw.circle(surf, color, b, size // 2)
    elif tool == "rect":
        pygame.draw.rect(surf, color, (min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1)), size)
    elif tool == "square":
        side = max(abs(x2 - x1), abs(y2 - y1))
        x = x1 if x2 >= x1 else x1 - side
        y = y1 if y2 >= y1 else y1 - side
        pygame.draw.rect(surf, color, (x, y, side, side), size)
    elif tool == "circle":  # drag from the centre outwards
        r = int(math.hypot(x2 - x1, y2 - y1))
        pygame.draw.circle(surf, color, a, r, min(size, r))
    elif tool == "right_triangle":  # right angle at (x1, y2)
        pygame.draw.polygon(surf, color, [(x1, y1), (x1, y2), (x2, y2)], size)
    elif tool == "equilateral_triangle":  # base from a, tip goes up or down with the drag
        h = int(abs(x2 - x1) * math.sqrt(3) / 2)
        tip_y = y1 + h if y2 >= y1 else y1 - h
        pygame.draw.polygon(surf, color, [(x1, y1), (x2, y1), ((x1 + x2) // 2, tip_y)], size)
    elif tool == "rhombus":
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        pygame.draw.polygon(surf, color, [(cx, y1), (x2, cy), (cx, y2), (x1, cy)], size)


def flood_fill(surf, x, y, color):
    """Fill the area under (x, y) with `color`. Stops at pixels of another color."""
    old = surf.get_at((x, y))[:3]
    if old == color:
        return
    w, h = surf.get_size()
    surf.set_at((x, y), color)
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
            if 0 <= nx < w and 0 <= ny < h and surf.get_at((nx, ny))[:3] == old:
                surf.set_at((nx, ny), color)  # paint right away = no "visited" list needed
                stack.append((nx, ny))


def save_canvas(surf):
    """Save as paint_YYYYMMDD_HHMMSS.png next to this file. Returns the file name."""
    path = Path(__file__).parent / f"paint_{datetime.now():%Y%m%d_%H%M%S}.png"
    pygame.image.save(surf, str(path))
    return path.name
