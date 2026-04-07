import pygame
from combat.core.combat_engine import run_combat
from combat.core.encounter_table import ENCOUNTERS

from game_core.constants import BAR_COLOR, BLACK, FPS, WHITE, WINDOW_WIDTH
from game_core.archer_data import ARCHER_SCENES
from game_core.storage import delete_save, save_progress
from game_core.ui import draw_centered_text, draw_left_text, draw_wrapped_block, run_info_screen


ARCHER_BERSERKER_OPENING_GATE_INDEX = 2
ARCHER_LANCER_TRAINING_GATE_INDEX = 6
ARCHER_BERSERKER_FINAL_GATE_INDEX = 8


def apply_archer_choice_effects(state, choice):
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
        flags = state.setdefault("archer_route_flags", [])
        if flag not in flags:
            flags.append(flag)


def summarize_archer_stats(state):
    return [
        f"Ending: {state.get('ending', 'Unknown')}",
        f"bond_girlfriend: {state.get('bond_girlfriend', 0)}",
        f"bond_atrox: {state.get('bond_atrox', 0)}",
        f"humility_pride: {state.get('humility_pride', 0)}",
        f"grand_verdict_readiness: {state.get('grand_verdict_readiness', 0)}",
        f"seen_heard: {state.get('seen_heard', 0)}",
        f"opening_loss_recorded: {state.get('archer_opening_berserker_done', False)}",
        f"training_lancer_won: {state.get('archer_training_lancer_won', False)}",
        f"final_berserker_won: {state.get('archer_final_berserker_won', False)}",
        f"combat_attempts: {state.get('archer_combat_attempts', 0)}",
        f"flags set: {len(state.get('archer_route_flags', []))}",
    ]


def _append_archer_flag(state, flag):
    flags = state.setdefault("archer_route_flags", [])
    if flag not in flags:
        flags.append(flag)


def _store_archer_combat_result(state, encounter_key, result, outcome_override=None):
    state["archer_combat_attempts"] = int(state.get("archer_combat_attempts", 0)) + 1
    outcome = outcome_override if outcome_override else result.winner
    latest = {
        "encounter": encounter_key,
        "winner": outcome,
        "raw_winner": result.winner,
        "turns_taken": result.turns_taken,
        "hp_remaining": result.hp_remaining,
        "sp_remaining": result.sp_remaining,
        "mana_remaining": result.mana_remaining,
        "flags": list(result.flags),
    }
    state["archer_last_combat"] = latest

    history = state.setdefault("archer_combat_history", [])
    history.append(latest)
    if len(history) > 10:
        history.pop(0)


def run_archer_berserker_opening_combat(screen, clock, state):
    result = run_combat(screen, clock, ENCOUNTERS["archer_vs_berserker_opening"])
    _store_archer_combat_result(state, "archer_vs_berserker_opening", result, outcome_override="enemy")

    state["archer_opening_berserker_done"] = True
    _append_archer_flag(state, "defeated_by_berserker_opening")

    if result.winner == "player":
        lines = [
            "You wound Bhaskar, but the pressure escalates beyond control.",
            "The clash still ends in collapse and retreat.",
            "This defeat is now part of Archer's route progression.",
        ]
    else:
        lines = [
            "The Burning Sun overwhelms you exactly as feared.",
            "You survive, but the defeat leaves a permanent mark.",
        ]

    should_quit = run_info_screen(screen, clock, "Defeat - The Burning Sun", lines)
    if should_quit:
        return True

    save_progress("Archer", state)
    return False


def run_archer_lancer_training_combat(screen, clock, state):
    result = run_combat(screen, clock, ENCOUNTERS["archer_vs_lancer"])
    _store_archer_combat_result(state, "archer_vs_lancer", result)

    if result.winner == "player":
        state["archer_training_lancer_won"] = True
        _append_archer_flag(state, "defeated_lancer_training")
        for flag in result.flags:
            _append_archer_flag(state, f"archer_vs_lancer_{flag}")

        lines = [
            "Training verdict: you outpace Nasir in the exchange.",
            f"Turns: {result.turns_taken}  HP/SP/Mana: {result.hp_remaining}/{result.sp_remaining}/{result.mana_remaining}",
            "You may continue the route.",
        ]
        return run_info_screen(screen, clock, "Training Victory", lines)

    if result.winner == "draw":
        lines = [
            "Training duel ends in a deadlock.",
            "Return from menu to retry this checkpoint.",
        ]
        return run_info_screen(screen, clock, "Training Draw", lines)

    lines = [
        "Nasir wins the training exchange.",
        "Return from menu to retry this checkpoint.",
    ]
    return run_info_screen(screen, clock, "Training Defeat", lines)


