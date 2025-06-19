from models.game_object import GameObject
import pygame
from settings import TILE_SIZE

class Tile(GameObject):
    def __init__(self, x, y, sprite, solid=False):
        super().__init__(x, y, sprite)
        self.solid = solid
        if solid:
            self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
        else:
            self.rect = self.sprite.get_rect(topleft=(self.x, self.y))

