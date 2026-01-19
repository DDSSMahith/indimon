import random

class Pokemon:
    def __init__(self, name, types, stats, moves, ability, sprite):
        self.name = name
        self.types = types
        self.stats = stats
        self.max_hp = stats["hp"]
        self.current_hp = stats["hp"]
        self.moves = moves
        self.ability = ability
        self.sprite = sprite
        self.fainted = False

    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp <= 0:
            self.current_hp = 0
            self.fainted = True

    def is_alive(self):
        return not self.fainted
