from utils.type_chart import type_multiplier
import random

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
            return 0

        if move.category == "Physical":
            attack = attacker.stats["attack"]
            defense = defender.stats["defense"]
        else:
            attack = attacker.stats["sp_attack"]
            defense = defender.stats["sp_defense"]

        base = ((2 * LEVEL / 5 + 2) * move.power * (attack / defense)) / 50 + 2
        stab = 1.5 if move.type.lower() in [t.lower() for t in attacker.types] else 1.0
        mult = type_multiplier(move.type, defender.types)

        return int(base * stab * mult)

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

        return self.check_faint()

    def check_faint(self):
        if self.player_active.fainted:
            if self.player_team.has_alive():
                return "player_faint"
            return "player_lost"

        if self.ai_active.fainted:
            if self.ai_team.has_alive():
                return "ai_faint"
            return "ai_lost"

        return None
