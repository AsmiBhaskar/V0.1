import pygame

from combat.combat_constants import COMBAT_DIM, COMBAT_GOLD, COMBAT_LOG_MAX_LINES, COMBAT_PANEL, COMBAT_WHITE

_FONTS = {}


def _font(size: int):
    if size not in _FONTS:
        _FONTS[size] = pygame.font.SysFont("consolas", size)
    return _FONTS[size]


def draw_combat_log(surface, state, x=0, y=200, w=1280, h=260):
    panel_rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(surface, COMBAT_PANEL, panel_rect)
    pygame.draw.rect(surface, COMBAT_GOLD, panel_rect, 2)

    title_font = _font(22)
    line_font = _font(20)

    title_surf = title_font.render("COMBAT LOG", True, COMBAT_GOLD)
    surface.blit(title_surf, (x + 16, y + 10))

    lines = state.log[-COMBAT_LOG_MAX_LINES :]
    if not lines:
        lines = ["The battlefield waits."]

    text_y = y + 52
    line_height = line_font.get_linesize() + 6
    for line in lines:
        color = COMBAT_WHITE if line is lines[-1] else COMBAT_DIM
        surf = line_font.render(line, True, color)
        surface.blit(surf, (x + 16, text_y))
        text_y += line_height
