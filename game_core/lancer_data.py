LANCER_STATS_TEMPLATE = {
    "lancer_route_flags": [],
    "bond_atrox": 0,
    "bond_kitik": 0,
    "understanding_bhaskar": 0,
    "zuxi_readiness": 0,
    "team_synergy": 0,
    "ending": "",
    "lancer_combat_won": False,
    "lancer_archer_combat_won": False,
    "lancer_berserker_combat_won": False,
    "lancer_combat_attempts": 0,
}

LANCER_SCENES = [
    {
        "title": "Scene 1: The Rupture",
        "text": [
            "Lucknow wakes under an unnatural red sky.",
            "Fusion completes. Nasir becomes Lancer.",
        ],
        "choices": [
            {
                "label": "Go to the window and observe the city",
                "result": "You map the battlefield in your mind.",
                "effects": {"understanding_bhaskar": 1},
                "flag": "s1_observe_city",
            },
            {
                "label": "Check your body and understand your power",
                "result": "You center your stance and accept the fusion.",
                "effects": {"zuxi_readiness": 1},
                "flag": "s1_understand_self",
            },
            {
                "label": "Reach for Zuxi",
                "result": "The weapon answers your grip.",
                "effects": {"zuxi_readiness": 2},
                "flag": "s1_reach_zuxi",
            },
        ],
    },
    {
        "title": "Scene 2: The First Day",
        "text": [
            "The city pretends everything is normal.",
            "You feel the other chosen nearby.",
        ],
        "choices": [
            {
                "label": "Train at the gym",
                "result": "Training Complete gained.",
                "effects": {"zuxi_readiness": 1},
                "flag": "s2_train",
            },
            {
                "label": "Walk the city and observe",
                "result": "City Knowledge gained.",
                "effects": {"understanding_bhaskar": 1},
                "flag": "s2_city_knowledge",
            },
            {
                "label": "Return home and rest",
                "result": "Centered state gained.",
                "effects": {"team_synergy": 1},
                "flag": "s2_centered",
            },
        ],
    },
    {
        "title": "Scene 3: The News Arrives",
        "text": [
            "Rumors spread of a fire-wreathed attacker.",
            "The war has started.",
        ],
        "choices": [
            {
                "label": "Go to the attack site",
                "result": "You gather evidence of survival.",
                "effects": {"understanding_bhaskar": 1},
                "flag": "s3_investigate",
            },
            {
                "label": "Continue your routine",
                "result": "You choose patience over panic.",
                "effects": {"zuxi_readiness": 1},
                "flag": "s3_patience",
            },
            {
                "label": "Search for other chosen",
                "result": "You learn the shape of the battlefield.",
                "effects": {"team_synergy": 1},
                "flag": "s3_search_others",
            },
        ],
    },
    {
        "title": "Scene 4: The Forest Road",
        "text": [
            "Atrox blocks your path before dawn.",
            "He tests your will in silence.",
        ],
        "choices": [
            {
                "label": "Stop and hold your ground",
                "result": "Atrox respects your resolve.",
                "effects": {"bond_atrox": 2},
                "flag": "s4_respect",
            },
            {
                "label": "Speak first",
                "result": "A direct understanding forms.",
                "effects": {"bond_atrox": 1, "understanding_bhaskar": 1},
                "flag": "s4_directness",
            },
            {
                "label": "Walk past him",
                "result": "Your composure sparks curiosity.",
                "effects": {"bond_atrox": 1},
                "flag": "s4_curiosity",
            },
        ],
    },
    {
        "title": "Scene 5: The Bond",
        "text": [
            "Atrox returns wounded after fighting Bhaskar.",
            "He asks for your help.",
        ],
        "choices": [
            {
                "label": "Accept immediately",
                "result": "Command Seal trust is formed.",
                "effects": {"bond_atrox": 2, "team_synergy": 1},
                "flag": "s5_accept",
            },
            {
                "label": "Ask what he needs",
                "result": "You commit with full context.",
                "effects": {"bond_atrox": 1, "understanding_bhaskar": 1},
                "flag": "s5_ask_need",
            },
            {
                "label": "Ask about Bhaskar",
                "result": "You learn his tragedy deeply.",
                "effects": {"understanding_bhaskar": 2},
                "flag": "s5_ask_bhaskar",
            },
        ],
    },
    {
        "title": "Scene 6: Training with Archer",
        "text": [
            "Kitik trains with you in Kiki's expanding room.",
            "Atrox watches both of you evolve.",
        ],
        "choices": [
            {
                "label": "Focus on teamwork",
                "result": "Your coordination with allies improves.",
                "effects": {"team_synergy": 2, "bond_kitik": 1},
                "flag": "s6_teamwork",
            },
            {
                "label": "Focus on perfecting your strike",
                "result": "Zuxi precision sharpens.",
                "effects": {"zuxi_readiness": 2},
                "flag": "s6_perfect_strike",
            },
            {
                "label": "Observe and analyze",
                "result": "You learn patterns before acting.",
                "effects": {"understanding_bhaskar": 1, "team_synergy": 1},
                "flag": "s6_observe",
            },
        ],
    },
    {
        "title": "Scene 7: The Revelation",
        "text": [
            "Truth surfaces in Kitik's Reality Marble.",
            "Atrox plans to die to stop Bhaskar.",
        ],
        "choices": [
            {
                "label": "Reject the sacrifice plan",
                "result": "You force a united front.",
                "effects": {"bond_atrox": 1, "bond_kitik": 1, "team_synergy": 1},
                "flag": "s7_unity",
            },
            {
                "label": "Ask why",
                "result": "Atrox reveals his full burden.",
                "effects": {"bond_atrox": 1, "understanding_bhaskar": 2},
                "flag": "s7_ask_why",
            },
            {
                "label": "Show them Zuxi",
                "result": "Your allies commit to protecting your strike.",
                "effects": {"bond_atrox": 1, "bond_kitik": 1, "zuxi_readiness": 1},
                "flag": "s7_show_zuxi",
            },
        ],
    },
    {
        "title": "Scene 8: The Battle Begins",
        "text": [
            "Bhool Bhoolaiya is ash and crater.",
            "Bhaskar descends. Final battle starts.",
        ],
        "choices": [
            {
                "label": "Let Atrox lead",
                "result": "Coordinated Assault initiated.",
                "effects": {"bond_atrox": 1, "team_synergy": 1},
                "flag": "s8_atrox_lead",
            },
            {
                "label": "Support Kitik",
                "result": "Archer support line stabilized.",
                "effects": {"bond_kitik": 1, "team_synergy": 1},
                "flag": "s8_support_kitik",
            },
            {
                "label": "Find the path and wait",
                "result": "You preserve focus for the final strike.",
                "effects": {"zuxi_readiness": 1},
                "flag": "s8_pathfinding",
            },
        ],
    },
    {
        "title": "Scene 9: The Final Strike",
        "text": [
            "Time slows. The opening appears.",
            "Zuxi is ready.",
        ],
        "choices": [
            {
                "label": "Strike to end. Strike to destroy.",
                "result": "Ending: Salvation.",
                "effects": {"ending": "Salvation"},
                "flag": "s9_salvation",
            },
            {
                "label": "Strike to reach. Strike to save.",
                "result": "Ending: Redemption.",
                "effects": {"ending": "Redemption"},
                "flag": "s9_redemption",
            },
            {
                "label": "Strike to end the war.",
                "result": "Ending: Unfinished.",
                "effects": {"ending": "Unfinished"},
                "flag": "s9_unfinished",
            },
        ],
    },
]
