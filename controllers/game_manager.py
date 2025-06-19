import pygame

class GameManager:
    """
    Управляет состоянием игры:
    - Таймер уровня
    - Подсчет очков
    - Перезапуск уровня
    """
    def __init__(self):
        self.start_time = pygame.time.get_ticks()  # Время старта уровня в миллисекундах
        self.score = 0


    def get_elapsed_time(self):
        """
        Возвращает прошедшее время с начала уровня в секундах.
        """
        elapsed_ms = pygame.time.get_ticks() - self.start_time
        return elapsed_ms / 1000  # Переводим миллисекунды в секунды


    def calculate_score(self, player):
        """
        Рассчитывает и обновляет текущий счет:
        - 150 очков за каждый взломанный компьютер
        - 100 очков за каждый собранный документ
        - 50 очков за каждую оставшуюся жизнь
        - 1 очко штрафа за каждую секунду, прошедшую с начала уровня
        """
        doc_points = player.documents_collected * 100 + player.hacked_computers * 150
        life_points = player.lives * 50
        time_penalty = int(self.get_elapsed_time())  #без int
        self.score = doc_points + life_points - time_penalty
        return self.score


    def reset(self):
        """
        Сбрасывает таймер и счет при перезапуске уровня.
        """
        self.start_time = pygame.time.get_ticks()
        self.score = 0
