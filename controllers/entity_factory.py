# Модуль для создания игровых сущностей: игрока, документов, врагов и источников света

from models.light_source import LightSource
from models.player import Player
from models.document import Document
from models.enemy import Enemy
from models.computer import Computer
from settings import ENEMY_VISION_RADIUS, DETECTION_TIME, CHASE_TIMEOUT


def init_entities(level, pathfinder):
    player = []
    documents = []
    enemies = []
    light_sources = []
    exit_points = []
    computers = []

    for ent in level.objects:
        t = ent['type']
        x, y = ent['x'], ent['y']
        if t == 'PlayerSpawn':
            player = Player(x, y)
        elif t == 'DocumentSpawn':
            documents.append(Document(x, y))
        elif t == 'EnemySpawn':
            patrol = ent.get('patrol', []) # Получение маршрута патрулирования
            enemies.append(Enemy(
                x, y,
                patrol,
                pathfinder,   # алгоритм для погони
                vision_radius=ENEMY_VISION_RADIUS,
                detection_time=DETECTION_TIME,
                chase_timeout=CHASE_TIMEOUT
            ))
        elif t == 'LightSource':
            # Источник света (радиус 100)
            radius = float(ent.get('radius', 100))
            light_sources.append(LightSource(x, y, radius))
        elif t == 'ComputerHack':
            # Компьютеры, которые можо взломать
            computers.append(Computer(x, y))
        elif t == 'ExitSpawn':
            # Точка выхода с уровня
            from models.exit_point import ExitPoint
            exit_points.append(ExitPoint(x, y))

    # Возврат созданных сущностей в виде кортежа
    return player, documents, enemies, light_sources, exit_points, computers
