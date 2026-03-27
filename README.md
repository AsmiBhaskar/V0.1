<p align="center">
  <img src="assets/new_order_logo.svg" alt="New Order logo" width="720" />
</p>

# New Order

A branching, choice-driven Pygame narrative project set during a Grail War-style conflict in Lucknow.

## What It Is

New Order is a keyboard-first, windowed story game where each route follows a different protagonist arc. Player choices update route-specific variables, flags, and endings, with per-route save persistence.

## Technical Snapshot

- Language: Python
- Framework: Pygame
- Rendering: 1280x720 window, black UI theme, white text, highlighted selection bars
- Input: Arrow keys for navigation, Enter to confirm, Esc to return/save from route scenes
- Persistence: JSON save files in the saves folder
- Logging: Runtime and failure logs written to game.log

## Current Route Status

- Fully modular, choice-driven routes:
  - Lancer
  - Archer
  - Caster
- Placeholder routes:
  - Berserker
  - Rider
  - Assassin

## Project Structure

- game.py: Main app loop and menu flow
- game_core/constants.py: Global constants and route list
- game_core/storage.py: Save/load and logging setup
- game_core/ui.py: Shared drawing and menu UI helpers
- game_core/routes.py: Route dispatcher and placeholder route flow
- game_core/lancer_data.py + game_core/lancer_route.py: Lancer route content and runtime
- game_core/archer_data.py + game_core/archer_route.py: Archer route content and runtime
- game_core/caster_data.py + game_core/caster_route.py: Caster route content and runtime

## Run

1. Install dependencies:
   - pip install pygame
2. Start the game:
   - python game.py
