CASTER_STATS_TEMPLATE = {
    "caster_route_flags": [],
    "system_integrity": 0,
    "bond_stella": 0,
    "humanity_vs_efficiency": 0,
    "grail_awareness": 0,
    "stella_fate": "unknown",
    "ending": "",
}

CASTER_SCENES = [
    {
        "title": "Scene 1: The Rupture",
        "text": [
            "Kiki awakens to a red sky and a world of systems.",
            "The Grail registers as an anomaly to be corrected.",
        ],
        "choices": [
            {
                "label": "Analyze and catalog everything",
                "result": "You secure a strong data foundation.",
                "effects": {"grail_awareness": 1, "system_integrity": 1},
                "flag": "s1_analyze",
            },
            {
                "label": "Set priorities and execute",
                "result": "Action flow becomes efficient and decisive.",
                "effects": {"system_integrity": 2, "humanity_vs_efficiency": -1},
                "flag": "s1_prioritize",
            },
            {
                "label": "Allow one moment of feeling, then process",
                "result": "You retain control without losing your center.",
                "effects": {"humanity_vs_efficiency": 1, "system_integrity": 1},
                "flag": "s1_humanity",
            },
        ],
    },
    {
        "title": "Scene 2: The First Day",
        "text": [
            "The city appears normal, but your perception has changed.",
            "You choose what to build first.",
        ],
        "choices": [
            {
                "label": "Search for territory",
                "result": "A Nawabi structure is marked for control.",
                "effects": {"system_integrity": 2},
                "flag": "s2_territory",
            },
            {
                "label": "Observe other chosen",
                "result": "Early behavioral profiles are recorded.",
                "effects": {"grail_awareness": 1},
                "flag": "s2_patterns",
            },
            {
                "label": "Return home and process",
                "result": "Your baseline remains stable and centered.",
                "effects": {"system_integrity": 1, "humanity_vs_efficiency": 1},
                "flag": "s2_centered",
            },
        ],
    },
    {
        "title": "Scene 3: The First Move",
        "text": [
            "At the chosen structure, Assassin is already watching.",
            "You decide the opening protocol.",
        ],
        "choices": [
            {
                "label": "Activate Core Matrix immediately",
                "result": "You lock the environment before escape is possible.",
                "effects": {"system_integrity": 1, "humanity_vs_efficiency": -1},
                "flag": "s3_instant_matrix",
            },
            {
                "label": "Reveal yourself, then activate",
                "result": "You gain a psychological edge.",
                "effects": {"bond_stella": 1},
                "flag": "s3_psychological",
            },
            {
                "label": "Speak first and offer terms",
                "result": "A dialogue window opens before combat.",
                "effects": {"bond_stella": 1, "humanity_vs_efficiency": 1},
                "flag": "s3_dialogue",
            },
        ],
    },
    {
        "title": "Scene 4: Defeat of Stella",
        "text": [
            "The matrix contains Stella with precision.",
            "Now you define the relationship terms.",
        ],
        "choices": [
            {
                "label": "Offer alliance",
                "result": "Information network starts with trust.",
                "effects": {"bond_stella": 2, "humanity_vs_efficiency": 1},
                "flag": "s4_alliance",
            },
            {
                "label": "Demand service",
                "result": "Obedience rises, trust falls.",
                "effects": {"bond_stella": 1, "humanity_vs_efficiency": -1, "system_integrity": 1},
                "flag": "s4_subordination",
            },
            {
                "label": "Grant freedom with conditions",
                "result": "A distant but cooperative channel forms.",
                "effects": {"bond_stella": 1, "grail_awareness": 1},
                "flag": "s4_distant_alliance",
            },
        ],
    },
    {
        "title": "Scene 5: The Workshop",
        "text": [
            "Your territory expands into a controlled workshop.",
            "Bhool Bhoolaiya is prepared as a containment labyrinth.",
        ],
        "choices": [
            {
                "label": "Maximum traps and segmentation",
                "result": "Containment pressure increases at heavy cost.",
                "effects": {"system_integrity": 2},
                "flag": "s5_max_traps",
            },
            {
                "label": "Adaptive information focus",
                "result": "Pattern learning improves with each exchange.",
                "effects": {"grail_awareness": 1, "bond_stella": 1},
                "flag": "s5_adaptive",
            },
            {
                "label": "Fallback layers for survival",
                "result": "Retreat pathways are secured early.",
                "effects": {"system_integrity": 1, "humanity_vs_efficiency": 1},
                "flag": "s5_fallback",
            },
        ],
    },
    {
        "title": "Scene 6: Information Network",
        "text": [
            "Stella's node feeds citywide observations.",
            "You choose where intelligence capacity is spent.",
        ],
        "choices": [
            {
                "label": "Prioritize Berserker analysis",
                "result": "High-risk fire-pattern data captured.",
                "effects": {"grail_awareness": 1, "system_integrity": 1},
                "flag": "s6_berserker_data",
            },
            {
                "label": "Profile all allies and rivals",
                "result": "Broad readiness against surviving variables.",
                "effects": {"system_integrity": 1},
                "flag": "s6_allied_data",
            },
            {
                "label": "Trace the Grail source",
                "result": "You confirm a waiting presence beyond the war.",
                "effects": {"grail_awareness": 2},
                "flag": "s6_grail_trace",
            },
        ],
    },
    {
        "title": "Scene 7: Hunt Intensifies",
        "text": [
            "Berserker adapts through the labyrinth faster than expected.",
            "Your system is being pushed past design limits.",
        ],
        "choices": [
            {
                "label": "Prepare a final stand",
                "result": "You buy time through concentrated resistance.",
                "effects": {"system_integrity": 1, "humanity_vs_efficiency": -1},
                "flag": "s7_final_stand",
            },
            {
                "label": "Prepare retreat and continuity",
                "result": "Core survival protocol remains intact.",
                "effects": {"system_integrity": 1},
                "flag": "s7_retreat",
            },
            {
                "label": "Prepare to witness and understand",
                "result": "You commit to comprehension over control.",
                "effects": {"grail_awareness": 1, "humanity_vs_efficiency": 1},
                "flag": "s7_witness",
            },
        ],
    },
    {
        "title": "Scene 8: The Fall of Stella",
        "text": [
            "Stella intercepts the impossible and buys your survival.",
            "The system cannot fully process this sacrifice.",
        ],
        "choices": [
            {
                "label": "Suppress grief and continue",
                "result": "Functionality remains high, distance increases.",
                "effects": {"humanity_vs_efficiency": -2},
                "flag": "s8_suppression",
            },
            {
                "label": "Carry the loss and remember",
                "result": "You preserve what she protected.",
                "effects": {"humanity_vs_efficiency": 2, "bond_stella": 1},
                "flag": "s8_humanity",
            },
            {
                "label": "Analyze and plan recovery",
                "result": "Recovery thread becomes your objective.",
                "effects": {"grail_awareness": 1},
                "flag": "s8_recovery_thread",
            },
        ],
    },
    {
        "title": "Scene 9: The Ruins",
        "text": [
            "Your territory is ash, but your will persists.",
            "You decide your next correction target.",
        ],
        "choices": [
            {
                "label": "Find allies and prepare together",
                "result": "Ending focus: Alliance protocol.",
                "effects": {"ending": "Alliance Protocol", "stella_fate": "searching"},
                "flag": "s9_alliance",
            },
            {
                "label": "Find Stella first",
                "result": "Ending focus: Stella recovery.",
                "effects": {"ending": "Stella Recovery", "stella_fate": "bound"},
                "flag": "s9_stella_hunt",
            },
            {
                "label": "Trace the deeper source",
                "result": "Ending focus: Grail mystery hunt.",
                "effects": {"ending": "Mystery Hunt", "stella_fate": "unknown"},
                "flag": "s9_mystery_hunt",
            },
        ],
    },
]
