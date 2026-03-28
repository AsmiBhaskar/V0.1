import pygame

from game_core.berserker_data import BERSERKER_SCENES, BERSERKER_TRUE_ENDING_FLAGS
from game_core.constants import BAR_COLOR, BLACK, FPS, WHITE, WINDOW_WIDTH
from game_core.storage import delete_save, save_progress
from game_core.ui import draw_centered_text, draw_left_text, draw_wrapped_block, run_info_screen


SALVATION_FLAG_LABELS = {
    "s1_salvation": "Scene 1 salvation choice",
    "s3_salvation": "Scene 3 salvation choice",
    "s5_salvation": "Scene 5 salvation choice",
    "s6_salvation": "Scene 6 salvation choice",
    "s7_salvation": "Scene 7 salvation choice",
    "s8_salvation": "Scene 8 salvation choice",
    "s9_salvation": "Scene 9 salvation choice",
}


def _clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def _adjust_state_value(state, key, delta):
    limits = {
        "rage_meter": (0, 20),
        "burning_ache": (0, 100),
        "memory_retention": (0, 10),
        "bond_atrox": (0, 10),
        "reverence_army": (0, 10),
        "saber_presence": (0, 10),
    }
    current = int(state.get(key, 0))
    updated = current + int(delta)
    if key in limits:
        low, high = limits[key]
        updated = _clamp(updated, low, high)
    state[key] = updated


def apply_burning_ache_turn(state, choice):
    # Special mechanic: every turn adds passive ache unless the turn includes
    # combat/hunting actions that feed and stabilize the fire.
    _adjust_state_value(state, "burning_ache", 5)

    if choice.get("combat_or_hunt"):
        ache_relief = int(choice.get("ache_relief", 10))
        _adjust_state_value(state, "burning_ache", -ache_relief)

    if state.get("burning_ache", 0) >= 40:
        _adjust_state_value(state, "rage_meter", 1)
        _adjust_state_value(state, "memory_retention", -1)


def apply_berserker_choice_effects(state, choice):
    apply_burning_ache_turn(state, choice)

    effects = choice.get("effects", {})
    for key, value in effects.items():
        if key == "ending":
            state[key] = value
            continue

        if isinstance(value, int):
            _adjust_state_value(state, key, value)

    flag = choice.get("flag")
    if flag:
        flags = state.setdefault("berserker_route_flags", [])
        if flag not in flags:
            flags.append(flag)


def _has_true_ending_flags(state):
    flags = set(state.get("berserker_route_flags", []))
    return BERSERKER_TRUE_ENDING_FLAGS.issubset(flags)


def _count_salvation_flag_hits(state):
    flags = set(state.get("berserker_route_flags", []))
    return len(flags.intersection(BERSERKER_TRUE_ENDING_FLAGS))


def resolve_berserker_ending(state):
    flags = set(state.get("berserker_route_flags", []))
    has_flags = _has_true_ending_flags(state)
    salvation_hits = _count_salvation_flag_hits(state)

    rage_ok = state.get("rage_meter", 0) <= 10
    memory_ok = state.get("memory_retention", 0) >= 3
    bond_ok = state.get("bond_atrox", 0) >= 4
    saber_ok = state.get("saber_presence", 0) >= 4
    final_salvation_choice = "s9_salvation" in flags

    destruction_lock = (
        "s9_destruction" in flags
        or state.get("rage_meter", 0) >= 14
        or state.get("memory_retention", 0) <= 1
    )

    near_perfect_salvation = salvation_hits >= 6 and final_salvation_choice

    if destruction_lock:
        return "BAD ENDING - CONSUMPTION"

    if (has_flags or near_perfect_salvation) and rage_ok and memory_ok and bond_ok and saber_ok:
        return "TRUE ENDING - SALVATION"
    return "BAD ENDING - CONSUMPTION"


def summarize_berserker_stats(state):
    salvation_hits = _count_salvation_flag_hits(state)
    required_flags_hit = "Yes" if _has_true_ending_flags(state) else "No"
    return [
        f"Ending: {state.get('ending', 'Unknown')}",
        f"rage_meter: {state.get('rage_meter', 0)}",
        f"burning_ache: {state.get('burning_ache', 0)}%",
        f"memory_retention: {state.get('memory_retention', 0)}",
        f"bond_atrox: {state.get('bond_atrox', 0)}",
        f"reverence_army: {state.get('reverence_army', 0)}",
        f"saber_presence: {state.get('saber_presence', 0)}",
        f"salvation flag hits: {salvation_hits}/7",
        f"required salvation flags met: {required_flags_hit}",
    ]


