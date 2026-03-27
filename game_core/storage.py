import json
import logging

from game_core.constants import LOG_FILE, SAVE_DIR
from game_core.archer_data import ARCHER_STATS_TEMPLATE
from game_core.lancer_data import LANCER_STATS_TEMPLATE


def setup_logging():
    logging.basicConfig(
        filename=LOG_FILE,
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )
    logging.info("Game started")


def default_route_state(route):
    state = {
        "scene_index": 0,
        "route": route,
    }
    if route == "Lancer":
        state.update({key: value[:] if isinstance(value, list) else value for key, value in LANCER_STATS_TEMPLATE.items()})
    if route == "Archer":
        state.update({key: value[:] if isinstance(value, list) else value for key, value in ARCHER_STATS_TEMPLATE.items()})
    return state


def get_save_path(route):
    return SAVE_DIR / f"{route.lower()}.json"


def save_progress(route, state):
    try:
        SAVE_DIR.mkdir(parents=True, exist_ok=True)
        save_data = {"route": route, "state": state}
        with get_save_path(route).open("w", encoding="utf-8") as save_file:
            json.dump(save_data, save_file)
    except OSError:
        logging.exception("Failed to save progress for route: %s", route)


def load_progress(route):
    save_path = get_save_path(route)
    if not save_path.exists():
        return default_route_state(route)

    try:
        with save_path.open("r", encoding="utf-8") as save_file:
            save_data = json.load(save_file)

        if "state" in save_data and isinstance(save_data["state"], dict):
            state = default_route_state(route)
            state.update(save_data["state"])
            return state

        # Backward compatibility for old saves that only stored scene index.
        scene_index = int(save_data.get("next_scene_index", 0))
        state = default_route_state(route)
        state["scene_index"] = scene_index
        return state
    except (OSError, json.JSONDecodeError, ValueError):
        logging.exception("Failed to load save file for route: %s", route)
        return default_route_state(route)


def delete_save(route):
    save_path = get_save_path(route)
    if save_path.exists():
        try:
            save_path.unlink()
        except OSError:
            logging.exception("Failed to delete save file for route: %s", route)


def get_saved_routes(routes):
    return [route for route in routes if get_save_path(route).exists()]


def get_latest_saved_route(routes):
    saved_routes = get_saved_routes(routes)
    if not saved_routes:
        return None
    try:
        return max(saved_routes, key=lambda route: get_save_path(route).stat().st_mtime)
    except OSError:
        logging.exception("Failed to determine latest saved route")
        return None
