## Pygame Project Progress Log

### Current Build Overview
- The game now runs in a Pygame windowed interface instead of terminal input.
- Visual style is black background with white text.
- Menu navigation uses keyboard controls only:
  - Up/Down arrows move selection.
  - Enter confirms selection.
  - Escape returns/backs out where applicable.
- Active option is shown with a hover-style highlight bar.

### Current Game Flow
1. On launch, save files are checked.
2. If no save exists, player is prompted into New Game.
3. New Game shows six route choices:
	- Lancer
	- Berserker
	- rider
	- caster
	- assassin
	- archer
4. If saves exist, Main Menu shows:
	- Continue
	- Load
	- Exit
5. Continue loads the most recently updated route save.
6. Load opens a route list for specific saved routes.

### Save System Status
- Save files are stored per route in the saves folder.
- Scene progress is written as the route advances.
- Exiting a route mid-progress preserves save data.
- Completing a route removes that route save.

### Route Scene Behavior
- Each route currently contains a 3-scene narrative sequence.
- Enter advances to the next scene.
- Escape saves progress and returns to menu.

### Technical Notes
- Window resolution is set to 1280x720.
- Frame timing uses a fixed clock tick at 60 FPS.
- Text rendering uses a monospaced system font for readability and consistent menu alignment.