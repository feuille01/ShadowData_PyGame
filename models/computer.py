import pygame
from models.game_object import GameObject
from settings import SPRITE_COMPUTER, COMPUTER_SCALE
from utils.sprites import load_image

class Computer(GameObject):
    def __init__(self, x, y):
        lock_img = load_image(SPRITE_COMPUTER)
        scaled = pygame.transform.scale_by(lock_img, COMPUTER_SCALE)
        super().__init__(x, y, scaled)
        self.hacked = False


    def try_hack(self, player_rect, hack_game, clock, fps, sound, player):
        if not self.hacked and self.rect.colliderect(player_rect): # если ещё не взломан и игрок у компьютера
            success = hack_game.run(clock, fps)
            if success:
                sound.play_sfx('collect')
                player.hack_computer()
                self.hacked = True
                return True
        return False


    def draw(self, surface):
        if not self.hacked:
            surface.blit(self.sprite, (self.x, self.y))
