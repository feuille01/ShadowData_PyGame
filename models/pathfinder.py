import heapq
from settings import TILE_SIZE

class PathFinder:
    # A* для поиска пути
    def __init__(self, level):
        # размеры уровня в тайлах
        self.width  = level.width
        self.height = level.height

        # инициализируем матрицу проходимости клеток
        self.walkable = [[True] * self.width for _ in range(self.height)]
        # отмечаем непроходимые клетки
        for col in getattr(level, 'collisions', []):
            # получение всех диапазонов (границ) коллизии в тайловых координатах
            x0 = col.left   // TILE_SIZE
            x1 = (col.right - 1) // TILE_SIZE
            y0 = col.top    // TILE_SIZE
            y1 = (col.bottom - 1) // TILE_SIZE
            # проходим по всем тайлам, которые пересекаются с коллизией
            for ty in range(y0, y1 + 1):
                for tx in range(x0, x1 + 1):
                    # проверка, что текущ тайловые координаты в пределах сетки
                    if 0 <= tx < self.width and 0 <= ty < self.height:
                        self.walkable[ty][tx] = False  # клетка непроходима


    def heuristic(self, a, b):
        # манхэттеновская эвристика (учитывает только гориз-е (X: a[0], b[0]) и верт-е перемещения)
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


    def neighbors(self, node):
        # возвращает проходимые соседние клетки для точки node
        x, y = node
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy     # вычисление координат соседней клетки
            # проверка, что клетка внутри сетки и проходима
            if 0 <= nx < self.width and 0 <= ny < self.height and self.walkable[ny][nx]:
                yield (nx, ny)  # возвращает по одному значению, не завершая выполнения


    def _reconstruct_path(self, came_from, current):
        # Восстанавливает путь от начальной точки до целевой
        path = []
        # если current в came_from - пришли из другой точки - восстанавливаем путь
        # если нет, значит мы в начальной точке - цикл завершается
        while current in came_from:
            path.append(current)  # текущая точка в конце пути
            current = came_from[current]  # заменяем текущую точку на ту из которой пришли
        path.reverse()
        return path


    def find_path(self, start, goal):
        # Ищет путь от start до goal
        # Возвращает список тайлов пути [(x1,y1), (x2,y2), ...] или пустой

        # хранит ещё не исследованные клетки
        open_set = [(self.heuristic(start, goal), start)]
        came_from = {}              # из какой клетки пришли в текущую
        g_score = {start: 0}        # стоимость пути от старта до узла
        closed = set()              # уже обработанные узлы

        while open_set:
            _, current = heapq.heappop(open_set)  # извлекает клетки с минимальным значением f_score из очереди
            if current in closed:   # если клетка уже обработана
                continue
            if current == goal:     # текущая клетка совпадает с goal - путь найден
                return self._reconstruct_path(came_from, current)

            closed.add(current)

            for nb in self.neighbors(current):
                tentative_g = g_score[current] + 1  # предп-я стоимость пути от start до соседней клетки через текущую
                # если предп-я стоимость пути меньше чем минимально известная
                if tentative_g < g_score.get(nb, float('inf')):
                    came_from[nb] = current     # пришли в 'nb' ч/з current
                    g_score[nb] = tentative_g
                    f = tentative_g + self.heuristic(nb, goal)  # общая оценка стоимости ч/з 'nb'
                    heapq.heappush(open_set, (f, nb))   # добавляем в очередь с новой оценкой
        # если путь не найден
        return []
