import pygame
from engine.ai import SimpleAI
from engine.battle import Battle
from engine.team import generate_random_team
from utils.helpers import (
    load_pokemon_data,
    load_moves,
    load_abilities,
    load_learnsets
)
from ui.renderer import BattleRenderer
from ui.buttons import Button
pygame.init()
screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption("Pokémon Battle")
clock = pygame.time.Clock()

# Load data
pokemon_db = load_pokemon_data("data/pokemon.csv")
move_db = load_moves("data/moves.csv")
abilities = load_abilities("data/abilities.json")
learnsets = load_learnsets("data/learnsets.js")

player_team = generate_random_team(pokemon_db, move_db, abilities, learnsets, "sprites")
ai_team = generate_random_team(pokemon_db, move_db, abilities, learnsets, "sprites")

battle = Battle(player_team, ai_team)
ai = SimpleAI()

renderer = BattleRenderer(screen)

selected_move = None

def make_move_callback(move):
    def callback():
        global selected_move
        selected_move = move
    return callback

def rebuild_buttons():
    buttons = []
    y = 380
    x = 40
    for move in battle.player_active.moves:
        buttons.append(
            Button(x, y, 180, 40, move.name, make_move_callback(move))
        )
        x += 200
    return buttons

buttons = rebuild_buttons()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for btn in buttons:
            btn.handle_event(event)

    if selected_move:
        ai_move = ai.choose_move(battle.ai_active)
        battle.execute_turn(selected_move, ai_move)
        selected_move = None
        buttons = rebuild_buttons()

    renderer.draw_battle(battle.player_active, battle.ai_active)

    for btn in buttons:
        btn.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

