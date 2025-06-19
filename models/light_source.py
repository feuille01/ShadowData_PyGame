class LightSource:
    # Источник света - область освещения
    def __init__(self, x, y, radius):
        # x, y — верхний левый угол спрайта/маски
        self.x = x
        self.y = y
        self.radius = radius
