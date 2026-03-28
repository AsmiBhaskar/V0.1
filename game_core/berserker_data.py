BERSERKER_STATS_TEMPLATE = {
    "berserker_route_flags": [],
    "rage_meter": 0,
    "burning_ache": 0,
    "memory_retention": 3,
    "bond_atrox": 0,
    "reverence_army": 0,
    "saber_presence": 0,
    "ending": "",
}

# Required flags for true ending path checks (special-case route logic).
BERSERKER_TRUE_ENDING_FLAGS = {
    "s1_salvation",
    "s3_salvation",
    "s5_salvation",
    "s6_salvation",
    "s7_salvation",
    "s8_salvation",
    "s9_salvation",
}

BERSERKER_SCENES = [
    {
        "title": "Scene 1: The Rupture",
        "text": [
            "Bhaskar awakens to a corrupted fusion and a fire that does not cool.",
            "The Burning Ache begins, demanding action or feeding on him.",
        ],
        "choices": [
            {
                "label": "Embrace the fire as correction",
                "result": "You accept rage as fuel and strike first.",
                "effects": {"rage_meter": 2, "memory_retention": -1},
                "flag": "s1_aggression",
            },
            {
                "label": "Suppress it and hold control",
                "result": "You keep form for now, though the ache remains.",
                "effects": {"memory_retention": 1, "saber_presence": 1},
                "flag": "s1_control",
            },
            {
                "label": "Understand what the fire is",
                "result": "You name the ache and preserve your humanity.",
                "effects": {"rage_meter": -1, "memory_retention": 2, "saber_presence": 1},
                "flag": "s1_salvation",
            },
        ],
    },
    {
        "title": "Scene 2: The First Day",
        "text": [
            "The city is mapped in heat signatures of five other chosen fighters.",
            "You decide where the first hunt begins.",
        ],
        "choices": [
            {
                "label": "Hunt Kitik first",
                "result": "You win the first clash and feed the fire through combat.",
                "effects": {"rage_meter": 1, "reverence_army": 1},
                "flag": "s2_victory",
                "combat_or_hunt": True,
                "ache_relief": 10,
            },
            {
                "label": "Pressure Kiki's system",
                "result": "You force the system to overprepare while you reposition.",
                "effects": {"saber_presence": 1},
                "flag": "s2_delay",
                "combat_or_hunt": True,
                "ache_relief": 8,
            },
            {
                "label": "Track Atrox from afar",
                "result": "You avoid direct contact and postpone the hardest truth.",
                "effects": {"bond_atrox": 1, "memory_retention": -1},
                "flag": "s2_avoidance",
            },
        ],
    },
    {
        "title": "Scene 3: After the Hunt",
        "text": [
            "In scorched silence, hunger grows if memory does not anchor you.",
            "You choose what remains at your core.",
        ],
        "choices": [
            {
                "label": "Remember Atrox",
                "result": "You hold onto the one bond the fire cannot erase.",
                "effects": {"rage_meter": -1, "memory_retention": 2, "bond_atrox": 2},
                "flag": "s3_salvation",
            },
            {
                "label": "Remember only correction",
                "result": "Purpose hardens while compassion thins.",
                "effects": {"rage_meter": 2, "memory_retention": -1},
                "flag": "s3_purpose",
            },
            {
                "label": "Remember nothing",
                "result": "You surrender identity to pure combustion.",
                "effects": {"rage_meter": 3, "memory_retention": -2, "saber_presence": -1},
                "flag": "s3_emptiness",
            },
        ],
    },
    {
        "title": "Scene 4: The Shadow Spirit",
        "text": [
            "A massive desire-spirit rises at the horizon and answers your rage.",
            "You decide how this correction is carried out.",
        ],
        "choices": [
            {
                "label": "Destroy it completely",
                "result": "The spirit is erased and the ache briefly quiets.",
                "effects": {"rage_meter": 2},
                "flag": "s4_victory",
                "combat_or_hunt": True,
                "ache_relief": 12,
            },
            {
                "label": "Consume it through Reverence",
                "result": "Power rises as another familiar joins your chain.",
                "effects": {"rage_meter": 1, "reverence_army": 2},
                "flag": "s4_reverence",
                "combat_or_hunt": True,
                "ache_relief": 10,
            },
            {
                "label": "Burn it with understanding",
                "result": "You win, but do not fully lose yourself.",
                "effects": {"memory_retention": 1, "saber_presence": 1},
                "flag": "s4_understanding",
                "combat_or_hunt": True,
                "ache_relief": 10,
            },
        ],
    },
    {
        "title": "Scene 5: The Watcher",
        "text": [
            "Stella watches from concealment as the fire surveys the ruins.",
            "You choose why she is allowed to live.",
        ],
        "choices": [
            {
                "label": "Restraint: she is not unjust",
                "result": "You keep one line uncrossed.",
                "effects": {"rage_meter": -1, "memory_retention": 1},
                "flag": "s5_salvation",
            },
            {
                "label": "Purpose: she must witness",
                "result": "You frame destruction as testimony.",
                "effects": {"rage_meter": 1, "saber_presence": 1},
                "flag": "s5_purpose",
            },
            {
                "label": "Confusion: you forgot why",
                "result": "The fire keeps outcomes while reasons disappear.",
                "effects": {"rage_meter": 2, "memory_retention": -1, "saber_presence": -1},
                "flag": "s5_confusion",
            },
        ],
    },
    {
        "title": "Scene 6: The Iron Path",
        "text": [
            "Atrox stands before you at the city line and asks what comes next.",
            "You decide what truth he is allowed to hear.",
        ],
        "choices": [
            {
                "label": "Push him away to protect him",
                "result": "You wound the bond to keep him distant from your fall.",
                "effects": {"rage_meter": 2, "bond_atrox": -1},
                "flag": "s6_protection",
            },
            {
                "label": "Tell him the truth",
                "result": "Honesty opens the only path that can still save you.",
                "effects": {"rage_meter": -1, "memory_retention": 1, "bond_atrox": 2, "saber_presence": 1},
                "flag": "s6_salvation",
            },
            {
                "label": "Say nothing and attack",
                "result": "Silence gives the fire full authority.",
                "effects": {"rage_meter": 3, "memory_retention": -1, "bond_atrox": -1},
                "flag": "s6_silence",
            },
        ],
    },
    {
        "title": "Scene 7: The Battle",
        "text": [
            "You clash with Atrox, fall, recurse, and rise again in fire.",
            "As he retreats, one feeling survives the ash.",
        ],
        "choices": [
            {
                "label": "Relief: he lived",
                "result": "Love survives where rage expected emptiness.",
                "effects": {"rage_meter": -1, "memory_retention": 1, "bond_atrox": 2},
                "flag": "s7_salvation",
                "combat_or_hunt": True,
                "ache_relief": 15,
            },
            {
                "label": "Hunger: not enough",
                "result": "The fire demands another hunt.",
                "effects": {"rage_meter": 2, "memory_retention": -1},
                "flag": "s7_hunger",
                "combat_or_hunt": True,
                "ache_relief": 15,
            },
            {
                "label": "Emptiness: nothing left",
                "result": "You flatten grief into function.",
                "effects": {"rage_meter": 3, "memory_retention": -2, "saber_presence": -1},
                "flag": "s7_emptiness",
                "combat_or_hunt": True,
                "ache_relief": 15,
            },
        ],
    },
    {
        "title": "Scene 8: The Labyrinth",
        "text": [
            "The maze collapses as Stella stands between you and Kiki.",
            "You choose what remains of her after Reverence.",
        ],
        "choices": [
            {
                "label": "Bind her gently and preserve who she was",
                "result": "You refuse to erase courage, even in victory.",
                "effects": {"rage_meter": -1, "memory_retention": 1, "reverence_army": 1, "saber_presence": 2},
                "flag": "s8_salvation",
                "combat_or_hunt": True,
                "ache_relief": 10,
            },
            {
                "label": "Bind her efficiently as a tool",
                "result": "You convert sacrifice into pure utility.",
                "effects": {"rage_meter": 2, "reverence_army": 2},
                "flag": "s8_efficiency",
                "combat_or_hunt": True,
                "ache_relief": 10,
            },
            {
                "label": "Consume her completely",
                "result": "The fire leaves no identity behind.",
                "effects": {"rage_meter": 3, "memory_retention": -2, "reverence_army": 3, "saber_presence": -2},
                "flag": "s8_consumption",
                "combat_or_hunt": True,
                "ache_relief": 10,
            },
        ],
    },
    {
        "title": "Scene 9: The Final Battle",
        "text": [
            "Atrox, Kitik, and Nasir make their stand at dawn.",
            "You choose whether this fight is correction or rescue.",
        ],
        "choices": [
            {
                "label": "Fight to win and correct",
                "result": "You force a victory path through overwhelming rage.",
                "effects": {"rage_meter": 3, "memory_retention": -1},
                "flag": "s9_victory",
                "combat_or_hunt": True,
                "ache_relief": 10,
            },
            {
                "label": "Fight to be reached",
                "result": "You leave an opening for Heaven's Mercy.",
                "effects": {"rage_meter": -1, "memory_retention": 1, "bond_atrox": 2, "saber_presence": 2},
                "flag": "s9_salvation",
                "combat_or_hunt": True,
                "ache_relief": 10,
            },
            {
                "label": "Fight to destroy everything",
                "result": "You invite total consumption, including yourself.",
                "effects": {"rage_meter": 5, "memory_retention": -3, "saber_presence": -2},
                "flag": "s9_destruction",
                "combat_or_hunt": True,
                "ache_relief": 10,
            },
        ],
    },
]
