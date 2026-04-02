import pygame

from combat.combat_constants import (
    ACTIONS,
    ACTION_ACT,
    ACTION_BLOCK,
    ACTION_DODGE,
    ACTION_ITEM,
    ACTION_NP,
    BAR_BG_COLOR,
    BAR_BORDER,
    COMBAT_DIM,
    COMBAT_GOLD,
    COMBAT_PANEL,
    COMBAT_SELECTED,
    COMBAT_WHITE,
    EXHAUSTION_THRESHOLD,
    HP_BAR_COLOR,
    MANA_BAR_COLOR,
    SP_COST_BLOCK,
    SP_BAR_COLOR,
)

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


def _wrap_text(font, text: str, max_width: int, max_lines: int = 2) -> list[str]:
    words = text.split()
    if not words:
        return [""]

    lines: list[str] = []
    current = words[0]

    for word in words[1:]:
        candidate = f"{current} {word}"
        if font.size(candidate)[0] <= max_width:
            current = candidate
            continue

        lines.append(current)
        current = word
        if len(lines) >= max_lines:
            break

    if len(lines) < max_lines:
        lines.append(current)

    if len(lines) > max_lines:
        lines = lines[:max_lines]

    if len(lines) == max_lines and font.size(lines[-1])[0] > max_width:
        lines[-1] = _fit_text(font, lines[-1], max_width)

    return lines


def draw_resource_bar(surface, label, current, maximum, color, x, y, w=260, h=18):
    font = _font(18)
    pygame.draw.rect(surface, BAR_BG_COLOR, (x, y, w, h))
    fill_w = int(w * (current / maximum)) if maximum > 0 else 0
    pygame.draw.rect(surface, color, (x, y, fill_w, h))
    pygame.draw.rect(surface, BAR_BORDER, (x, y, w, h), 1)

    text = f"{label:<4} {current:>5} / {maximum}"
    surface.blit(font.render(text, True, COMBAT_WHITE), (x + w + 12, y - 2))


def draw_player_status(surface, state):
    x, y, w, h = 0, 462, 640, 130
    panel_rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(surface, COMBAT_PANEL, panel_rect)
    pygame.draw.rect(surface, COMBAT_GOLD, panel_rect, 2)

    header_font = _font(22, bold=True)
    surface.blit(header_font.render(state.player.name, True, COMBAT_GOLD), (16, y + 8))

    hp_color = HP_BAR_COLOR
    sp_color = SP_BAR_COLOR
    mana_color = MANA_BAR_COLOR

    ticks = pygame.time.get_ticks()
    if state.player.sp < EXHAUSTION_THRESHOLD and ticks % 800 < 400:
        sp_color = (220, 60, 60)

    if state.player.mana < int(state.player.mana_max * 0.1) and ticks % 1000 < 500:
        mana_color = (110, 150, 255)

    draw_resource_bar(surface, "HP", state.player.hp, state.player.hp_max, hp_color, 18, y + 42)
    draw_resource_bar(surface, "SP", state.player.sp, state.player.sp_max, sp_color, 18, y + 72)
    draw_resource_bar(surface, "MANA", state.player.mana, state.player.mana_max, mana_color, 18, y + 102)


def _button_enabled(state, action: str):
    if state.phase in ("enemy_attack", "dodge_phase"):
        return action == ACTION_DODGE

    if state.phase != "player_action":
        return False

    if action == ACTION_NP:
        return bool(state.player.np_item)

    if action == ACTION_ACT:
        return len(state.player.actives) > 0

    if action == ACTION_ITEM:
        return len(state.context_flags.get("inventory", [])) > 0

    if action == ACTION_BLOCK and state.player.sp < SP_COST_BLOCK:
        return False

    return True


