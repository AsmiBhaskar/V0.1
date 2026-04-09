import pygame

from combat.data.combat_constants import COMBAT_DIM, COMBAT_GOLD, COMBAT_LOG_MAX_LINES, COMBAT_PANEL, COMBAT_WHITE

_FONTS = {}


def _font(size: int):
    if size not in _FONTS:
        _FONTS[size] = pygame.font.SysFont("consolas", size)
    return _FONTS[size]


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
    words = str(text).split()
    if not words:
        return [""]

    lines: list[str] = []
    current = words[0]

    # Handle a very long first token that cannot fit on one line.
    if font.size(current)[0] > max_width:
        current = _fit_text(font, current, max_width)

    for word in words[1:]:
        token = word
        if font.size(token)[0] > max_width:
            token = _fit_text(font, token, max_width)

        candidate = f"{current} {token}"
        if font.size(candidate)[0] <= max_width:
            current = candidate
            continue

        lines.append(current)
        current = token
        if len(lines) >= max_lines:
            break

    if len(lines) < max_lines:
        lines.append(current)

    if len(lines) > max_lines:
        lines = lines[:max_lines]

    # If text still overflows max_lines, keep last line within width with ellipsis.
    if len(lines) == max_lines:
        lines[-1] = _fit_text(font, lines[-1], max_width)

    return lines


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

    content_rect = pygame.Rect(x + 16, y + 52, w - 32, h - 64)
    text_y = content_rect.y
    line_height = line_font.get_linesize() + 6
    entry_gap = 2
    previous_clip = surface.get_clip()
    surface.set_clip(content_rect)

    for line in lines:
        color = COMBAT_WHITE if line is lines[-1] else COMBAT_DIM
        wrapped_lines = _wrap_text(line_font, str(line), content_rect.width, max_lines=2)

        for segment in wrapped_lines:
            if text_y + line_height > content_rect.bottom:
                surface.set_clip(previous_clip)
                return

            surf = line_font.render(segment, True, color)
            surface.blit(surf, (content_rect.x, text_y))
            text_y += line_height

        text_y += entry_gap

    surface.set_clip(previous_clip)

