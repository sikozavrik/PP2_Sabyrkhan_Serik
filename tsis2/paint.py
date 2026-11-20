from datetime import datetime
from pathlib import Path
import pygame
from tools import PaintCanvas

WIDTH, HEIGHT = 1000, 700
TOP_BAR_HEIGHT = 60
FPS = 60

COLORS = [
    ("Black", (20, 20, 20)),
    ("Red", (220, 35, 35)),
    ("Green", (30, 160, 70)),
    ("Blue", (35, 95, 220)),
    ("Yellow", (235, 195, 30)),
]

BRUSH_SIZES = [2, 5, 10]


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS 2 - Extended Paint")
    clock = pygame.time.Clock()

    ui_font = pygame.font.SysFont(None, 24)
    text_font = pygame.font.SysFont(None, 32)

    canvas = PaintCanvas(width=WIDTH, height=HEIGHT - TOP_BAR_HEIGHT)

    tool = "pencil"  # "pencil" | "line" | "fill" | "text"
    color_idx = 0
    thickness_idx = 0

    drawing = False
    line_start: tuple[int, int] | None = None
    last_pos: tuple[int, int] | None = None

    typing_mode = False
    text_pos: tuple[int, int] | None = None
    current_text = ""

    save_message = ""
    save_timer = 0.0

    def to_canvas_pos(pos: tuple[int, int]) -> tuple[int, int]:
        return pos[0], pos[1] - TOP_BAR_HEIGHT

    def save_image() -> None:
        nonlocal save_message, save_timer
        out_dir = Path(__file__).resolve().parent / "exports"
        out_dir.mkdir(exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = out_dir / f"paint_{stamp}.png"
        pygame.image.save(canvas.surface, str(out_path))
        save_message = f"Saved: {out_path.name}"
        save_timer = 3.0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        if save_timer > 0:
            save_timer = max(0.0, save_timer - dt)
            if save_timer == 0.0:
                save_message = ""

        current_color = COLORS[color_idx][1]
        current_thickness = BRUSH_SIZES[thickness_idx]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                mods = pygame.key.get_mods()

                # Сохранение по Ctrl + S
                if event.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                    save_image()
                    continue

                # Режим ввода текста
                if typing_mode:
                    if event.key == pygame.K_RETURN:
                        if text_pos is not None:
                            canvas.draw_text(text_pos, current_text, current_color, text_font)
                        typing_mode = False
                        current_text = ""
                        text_pos = None
                    elif event.key == pygame.K_ESCAPE:
                        typing_mode = False
                        current_text = ""
                        text_pos = None
                    elif event.key == pygame.K_BACKSPACE:
                        current_text = current_text[:-1]
                    else:
                        if event.unicode and event.unicode.isprintable():
                            current_text += event.unicode
                    continue

                # Выбор инструмента
                if event.key == pygame.K_1:
                    tool = "pencil"
                elif event.key == pygame.K_2:
                    tool = "line"
                elif event.key == pygame.K_3:
                    tool = "fill"
                elif event.key == pygame.K_4:
                    tool = "text"

                # Выбор толщины кисти (2 / 5 / 10 px)
                elif event.key == pygame.K_z:
                    thickness_idx = 0
                elif event.key == pygame.K_x:
                    thickness_idx = 1
                elif event.key == pygame.K_c:
                    thickness_idx = 2

                # Быстрый выбор цвета (Q/W/E/R/T)
                elif event.key == pygame.K_q:
                    color_idx = 0
                elif event.key == pygame.K_w:
                    color_idx = 1
                elif event.key == pygame.K_e:
                    color_idx = 2
                elif event.key == pygame.K_r:
                    color_idx = 3
                elif event.key == pygame.K_t:
                    color_idx = 4

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if my < TOP_BAR_HEIGHT:
                    # Клик по палитре цветов на верхней панели
                    for i, (_, col) in enumerate(COLORS):
                        rect = pygame.Rect(420 + i * 32, 16, 26, 26)
                        if rect.collidepoint(mx, my):
                            color_idx = i
                            break
                    continue

                cpos = to_canvas_pos((mx, my))

                if tool == "pencil":
                    drawing = True
                    last_pos = cpos
                    canvas.draw_pencil(cpos, cpos, current_color, current_thickness)

                elif tool == "line":
                    drawing = True
                    line_start = cpos

                elif tool == "fill":
                    canvas.flood_fill(cpos[0], cpos[1], current_color)

                elif tool == "text":
                    typing_mode = True
                    text_pos = cpos
                    current_text = ""

            elif event.type == pygame.MOUSEMOTION:
                if drawing and tool == "pencil" and last_pos is not None:
                    mx, my = event.pos
                    cpos = to_canvas_pos((mx, max(TOP_BAR_HEIGHT, my)))
                    canvas.draw_pencil(last_pos, cpos, current_color, current_thickness)
                    last_pos = cpos

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if drawing and tool == "line" and line_start is not None:
                    mx, my = event.pos
                    cpos = to_canvas_pos((mx, max(TOP_BAR_HEIGHT, my)))
                    canvas.draw_line(line_start, cpos, current_color, current_thickness)
                drawing = False
                line_start = None
                last_pos = None

        # Отрисовка экрана
        screen.fill((235, 238, 244))
        screen.blit(canvas.surface, (0, TOP_BAR_HEIGHT))

        # Превью линии во время перетаскивания
        if drawing and tool == "line" and line_start is not None:
            mx, my = pygame.mouse.get_pos()
            cpos = to_canvas_pos((mx, max(TOP_BAR_HEIGHT, my)))
            preview_surf = screen.subsurface((0, TOP_BAR_HEIGHT, WIDTH, HEIGHT - TOP_BAR_HEIGHT))
            canvas.draw_line_preview(preview_surf, line_start, cpos, current_color, current_thickness)

        # Превью набираемого текста
        if typing_mode and text_pos is not None:
            preview_txt = text_font.render(current_text + "|", True, current_color)
            screen.blit(preview_txt, (text_pos[0], text_pos[1] + TOP_BAR_HEIGHT))

        # Верхняя панель инструментов
        pygame.draw.rect(screen, (40, 44, 52), (0, 0, WIDTH, TOP_BAR_HEIGHT))

        info_text = (
            f"[1]Pencil [2]Line [3]Fill [4]Text | "
            f"Size:{current_thickness}px (Z/X/C) | Colors(Q-T):"
        )
        screen.blit(ui_font.render(info_text, True, (240, 240, 240)), (12, 20))

        for i, (_, col) in enumerate(COLORS):
            rect = pygame.Rect(420 + i * 32, 16, 26, 26)
            pygame.draw.rect(screen, col, rect)
            border_col = (255, 255, 255) if i == color_idx else (15, 15, 15)
            pygame.draw.rect(screen, border_col, rect, 2)

        right_hint = save_message if save_message else "Ctrl+S: Save"
        right_col = (130, 235, 150) if save_message else (190, 200, 215)
        right_surf = ui_font.render(right_hint, True, right_col)
        screen.blit(right_surf, (WIDTH - right_surf.get_width() - 15, 20))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()