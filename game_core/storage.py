import json
import logging
import uuid
from pathlib import Path

from game_core.constants import LOG_FILE, SAVE_DIR
from game_core.berserker_data import BERSERKER_STATS_TEMPLATE
from game_core.archer_data import ARCHER_STATS_TEMPLATE
from game_core.caster_data import CASTER_STATS_TEMPLATE
from game_core.lancer_data import LANCER_STATS_TEMPLATE
from game_core.assassin_data import ASSASSIN_STATS_TEMPLATE
from game_core.rider_data import RIDER_STATS_TEMPLATE


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
        "save_id": None,
    }
    if route == "Lancer":
        state.update({key: value[:] if isinstance(value, list) else value for key, value in LANCER_STATS_TEMPLATE.items()})
    if route == "Archer":
        state.update({key: value[:] if isinstance(value, list) else value for key, value in ARCHER_STATS_TEMPLATE.items()})
    if route == "Caster":
        state.update({key: value[:] if isinstance(value, list) else value for key, value in CASTER_STATS_TEMPLATE.items()})
    if route == "Assassin":
        state.update({key: value[:] if isinstance(value, list) else value for key, value in ASSASSIN_STATS_TEMPLATE.items()})
    if route == "Rider":
        state.update({key: value[:] if isinstance(value, list) else value for key, value in RIDER_STATS_TEMPLATE.items()})
    if route == "Berserker":
        state.update({key: value[:] if isinstance(value, list) else value for key, value in BERSERKER_STATS_TEMPLATE.items()})
    return state


def create_new_save_state(route):
    state = default_route_state(route)
    state["save_id"] = uuid.uuid4().hex[:10]
    return state


def get_save_path(route, save_id=None):
    if save_id:
        return SAVE_DIR / f"{route.lower()}_{save_id}.json"
    return SAVE_DIR / f"{route.lower()}.json"


def _extract_save_id(path: Path, route: str):
    name = path.stem
    route_prefix = f"{route.lower()}_"
    if name.startswith(route_prefix):
        return name[len(route_prefix) :]
    return None


def _state_to_entry(route, save_id, save_path, state):
    scene_index = int(state.get("scene_index", 0))
    label_suffix = save_id if save_id else "legacy"
    return {
        "route": route,
        "save_id": save_id,
        "path": str(save_path),
        "scene_index": scene_index,
        "label": f"{route} | Scene {scene_index + 1} | {label_suffix}",
        "mtime": save_path.stat().st_mtime,
    }


def save_progress(route, state):
    try:
        SAVE_DIR.mkdir(parents=True, exist_ok=True)
        save_id = state.get("save_id")
        if not save_id:
            save_id = uuid.uuid4().hex[:10]
            state["save_id"] = save_id
        save_data = {"route": route, "state": state}
        with get_save_path(route, save_id).open("w", encoding="utf-8") as save_file:
            json.dump(save_data, save_file)
    except OSError:
        logging.exception("Failed to save progress for route: %s", route)


def load_progress(route, save_id=None):
    save_path = get_save_path(route, save_id)
    if not save_path.exists() and save_id is not None:
        # Backward compatibility for a legacy per-route save file.
        save_path = get_save_path(route)

    if not save_path.exists():
        return default_route_state(route)

    try:
        with save_path.open("r", encoding="utf-8") as save_file:
            save_data = json.load(save_file)

        if "state" in save_data and isinstance(save_data["state"], dict):
            state = default_route_state(route)
            state.update(save_data["state"])
            if not state.get("save_id"):
                extracted_id = _extract_save_id(save_path, route)
                state["save_id"] = extracted_id
            return state

        # Backward compatibility for old saves that only stored scene index.
        scene_index = int(save_data.get("next_scene_index", 0))
        state = default_route_state(route)
        state["scene_index"] = scene_index
        state["save_id"] = _extract_save_id(save_path, route)
        return state
    except (OSError, json.JSONDecodeError, ValueError):
        logging.exception("Failed to load save file for route: %s", route)
        return default_route_state(route)


def delete_save(route, state=None, save_id=None):
    resolved_save_id = save_id
    if resolved_save_id is None and state is not None:
        resolved_save_id = state.get("save_id")

    save_path = get_save_path(route, resolved_save_id)

    # Legacy cleanup fallback if a slot id wasn't available.
    if not save_path.exists() and resolved_save_id is None:
        save_path = get_save_path(route)

    if save_path.exists():
        try:
            save_path.unlink()
        except OSError:
            logging.exception("Failed to delete save file for route: %s", route)


def get_saved_routes(routes):
    saved = set()
    for entry in list_save_entries(routes):
        saved.add(entry["route"])
    return [route for route in routes if route in saved]


def list_save_entries(routes):
    if not SAVE_DIR.exists():
        return []

    entries = []
    route_lookup = {route.lower(): route for route in routes}

    for save_path in SAVE_DIR.glob("*.json"):
        route = None
        save_id = None
        stem = save_path.stem

        for route_lower, route_name in route_lookup.items():
            prefix = f"{route_lower}_"
            if stem == route_lower:
                route = route_name
                save_id = None
                break
            if stem.startswith(prefix):
                route = route_name
                save_id = stem[len(prefix) :]
                break

        if route is None:
            continue

        try:
            state = load_progress(route, save_id)
            entries.append(_state_to_entry(route, save_id, save_path, state))
        except OSError:
            logging.exception("Failed reading save metadata for %s", save_path)

    entries.sort(key=lambda entry: entry["mtime"], reverse=True)
    return entries


def get_latest_save(routes):
    entries = list_save_entries(routes)
    if not entries:
        return None
    return entries[0]


def get_latest_saved_route(routes):
    latest = get_latest_save(routes)
    return latest["route"] if latest else None