def build_berserker_requirements_lines(state):
    flags = set(state.get("berserker_route_flags", []))
    rage = int(state.get("rage_meter", 0))
    ache = int(state.get("burning_ache", 0))
    memory = int(state.get("memory_retention", 0))
    bond = int(state.get("bond_atrox", 0))
    saber = int(state.get("saber_presence", 0))

    rage_ok = rage <= 10
    memory_ok = memory >= 3
    bond_ok = bond >= 4
    saber_ok = saber >= 4

    salvation_hits = _count_salvation_flag_hits(state)
    strict_flags = _has_true_ending_flags(state)
    near_perfect = salvation_hits >= 6 and "s9_salvation" in flags

    destruction_lock = (
        "s9_destruction" in flags
        or rage >= 14
        or memory <= 1
    )

    missing_flags = [
        label for key, label in SALVATION_FLAG_LABELS.items() if key not in flags
    ]

    predicted_ending = resolve_berserker_ending(state)

    return [
        "Final requirement check before ending resolution:",
        f"- Rage <= 10: {'PASS' if rage_ok else 'FAIL'} (current {rage})",
        f"- Memory >= 3: {'PASS' if memory_ok else 'FAIL'} (current {memory})",
        f"- Bond Atrox >= 4: {'PASS' if bond_ok else 'FAIL'} (current {bond})",
        f"- Saber Presence >= 4: {'PASS' if saber_ok else 'FAIL'} (current {saber})",
        f"- Salvation flags: {salvation_hits}/7 ({'PASS' if strict_flags else 'Not full set'})",
        f"- Near-perfect path (6/7 + Scene 9 salvation): {'PASS' if near_perfect else 'FAIL'}",
        f"- Destruction lock: {'TRIGGERED' if destruction_lock else 'CLEAR'}",
        f"- Burning Ache: {ache}%",
        "- Missing salvation flags: " + (", ".join(missing_flags) if missing_flags else "none"),
        f"Predicted ending now: {predicted_ending}",
    ]


def run_berserker_choice_scene(screen, clock, scene, state):
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
            f"Rage {state.get('rage_meter', 0)} | "
            f"Ache {state.get('burning_ache', 0)}% | "
            f"Memory {state.get('memory_retention', 0)} | "
            f"Atrox {state.get('bond_atrox', 0)} | "
            f"Saber {state.get('saber_presence', 0)}"
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


def play_berserker_route(screen, clock, state):
    while state["scene_index"] < len(BERSERKER_SCENES):
        scene = BERSERKER_SCENES[state["scene_index"]]
        selected_index, should_quit = run_berserker_choice_scene(screen, clock, scene, state)

        if should_quit:
            return True
        if selected_index is None:
            save_progress("Berserker", state)
            return False

        selected_choice = scene["choices"][selected_index]
        apply_berserker_choice_effects(state, selected_choice)
        state["scene_index"] += 1
        save_progress("Berserker", state)

        should_quit = run_info_screen(screen, clock, "Choice Result", [selected_choice["result"]])
        if should_quit:
            return True

    should_quit = run_info_screen(
        screen,
        clock,
        "Ending Requirements Check",
        build_berserker_requirements_lines(state),
    )
    if should_quit:
        return True

    state["ending"] = resolve_berserker_ending(state)

    if state["ending"] == "TRUE ENDING - SALVATION":
        ending_lines = [
            "Heaven's Mercy reaches the fire and tears Berserker free from Bhaskar.",
            "Atrox catches him as dawn breaks and the Burning Ache finally fades.",
            "The path not taken becomes the path forward.",
        ]
        reward_lines = [
            "Unlocked: Gallery - Heaven's Mercy",
            "Unlocked: Music - The Sun Also Rises",
            "Unlocked: Epilogue - The Path Not Taken",
        ]
    else:
        ending_lines = [
            "The fire consumes the city, the war, and every hand reaching to save him.",
            "Correction collapses into pure destruction under an endless sun.",
            "The world becomes ash beneath the Burning Sun.",
        ]
        reward_lines = [
            "Unlocked: Gallery - The Burning Sun",
            "Unlocked: Music - Ash and Ember",
            "Unlocked: Epilogue - The World That Was",
        ]

    should_quit = run_info_screen(screen, clock, "Scene 10: The Ending", ending_lines)
    if should_quit:
        return True

    should_quit = run_info_screen(screen, clock, "Berserker Route Rewards", reward_lines)
    if should_quit:
        return True

    should_quit = run_info_screen(screen, clock, "Berserker Route Complete", summarize_berserker_stats(state))
    if should_quit:
        return True

    delete_save("Berserker", state=state)
    return False
