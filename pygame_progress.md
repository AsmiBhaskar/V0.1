## Pygame Project Progress Log

### Current Build Overview
- The game now runs in a Pygame windowed interface instead of terminal input.
- Visual style is black background with white text.
- Main menu presentation is finalized with the repo SVG logo as the menu background centerpiece.
- SVG and alpha tuning pass completed for stable, readable menu visuals.
- Menu navigation uses keyboard controls only:
  - Up/Down arrows move selection.
  - Enter confirms selection.
  - Escape returns/backs out where applicable.
- Active option is shown with a hover-style highlight bar.
- Menu typography uses bold italic styling for stronger visual emphasis.

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
4. Main Menu always shows:
   - Continue
   - Load
   - New Game
   - Exit
5. Continue loads the most recently updated save slot.
6. Load opens a list of save slots across routes.
7. New Game can always create another save slot, even when saves already exist.

### Save System Status
- Save files are stored in the saves folder as multiple save slots.
- Save filenames use route + save id format for multi-slot support.
- Full route state is written as routes advance (scene index plus route-specific variables).
- Exiting a route mid-progress preserves save data.
- Completing a route removes only the active save slot for that run.

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
- Menu screens use SVG-backed branding and bold italic text styling.
- Optional SVG conversion fallback is supported when direct SVG loading is unavailable.