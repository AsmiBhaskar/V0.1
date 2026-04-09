import pygame
from combat.core.combat_engine import run_combat
from combat.core.encounter_table import ENCOUNTERS

from game_core.assassin_data import ASSASSIN_SCENES
from game_core.constants import BAR_COLOR, BLACK, FPS, WHITE, WINDOW_WIDTH
from game_core.storage import delete_save, save_progress
from game_core.ui import draw_centered_text, draw_left_text, draw_wrapped_block, run_info_screen


ASSASSIN_CASTER_HOOK_INDEX = 3
ASSASSIN_SCENE4_FIGHT_FLAG = "s4_fight_learn"
ASSASSIN_SCENE6_OPTIONAL_HOOK_INDEX = 5
ASSASSIN_SCENE6_OPTIONAL_FIGHT_FLAG = "s6_final_data"
ASSASSIN_SCENE7_BERSERKER_HOOK_INDEX = 6
ASSASSIN_SCENE9_FINAL_HOOK_INDEX = 8


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
        f"caster_hook_done: {state.get('assassin_caster_hook_done', False)}",
        f"alliance_offer_applied: {state.get('assassin_alliance_offer_applied', False)}",
        f"scene6_optional_hook_done: {state.get('assassin_scene6_optional_hook_done', False)}",
        f"scene7_berserker_hook_done: {state.get('assassin_scene7_berserker_hook_done', False)}",
        f"scene9_final_hook_done: {state.get('assassin_scene9_final_hook_done', False)}",
        f"combat_attempts: {state.get('assassin_combat_attempts', 0)}",
        f"flags set: {len(state.get('assassin_route_flags', []))}",
    ]


def _append_assassin_flag(state, flag):
    flags = state.setdefault("assassin_route_flags", [])
    if flag not in flags:
        flags.append(flag)


def _store_assassin_combat_result(state, encounter_key, result, outcome_override=None):
    state["assassin_combat_attempts"] = int(state.get("assassin_combat_attempts", 0)) + 1
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
    state["assassin_last_combat"] = latest

    history = state.setdefault("assassin_combat_history", [])
    history.append(latest)
    if len(history) > 10:
        history.pop(0)


def _apply_assassin_alliance_offer_effects(state):
    if state.get("assassin_alliance_offer_applied", False):
        return

    state["bond_kiki"] = int(state.get("bond_kiki", 0)) + 1
    state["information_network"] = int(state.get("information_network", 0)) + 1
    state["assassin_alliance_offer_applied"] = True
    _append_assassin_flag(state, "assassin_alliance_offer_accepted")


def run_assassin_caster_opening_combat(screen, clock, state):
    result = run_combat(screen, clock, ENCOUNTERS["assassin_vs_caster_opening"])
    _store_assassin_combat_result(state, "assassin_vs_caster_opening", result, outcome_override="enemy")

    state["assassin_caster_hook_done"] = True
    _append_assassin_flag(state, "assassin_caster_first_hook")
    _apply_assassin_alliance_offer_effects(state)

    # Hook #1 is always a power-gap beat: combat outcome feeds into a forced narrative fallback.
    if result.winner == "player":
        lines = [
            "Stella breaks through briefly - then Core Matrix escalates beyond her read.",
            "Kiki reveals he was holding back and forcibly resets the field.",
            "Outcome defaults to defeat-state; alliance terms are still offered.",
            "Alliance effect applied: bond_kiki +1, information_network +1.",
        ]
        _append_assassin_flag(state, "assassin_caster_hook_forced_loss_from_win")
    elif result.winner == "draw":
        lines = [
            "Stella survives longer than expected under relentless Core Matrix pressure.",
            "Kiki is impressed by her endurance, but the trap still closes.",
            "Outcome resolves as defeat-state with alliance offer.",
            "Alliance effect applied: bond_kiki +1, information_network +1.",
        ]
        _append_assassin_flag(state, "assassin_caster_hook_forced_loss_from_draw")
    else:
        lines = [
            "Core Matrix traps Stella and locks out escape vectors.",
            "Kiki suppresses the finishing strike and offers alliance terms.",
            "Power gap established: this encounter is overwhelmingly one-sided.",
            "Alliance effect applied: bond_kiki +1, information_network +1.",
        ]
        _append_assassin_flag(state, "assassin_caster_hook_defeat")

    return run_info_screen(screen, clock, "Scene 4 Combat - Caster Supremacy", lines)


