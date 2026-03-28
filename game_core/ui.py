import logging
from pathlib import Path

import pygame

from game_core.constants import BAR_COLOR, BLACK, FPS, WHITE, WINDOW_HEIGHT, WINDOW_WIDTH


LOGGER = logging.getLogger(__name__)
_LOGO_SURFACE = None


def _load_logo_surface():
    global _LOGO_SURFACE
    if _LOGO_SURFACE is not None:
        return _LOGO_SURFACE

    logo_svg_path = Path(__file__).resolve().parent.parent / "assets" / "new_order_logo3.svg"
    if not logo_svg_path.exists():
        LOGGER.warning("Main menu logo not found at %s", logo_svg_path)
        _LOGO_SURFACE = False
        return None

    try:
        logo_surface = pygame.image.load(str(logo_svg_path))
        if pygame.display.get_surface():
            logo_surface = logo_surface.convert_alpha()
        _LOGO_SURFACE = logo_surface
        return logo_surface
    except pygame.error as e:
        LOGGER.warning("Native pygame SVG load failed: %s", e)
        _LOGO_SURFACE = False
        return None


def _draw_main_menu_logo_background(screen):
    logo_surface = _load_logo_surface()
    # print(f"[DEBUG] surface={logo_surface}, size={logo_surface.get_size() if logo_surface else 'N/A'}")
    if not logo_surface:
        return

    logo_rect = logo_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    logo_copy = logo_surface.copy()
    logo_copy.set_alpha(255)  # very subtle watermark
    screen.blit(logo_copy, logo_rect)


def draw_centered_text(screen, font, text, y, color=WHITE):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(WINDOW_WIDTH // 2, y))
    screen.blit(surface, rect)


def draw_left_text(screen, font, text, x, y, color=WHITE):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        candidate = word if not current_line else f"{current_line} {word}"
        if font.size(candidate)[0] <= max_width:
            current_line = candidate
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def draw_wrapped_block(screen, font, lines, x, y, max_width, line_spacing=10):
    cursor_y = y
    for line in lines:
        wrapped_lines = wrap_text(line, font, max_width)
        for wrapped_line in wrapped_lines:
            draw_left_text(screen, font, wrapped_line, x, cursor_y)
            cursor_y += font.get_linesize() + line_spacing
    return cursor_y


def run_menu(screen, clock, title, options, subtitle="", start_index=0):
    if not options:
        return None, False

    title_font = pygame.font.SysFont("georgia", 62, bold=True, italic=True)
    menu_font = pygame.font.SysFont("georgia", 44, bold=True, italic=True)
    subtitle_font = pygame.font.SysFont("georgia", 30, bold=True, italic=True)
    selected = max(0, min(start_index, len(options) - 1))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return selected, False
                elif event.key == pygame.K_ESCAPE:
                    return None, False

        screen.fill(BLACK)
        _draw_main_menu_logo_background(screen)

        draw_centered_text(screen, title_font, title, 88)
        if subtitle:
            draw_centered_text(screen, subtitle_font, subtitle, 132)

        start_y = 318
        spacing = 62
        bar_width = 560
        bar_height = 52

        for index, option in enumerate(options):
            y = start_y + index * spacing

            if index == selected:
                bar_rect = pygame.Rect(0, 0, bar_width, bar_height)
                bar_rect.center = (WINDOW_WIDTH // 2, y)
                pygame.draw.rect(screen, BAR_COLOR, bar_rect, border_radius=8)
                pygame.draw.rect(screen, WHITE, bar_rect, 2, border_radius=8)

            text_surface = menu_font.render(option, True, WHITE)
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, y))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()
        clock.tick(FPS)


def run_message_screen(screen, clock, title, line1, line2=""):
    title_font = pygame.font.SysFont("consolas", 56)
    body_font = pygame.font.SysFont("consolas", 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                return False

        screen.fill(BLACK)
        draw_centered_text(screen, title_font, title, 220)
        draw_centered_text(screen, body_font, line1, 320)
        if line2:
            draw_centered_text(screen, body_font, line2, 365)
        pygame.display.flip()
        clock.tick(FPS)


def run_info_screen(screen, clock, title, lines):
    title_font = pygame.font.SysFont("consolas", 50)
    body_font = pygame.font.SysFont("consolas", 28)
    hint_font = pygame.font.SysFont("consolas", 24)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                return False

        screen.fill(BLACK)
        draw_centered_text(screen, title_font, title, 90)
        draw_wrapped_block(screen, body_font, lines, 90, 170, WINDOW_WIDTH - 180, line_spacing=8)
        draw_centered_text(screen, hint_font, "Press Enter to continue", WINDOW_HEIGHT - 40)
        pygame.display.flip()
        clock.tick(FPS)