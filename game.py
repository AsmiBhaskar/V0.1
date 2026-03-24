import logging

import pygame

from game_core.constants import FPS, ROUTES, WINDOW_HEIGHT, WINDOW_WIDTH
from game_core.routes import play_route
from game_core.storage import (
    default_route_state,
    get_latest_saved_route,
    get_saved_routes,
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
            saved_routes = get_saved_routes(ROUTES)

            if not saved_routes:
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
                state = default_route_state(selected_route)
                running = not play_route(screen, clock, selected_route, state)
                continue

            selected_index, should_quit = run_menu(
                screen,
                clock,
                "Main Menu",
                ["Continue", "Load", "Exit"],
                "Arrow Keys: move   Enter: select",
            )
            if should_quit or selected_index is None:
                break

            main_choice = selected_index

            if main_choice == 0:
                route = get_latest_saved_route(ROUTES)
                if route is None:
                    continue
                state = load_progress(route)
                running = not play_route(screen, clock, route, state)
            elif main_choice == 1:
                saved_routes = get_saved_routes(ROUTES)
                if not saved_routes:
                    continue
                route_index, should_quit = run_menu(
                    screen,
                    clock,
                    "Load Route",
                    saved_routes,
                    "Choose a saved route",
                )
                if should_quit:
                    break
                if route_index is None:
                    continue

                route = saved_routes[route_index]
                state = load_progress(route)
                running = not play_route(screen, clock, route, state)
            elif main_choice == 2:
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

