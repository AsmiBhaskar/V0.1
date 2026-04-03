import pygame

from combat.data.combat_constants import BAR_BG_COLOR, BAR_BORDER, COMBAT_GOLD, COMBAT_PANEL, COMBAT_WHITE, HP_BAR_COLOR

_FONTS = {}


def _font(size: int, bold: bool = False):
    key = (size, bold)
    if key not in _FONTS:
        _FONTS[key] = pygame.font.SysFont("consolas", size, bold=bold)
    return _FONTS[key]


def _fit_text(font, text: str, max_width: int) -> str:
    if font.size(text)[0] <= max_width:
        return text

    suffix = "..."
    for i in range(len(text), 0, -1):
        candidate = text[:i].rstrip() + suffix
        if font.size(candidate)[0] <= max_width:
            return candidate
    return suffix


def _draw_hp_bar(surface, current: int, maximum: int, x: int, y: int, w: int, h: int):
    pygame.draw.rect(surface, BAR_BG_COLOR, (x, y, w, h))
    fill_w = int(w * (current / maximum)) if maximum > 0 else 0
    pygame.draw.rect(surface, HP_BAR_COLOR, (x, y, fill_w, h))
    pygame.draw.rect(surface, BAR_BORDER, (x, y, w, h), 1)


def draw_enemy_panel(surface, state, title: str):
    x, y, w, h = 0, 0, 1280, 200
    panel_rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(surface, COMBAT_PANEL, panel_rect)
    pygame.draw.rect(surface, COMBAT_GOLD, panel_rect, 2)

    title_font = _font(24, bold=True)
    enemy_font = _font(44, bold=True)
    class_font = _font(22)
    hp_font = _font(20)
    right_margin = x + w - 18

    title_text = _fit_text(title_font, title, w - 40)
    title_surf = title_font.render(title_text, True, COMBAT_GOLD)
    surface.blit(title_surf, (20, 14))

    name_surf = enemy_font.render(state.enemy.name, True, COMBAT_GOLD)
    surface.blit(name_surf, (20, 56))

    class_text = f"Class: {state.enemy.servant_class}"
    class_surf = class_font.render(class_text, True, COMBAT_WHITE)
    surface.blit(class_surf, (24, 110))

    hp_label = _fit_text(hp_font, f"HP  {state.enemy.hp} / {state.enemy.hp_max}", 220)
    hp_surf = hp_font.render(hp_label, True, COMBAT_WHITE)
    hp_rect = hp_surf.get_rect(midright=(right_margin, 128))

    bar_left = 350
    bar_right = hp_rect.left - 16
    bar_width = max(220, bar_right - bar_left)
    _draw_hp_bar(surface, state.enemy.hp, state.enemy.hp_max, bar_left, 116, bar_width, 24)
    surface.blit(hp_surf, hp_rect)

    turn_text = hp_font.render(f"TURN {state.turn + 1}", True, COMBAT_WHITE)
    turn_rect = turn_text.get_rect(topright=(right_margin, 18))
    surface.blit(turn_text, turn_rect)

