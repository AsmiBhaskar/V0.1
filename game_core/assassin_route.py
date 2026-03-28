import pygame

from game_core.assassin_data import ASSASSIN_SCENES
from game_core.constants import BAR_COLOR, BLACK, FPS, WHITE, WINDOW_WIDTH
from game_core.storage import delete_save, save_progress
from game_core.ui import draw_centered_text, draw_left_text, draw_wrapped_block, run_info_screen


def apply_assassin_choice_effects(state, choice):
    effects = choice.get("effects", {})
    for key, value in effects.items():
        if key == "ending":
            state[key] = value
            continue

        current_value = state.get(key, 0)
        if isinstance(current_value, int):
            state[key] = current_value + int(value)

    flag = choice.get("flag")
    if flag:
        flags = state.setdefault("assassin_route_flags", [])
        if flag not in flags:
            flags.append(flag)


def summarize_assassin_stats(state):
    return [
        f"Ending: {state.get('ending', 'Unknown')}",
        f"information_network: {state.get('information_network', 0)}",
        f"bond_kiki: {state.get('bond_kiki', 0)}",
        f"memory_retention: {state.get('memory_retention', 0)}",
        f"reverence_binding: {state.get('reverence_binding', 0)}",
        f"hunt_progress: {state.get('hunt_progress', 0)}",
        f"flags set: {len(state.get('assassin_route_flags', []))}",
    ]


def run_assassin_choice_scene(screen, clock, scene, state):
    title_font = pygame.font.SysFont("consolas", 44)
    body_font = pygame.font.SysFont("consolas", 27)
    option_font = pygame.font.SysFont("consolas", 30)
    hint_font = pygame.font.SysFont("consolas", 22)

    choices = scene["choices"]
    selected = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(choices)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(choices)
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return selected, False
                elif event.key == pygame.K_ESCAPE:
                    return None, False

        screen.fill(BLACK)
        draw_centered_text(screen, title_font, scene["title"], 65)

        body_end_y = draw_wrapped_block(
            screen,
            body_font,
            scene["text"],
            90,
            130,
            WINDOW_WIDTH - 180,
            line_spacing=6,
        )

        stats_line = (
            f"Info {state.get('information_network', 0)} | "
            f"Kiki {state.get('bond_kiki', 0)} | "
            f"Memory {state.get('memory_retention', 0)} | "
            f"Binding {state.get('reverence_binding', 0)} | "
            f"Hunt {state.get('hunt_progress', 0)}"
        )
        draw_centered_text(screen, hint_font, stats_line, min(body_end_y + 20, 420))

        option_start_y = max(460, body_end_y + 50)
        option_spacing = 52
        bar_width = WINDOW_WIDTH - 160
        bar_height = 44

        for index, choice in enumerate(choices):
            y = option_start_y + index * option_spacing

            if index == selected:
                bar_rect = pygame.Rect(80, y - 24, bar_width, bar_height)
                pygame.draw.rect(screen, BAR_COLOR, bar_rect, border_radius=8)
                pygame.draw.rect(screen, WHITE, bar_rect, 2, border_radius=8)

            draw_left_text(screen, option_font, f"{chr(65 + index)}) {choice['label']}", 95, y - 14)

        draw_centered_text(screen, hint_font, "Arrow Keys: move  Enter: select  Esc: save and return", 690)
        pygame.display.flip()
        clock.tick(FPS)


def play_assassin_route(screen, clock, state):
    while state["scene_index"] < len(ASSASSIN_SCENES):
        scene = ASSASSIN_SCENES[state["scene_index"]]
        selected_index, should_quit = run_assassin_choice_scene(screen, clock, scene, state)

        if should_quit:
            return True
        if selected_index is None:
            save_progress("Assassin", state)
            return False

        selected_choice = scene["choices"][selected_index]
        apply_assassin_choice_effects(state, selected_choice)
        state["scene_index"] += 1
        save_progress("Assassin", state)

        should_quit = run_info_screen(screen, clock, "Choice Result", [selected_choice["result"]])
        if should_quit:
            return True

    ending = state.get("ending") or "Assassin Route Complete"
    if state.get("memory_retention", 0) <= 0:
        memory_line = "You continue the hunt as a hollow familiar under Reverence."
    else:
        memory_line = "Fragments of self endure while the hunt continues."

    aftermath_lines = [
        "Dawn rises over Bhool Bhoolaiya while Stella watches from above.",
        f"Route result: {ending}.",
        memory_line,
    ]
    should_quit = run_info_screen(screen, clock, "Scene 10: The Dawn", aftermath_lines)
    if should_quit:
        return True

    should_quit = run_info_screen(screen, clock, "Assassin Route Complete", summarize_assassin_stats(state))
    if should_quit:
        return True

    delete_save("Assassin", state=state)
    return False
