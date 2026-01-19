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

    def first_alive_index(self):
        for i, p in enumerate(self.pokemon):
            if p.is_alive():
                return i
        return None

    def switch(self, index):
        if 0 <= index < len(self.pokemon) and self.pokemon[index].is_alive():
            self.active_index = index


def generate_moves(pokemon_key, learnsets, move_db):
    pool = learnsets.get(pokemon_key, [])

    if not pool:
        for key in learnsets:
            if re.search(pokemon_key, key) or re.search(key, pokemon_key):
                pool = learnsets[key]
                break

    if not pool:
        return None

    pool = [m for m in pool if m in move_db]
    damaging = [m for m in pool if move_db[m]["power"] > 0]

    if not damaging:
        return None

    chosen = random.sample(pool, min(4, len(pool)))
    if not any(move_db[m]["power"] > 0 for m in chosen):
        chosen[0] = random.choice(damaging)

    moves = []
    for m in chosen:
        d = move_db[m]
        moves.append(
            Move(m, d["type"], d["power"], d["accuracy"], d["category"])
        )

    return moves


def generate_random_team(pokemon_db, move_db, abilities, learnsets, sprites_path):
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
        raise RuntimeError("Team generation failed")

    return Team(team)
