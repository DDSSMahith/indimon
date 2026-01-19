import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (80, 200, 120)
RED = (220, 80, 80)

class BattleRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 20)
        self.background = pygame.Surface(screen.get_size())
        self.background.fill((235, 235, 235))

    def draw_hp_bar(self, x, y, w, h, cur, maxhp):
        pygame.draw.rect(self.screen, BLACK, (x, y, w, h), 2)
        ratio = cur / maxhp
        color = GREEN if ratio > 0.5 else RED
        pygame.draw.rect(
            self.screen, color,
            (x + 2, y + 2, int((w - 4) * ratio), h - 4)
        )

    def draw_pokemon(self, pokemon, pos, flip=False):
        sprite = pygame.image.load(pokemon.sprite).convert_alpha()
        sprite = pygame.transform.scale(sprite, (160, 160))
        if flip:
            sprite = pygame.transform.flip(sprite, True, False)
        self.screen.blit(sprite, pos)

    def draw_status_box(self, pokemon, x, y):
        pygame.draw.rect(self.screen, WHITE, (x, y, 220, 60))
        pygame.draw.rect(self.screen, BLACK, (x, y, 220, 60), 2)
        self.screen.blit(
            self.font.render(pokemon.name, True, BLACK),
            (x + 10, y + 5)
        )
        self.draw_hp_bar(
            x + 10, y + 30, 200, 15,
            pokemon.current_hp, pokemon.max_hp
        )

    def draw_battle(self, player_poke, ai_poke):
        self.screen.blit(self.background, (0, 0))

        # ✅ FIXED ORIENTATION
        self.draw_pokemon(player_poke, (100, 220), flip=True)
        self.draw_pokemon(ai_poke, (520, 120), flip=False)

        self.draw_status_box(player_poke, 60, 160)
        self.draw_status_box(ai_poke, 520, 40)