def run_archer_berserker_final_combat(screen, clock, state):
    result = run_combat(screen, clock, ENCOUNTERS["archer_vs_berserker_final"])
    _store_archer_combat_result(state, "archer_vs_berserker_final", result)

    if result.winner == "player":
        state["archer_final_berserker_won"] = True
        _append_archer_flag(state, "defeated_berserker_final")
        for flag in result.flags:
            _append_archer_flag(state, f"archer_vs_berserker_final_{flag}")

        lines = [
            "Grand Verdict lands true against the Burning Sun.",
            f"Turns: {result.turns_taken}  HP/SP/Mana: {result.hp_remaining}/{result.sp_remaining}/{result.mana_remaining}",
            "You may continue the route.",
        ]
        return run_info_screen(screen, clock, "Final Combat Victory", lines)

    if result.winner == "draw":
        lines = [
            "The final clash stalls before resolution.",
            "Return from menu to retry this checkpoint.",
        ]
        return run_info_screen(screen, clock, "Final Combat Draw", lines)

    lines = [
        "Bhaskar crushes the final push.",
        "Return from menu to retry this checkpoint.",
    ]
    return run_info_screen(screen, clock, "Final Combat Defeat", lines)


def run_archer_choice_scene(screen, clock, scene, state):
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
            f"Bond(GF) {state.get('bond_girlfriend', 0)} | "
            f"Atrox {state.get('bond_atrox', 0)} | "
            f"Pride {state.get('humility_pride', 0)} | "
            f"Verdict {state.get('grand_verdict_readiness', 0)} | "
            f"Seen {state.get('seen_heard', 0)}"
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


def play_archer_route(screen, clock, state):
    while state["scene_index"] < len(ARCHER_SCENES):
        if state["scene_index"] >= ARCHER_BERSERKER_OPENING_GATE_INDEX and not state.get("archer_opening_berserker_done", False):
            should_quit = run_archer_berserker_opening_combat(screen, clock, state)
            if should_quit:
                return True

        if state["scene_index"] >= ARCHER_LANCER_TRAINING_GATE_INDEX and not state.get("archer_training_lancer_won", False):
            should_quit = run_archer_lancer_training_combat(screen, clock, state)
            if should_quit:
                return True

            if not state.get("archer_training_lancer_won", False):
                save_progress("Archer", state)
                return False

            save_progress("Archer", state)

        if state["scene_index"] >= ARCHER_BERSERKER_FINAL_GATE_INDEX and not state.get("archer_final_berserker_won", False):
            should_quit = run_archer_berserker_final_combat(screen, clock, state)
            if should_quit:
                return True

            if not state.get("archer_final_berserker_won", False):
                save_progress("Archer", state)
                return False

            save_progress("Archer", state)

        scene = ARCHER_SCENES[state["scene_index"]]
        selected_index, should_quit = run_archer_choice_scene(screen, clock, scene, state)

        if should_quit:
            return True
        if selected_index is None:
            save_progress("Archer", state)
            return False

        selected_choice = scene["choices"][selected_index]
        apply_archer_choice_effects(state, selected_choice)
        state["scene_index"] += 1
        save_progress("Archer", state)

        should_quit = run_info_screen(screen, clock, "Choice Result", [selected_choice["result"]])
        if should_quit:
            return True

    ending = state.get("ending") or "Archer Route Complete"
    aftermath_lines = [
        "The fire is gone. Dawn returns over Lucknow.",
        f"Route result: {ending}.",
        "You were seen. You were heard. You survived.",
    ]
    should_quit = run_info_screen(screen, clock, "Scene 10: The Aftermath", aftermath_lines)
    if should_quit:
        return True

    should_quit = run_info_screen(screen, clock, "Archer Route Complete", summarize_archer_stats(state))
    if should_quit:
        return True

    delete_save("Archer", state=state)
    return False
