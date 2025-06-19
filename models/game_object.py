import pygame

class GameObject:
    def __init__(self, x, y, sprite_arg):
        self.x = x
        self.y = y
        if isinstance(sprite_arg, pygame.Surface):
            self.sprite = sprite_arg
        else:
            self.sprite = pygame.image.load(sprite_arg).convert_alpha()
        self.rect = self.sprite.get_rect(topleft=(self.x, self.y))


    def draw(self, surface):
        surface.blit(self.sprite, (self.x, self.y))
