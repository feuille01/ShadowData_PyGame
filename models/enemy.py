import math
import pygame
from pygame.math import Vector2
from models.game_object import GameObject
from utils.sprites import load_animation_strip, load_image
from settings import (
    TILE_SIZE, ENEMY_SPEED,
    SPRITE_ENEMY_WALK_UP, SPRITE_ENEMY_WALK_DOWN,
    SPRITE_ENEMY_WALK_LEFT, SPRITE_ENEMY_WALK_RIGHT,
    SPRITE_ENEMY_IDLE_UP, SPRITE_ENEMY_IDLE_DOWN,
    SPRITE_ENEMY_IDLE_LEFT, SPRITE_ENEMY_IDLE_RIGHT,
    ENEMY_FOV, ENEMY_VISION_RADIUS
)

class Enemy(GameObject):
    def __init__(self, x, y, patrol_path, pathfinder,
                 vision_radius, detection_time, chase_timeout):
        # Если нет точек патруля — остаёмся на месте
        if not patrol_path:
            patrol_path = [(x, y)]

        # Загрузка анимаций
        self.walk_frames = {
            'up':    load_animation_strip(SPRITE_ENEMY_WALK_UP,    TILE_SIZE),
            'down':  load_animation_strip(SPRITE_ENEMY_WALK_DOWN,  TILE_SIZE),
            'left':  load_animation_strip(SPRITE_ENEMY_WALK_LEFT,  TILE_SIZE),
            'right': load_animation_strip(SPRITE_ENEMY_WALK_RIGHT, TILE_SIZE),
        }
        self.idle_frames = {
            'up':    load_animation_strip(SPRITE_ENEMY_IDLE_UP,    TILE_SIZE),
            'down':  [load_image(SPRITE_ENEMY_IDLE_DOWN)],
            'left':  load_animation_strip(SPRITE_ENEMY_IDLE_LEFT,  TILE_SIZE),
            'right': load_animation_strip(SPRITE_ENEMY_IDLE_RIGHT, TILE_SIZE),
        }

        # Инициализируем базовый класс спрайтом вниз
        super().__init__(x, y, self.idle_frames['down'][0])
        self.rect.topleft = (self.x, self.y)

        # Анимационные параметры
        self.direction    = 'down'
        self.frame_index  = 0       # индекс текущего кадра анимации
        self.frame_timer  = 0.0     # времени с момента последнего переключения кадра
        self.frame_delay  = 0.15    # пауза между кадрами анимации (сек)

        # Патруль
        self.patrol_path          = patrol_path
        self.current_patrol_index = 0
        self.speed                = ENEMY_SPEED
        self.pathfinder           = pathfinder

        # Детекция игрока
        self.vision_radius   = vision_radius
        self.detection_time  = detection_time
        self.detection_timer = 0.0

        # Погони
        self.chase_timeout       = chase_timeout
        self.chasing             = False
        self.chase_path          = []    # список точек маршрута
        self.current_chase_index = 0     # индекс точки преследования
        self.chase_timer         = 0     # время после ухода игрока из зоны
        self.recalc_interval     = 0.5   # пересчёт пути каждые 0.5 с
        self.recalc_timer        = 0.0

        # Застревание
        self.stuck_timer         = 0.0   # сколько времени не двигаемся
        self.STUCK_LIMIT         = 0.5   # сек без движения -> считаем застрял


    def detect_player(self, player, level):
        # Игрок вплотную к врагу – считаем, что виден.
        if self.rect.colliderect(player.rect):
            return True

        # Расстояние и направление до игрока
        enemy_pos = Vector2(self.x + self.rect.width/2, self.y + self.rect.height/2)    # центр спрайта
        player_pos = Vector2(player.x + player.rect.width/2, player.y + player.rect.height/2) # центр спрайта
        to_player = player_pos - enemy_pos  # в какую сторону идти до игрока
        dist_sq = to_player.length_squared()

        # Проверка радиуса
        if dist_sq > ENEMY_VISION_RADIUS ** 2:  # проверка расстояния до игрока
            return False
        dist = math.sqrt(dist_sq)  # если игрок в радиусе - извлекаем корень

        # Проверка угла (FOV)
        # вектор направления взгляда
        if self.direction == 'up':
            dir_vec = Vector2(0, -1)
        elif self.direction == 'down':
            dir_vec = Vector2(0, 1)
        elif self.direction == 'left':
            dir_vec = Vector2(-1, 0)
        else:  # 'right'
            dir_vec = Vector2(1, 0)

        cos_half_fov = math.cos(math.radians(ENEMY_FOV / 2))
        cos_theta = dir_vec.dot(to_player) / dist

        # проверка нахождения игрока в угле обзора врага
        if cos_theta < cos_half_fov:
            return False

        # Отрезок разбивается на шаги и проверяется, не преграждает ли путь коллизия (raycasting)
        steps = int(dist / (TILE_SIZE / 2)) # определение количества шагов
        steps = max(1, steps)               # шагов > 0
        step_vec = to_player / steps        # куда идти и на сколько шагов
        sample = Vector2(enemy_pos)         # начальная позиция врага

        for _ in range(steps):
            sample += step_vec  # каждый шаг сдвигаемся на step_vec
            point = (int(sample.x), int(sample.y))  # получение пиксельной точки (целые числа)
            for col in level.collisions:
                if col.collidepoint(point): # Если хотя бы одна точка луча пересекает препятствие -> игрок не виден
                    return False
        # игрок виден
        return True


    def _start_chase(self, player):
        start = (int(self.x)//TILE_SIZE, int(self.y)//TILE_SIZE)
        goal  = (int(player.x)//TILE_SIZE, int(player.y)//TILE_SIZE)

        path = self.pathfinder.find_path(start, goal)

        if path:  # если есть путь
            # Конвертируем в пиксели (центр тайла)
            self.chase_path = [
                (tx * TILE_SIZE + TILE_SIZE / 2,  # движение по центру тайлов
                 ty * TILE_SIZE + TILE_SIZE / 2)
                for tx, ty in path
            ]
            self.current_chase_index = 0


    def update(self, level, player, dt, sound=None):
        # Детекция и пересчёт пути
        if self.detect_player(player, level):
            self.detection_timer += dt      # таймер обнаружения для урона
            self.chase_timer = 0.0          # видим цель -> обнуляем таймер
            if not self.chasing:
                self.chasing = True         # входим в режим погони
                self._start_chase(player)   # строим первый маршрут
            else:
                # пересчёт маршрута по таймеру
                self.recalc_timer += dt
                if self.recalc_timer >= self.recalc_interval or not self.chase_path:
                    self.recalc_timer = 0.0
                    self._start_chase(player)
        else:   # игрок не в поле зрения
            self.detection_timer = 0.0  # сброс таймера обнаружения
            if self.chasing:
                # считаем, сколько времени не видим цель
                self.chase_timer += dt
                if self.chase_timer >= self.chase_timeout:
                    # таймаут вышел — сбрасываем режим погони
                    self.chasing = False
                    self.chase_path = []
                    self.current_chase_index = 0
                    self.chase_timer = 0.0

        # Урон игроку
        if self.detection_timer >= self.detection_time:
            player.lose_life()
            sound.play_sfx('hit')
            self.detection_timer = 0.0
            self.detection_timer = 0.0

        # Определение погоня или патрульный маршрут
        if self.chasing and self.chase_path:    # в режиме погони и есть маршрут до игрока
            # дошли до конца пути - пробуем достроить ещё раз, если игрок в зоне видимости
            if self.current_chase_index >= len(self.chase_path):
                self._start_chase(player)
            # если путь построился - идём на следующую точку маршрута погони
            if self.current_chase_index < len(self.chase_path):
                tx, ty = self.chase_path[self.current_chase_index]
            else:
                # путь не найден - стоим на месте без выхода из погони пока не закончится chase_timeout
                tx, ty = self.x, self.y
        else:  # не в режиме погони - обычный патруль
            tx, ty = self.patrol_path[self.current_patrol_index]

        # Пошаговое движение с приоритетом главной оси и проверкой коллизий
        dx = tx - self.x    # количество шагов по x
        dy = ty - self.y    # количество шагов по y
        moved = False

        # Определяем направление анимации для диагонального движения
        if dx != 0 and dy != 0:
            self.direction = 'right' if dx > 0 else 'left'
        else:
            # Не диагональное движение: определяем направление по главной оси
            if abs(dx) > abs(dy):
                self.direction = 'right' if dx > 0 else 'left'
            elif dy != 0:
                self.direction = 'down' if dy > 0 else 'up'

        # сначала двигаемся по x, если не получилось, то по y
        if abs(dx) > abs(dy):
            axes = (('x', dx), ('y', dy))
        else:
            axes = (('y', dy), ('x', dx))

        # двигаемся по одной оси за раз
        for axis, delta in axes:
            if delta == 0:
                continue
            # шаг по оси
            step = math.copysign(self.speed, delta)
            if axis == 'x':     # проверка нет ли коллизий, если сдвинуться на один шаг по x
                new_x = self.x + step
                new_rect = pygame.Rect(int(new_x), int(self.y), self.rect.width, self.rect.height)
                self.direction = 'right' if step > 0 else 'left'  # направление анимации
            else:
                new_y = self.y + step
                new_rect = pygame.Rect(
                    int(self.x), int(new_y),
                    self.rect.width, self.rect.height
                )
                self.direction = 'down' if step > 0 else 'up'

            # проверяем все стены, если нет пересечений - двигаемся
            if not any(new_rect.colliderect(col) for col in level.collisions):
                # двигаемся и обновляем позицию
                if axis == 'x':
                    self.x = new_x
                else:
                    self.y = new_y
                self.rect.topleft = (int(self.x), int(self.y))
                moved = True
                break

        # Обработка застревания, если moved = False
        if moved:
            self.stuck_timer = 0.0
        else:
            self.stuck_timer += dt
            if self.stuck_timer >= self.STUCK_LIMIT:
                if self.chasing:
                    self._start_chase(player)
                else:
                    self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_path)
                self.stuck_timer = 0.0

        # Смена точки при достижении цели
        if moved and math.hypot(tx - self.x, ty - self.y) < self.speed:
            if self.chasing:    # враг в режиме погони
                self.current_chase_index += 1
            else:               # враг патрулирует
                self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_path)
            return

        # Анимация
        if not moved:
            self.direction = 'down'
            self.frame_timer = 0.0
            self.frame_index = 0
            self.sprite = self.idle_frames['down'][0]
            return
        # Анимация при движении
        self.frame_timer += dt
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0.0
            # зацикливаем кадры анимации
            self.frame_index = (self.frame_index + 1) % len(self.walk_frames[self.direction])
        self.sprite = self.walk_frames[self.direction][self.frame_index]

