TYPE_CHART = {
    ("Fire", "Grass"): 2.0,
    ("Fire", "Water"): 0.5,
    ("Water", "Fire"): 2.0,
    ("Electric", "Water"): 2.0,
    # extend later
}

def type_multiplier(move_type, defender_types):
    multiplier = 1.0
    for t in defender_types:
        multiplier *= TYPE_CHART.get((move_type, t), 1.0)
    return multiplier
