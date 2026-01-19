import random

class SimpleAI:
    def choose_move(self, pokemon):
        return random.choice(pokemon.moves)
