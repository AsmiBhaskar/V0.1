from combat.servants.atrox_servant import make_atrox
from combat.servants.bhaskar_servant import make_bhaskar
from combat.servants.kiki_servant import make_kiki
from combat.servants.kitik_servant import make_kitik
from combat.servants.nasir_servant import make_nasir
from combat.servants.stella_servant import make_stella

ENCOUNTERS = {
    "lancer_vs_archer": {
        "player_fn": make_nasir,
        "enemy_fn": lambda: make_kitik(is_enemy=True),
        "title": "ENCOUNTER - THE UNIGNORABLE VERDICT",
        "context": {"route": "Lancer", "spirit_hunt": False, "ache_active": False},
    },
    "lancer_vs_berserker": {
        "player_fn": make_nasir,
        "enemy_fn": lambda: make_bhaskar(is_enemy=True),
        "title": "ENCOUNTER - THE BURNING SUN",
        "context": {"route": "Lancer", "spirit_hunt": False, "ache_active": False},
    },
    "archer_vs_lancer": {
        "player_fn": make_kitik,
        "enemy_fn": lambda: make_nasir(is_enemy=True),
        "title": "ENCOUNTER - THE UNBROKEN AXIS",
        "context": {"route": "Archer", "spirit_hunt": False, "ache_active": False},
    },
    "caster_vs_assassin": {
        "player_fn": make_kiki,
        "enemy_fn": lambda: make_stella(is_enemy=True),
        "title": "ENCOUNTER - THE LEGEND EATER",
        "context": {"route": "Caster", "spirit_hunt": False, "ache_active": False},
    },
    "assassin_vs_caster": {
        "player_fn": make_stella,
        "enemy_fn": lambda: make_kiki(is_enemy=True),
        "title": "ENCOUNTER - THE SILENT ADMINISTRATOR",
        "context": {"route": "Assassin", "spirit_hunt": False, "ache_active": False},
    },
    "rider_spirit_hunt": {
        "player_fn": make_atrox,
        "enemy_fn": None,
        "title": "HUNT - A SPIRIT ENTERS THE IRON PATH",
        "context": {"route": "Rider", "spirit_hunt": True, "ache_active": False},
    },
    "berserker_ache_fight": {
        "player_fn": make_bhaskar,
        "enemy_fn": None,
        "title": "THE FIRE WITHIN - BURNING ACHE COMBAT",
        "context": {"route": "Berserker", "spirit_hunt": False, "ache_active": True},
    },
}
