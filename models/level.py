import pygame
import re
from utils.tiled_Loader import load_tiled_map
from models.tile import Tile
from settings import TILE_SIZE

class Level:
    def __init__(self, map_path, gid_map):
        data = load_tiled_map(map_path)

        self.width  = data['width']
        self.height = data['height']

        # тайлы
        self.layered_tiles = {
            'ground': [], 'objects_floor': [],
            'walls1': [], 'walls2': [], 'objects': [],
            'walls3': [], 'walls4': []
        }

        self.collisions = []    # коллизии
        self.objects = []       # точки спавна, выхода, взлома
        self.patrol_paths = {}  # маршруты патруля врагов

        # TILE-слои
        # пропускаем всё, кроме нужных слоёв, указанных в self.layered_tiles
        for layer in data['layers']:
            if layer['type'] != 'tilelayer' or layer['name'] not in self.layered_tiles:
                continue
            name = layer['name']
            for idx, gid in enumerate(layer['data']):
                if gid == 0:
                    continue
                sprite = gid_map.get(gid)
                if not sprite:  # неизвестный тайл
                    continue
                col, row = idx % self.width, idx // self.width
                x, y = col * TILE_SIZE, row * TILE_SIZE
                self.layered_tiles[name].append(Tile(x, y, sprite, solid=False))

        # OBJECT-слои
        for layer in data['layers']:
            if layer['type'] != 'objectgroup':
                continue

            for obj in layer['objects']:
                props = {p['name']: p['value'] for p in obj.get('properties', [])}
                u_type = props.get('type') or obj.get('type') \
                         or obj.get('class') or obj.get('name')

                if u_type == 'Collision':
                    w, h = obj['width'], obj['height']
                    if w == 0 or h == 0:
                        tx = int(obj['x']) // TILE_SIZE
                        ty = int(obj['y']) // TILE_SIZE
                        rect = pygame.Rect(tx * TILE_SIZE, ty * TILE_SIZE,
                                           TILE_SIZE, TILE_SIZE)
                    else:
                        rect = pygame.Rect(obj['x'], obj['y'], w, h)
                    self.collisions.append(rect)
                    continue

                if u_type == 'PatrolPath':
                    name = obj.get('name') or props.get('name')
                    if not name:
                        continue
                    base_x, base_y = obj['x'], obj['y']
                    pts = [(base_x + pt['x'], base_y + pt['y'])
                           for pt in obj['polyline']]
                    self.patrol_paths[name] = pts
                    continue

                entry = {'type': u_type,
                         'x': obj['x'],
                         'y': obj['y'],
                         'name': obj.get('name', ''), **props
                         }

                # К EnemySpawn прикрепляем маршрут
                if u_type == 'EnemySpawn':
                    entry['patrol'] = self._attach_patrol(entry)

                self.objects.append(entry)


    # вспомогательный метод выбора подходящего маршрута
    def _attach_patrol(self, enemy: dict) -> list[tuple[float, float]]:
        """
        Возвращает список точек polyline, который должен использовать EnemySpawn.
        Проверяет:
        1) пользовательское свойство path="Guard1Path"
        2) совпадение номера в именах enemy_01 -> Guard1Path
        3) кратчайшая дистанция до 1-й точки polyline
        Если ничего не нашли — враг остаётся на месте.
        """

        if 'path' in enemy:
            return self.patrol_paths.get(str(enemy['path']), [])

        # проверка совпадения номера
        m = re.search(r'(\d+)', enemy.get('name', '')) # поиск числа в имени врага
        if m:
            num = m.group(1).lstrip('0')  # '04' -> '4'
            for pname in self.patrol_paths:
                if num and num in pname:
                    return self.patrol_paths[pname]

        # ближайший polyline
        if self.patrol_paths:
            ex, ey = enemy['x'], enemy['y']
            best_name = min(self.patrol_paths,
                            key=lambda n: (self.patrol_paths[n][0][0] - ex) ** 2 +
                                          (self.patrol_paths[n][0][1] - ey) ** 2)
            return self.patrol_paths[best_name]

        # маршрутов нет вообще
        return []