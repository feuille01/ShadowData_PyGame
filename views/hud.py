import pygame
from settings import SCREEN_WIDTH, COLOR_WHITE, TILE_SIZE, SPRITE_LIFE, LIFE_ICON_SIZE

class HUD:
    """
    Рисует интерфейс:
    - Счетчик документов
    - Иконки жизней
    - Таймер уровня
    - Текущий счет
    """
    def __init__(self):
        # Используем системный шрифт по умолчанию, размер 24
        self.font = pygame.font.Font(None, 24)
        img = pygame.image.load(SPRITE_LIFE).convert_alpha()
        self.life_icon = pygame.transform.scale(img, (LIFE_ICON_SIZE, LIFE_ICON_SIZE))

    def draw(self, screen, player, elapsed_time, score):
        # Отображаем количество документов
        doc_text = self.font.render(f'Documents: {player.documents_collected}', True, COLOR_WHITE)
        screen.blit(doc_text, (10, 10))

        # Отображаем иконки жизней (глаза)
        for i in range(player.lives):
            x = 10 + i * (LIFE_ICON_SIZE + 5)
            y = 40
            screen.blit(self.life_icon, (x, y))

        # Отображаем таймер уровня (MM:SS)
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        time_str = f'Time: {minutes:02}:{seconds:02}'
        time_text = self.font.render(time_str, True, COLOR_WHITE)
        screen.blit(time_text, (SCREEN_WIDTH - 120, 10))

        # Отображаем текущий счет
        score_text = self.font.render(f'Score: {score}', True, COLOR_WHITE)
        screen.blit(score_text, (SCREEN_WIDTH - 120, 40))