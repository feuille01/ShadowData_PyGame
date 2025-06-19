import pygame
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_FOV, PIXEL_FONT_PATH


def _ray_rect_intersection(px, py, dx, dy, rect):
    # Проверяет, пересекает ли луч границы стены
    ts = []
    # вертикальные грани rect
    if dx != 0:
        for x_edge in (rect.left, rect.right):
            t = (x_edge - px) / dx
            if t > 0:
                y = py + dy * t
                if rect.top <= y <= rect.bottom:
                    ts.append(t)
    # горизонтальные грани rect
    if dy != 0:
        for y_edge in (rect.top, rect.bottom):
            t = (y_edge - py) / dy
            if t > 0:
                x = px + dx * t
                if rect.left <= x <= rect.right:
                    ts.append(t)
    return min(ts) if ts else None


class GameView:
    # Класс для отрисовки игрового мира
    def __init__(self, screen, game_size, game_manager, hud):
        self.screen = screen
        self.game_width, self.game_height = game_size
        self.game_manager = game_manager
        self.hud = hud

    def _draw_light_mask(self, game_surface, light_sources, enemies, level):
        # Полупрозрачная чёрная маска
        mask = pygame.Surface((self.game_width, self.game_height), pygame.SRCALPHA)
        mask.fill((0, 0, 0, 100))  # alpha=100

        # Круги света
        for light in light_sources:
            pygame.draw.circle(
                mask,
                (0, 0, 0, 0),            # полностью прозрачный
                (int(light.x), int(light.y)),
                int(light.radius)
            )

        # Конусы света врагов
        for enemy in enemies:
            cx, cy = enemy.rect.center
            base_angle = {
                'right': 0,
                'down': math.pi / 2,
                'left': math.pi,
                'up': 3 * math.pi / 2,
            }[enemy.direction]
            half_fov = math.radians(ENEMY_FOV / 2)

            num_rays = 30  # чем больше — тем ровнее конус, но медленнее
            angle_step = (half_fov * 2) / (num_rays - 1)

            # Точки полигона: сначала центр
            poly = [(cx, cy)]
            for i in range(num_rays):
                ang = base_angle - half_fov + i * angle_step
                dx, dy = math.cos(ang), math.sin(ang)

                # максимально далекая точка
                max_t = enemy.vision_radius
                # ищем ближайшее пересечение со всеми стенами
                for col in level.collisions:
                    t = _ray_rect_intersection(cx, cy, dx, dy, col)
                    if t is not None and t < max_t:
                        max_t = t
                # конечная точка луча
                poly.append((cx + dx * max_t, cy + dy * max_t))

            pygame.draw.polygon(mask, (0, 0, 0, 0), poly)

        # Тёмная маска
        game_surface.blit(mask, (0, 0))


    def draw(self, player, level, enemies, documents, light_sources, exit_points, elapsed_time, computers, hack_prompts):
        # Очистка
        game_surface = pygame.Surface((self.game_width, self.game_height))
        game_surface.fill((0, 0, 0))

        for tile in level.layered_tiles['ground']:
            tile.draw(game_surface)
        for layer in ['walls3', 'walls4']:
            for tile in level.layered_tiles.get(layer, []):
                tile.draw(game_surface)
        for tile in level.layered_tiles.get('objects_floor', []):
            tile.draw(game_surface)

        # Игрок
        player.draw(game_surface)

        # Враги
        for enemy in enemies:
            enemy.draw(game_surface)

        # Стены над игроком
        for layer in ['walls1', 'walls2']:
            for tile in level.layered_tiles[layer]:
                tile.draw(game_surface)

        for tile in level.layered_tiles.get('objects', []):
            tile.draw(game_surface)

        # Маска света
        self._draw_light_mask(game_surface, light_sources, enemies, level)

        # Документы
        for doc in documents:
            doc.draw(game_surface)

        # Замок компьютера
        for comp in computers:
            comp.draw(game_surface)

        # Точка выхода
        for exit_pt in exit_points:
            exit_pt.draw(self.screen)

        for exit_pt in exit_points:
            exit_pt.draw(game_surface)

        # Масштабирование и вывод на экран
        scaled = pygame.transform.scale(game_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(scaled, (0, 0))

        for rect in hack_prompts:
            font = pygame.font.Font(PIXEL_FONT_PATH, 12)
            text = font.render("Нажмите [E], чтобы начать взлом", True, (255, 255, 0))
            x = rect.centerx - text.get_width() // 2
            y = rect.top - 25
            self.screen.blit(text, (x, y))

        # HUD поверх всего
        score = self.game_manager.calculate_score(player)
        self.hud.draw(self.screen, player, elapsed_time, score)
