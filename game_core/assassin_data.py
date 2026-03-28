ASSASSIN_STATS_TEMPLATE = {
    "assassin_route_flags": [],
    "information_network": 0,
    "bond_kiki": 0,
    "memory_retention": 0,
    "reverence_binding": 0,
    "hunt_progress": 0,
    "ending": "",
}

ASSASSIN_SCENES = [
    {
        "title": "Scene 1: The Rupture",
        "text": [
            "Stella awakens with impossible knowledge flooding her mind.",
            "The Grail names her Assassin, the Legend Eater.",
        ],
        "choices": [
            {
                "label": "Know all their secrets",
                "result": "You map hidden motives before anyone notices.",
                "effects": {"information_network": 2, "hunt_progress": 1},
                "flag": "s1_deep_knowledge",
            },
            {
                "label": "Know yourself first",
                "result": "You gain clarity about your own fractures.",
                "effects": {"memory_retention": 1},
                "flag": "s1_self_awareness",
            },
            {
                "label": "Know what is coming",
                "result": "You lock onto the sacrifice thread early.",
                "effects": {"hunt_progress": 2},
                "flag": "s1_foreknowledge",
            },
        ],
    },
    {
        "title": "Scene 2: The First Day",
        "text": [
            "Lucknow acts normal while six altered souls move beneath it.",
            "You choose distance, engagement, or pure observation.",
        ],
        "choices": [
            {
                "label": "Observe and profile everyone",
                "result": "Your dossier of all players grows quickly.",
                "effects": {"information_network": 2},
                "flag": "s2_observe",
            },
            {
                "label": "Engage and gain access",
                "result": "You gather data from within social circles.",
                "effects": {"information_network": 1, "memory_retention": 1},
                "flag": "s2_engage",
            },
            {
                "label": "Withdraw and isolate",
                "result": "You reduce risk but increase internal distance.",
                "effects": {"memory_retention": -1, "information_network": 1},
                "flag": "s2_withdraw",
            },
        ],
    },
    {
        "title": "Scene 3: The First Strike",
        "text": [
            "You arrive at the aftermath of fire and song colliding.",
            "Every scorch mark becomes a clue.",
        ],
        "choices": [
            {
                "label": "Decode Bhaskar's hunting rhythm",
                "result": "You identify purpose behind the violence.",
                "effects": {"hunt_progress": 1, "information_network": 1},
                "flag": "s3_bhaskar_pattern",
            },
            {
                "label": "Profile Kitik's retreat response",
                "result": "You capture survival psychology under pressure.",
                "effects": {"information_network": 1, "memory_retention": 1},
                "flag": "s3_kitik_profile",
            },
            {
                "label": "Map tactical terrain advantages",
                "result": "You preserve a battlefield edge for later.",
                "effects": {"information_network": 1, "bond_kiki": 1},
                "flag": "s3_terrain",
            },
        ],
    },
    {
        "title": "Scene 4: Encounter with Caster",
        "text": [
            "Kiki catches you despite perfect concealment.",
            "The system and the ghost negotiate terms.",
        ],
        "choices": [
            {
                "label": "Fight and learn while falling",
                "result": "You lose the exchange but record his patterns.",
                "effects": {"information_network": 2},
                "flag": "s4_fight_learn",
            },
            {
                "label": "Negotiate alliance immediately",
                "result": "You and Kiki form a functional pact.",
                "effects": {"bond_kiki": 2, "information_network": 1},
                "flag": "s4_alliance",
            },
            {
                "label": "Test what he values",
                "result": "Kiki recognizes your strategic worth.",
                "effects": {"bond_kiki": 1, "information_network": 1},
                "flag": "s4_respect",
            },
        ],
    },
    {
        "title": "Scene 5: Information Network",
        "text": [
            "A node binds your whisper network to Kiki's system.",
            "You choose what data stream matters most.",
        ],
        "choices": [
            {
                "label": "Prioritize Bhaskar data",
                "result": "You uncover the tragedy behind the fire.",
                "effects": {"hunt_progress": 2, "information_network": 1},
                "flag": "s5_bhaskar_data",
            },
            {
                "label": "Prioritize all surviving variables",
                "result": "Your models of allies and rivals become robust.",
                "effects": {"information_network": 2, "memory_retention": 1},
                "flag": "s5_allied_data",
            },
            {
                "label": "Trace the Grail source",
                "result": "You detect a deeper thread beneath the war.",
                "effects": {"hunt_progress": 1, "reverence_binding": 1},
                "flag": "s5_grail_awareness",
            },
        ],
    },
    {
        "title": "Scene 6: The Four Days",
        "text": [
            "Bhool Bhoolaiya fails one corridor at a time under fire.",
            "You decide how to face the collapse.",
        ],
        "choices": [
            {
                "label": "Feed Kiki final data until the end",
                "result": "Your last packets keep the system alive longer.",
                "effects": {"information_network": 1, "bond_kiki": 1},
                "flag": "s6_final_data",
            },
            {
                "label": "Accept the sacrifice path",
                "result": "You stop resisting what you already foresaw.",
                "effects": {"memory_retention": 1, "reverence_binding": 1},
                "flag": "s6_acceptance",
            },
            {
                "label": "Defy fate and search another way",
                "result": "You preserve agency against inevitability.",
                "effects": {"memory_retention": 1, "reverence_binding": -1},
                "flag": "s6_defiance",
            },
        ],
    },
    {
        "title": "Scene 7: The Choice",
        "text": [
            "At the center of the labyrinth, you step between Kiki and ruin.",
            "Stellae Scriptum asks what truth you will force into existence.",
        ],
        "choices": [
            {
                "label": "Write: I can absorb the Divine Spear",
                "result": "You save Kiki by taking the impossible into yourself.",
                "effects": {"bond_kiki": 2, "reverence_binding": 2},
                "flag": "s7_sacrifice",
            },
            {
                "label": "Write: I can survive this",
                "result": "You endure, but the cost shifts to everyone else.",
                "effects": {"reverence_binding": 1, "memory_retention": -1},
                "flag": "s7_survival",
            },
            {
                "label": "Write: I am more than I seemed",
                "result": "You transform into a new, unstable state.",
                "effects": {"reverence_binding": 1, "hunt_progress": 1, "memory_retention": 1},
                "flag": "s7_transformation",
            },
        ],
    },
    {
        "title": "Scene 8: The Binding",
        "text": [
            "Bhaskar binds you instead of ending you.",
            "Only chosen memories can survive Reverence.",
        ],
        "choices": [
            {
                "label": "Hold onto Kiki's face",
                "result": "A personal thread survives the command chain.",
                "effects": {"memory_retention": 2, "bond_kiki": 1, "reverence_binding": -1},
                "flag": "s8_memory_kiki",
            },
            {
                "label": "Hold onto your connections",
                "result": "You preserve social anchors against erasure.",
                "effects": {"memory_retention": 1, "information_network": 1},
                "flag": "s8_memory_connections",
            },
            {
                "label": "Let everything go",
                "result": "Binding reaches near-total control.",
                "effects": {"memory_retention": -2, "reverence_binding": 2},
                "flag": "s8_empty",
            },
        ],
    },
    {
        "title": "Scene 9: The Hunt",
        "text": [
            "You move through Lucknow as a watcher bound to a command.",
            "Choose what your hunt is truly for.",
        ],
        "choices": [
            {
                "label": "Search for the Grail source",
                "result": "Ending focus: Grail Hunt.",
                "effects": {"ending": "Grail Hunt", "hunt_progress": 2},
                "flag": "s9_grail_hunt",
            },
            {
                "label": "Search for fusion truth",
                "result": "Ending focus: Truth Hunt.",
                "effects": {"ending": "Truth Hunt", "hunt_progress": 1, "information_network": 1},
                "flag": "s9_truth_hunt",
            },
            {
                "label": "Search for your lost memory",
                "result": "Ending focus: Recovery Hunt.",
                "effects": {"ending": "Recovery Hunt", "memory_retention": 1},
                "flag": "s9_recovery_hunt",
            },
        ],
    },
]
