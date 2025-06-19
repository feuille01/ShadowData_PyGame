import pygame
from models.game_object import GameObject
from settings import SPRITE_EXIT, EXIT_SIZE

class ExitPoint(GameObject):
    # Точка выхода из уровня
    def __init__(self, x, y):
        img = pygame.image.load(SPRITE_EXIT).convert_alpha()
        sprite = pygame.transform.scale(img, (EXIT_SIZE, EXIT_SIZE))
        super().__init__(x, y, sprite)
        self.rect = self.sprite.get_rect(topleft=(x, y))


    def draw(self, surface):
        surface.blit(self.sprite, (self.x, self.y))