import pygame

from tools import SHAPES, draw_shape, flood_fill, save_canvas

WIDTH, HEIGHT, TOP = 1000, 700, 84  # TOP = height of the toolbar
WHITE = (255, 255, 255)
SIZES = [2, 5, 10]  # small / medium / large brush (keys 1 / 2 / 3)

COLORS = [(25, 25, 28), (226, 60, 60), (244, 140, 40), (250, 204, 50), (52, 168, 83),
          (32, 178, 170), (52, 110, 230), (142, 84, 214), (236, 100, 170), (139, 92, 58)]

COLOR_KEYS = list("qwyuioghjk")  # hotkey of every color above, in the same order

# (tool, button text, hotkey)
TOOLS = [("pencil", "Pencil", "p"), ("line", "Line", "l"), ("rect", "Rect", "r"),
         ("square", "Square", "s"), ("circle", "Circle", "c"), ("right_triangle", "R-Triangle", "a"),
         ("equilateral_triangle", "Triangle", "e"), ("rhombus", "Rhombus", "d"),
         ("eraser", "Eraser", "x"), ("fill", "Fill", "f"), ("text", "Text", "t")]
TOOL_KEYS = {key: name for name, _, key in TOOLS}  # {"p": "pencil", "l": "line", ...}

# Button rectangles
tool_rects = [pygame.Rect(10 + i * 90, 8, 84, 30) for i in range(len(TOOLS))]
size_rects = [pygame.Rect(10 + i * 56, 46, 50, 28) for i in range(len(SIZES))]
color_rects = [pygame.Rect(200 + i * 34, 46, 28, 28) for i in range(len(COLORS))]


def button(screen, font, rect, label, active, key=""):
    pygame.draw.rect(screen, (82, 136, 255) if active else (70, 75, 90), rect, border_radius=8)
    img = font.render(label, True, WHITE)
    screen.blit(img, img.get_rect(center=rect.center))
    if key:  # small hotkey letter in the corner
        screen.blit(font.render(key.upper(), True, (170, 178, 195)), (rect.x + 5, rect.y + 2))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS 2 - Extended Paint")
    clock = pygame.time.Clock()
    ui_font = pygame.font.SysFont("arial", 16)
    text_font = pygame.font.SysFont("arial", 30)

    canvas = pygame.Surface((WIDTH, HEIGHT - TOP))  # the paper
    canvas.fill(WHITE)

    tool, size, color = "pencil", SIZES[0], COLORS[0]
    drawing, start, last = False, None, None  # mouse is held on the canvas
    typing, text, text_pos = False, "", (0, 0)  # text tool
    message, message_until = "", 0

    def to_canvas(pos):  # window coordinates -> canvas coordinates
        return pos[0], max(pos[1] - TOP, 0)

    def pen():  # eraser = white and 3x thicker
        return (WHITE, size * 3) if tool == "eraser" else (color, size)

    running = True
    while running:
        clock.tick(60)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:  # Ctrl+S
                    message = "Saved: " + save_canvas(canvas)
                    message_until = pygame.time.get_ticks() + 3000
                elif typing:
                    if e.key == pygame.K_RETURN:  # confirm: text goes onto the canvas
                        canvas.blit(text_font.render(text, True, color), text_pos)
                        typing = False
                    elif e.key == pygame.K_ESCAPE:  # cancel
                        typing = False
                    elif e.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif e.unicode.isprintable():
                        text += e.unicode
                elif e.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    size = SIZES[e.key - pygame.K_1]
                elif not drawing:
                    name = pygame.key.name(e.key)  # "p", "q", ...
                    if name in TOOL_KEYS:  # P, L, R, S, ... -> tool
                        tool = TOOL_KEYS[name]
                    elif name in COLOR_KEYS:  # Q, W, Y, ... -> color
                        color = COLORS[COLOR_KEYS.index(name)]

            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if e.pos[1] < TOP:  # click on the toolbar
                    for (name, _, _), rect in zip(TOOLS, tool_rects):
                        if rect.collidepoint(e.pos):
                            tool, typing = name, False
                    for s, rect in zip(SIZES, size_rects):
                        if rect.collidepoint(e.pos):
                            size = s
                    for c, rect in zip(COLORS, color_rects):
                        if rect.collidepoint(e.pos):
                            color = c
                else:  # click on the canvas
                    pos = to_canvas(e.pos)
                    if tool == "fill":
                        flood_fill(canvas, pos[0], pos[1], color)
                    elif tool == "text":
                        typing, text, text_pos = True, "", pos
                    else:
                        drawing, start, last = True, pos, pos
                        if tool in ("pencil", "eraser"):
                            draw_shape(canvas, "line", pos, pos, *pen())  # one click = one dot

            elif e.type == pygame.MOUSEMOTION and drawing and tool in ("pencil", "eraser"):
                pos = to_canvas(e.pos)
                draw_shape(canvas, "line", last, pos, *pen())  # tiny line between mouse positions
                last = pos

            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                if drawing and tool in SHAPES:  # line / shape is finished
                    draw_shape(canvas, tool, start, to_canvas(e.pos), color, size)
                drawing = False

        # ---- draw everything ----
        view = canvas.copy()  # canvas + temporary things
        if drawing and tool in SHAPES:  # live preview while dragging
            draw_shape(view, tool, start, to_canvas(pygame.mouse.get_pos()), color, size)
        if typing:  # text that is being typed
            view.blit(text_font.render(text + "|", True, color), text_pos)

        screen.fill((40, 44, 54))
        screen.blit(view, (0, TOP))

        for (name, label, key), rect in zip(TOOLS, tool_rects):
            button(screen, ui_font, rect, label, tool == name, key)
        for s, rect in zip(SIZES, size_rects):
            button(screen, ui_font, rect, f"{s}px", size == s)
        for c, rect, key in zip(COLORS, color_rects, COLOR_KEYS):
            pygame.draw.rect(screen, c, rect, border_radius=6)
            letter = ui_font.render(key.upper(), True, (0, 0, 0) if sum(c) > 450 else WHITE)
            screen.blit(letter, letter.get_rect(center=rect.center))
            if c == color:
                pygame.draw.rect(screen, WHITE, rect, 3, border_radius=6)

        showing = pygame.time.get_ticks() < message_until
        hint = message if showing else "Ctrl+S: save   |   1 2 3: size   |   letters: tools, colors"
        img = ui_font.render(hint, True, (120, 224, 150) if showing else (150, 157, 170))
        screen.blit(img, (WIDTH - img.get_width() - 12, 52))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
