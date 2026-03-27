import pygame

from game_core.archer_route import play_archer_route
from game_core.caster_route import play_caster_route
from game_core.constants import BLACK, FPS
from game_core.lancer_route import play_lancer_route
from game_core.storage import delete_save, save_progress
from game_core.ui import (
    draw_centered_text,
    run_message_screen,
    wrap_text,
)


def route_scenes(route):
    return [
        f"{route} route begins under a crimson sky.",
        "A rival appears and challenges your resolve.",
        "The final duel decides the fate of this route.",
    ]


def play_placeholder_route(screen, clock, route, state):
    title_font = pygame.font.SysFont("consolas", 52)
    scene_font = pygame.font.SysFont("consolas", 34)
    hint_font = pygame.font.SysFont("consolas", 26)
    scenes = route_scenes(route)

    scene_index = int(state.get("scene_index", 0))

    while scene_index < len(scenes):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    scene_index += 1
                    state["scene_index"] = scene_index
                    save_progress(route, state)
                elif event.key == pygame.K_ESCAPE:
                    state["scene_index"] = scene_index
                    save_progress(route, state)
                    return False

        # If Enter advanced past the last scene this frame, exit loop cleanly
        # instead of rendering with an out-of-range scene index.
        if scene_index >= len(scenes):
            break

        screen.fill(BLACK)
        draw_centered_text(screen, title_font, f"Route: {route}", 120)

        wrapped = wrap_text(scenes[scene_index], scene_font, 1040)
        y = 300
        for line in wrapped:
            draw_centered_text(screen, scene_font, line, y)
            y += 46

        draw_centered_text(screen, hint_font, "Enter: next scene", 620)
        draw_centered_text(screen, hint_font, "Esc: save and return", 655)

        pygame.display.flip()
        clock.tick(FPS)

    delete_save(route, state=state)
    return run_message_screen(
        screen,
        clock,
        "Route Complete",
        f"You completed the {route} route.",
        "Press Enter to return to menu.",
    )


def play_route(screen, clock, route, state):
    if route == "Lancer":
        return play_lancer_route(screen, clock, state)
    if route == "Archer":
        return play_archer_route(screen, clock, state)
    if route == "Caster":
        return play_caster_route(screen, clock, state)
    return play_placeholder_route(screen, clock, route, state)
