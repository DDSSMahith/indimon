import pygame
from engine.battle import Battle
from engine.ai import SimpleAI
from engine.team import generate_random_team
from utils.helpers import (
    load_pokemon_data,
    load_moves,
    load_abilities,
    load_learnsets
)
from ui.renderer import BattleRenderer
from ui.buttons import Button, SwitchButton

# --------------------------------------------------
# Pygame setup
# --------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption("Pokémon Battle")
clock = pygame.time.Clock()

# --------------------------------------------------
# Load data
# --------------------------------------------------
pokemon_db = load_pokemon_data("data/pokemon.csv")
move_db = load_moves("data/moves.csv")
abilities = load_abilities("data/abilities.json")
learnsets = load_learnsets("data/learnsets.js")

# --------------------------------------------------
# Create teams
# --------------------------------------------------
player_team = generate_random_team(
    pokemon_db, move_db, abilities, learnsets, "sprites"
)
ai_team = generate_random_team(
    pokemon_db, move_db, abilities, learnsets, "sprites"
)

battle = Battle(player_team, ai_team)
ai = SimpleAI()
renderer = BattleRenderer(screen)

# --------------------------------------------------
# UI state
# --------------------------------------------------
selected_move = None
switch_mode = False
buttons = []

# --------------------------------------------------
# Callbacks
# --------------------------------------------------
def make_move_callback(move):
    def cb():
        global selected_move
        if switch_mode:
            return
        selected_move = move
    return cb


def switch_pokemon(index):
    global switch_mode, buttons

    # ❌ Cannot switch to same Pokémon
    if index == player_team.active_index:
        return

    # ❌ Cannot switch to fainted Pokémon
    if not player_team.pokemon[index].is_alive():
        return

    # ✅ Perform switch
    player_team.switch(index)
    battle.player_active = player_team.get_active()

    switch_mode = False
    buttons = rebuild_buttons()


def toggle_switch():
    global switch_mode, buttons
    switch_mode = True
    buttons = rebuild_buttons()


# --------------------------------------------------
# Button builder
# --------------------------------------------------
def rebuild_buttons():
    btns = []

    # -------------------------------
    # SWITCH MODE (HORIZONTAL)
    # -------------------------------
    if switch_mode:
        x, y = 40, 350
        for i, p in enumerate(player_team.pokemon):
            btns.append(
                SwitchButton(x, y, 140, 50, p, i, switch_pokemon)
            )
            x += 150
        return btns

    # -------------------------------
    # MOVE BUTTONS
    # -------------------------------
    x, y = 40, 380
    for m in battle.player_active.moves:
        btns.append(
            Button(
                x, y, 180, 40,
                m.name,
                make_move_callback(m),
                m.type.lower()
            )
        )
        x += 200

    # -------------------------------
    # SWITCH BUTTON
    # -------------------------------
    btns.append(
        Button(700, 330, 160, 40, "SWITCH", toggle_switch)
    )

    return btns


buttons = rebuild_buttons()

# --------------------------------------------------
# Main game loop
# --------------------------------------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for b in buttons:
            b.handle_event(event)

    # -------------------------------
    # Turn execution
    # -------------------------------
    if selected_move and not switch_mode:
        ai_move = ai.choose_move(battle.ai_active)
        result = battle.execute_turn(selected_move, ai_move)
        selected_move = None

        # PLAYER FAINTED → FORCED SWITCH
        if result == "player_faint":
            switch_mode = True

        # AI FAINTED → AUTO SWITCH
        if result == "ai_faint":
            idx = ai_team.first_alive_index()
            ai_team.switch(idx)
            battle.ai_active = ai_team.get_active()

        buttons = rebuild_buttons()

    # -------------------------------
    # Render
    # -------------------------------
    renderer.draw_battle(
        battle.player_active,
        battle.ai_active
    )

    for b in buttons:
        b.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