def run_assassin_scene6_optional_combat(screen, clock, state):
    result = run_combat(screen, clock, ENCOUNTERS["assassin_scene6_minor_spirits"])
    _store_assassin_combat_result(state, "assassin_scene6_minor_spirits", result)

    state["assassin_scene6_optional_hook_done"] = True
    _append_assassin_flag(state, "assassin_scene6_optional_hook")

    if result.winner == "player":
        state["information_network"] = int(state.get("information_network", 0)) + 1
        state["hunt_progress"] = int(state.get("hunt_progress", 0)) + 1
        _append_assassin_flag(state, "assassin_scene6_optional_victory")
        lines = [
            "Minor spirits breach the corridor and Stella cuts through the swarm.",
            "She extracts pattern fragments for Kiki's network before regrouping.",
            "Optional hook reward: information_network +1, hunt_progress +1.",
        ]
        return run_info_screen(screen, clock, "Scene 6 Optional Combat - Victory", lines)

    if result.winner == "draw":
        state["information_network"] = int(state.get("information_network", 0)) + 1
        _append_assassin_flag(state, "assassin_scene6_optional_draw")
        lines = [
            "Stella survives the spirit rush and disengages with partial data.",
            "Kiki's system receives only a fragmented upload.",
            "Optional hook reward: information_network +1.",
        ]
        return run_info_screen(screen, clock, "Scene 6 Optional Combat - Stalemate", lines)

    state["reverence_binding"] = int(state.get("reverence_binding", 0)) + 1
    _append_assassin_flag(state, "assassin_scene6_optional_defeat")
    lines = [
        "The breach forces Stella into retreat under sustained pressure.",
        "She survives, but the loss deepens the sense of binding and inevitability.",
        "Optional hook penalty: reverence_binding +1.",
    ]
    return run_info_screen(screen, clock, "Scene 6 Optional Combat - Defeat", lines)


def run_assassin_scene7_berserker_cutscene_combat(screen, clock, state, choice_flag: str | None = None):
    result = run_combat(screen, clock, ENCOUNTERS["assassin_vs_berserker_cutscene"])
    _store_assassin_combat_result(state, "assassin_vs_berserker_cutscene", result)

    state["assassin_scene7_berserker_hook_done"] = True
    _append_assassin_flag(state, "assassin_scene7_berserker_hook")
    if choice_flag:
        _append_assassin_flag(state, f"assassin_scene7_choice_{choice_flag}")

    if result.winner == "player":
        state["memory_retention"] = int(state.get("memory_retention", 0)) + 1
        _append_assassin_flag(state, "assassin_scene7_berserker_cutscene_victory")
        lines = [
            "Stella forces a brief opening against the Burning Sun.",
            "Bhaskar's pressure still floods the chamber and the sacrifice path locks in.",
            "Cutscene reward: memory_retention +1.",
        ]
        return run_info_screen(screen, clock, "Scene 7 Cutscene Combat - Breakthrough", lines)

    if result.winner == "draw":
        state["information_network"] = int(state.get("information_network", 0)) + 1
        _append_assassin_flag(state, "assassin_scene7_berserker_cutscene_draw")
        lines = [
            "Stella survives the clash long enough to capture final pattern fragments.",
            "The labyrinth still collapses toward binding.",
            "Cutscene reward: information_network +1.",
        ]
        return run_info_screen(screen, clock, "Scene 7 Cutscene Combat - Deadlock", lines)

    state["reverence_binding"] = int(state.get("reverence_binding", 0)) + 1
    _append_assassin_flag(state, "assassin_scene7_berserker_cutscene_defeat")
    lines = [
        "Bhaskar's force crushes Stella's guard and drives the binding sequence forward.",
        "She still reaches Scene 8, but under heavier compulsion.",
        "Cutscene penalty: reverence_binding +1.",
    ]
    return run_info_screen(screen, clock, "Scene 7 Cutscene Combat - Overrun", lines)


