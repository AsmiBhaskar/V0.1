import pygame

from game_core.constants import BAR_COLOR, BLACK, FPS, WHITE, WINDOW_HEIGHT, WINDOW_WIDTH


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

    title_font = pygame.font.SysFont("consolas", 56)
    menu_font = pygame.font.SysFont("consolas", 42)
    subtitle_font = pygame.font.SysFont("consolas", 28)
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
        draw_centered_text(screen, title_font, title, 110)
        if subtitle:
            draw_centered_text(screen, subtitle_font, subtitle, 170)

        start_y = 270
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
