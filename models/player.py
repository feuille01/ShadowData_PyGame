import pygame
from models.game_object import GameObject
from utils.sprites import load_animation_strip
from settings import (
    TILE_SIZE, PLAYER_SPEED, PLAYER_LIVES,
    SPRITE_WALK_UP, SPRITE_WALK_DOWN,
    SPRITE_WALK_LEFT, SPRITE_WALK_RIGHT,
    SPRITE_IDLE_UP, SPRITE_IDLE_DOWN,
    SPRITE_IDLE_LEFT, SPRITE_IDLE_RIGHT
)

class Player(GameObject):
    def __init__(self, x, y):
        # загрузка анимаций
        self.walk_frames = {
            'up': load_animation_strip(SPRITE_WALK_UP, TILE_SIZE),
            'down': load_animation_strip(SPRITE_WALK_DOWN, TILE_SIZE),
            'left': load_animation_strip(SPRITE_WALK_LEFT, TILE_SIZE),
            'right': load_animation_strip(SPRITE_WALK_RIGHT, TILE_SIZE),
        }
        self.idle_frames = {
            'up': load_animation_strip(SPRITE_IDLE_UP, TILE_SIZE),
            'down': load_animation_strip(SPRITE_IDLE_DOWN, TILE_SIZE),
            'left': load_animation_strip(SPRITE_IDLE_LEFT, TILE_SIZE),
            'right': load_animation_strip(SPRITE_IDLE_RIGHT, TILE_SIZE),
        }

        # инициализируем спрайт и rect
        super().__init__(x, y, self.idle_frames['down'][0])
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)

        self.speed = PLAYER_SPEED
        self.direction = 'down'
        self.frame_index = 0
        self.frame_timer = 0.0
        self.frame_delay = 0.15
        self.moving = False
        self.documents_collected = 0
        self.hacked_computers = 0
        self.lives = PLAYER_LIVES


    def move(self, dx, dy, level):
        self.moving = (dx != 0 or dy != 0)
        if not self.moving:
            return

        # рассчитываем новый rect
        step_x = dx * self.speed
        step_y = dy * self.speed
        new_rect = self.rect.move(step_x, step_y)

        # проверяем коллизии
        if any(new_rect.colliderect(col) for col in level.collisions):
            # упёрлись — не двигаемся
            return

        # свободно — обновляем координаты
        self.rect = new_rect
        self.x, self.y = self.rect.topleft

        # направления для анимации
        if dx > 0:
            self.direction = 'right'
        elif dx < 0:
            self.direction = 'left'
        elif dy > 0:
            self.direction = 'down'
        elif dy < 0:
            self.direction = 'up'


    def collect_document(self):
        self.documents_collected += 1


    def hack_computer(self):
        self.hacked_computers += 1


    def lose_life(self):
        self.lives -= 1


    def update(self, level, dt):
        # анимация
        if self.moving:
            self.frame_timer += dt
            if self.frame_timer >= self.frame_delay:
                self.frame_timer = 0.0
                self.frame_index = (
                    self.frame_index + 1
                ) % len(self.walk_frames[self.direction])
            self.sprite = self.walk_frames[self.direction][self.frame_index]
        else:
            self.frame_index = 0
            self.sprite = self.idle_frames[self.direction][0]

        self.moving = False
