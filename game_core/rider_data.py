RIDER_STATS_TEMPLATE = {
    "rider_route_flags": [],
    "army_strength": 0,
    "bond_nasir": 0,
    "bond_kitik": 0,
    "sacrifice_acceptance": 0,
    "bhaskar_connection": 0,
    "ending": "",
}

RIDER_SCENES = [
    {
        "title": "Scene 1: The Rupture",
        "text": [
            "Fire tears through Atrox as Rider takes root in his Saint Graph.",
            "He feels Bhaskar in Lucknow and chooses how to begin the Iron Path.",
        ],
        "choices": [
            {
                "label": "Move immediately",
                "result": "You leave without delay and reach Lucknow by the first night.",
                "effects": {"bhaskar_connection": 2},
                "flag": "s1_determination",
            },
            {
                "label": "Prepare before departure",
                "result": "You master your new power and depart with an initial force.",
                "effects": {"army_strength": 2, "sacrifice_acceptance": 1},
                "flag": "s1_preparation",
            },
            {
                "label": "Remember then move",
                "result": "Memory hardens your resolve and deepens your reason to fight.",
                "effects": {"bhaskar_connection": 2, "bond_kitik": 1},
                "flag": "s1_resolve",
            },
        ],
    },
    {
        "title": "Scene 2: The Road to Lucknow",
        "text": [
            "The highway becomes the Iron Path under your feet.",
            "Spirits gather as they recognize a king among the wicked.",
        ],
        "choices": [
            {
                "label": "Dominate and conquer them",
                "result": "Your force grows large through fear and force.",
                "effects": {"army_strength": 3, "sacrifice_acceptance": 1},
                "flag": "s2_conquered_army",
            },
            {
                "label": "Accept those who submit",
                "result": "Your force grows slower but with stronger cohesion.",
                "effects": {"army_strength": 2, "bond_nasir": 1},
                "flag": "s2_loyal_army",
            },
            {
                "label": "Ignore them and stay focused",
                "result": "You keep your pace and preserve your intent to reach Bhaskar.",
                "effects": {"army_strength": 1, "bhaskar_connection": 1},
                "flag": "s2_focus",
            },
        ],
    },
    {
        "title": "Scene 3: Arrival in Lucknow",
        "text": [
            "The city hums with six transformed presences under the Grail.",
            "Bhaskar burns like a furnace at the edge of your awareness.",
        ],
        "choices": [
            {
                "label": "Hunt through the night",
                "result": "You strengthen your position before direct contact.",
                "effects": {"army_strength": 2},
                "flag": "s3_night_hunt",
            },
            {
                "label": "Observe the other Servants",
                "result": "You build tactical understanding before committing.",
                "effects": {"bond_nasir": 1, "bond_kitik": 1},
                "flag": "s3_observation",
            },
            {
                "label": "Seek Bhaskar at once",
                "result": "You learn early that he is no longer the boy you knew.",
                "effects": {"bhaskar_connection": 2, "sacrifice_acceptance": 1},
                "flag": "s3_bhaskar_encounter",
            },
        ],
    },
    {
        "title": "Scene 4: The Forest Road",
        "text": [
            "You meet Nasir at dawn, calm and unshaken beneath your pressure.",
            "You decide how to test the man who might reach the unreachable.",
        ],
        "choices": [
            {
                "label": "Block his path",
                "result": "You recognize discipline that does not bend.",
                "effects": {"bond_nasir": 1},
                "flag": "s4_respect",
            },
            {
                "label": "Press him with shadows",
                "result": "He walks through your pressure and proves his composure.",
                "effects": {"bond_nasir": 2, "army_strength": -1},
                "flag": "s4_recognition",
            },
            {
                "label": "Speak and ask his intent",
                "result": "You trust his patience because it is rooted in purpose.",
                "effects": {"bond_nasir": 2, "sacrifice_acceptance": -1},
                "flag": "s4_understanding",
            },
        ],
    },
    {
        "title": "Scene 5: The Bond",
        "text": [
            "After failing to stop Bhaskar, you return wounded but unbroken.",
            "You ask Nasir for help and define how this alliance begins.",
        ],
        "choices": [
            {
                "label": "Ask directly and honestly",
                "result": "Trust forms quickly between you and Nasir.",
                "effects": {"bond_nasir": 2, "sacrifice_acceptance": -1},
                "flag": "s5_trust",
            },
            {
                "label": "Test him one last time",
                "result": "You witness his strike and fully commit to him.",
                "effects": {"bond_nasir": 2, "army_strength": 1},
                "flag": "s5_recognition",
            },
            {
                "label": "Present a practical plan",
                "result": "You establish a disciplined tactical partnership.",
                "effects": {"bond_nasir": 1, "army_strength": 1},
                "flag": "s5_partnership",
            },
        ],
    },
    {
        "title": "Scene 6: The Training",
        "text": [
            "In Kiki's adaptive room, you train with Kitik while Nasir watches.",
            "You choose whether to prioritize bonds, strategy, or sheer growth.",
        ],
        "choices": [
            {
                "label": "Fight Kitik and build trust",
                "result": "Mutual respect with Kitik evolves into combat synergy.",
                "effects": {"bond_kitik": 2},
                "flag": "s6_kitik_bond",
            },
            {
                "label": "Study Nasir's decisive strike",
                "result": "You internalize the rhythm needed for the final opening.",
                "effects": {"bond_nasir": 1, "sacrifice_acceptance": -1},
                "flag": "s6_final_strategy",
            },
            {
                "label": "Fight both and push limits",
                "result": "You become harder to break and harder to ignore.",
                "effects": {"army_strength": 1, "bond_nasir": 1, "bond_kitik": 1},
                "flag": "s6_self_improvement",
            },
        ],
    },
    {
        "title": "Scene 7: The Verdict",
        "text": [
            "Kitik confronts your willingness to die for the plan.",
            "You choose whether to carry that burden alone or stay with your team.",
        ],
        "choices": [
            {
                "label": "Defend the sacrifice plan",
                "result": "Your resolve remains severe, but your team pushes back.",
                "effects": {"sacrifice_acceptance": 2, "bond_kitik": -1},
                "flag": "s7_challenged",
            },
            {
                "label": "Accept Kitik's judgment",
                "result": "You admit fear and choose to live through what comes next.",
                "effects": {"sacrifice_acceptance": -2, "bond_kitik": 1, "bhaskar_connection": 1},
                "flag": "s7_vulnerability",
            },
            {
                "label": "Commit to unity with Nasir and Kitik",
                "result": "You lock in a full team plan for the final encounter.",
                "effects": {"sacrifice_acceptance": -1, "bond_nasir": 1, "bond_kitik": 1},
                "flag": "s7_unity",
            },
        ],
    },
    {
        "title": "Scene 8: The Final Battle",
        "text": [
            "At Bhool Bhoolaiya's ruins, the Burning Sun descends.",
            "You choose your battlefield role as the team seeks one opening.",
        ],
        "choices": [
            {
                "label": "Lead the charge as decoy",
                "result": "Bhaskar focuses on you, creating room for the strike.",
                "effects": {"bhaskar_connection": 1, "army_strength": -1},
                "flag": "s8_decoy",
            },
            {
                "label": "Fight beside Kitik",
                "result": "Your coordination with Kitik stabilizes the front.",
                "effects": {"bond_kitik": 2},
                "flag": "s8_synergy",
            },
            {
                "label": "Guard Nasir's execution window",
                "result": "You protect the one strike that must not fail.",
                "effects": {"bond_nasir": 2, "sacrifice_acceptance": -1},
                "flag": "s8_guardian",
            },
        ],
    },
    {
        "title": "Scene 9: The Sacrifice That Wasn't",
        "text": [
            "At the edge of collapse, your brothers refuse to let you die alone.",
            "You choose what final words to give Bhaskar before the turning point.",
        ],
        "choices": [
            {
                "label": "I never left. I never will.",
                "result": "Bhaskar hesitates as old trust breaks through the fire.",
                "effects": {"bhaskar_connection": 2, "sacrifice_acceptance": -1},
                "flag": "s9_connection",
            },
            {
                "label": "You are not alone. You never were.",
                "result": "Buried memories stir at the edge of his rage.",
                "effects": {"bhaskar_connection": 2, "bond_kitik": 1},
                "flag": "s9_remembrance",
            },
            {
                "label": "I am here. I have always been here.",
                "result": "Your presence alone shifts his focus toward home.",
                "effects": {"bhaskar_connection": 3, "bond_nasir": 1},
                "flag": "s9_presence",
            },
        ],
    },
]
