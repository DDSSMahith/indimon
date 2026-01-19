import pygame

TYPE_COLORS = {
    "fire": (240, 128, 48),
    "water": (104, 144, 240),
    "grass": (120, 200, 80),
    "electric": (248, 208, 48),
    "psychic": (248, 88, 136),
    "dark": (112, 88, 72),
    "fairy": (238, 153, 172),
    "poison": (160, 64, 160),
    "normal": (168, 168, 120),
    "fighting": (192, 48, 40),
    "flying": (168, 144, 240),
    "ground": (224, 192, 104),
    "rock": (184, 160, 56),
    "ice": (152, 216, 216),
    "bug": (168, 184, 32),
    "ghost": (112, 88, 152),
    "steel": (184, 184, 208),
    "dragon": (112, 56, 248)
}

class Button:
    def __init__(self, x, y, w, h, text, callback, color_key=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.color_key = color_key
        self.font = pygame.font.SysFont("arial", 16)

    def draw(self, screen):
        color = TYPE_COLORS.get(self.color_key, (240, 240, 240))
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        txt = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()


class SwitchButton(Button):
    def __init__(self, x, y, w, h, pokemon, index, callback):
        super().__init__(x, y, w, h, pokemon.name, lambda: callback(index))
        self.pokemon = pokemon
        self.index = index
        self.preview = pygame.transform.scale(
            pygame.image.load(pokemon.sprite).convert_alpha(),
            (40, 40)
        )

    def draw(self, screen):
        bg = (180, 180, 180) if self.pokemon.fainted else (240, 240, 240)
        pygame.draw.rect(screen, bg, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        # Name
        txt = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(txt, (self.rect.x + 50, self.rect.y + 5))

        # Sprite preview
        screen.blit(self.preview, (self.rect.x + 5, self.rect.y + 5))
