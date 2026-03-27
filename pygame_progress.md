## Pygame Project Progress Log

### Current Build Overview
- The game now runs in a Pygame windowed interface instead of terminal input.
- Visual style is black background with white text.
- Menu navigation uses keyboard controls only:
  - Up/Down arrows move selection.
  - Enter confirms selection.
  - Escape returns/backs out where applicable.
- Active option is shown with a hover-style highlight bar.

### Modular Structure (Current)
- Main entry and app loop:
   - game.py
- Core configuration:
   - game_core/constants.py
- Save/load and logging:
   - game_core/storage.py
- Shared UI rendering/menu helpers:
   - game_core/ui.py
- Route dispatcher and placeholder routes:
   - game_core/routes.py
- Lancer route modules:
   - game_core/lancer_data.py
   - game_core/lancer_route.py
- Archer route modules:
   - game_core/archer_data.py
   - game_core/archer_route.py
- Caster route modules:
   - game_core/caster_data.py
   - game_core/caster_route.py

### Current Game Flow
1. On launch, save files are checked.
2. If no save exists, player is prompted into New Game.
3. New Game shows six route choices:
   - Lancer
   - Berserker
   - Rider
   - Caster
   - Assassin
   - Archer
4. If saves exist, Main Menu shows:
   - Continue
   - Load
   - Exit
5. Continue loads the most recently updated route save.
6. Load opens a route list for specific saved routes.

### Save System Status
- Save files are stored per route in the saves folder.
- Full route state is written as routes advance (scene index plus route-specific variables).
- Exiting a route mid-progress preserves save data.
- Completing a route removes that route save.

### Route Scene Behavior
- Lancer route is fully modular and choice-driven with tracked variables and ending branches.
- Archer route is fully modular and choice-driven with tracked variables and ending branches.
- Caster route is fully modular and choice-driven with tracked variables and ending branches.
- Remaining routes currently use placeholder 3-scene flow: Berserker, Rider, Assassin.
- Enter advances to the next scene.
- Escape saves progress and returns to menu.

### Technical Notes
- Window resolution is set to 1280x720.
- Frame timing uses a fixed clock tick at 60 FPS.
- Text rendering uses a monospaced system font for readability and consistent menu alignment.