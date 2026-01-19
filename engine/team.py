import random
import re
from engine.pokemon import Pokemon
from engine.move import Move


class Team:
    def __init__(self, pokemon_list):
        self.pokemon = pokemon_list
        self.active_index = 0

    def get_active(self):
        return self.pokemon[self.active_index]

    def has_alive(self):
        return any(p.is_alive() for p in self.pokemon)

    def switch(self, index):
        if 0 <= index < len(self.pokemon) and self.pokemon[index].is_alive():
            self.active_index = index


# ==================================================
# Move generation with REGEX FALLBACK MATCHING
# ==================================================
def generate_moves(pokemon_key, learnsets, move_db):
    """
    1. Exact key match
    2. Regex fallback (partial similarity)
    3. Guarantees at least one damaging move
    """

    # 1️⃣ Exact match
    pool = learnsets.get(pokemon_key, [])

    # 2️⃣ Regex fallback
    if not pool:
        for key in learnsets:
            if re.search(pokemon_key, key) or re.search(key, pokemon_key):
                pool = learnsets[key]
                break

    if not pool:
        return None

    # Keep only valid moves
    pool = [m for m in pool if m in move_db]

    damaging = [m for m in pool if move_db[m]["power"] > 0]
    if not damaging:
        return None

    chosen = random.sample(pool, min(4, len(pool)))

    # Force at least 1 damaging move
    if not any(move_db[m]["power"] > 0 for m in chosen):
        chosen[0] = random.choice(damaging)

    moves = []
    for m in chosen:
        data = move_db[m]
        moves.append(
            Move(
                name=m,
                move_type=data["type"],
                power=data["power"],
                accuracy=data["accuracy"],
                category=data["category"]
            )
        )

    return moves


# ==================================================
# Random 6v6 team generator (FAIL-SAFE)
# ==================================================
def generate_random_team(
    pokemon_db,
    move_db,
    abilities,
    learnsets,
    sprites_path
):
    team = []
    keys = list(pokemon_db.keys())
    random.shuffle(keys)

    for key in keys:
        moves = generate_moves(key, learnsets, move_db)
        if not moves:
            continue

        data = pokemon_db[key]

        team.append(
            Pokemon(
                name=key.capitalize(),
                types=data["types"],
                stats=data["stats"],
                moves=moves,
                ability=random.choice(abilities),
                sprite=f"{sprites_path}/{key}.png"
            )
        )

        if len(team) == 6:
            break

    if len(team) < 6:
        raise RuntimeError(
            f"Team generation failed ({len(team)}/6 Pokémon). "
            "Check learnsets or name normalization."
        )

    return Team(team)
