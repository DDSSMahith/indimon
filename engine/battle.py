import random
from utils.type_chart import type_multiplier

LEVEL = 50

class Battle:
    def __init__(self, player_team, ai_team):
        self.player_team = player_team
        self.ai_team = ai_team
        self.player_active = player_team.get_active()
        self.ai_active = ai_team.get_active()

    def calculate_damage(self, attacker, defender, move):
        if move.power == 0:
            return 0

        if random.randint(1, 100) > move.accuracy:
            return 0  # miss

        if move.category == "Physical":
            attack = attacker.stats["attack"]
            defense = defender.stats["defense"]
        else:
            attack = attacker.stats["sp_attack"]
            defense = defender.stats["sp_defense"]

        base_damage = (
            ((2 * LEVEL / 5 + 2) * move.power * (attack / defense)) / 50
        ) + 2

        multiplier = type_multiplier(move.type, defender.types)
        stab = 1.5 if move.type in attacker.types else 1.0

        return int(base_damage * multiplier * stab)

    def execute_turn(self, player_move, ai_move):
        first, first_move, second, second_move = (
            (self.player_active, player_move, self.ai_active, ai_move)
            if self.player_active.stats["speed"] >= self.ai_active.stats["speed"]
            else (self.ai_active, ai_move, self.player_active, player_move)
        )

        damage = self.calculate_damage(first, second, first_move)
        second.take_damage(damage)

        if second.is_alive():
            damage = self.calculate_damage(second, first, second_move)
            first.take_damage(damage)