def _apply_scene9_focus_reward(state, choice_flag: str | None, amount: int):
    if amount <= 0:
        return "hunt_progress", amount

    if choice_flag == "s9_truth_hunt":
        key = "information_network"
    elif choice_flag == "s9_recovery_hunt":
        key = "memory_retention"
    else:
        key = "hunt_progress"

    state[key] = int(state.get(key, 0)) + int(amount)
    return key, amount


def run_assassin_scene9_final_hook_combat(screen, clock, state, choice_flag: str | None = None):
    result = run_combat(screen, clock, ENCOUNTERS["assassin_scene9_final_mystery"])
    _store_assassin_combat_result(state, "assassin_scene9_final_mystery", result)

    state["assassin_scene9_final_hook_done"] = True
    _append_assassin_flag(state, "assassin_scene9_final_hook")
    if choice_flag:
        _append_assassin_flag(state, f"assassin_scene9_choice_{choice_flag}")

    if result.winner == "player":
        reward_key, reward_amount = _apply_scene9_focus_reward(state, choice_flag, 2)
        _append_assassin_flag(state, "assassin_scene9_final_hook_victory")
        lines = [
            "Stella isolates the unknown signal and tears down its manifested shell.",
            "The hunt vector sharpens as she secures a decisive data lock.",
            f"Final hook reward: {reward_key} +{reward_amount}.",
        ]
        return run_info_screen(screen, clock, "Scene 9 Final Hook - Signal Broken", lines)

    if result.winner == "draw":
        reward_key, reward_amount = _apply_scene9_focus_reward(state, choice_flag, 1)
        _append_assassin_flag(state, "assassin_scene9_final_hook_draw")
        lines = [
            "The signal withstands full collapse but Stella extracts actionable trace fragments.",
            "She remains locked on the target line into dawn.",
            f"Final hook reward: {reward_key} +{reward_amount}.",
        ]
        return run_info_screen(screen, clock, "Scene 9 Final Hook - Trace Captured", lines)

    state["reverence_binding"] = int(state.get("reverence_binding", 0)) + 1
    _append_assassin_flag(state, "assassin_scene9_final_hook_defeat")
    lines = [
        "The unknown pressure overwhelms Stella's read and forces a compromised disengage.",
        "She survives to continue the hunt, but under tighter internal compulsion.",
        "Final hook penalty: reverence_binding +1.",
    ]
    return run_info_screen(screen, clock, "Scene 9 Final Hook - Compromised", lines)


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

        if (
            state["scene_index"] == ASSASSIN_CASTER_HOOK_INDEX
            and selected_choice.get("flag") == ASSASSIN_SCENE4_FIGHT_FLAG
            and not state.get("assassin_caster_hook_done", False)
        ):
            should_quit = run_assassin_caster_opening_combat(screen, clock, state)
            if should_quit:
                return True

        if (
            state["scene_index"] == ASSASSIN_SCENE6_OPTIONAL_HOOK_INDEX
            and selected_choice.get("flag") == ASSASSIN_SCENE6_OPTIONAL_FIGHT_FLAG
            and not state.get("assassin_scene6_optional_hook_done", False)
        ):
            should_quit = run_assassin_scene6_optional_combat(screen, clock, state)
            if should_quit:
                return True

        if (
            state["scene_index"] == ASSASSIN_SCENE7_BERSERKER_HOOK_INDEX
            and not state.get("assassin_scene7_berserker_hook_done", False)
        ):
            should_quit = run_assassin_scene7_berserker_cutscene_combat(
                screen,
                clock,
                state,
                selected_choice.get("flag"),
            )
            if should_quit:
                return True

        if (
            state["scene_index"] == ASSASSIN_SCENE9_FINAL_HOOK_INDEX
            and not state.get("assassin_scene9_final_hook_done", False)
        ):
            should_quit = run_assassin_scene9_final_hook_combat(
                screen,
                clock,
                state,
                selected_choice.get("flag"),
            )
            if should_quit:
                return True

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
