ARCHER_STATS_TEMPLATE = {
    "archer_route_flags": [],
    "bond_girlfriend": 0,
    "bond_atrox": 0,
    "humility_pride": 0,
    "grand_verdict_readiness": 0,
    "seen_heard": 0,
    "ending": "",
    "archer_opening_berserker_done": False,
    "archer_training_lancer_won": False,
    "archer_final_berserker_won": False,
    "archer_combat_attempts": 0,
}

ARCHER_SCENES = [
    {
        "title": "Scene 1: The Rupture",
        "text": [
            "Kitik awakens to a red sky and a voice in his soul.",
            "Fusion completes, and Grand Verdict answers his call.",
        ],
        "choices": [
            {
                "label": "Exhilaration: finally being seen",
                "result": "Pride surges through your voice.",
                "effects": {"humility_pride": 2, "seen_heard": 1},
                "flag": "s1_pride",
            },
            {
                "label": "Fear: hold the power back",
                "result": "You contain the song and survive the shock.",
                "effects": {"humility_pride": -1, "grand_verdict_readiness": 1},
                "flag": "s1_fear",
            },
            {
                "label": "Determination: endure and adapt",
                "result": "You settle into a balanced stance.",
                "effects": {"humility_pride": 0, "seen_heard": 1, "grand_verdict_readiness": 1},
                "flag": "s1_resolve",
            },
        ],
    },
    {
        "title": "Scene 2: The First Day",
        "text": [
            "The city keeps moving, but the song inside you grows.",
            "You decide how to prepare before first blood.",
        ],
        "choices": [
            {
                "label": "Go out and be seen",
                "result": "Your presence starts drawing attention.",
                "effects": {"seen_heard": 2, "humility_pride": 1},
                "flag": "s2_visibility",
            },
            {
                "label": "Stay home and sing",
                "result": "Your control stabilizes in solitude.",
                "effects": {"grand_verdict_readiness": 1},
                "flag": "s2_centered",
            },
            {
                "label": "Go to your girlfriend",
                "result": "Your core bond strengthens early.",
                "effects": {"bond_girlfriend": 2, "seen_heard": 1},
                "flag": "s2_bond",
            },
        ],
    },
    {
        "title": "Scene 3: The Attack",
        "text": [
            "The Burning Sun attacks without warning.",
            "You are outmatched and forced into defeat.",
        ],
        "choices": [
            {
                "label": "Fight to the last",
                "result": "Your voice rings out even in collapse.",
                "effects": {"humility_pride": 1, "seen_heard": 1},
                "flag": "s3_last_stand",
            },
            {
                "label": "Retreat and survive",
                "result": "You preserve yourself for what comes next.",
                "effects": {"grand_verdict_readiness": 1},
                "flag": "s3_retreat",
            },
            {
                "label": "Accept defeat and learn",
                "result": "Humility becomes a weapon.",
                "effects": {"humility_pride": -1, "grand_verdict_readiness": 2},
                "flag": "s3_humility",
            },
        ],
    },
    {
        "title": "Scene 4: The Bond",
        "text": [
            "In the dark, she finds you and refuses to let you disappear.",
            "A Command Seal appears as a shared promise.",
        ],
        "choices": [
            {
                "label": "Ask her to stay",
                "result": "Your trust deepens through vulnerability.",
                "effects": {"bond_girlfriend": 2, "seen_heard": 1},
                "flag": "s4_stay",
            },
            {
                "label": "Ask for command-seal intervention",
                "result": "Emergency support path unlocked.",
                "effects": {"bond_girlfriend": 1, "grand_verdict_readiness": 1},
                "flag": "s4_command_seal",
            },
            {
                "label": "Ask her to trust your strength",
                "result": "Resolve hardens under pressure.",
                "effects": {"bond_girlfriend": 1, "humility_pride": 1},
                "flag": "s4_trust_me",
            },
        ],
    },
    {
        "title": "Scene 5: Encounter with Rider",
        "text": [
            "Atrox appears in the night with shadows in tow.",
            "You must define the tone of the encounter.",
        ],
        "choices": [
            {
                "label": "Stand your ground",
                "result": "Atrox recognizes your nerve.",
                "effects": {"bond_atrox": 1, "seen_heard": 1},
                "flag": "s5_ground",
            },
            {
                "label": "Speak first and set terms",
                "result": "Mutual honor tempers hostility.",
                "effects": {"bond_atrox": 2},
                "flag": "s5_honor",
            },
            {
                "label": "Prepare for battle immediately",
                "result": "Readiness over trust.",
                "effects": {"grand_verdict_readiness": 1},
                "flag": "s5_readiness",
            },
        ],
    },
    {
        "title": "Scene 6: The Verdict",
        "text": [
            "Atrox falls at your feet, but you choose not to kill him.",
            "Mercy becomes your declaration.",
        ],
        "choices": [
            {
                "label": "Spare him because you see yourself in him",
                "result": "Shared burden creates understanding.",
                "effects": {"bond_atrox": 2, "humility_pride": -1},
                "flag": "s6_understanding",
            },
            {
                "label": "Spare him because mercy was shown to you",
                "result": "You carry mercy forward.",
                "effects": {"seen_heard": 1, "bond_atrox": 1},
                "flag": "s6_honor",
            },
            {
                "label": "Spare him because war is more than killing",
                "result": "You reject the Grail's simplest logic.",
                "effects": {"humility_pride": -1, "grand_verdict_readiness": 1},
                "flag": "s6_wisdom",
            },
        ],
    },
    {
        "title": "Scene 7: The Alliance",
        "text": [
            "Training begins in Kiki's room with Atrox and Nasir.",
            "You choose where to invest your growth.",
        ],
        "choices": [
            {
                "label": "Focus on Atrox and his rhythm",
                "result": "Combination potential rises.",
                "effects": {"bond_atrox": 2},
                "flag": "s7_atrox",
            },
            {
                "label": "Focus on Nasir and support role",
                "result": "You align with the final spearpoint.",
                "effects": {"seen_heard": 1, "grand_verdict_readiness": 1},
                "flag": "s7_nasir",
            },
            {
                "label": "Focus on your own art",
                "result": "Grand Verdict sharpens.",
                "effects": {"grand_verdict_readiness": 2, "humility_pride": 1},
                "flag": "s7_self",
            },
        ],
    },
    {
        "title": "Scene 8: The Revelation",
        "text": [
            "Your court reveals Atrox's plan to die.",
            "You reject solitary sacrifice.",
        ],
        "choices": [
            {
                "label": "Reject it through empathy",
                "result": "You speak as someone who knows loneliness.",
                "effects": {"bond_atrox": 1, "humility_pride": -1},
                "flag": "s8_empathy",
            },
            {
                "label": "Reject it through determination",
                "result": "You demand a future where allies live.",
                "effects": {"bond_atrox": 1, "seen_heard": 1},
                "flag": "s8_determination",
            },
            {
                "label": "Reject it through tactics",
                "result": "Nasir-centered strategy is locked in.",
                "effects": {"grand_verdict_readiness": 1, "bond_atrox": 1},
                "flag": "s8_tactics",
            },
        ],
    },
    {
        "title": "Scene 9: The Final Battle",
        "text": [
            "Bhool Bhoolaiya burns as the last stand begins.",
            "You choose your battlefield role.",
        ],
        "choices": [
            {
                "label": "Guard Nasir",
                "result": "Ending focus: Guardian.",
                "effects": {"ending": "Guardian Verdict", "bond_atrox": 1},
                "flag": "s9_guardian",
            },
            {
                "label": "Pressure Bhaskar relentlessly",
                "result": "Ending focus: Relentless.",
                "effects": {"ending": "Relentless Verdict", "seen_heard": 2},
                "flag": "s9_relentless",
            },
            {
                "label": "Hold for the decisive opening",
                "result": "Ending focus: Patience.",
                "effects": {"ending": "Patient Verdict", "grand_verdict_readiness": 1},
                "flag": "s9_patience",
            },
        ],
    },
]
