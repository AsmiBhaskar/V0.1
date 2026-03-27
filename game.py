import logging

import pygame

from game_core.constants import FPS, ROUTES, WINDOW_HEIGHT, WINDOW_WIDTH
from game_core.routes import play_route
from game_core.storage import (
    create_new_save_state,
    get_latest_save,
    list_save_entries,
    load_progress,
    setup_logging,
)
from game_core.ui import run_menu, run_message_screen


def main():
    pygame.init()
    pygame.display.set_caption("Text Route Game")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), vsync=1)
    clock = pygame.time.Clock()

    try:
        running = True
        while running:
            saved_entries = list_save_entries(ROUTES)

            if not saved_entries:
                should_quit = run_message_screen(
                    screen,
                    clock,
                    "No Save File",
                    "Press Enter to start a New Game.",
                    "Use Arrow Keys and Enter to select.",
                )
                if should_quit:
                    break

                selected_index, should_quit = run_menu(
                    screen,
                    clock,
                    "New Game",
                    ROUTES,
                    "Choose a route",
                )
                if should_quit:
                    break
                if selected_index is None:
                    continue

                selected_route = ROUTES[selected_index]
                state = create_new_save_state(selected_route)
                running = not play_route(screen, clock, selected_route, state)
                continue

            selected_index, should_quit = run_menu(
                screen,
                clock,
                "Main Menu",
                ["Continue", "Load", "New Game", "Exit"],
                "Arrow Keys: move   Enter: select",
            )
            if should_quit or selected_index is None:
                break

            main_choice = selected_index

            if main_choice == 0:
                latest = get_latest_save(ROUTES)
                if latest is None:
                    continue
                route = latest["route"]
                state = load_progress(route, latest["save_id"])
                running = not play_route(screen, clock, route, state)
            elif main_choice == 1:
                saved_entries = list_save_entries(ROUTES)
                if not saved_entries:
                    continue
                route_index, should_quit = run_menu(
                    screen,
                    clock,
                    "Load Save",
                    [entry["label"] for entry in saved_entries],
                    "Choose a save slot",
                )
                if should_quit:
                    break
                if route_index is None:
                    continue

                selected_save = saved_entries[route_index]
                route = selected_save["route"]
                state = load_progress(route, selected_save["save_id"])
                running = not play_route(screen, clock, route, state)
            elif main_choice == 2:
                selected_index, should_quit = run_menu(
                    screen,
                    clock,
                    "New Game",
                    ROUTES,
                    "Choose a route",
                )
                if should_quit:
                    break
                if selected_index is None:
                    continue

                selected_route = ROUTES[selected_index]
                state = create_new_save_state(selected_route)
                running = not play_route(screen, clock, selected_route, state)
            elif main_choice == 3:
                break
    except Exception:
        logging.exception("Unhandled game error")
        raise
    finally:
        pygame.quit()
        logging.info("Game closed")


if __name__ == "__main__":
    setup_logging()
    main()

