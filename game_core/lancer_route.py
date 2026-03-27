import pygame

from game_core.constants import BAR_COLOR, BLACK, FPS, WHITE, WINDOW_WIDTH
from game_core.lancer_data import LANCER_SCENES
from game_core.storage import delete_save, save_progress
from game_core.ui import draw_centered_text, draw_left_text, draw_wrapped_block, run_info_screen


def apply_lancer_choice_effects(state, choice):
    effects = choice.get("effects", {})
    for key, value in effects.items():
        if key == "ending":
            state["ending"] = value
            continue

        current_value = state.get(key, 0)
        if isinstance(current_value, int):
            state[key] = current_value + int(value)

    flag = choice.get("flag")
    if flag:
        flags = state.setdefault("lancer_route_flags", [])
        if flag not in flags:
            flags.append(flag)


def summarize_lancer_stats(state):
    return [
        f"Ending: {state.get('ending', 'Unknown')}",
        f"bond_atrox: {state.get('bond_atrox', 0)}",
        f"bond_kitik: {state.get('bond_kitik', 0)}",
        f"understanding_bhaskar: {state.get('understanding_bhaskar', 0)}",
        f"zuxi_readiness: {state.get('zuxi_readiness', 0)}",
        f"team_synergy: {state.get('team_synergy', 0)}",
        f"flags set: {len(state.get('lancer_route_flags', []))}",
    ]


def run_lancer_choice_scene(screen, clock, scene, state):
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
            f"Atrox {state.get('bond_atrox', 0)} | "
            f"Kitik {state.get('bond_kitik', 0)} | "
            f"Bhaskar {state.get('understanding_bhaskar', 0)} | "
            f"Zuxi {state.get('zuxi_readiness', 0)} | "
            f"Synergy {state.get('team_synergy', 0)}"
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


def play_lancer_route(screen, clock, state):
    while state["scene_index"] < len(LANCER_SCENES):
        scene = LANCER_SCENES[state["scene_index"]]
        selected_index, should_quit = run_lancer_choice_scene(screen, clock, scene, state)

        if should_quit:
            return True
        if selected_index is None:
            save_progress("Lancer", state)
            return False

        selected_choice = scene["choices"][selected_index]
        apply_lancer_choice_effects(state, selected_choice)
        state["scene_index"] += 1
        save_progress("Lancer", state)

        should_quit = run_info_screen(screen, clock, "Choice Result", [selected_choice["result"]])
        if should_quit:
            return True

    ending = state.get("ending") or "Unfinished"
    aftermath_lines = [
        "Dawn returns over Lucknow after Bhool Bhoolaiya.",
        f"Route result: {ending}.",
        "The Grail war continues beyond this point.",
    ]
    should_quit = run_info_screen(screen, clock, "Scene 10: Aftermath", aftermath_lines)
    if should_quit:
        return True

    should_quit = run_info_screen(screen, clock, "Lancer Route Complete", summarize_lancer_stats(state))
    if should_quit:
        return True

    delete_save("Lancer")
    return False