def draw_action_bar(surface, state):
    x, y, w, h = 640, 462, 640, 130
    panel_rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(surface, COMBAT_PANEL, panel_rect)
    pygame.draw.rect(surface, COMBAT_GOLD, panel_rect, 2)

    label_font = _font(22, bold=True)
    key_font = _font(16)

    selected = int(state.context_flags.get("action_index", 0))
    button_w = max(1, w // max(1, len(ACTIONS)))

    key_hint = {
        "FIGHT": "F",
        "ACT": "A",
        "ITEM": "I",
        "NOBLE PHANTASM": "N",
        "DODGE": "D",
        "BLOCK": "B",
    }

    for i, action in enumerate(ACTIONS):
        btn_x = x + i * button_w
        btn_width = button_w if i < (len(ACTIONS) - 1) else (x + w - btn_x)
        btn_rect = pygame.Rect(btn_x, y, btn_width, h)
        enabled = _button_enabled(state, action)

        if i == selected and state.phase == "player_action" and not state.context_flags.get("submenu_open", False):
            pygame.draw.rect(surface, COMBAT_SELECTED, btn_rect)
            pygame.draw.rect(surface, COMBAT_GOLD, btn_rect, 2)

        text_color = COMBAT_WHITE if enabled else COMBAT_DIM
        label = "NP" if action == ACTION_NP else action
        label_surf = label_font.render(label, True, text_color)
        label_rect = label_surf.get_rect(center=(btn_rect.centerx, y + 52))
        surface.blit(label_surf, label_rect)

        hint_surf = key_font.render(key_hint.get(action, "?"), True, text_color)
        hint_rect = hint_surf.get_rect(center=(btn_rect.centerx, y + 95))
        surface.blit(hint_surf, hint_rect)


def draw_skill_submenu(surface, state):
    x, y, w, h = 0, 592, 1280, 128
    panel_rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(surface, COMBAT_PANEL, panel_rect)
    pygame.draw.rect(surface, COMBAT_GOLD, panel_rect, 2)

    title_font = _font(20, bold=True)
    body_font = _font(18)

    submenu_open = bool(state.context_flags.get("submenu_open", False))
    options = state.context_flags.get("submenu_options", [])
    selected = int(state.context_flags.get("submenu_index", 0))

    if not submenu_open or not options:
        help_text = "Enter: confirm action  |  Arrows: navigate  |  Esc: cancel"
        if state.phase == "dodge_phase":
            help_text = "Space/Enter: attempt dodge  |  Esc: take the hit"
        help_text = _fit_text(body_font, help_text, w - 48)
        surface.blit(body_font.render(help_text, True, COMBAT_DIM), (24, y + 52))
        return

    title = state.context_flags.get("submenu_title", "SUBMENU")
    title = _fit_text(title_font, title, w - 48)
    surface.blit(title_font.render(title, True, COMBAT_GOLD), (24, y + 8))

    # Render a sliding window so long menus remain navigable and in-bounds.
    visible_rows = 4
    row_height = 22
    row_start_y = y + 34
    row_x = 18
    row_w = w - 36

    if selected >= len(options):
        selected = len(options) - 1
        state.context_flags["submenu_index"] = selected

    if len(options) <= visible_rows:
        start_index = 0
    else:
        max_start = len(options) - visible_rows
        start_index = min(max(selected - (visible_rows // 2), 0), max_start)

    visible_options = options[start_index : start_index + visible_rows]
    for offset, option in enumerate(visible_options):
        option_index = start_index + offset
        row_y = row_start_y + (offset * row_height)
        is_selected = option_index == selected
        text = _fit_text(body_font, option.get("label", "-"), row_w - 18)
        color = COMBAT_WHITE if is_selected else COMBAT_DIM

        if is_selected:
            pygame.draw.rect(surface, COMBAT_SELECTED, (row_x, row_y - 2, row_w, row_height))
            pygame.draw.rect(surface, COMBAT_GOLD, (row_x, row_y - 2, row_w, row_height), 1)

        surface.blit(body_font.render(text, True, color), (row_x + 8, row_y))

    if start_index > 0:
        surface.blit(body_font.render("^ more", True, COMBAT_DIM), (w - 96, y + 10))

    if start_index + visible_rows < len(options):
        surface.blit(body_font.render("v more", True, COMBAT_DIM), (w - 96, y + h - 24))


def draw_combat_tracker(surface, state, x=850, y=208, w=414, h=244):
    panel_rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(surface, COMBAT_PANEL, panel_rect)
    pygame.draw.rect(surface, COMBAT_GOLD, panel_rect, 2)

    title_font = _font(18, bold=True)
    line_font = _font(14)
    sub_font = _font(13)

    title = _fit_text(title_font, "TURN SKILL LOG", w - 18)
    surface.blit(title_font.render(title, True, COMBAT_GOLD), (x + 9, y + 8))

    np_current = int(state.context_flags.get("player_np", 0))
    summary_text = _fit_text(sub_font, f"NP {np_current}/100  |  Logs update each completed turn", w - 18)
    surface.blit(sub_font.render(summary_text, True, COMBAT_DIM), (x + 9, y + 28))

    tracker_log = state.context_flags.get("turn_skill_cooldown_log", [])
    current_action = state.context_flags.get("turn_action_label") or "none"

    if not tracker_log:
        hint = "No turn snapshots yet. Complete a turn to log skill and cooldown state."
        for idx, line in enumerate(_wrap_text(sub_font, hint, w - 18, max_lines=3)):
            surface.blit(sub_font.render(line, True, COMBAT_DIM), (x + 9, y + 56 + (idx * 16)))

        pending = _fit_text(sub_font, f"Current action: {current_action}", w - 18)
        surface.blit(sub_font.render(pending, True, COMBAT_WHITE), (x + 9, y + h - 20))
        return

    row_y = y + 50
    row_limit = y + h - 10
    shown = 0

    for entry in reversed(tracker_log):
        action_line = _fit_text(line_font, f"T{int(entry.get('turn', 0)):02d}  Action: {entry.get('action', 'No skill')}", w - 18)
        cd_lines = _wrap_text(sub_font, f"CD  {entry.get('cooldowns', 'No skills')}", w - 18, max_lines=2)
        fx_lines = _wrap_text(sub_font, f"FX  {entry.get('effects', 'none')}", w - 18, max_lines=1)

        needed_height = 16 + (len(cd_lines) * 15) + (len(fx_lines) * 15) + 6
        if row_y + needed_height > row_limit:
            break

        surface.blit(line_font.render(action_line, True, COMBAT_GOLD), (x + 9, row_y))
        row_y += 16

        for line in cd_lines:
            surface.blit(sub_font.render(line, True, COMBAT_WHITE), (x + 9, row_y))
            row_y += 15

        for line in fx_lines:
            surface.blit(sub_font.render(line, True, COMBAT_DIM), (x + 9, row_y))
            row_y += 15

        row_y += 6
        shown += 1

    hidden = len(tracker_log) - shown
    if hidden > 0:
        more_text = _fit_text(sub_font, f"+{hidden} older turn logs", w - 18)
        surface.blit(sub_font.render(more_text, True, COMBAT_DIM), (x + 9, y + h - 20))
