import pygame
from models.game_object import GameObject
from settings import SPRITE_DOCUMENT, DOCUMENT_SIZE

class Document(GameObject):
    def __init__(self, x, y):
        sprite = pygame.image.load(SPRITE_DOCUMENT).convert_alpha()
        scaled_sprite = pygame.transform.scale(sprite, (DOCUMENT_SIZE, DOCUMENT_SIZE))
        super().__init__(x, y, scaled_sprite)
        self.collected = False
        self.rect = self.sprite.get_rect(topleft=(self.x, self.y))


    def collect(self, player):
        self.rect.topleft = (self.x, self.y)
        if not self.collected and self.rect.colliderect(player.rect): # если ещё не взяли и игрок у документа
            self.collected = True
            return True
        return False

