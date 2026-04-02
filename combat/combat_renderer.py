import pygame

from combat.combat_constants import COMBAT_BG, COMBAT_GOLD
from combat.combat_log import draw_combat_log
from combat.combat_ui import draw_action_bar, draw_combat_tracker, draw_player_status, draw_skill_submenu
from combat.enemy_panel import draw_enemy_panel

_FONTS = {}


def _font(size: int):
    if size not in _FONTS:
        _FONTS[size] = pygame.font.SysFont("consolas", size)
    return _FONTS[size]


def render_combat_frame(screen, state, title: str):
    screen.fill(COMBAT_BG)

    draw_enemy_panel(screen, state, title)
    draw_combat_log(screen, state)
    draw_combat_tracker(screen, state)

    pygame.draw.rect(screen, COMBAT_GOLD, (0, 460, 1280, 2))

    draw_player_status(screen, state)
    draw_action_bar(screen, state)
    draw_skill_submenu(screen, state)
