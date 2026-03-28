## Pygame Project Progress Log

### Phase Status
- Phase 1 Narrative: COMPLETE
- All six core routes are now implemented as dedicated modular route systems.
- Placeholder flow is no longer used for primary route content.

### Recent Fixes (Post Phase 1)
- Berserker ending branch bug addressed:
   - True ending is no longer hard-locked behind a single exact path.
   - Near-perfect salvation path support added (6 of 7 salvation flags with Scene 9 salvation), alongside stat checks.
   - Destruction lock conditions remain in place for explicit collapse outcomes.
- Added a new Berserker pre-ending Requirements Check screen:
   - Shows pass/fail for each true-ending threshold.
   - Shows salvation flag hit count and any missing salvation flags.
   - Shows destruction lock status and predicted ending before final resolution.

### Current Build Overview
- The game runs in a Pygame windowed interface with keyboard-only navigation.
- Visual direction is black background with white text and SVG-branded menu background.
- Main menu interactions are stable:
   - Up and Down arrows move selection.
   - Enter confirms a selection.
   - Escape backs out or saves and returns where applicable.
- Active options render with a hover-style highlight bar.
- Menu typography remains bold and italic for emphasis and readability.

### Modular Structure (Current)
- Main entry and app loop:
   - game.py
- Core constants/config:
   - game_core/constants.py
- Save system and logging:
   - game_core/storage.py
- Shared UI and menu rendering helpers:
   - game_core/ui.py
- Route dispatch:
   - game_core/routes.py
- Lancer route:
   - game_core/lancer_data.py
   - game_core/lancer_route.py
- Archer route:
   - game_core/archer_data.py
   - game_core/archer_route.py
- Caster route:
   - game_core/caster_data.py
   - game_core/caster_route.py
- Assassin route:
   - game_core/assassin_data.py
   - game_core/assassin_route.py
- Rider route:
   - game_core/rider_data.py
   - game_core/rider_route.py
- Berserker route:
   - game_core/berserker_data.py
   - game_core/berserker_route.py

### Route Completion Status
- Lancer: complete modular route with choice-driven progression and tracked variables.
- Archer: complete modular route with choice-driven progression and tracked variables.
- Caster: complete modular route with choice-driven progression and tracked variables.
- Assassin: complete modular route with choice-driven progression and tracked variables.
- Rider: complete modular route with choice-driven progression and tracked variables.
- Berserker: complete special-case modular route with custom mechanics and dual ending logic.

### Berserker Special Logic (Implemented)
- Burning Ache mechanic:
   - Passive ache increases per decision turn.
   - Combat or active hunt choices reduce ache.
   - High ache levels increase rage and reduce memory retention.
- Ending branch logic:
   - True Ending (Salvation) can be reached via full required salvation flags, or a near-perfect salvation path, plus stat thresholds.
   - Bad Ending (Consumption) is used when salvation requirements are not met, or destruction lock conditions are triggered.
- Ending requirements transparency:
   - A dedicated pre-ending screen now displays requirement status and predicted branch before Scene 10 resolves.
- Distinct unlock/reward output is shown based on ending branch.

### Current Game Flow
1. Game launches and checks for save slots.
2. If no saves exist, player is prompted into New Game route selection.
3. New Game offers all six routes:
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
6. Load opens slot list across all routes.
7. New Game can always create additional save slots.

### Save System Status
- Multi-slot saves are active in the saves folder.
- Save filename pattern uses route plus save id.
- Route state includes scene index and route-specific tracked variables.
- Escape from active route saves state and returns to menu.
- Route completion deletes only the active slot for that run.

### Technical Notes
- Resolution: 1280x720.
- Frame timing: fixed 60 FPS.
- Menu screens support SVG-backed branding with robust rendering fallback behavior.
- Logging to game.log remains active for runtime and save/load error tracing.