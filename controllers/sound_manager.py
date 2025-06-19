import pygame

class SoundManager:
    def __init__(self):
        # Меню + пауза
        self.menu_music  = "assets/sounds/coherence.ogg"
        # Поражение
        self.lose_music  = "assets/sounds/mediathreat.ogg"
        # Успешное прохождение уровня
        self.win_music   = "assets/sounds/win.ogg"
        # Прохождение уровня
        self.game_music  = "assets/sounds/awakening.ogg"
        # Погоня
        self.chase_music = "assets/sounds/by-product.ogg"

        # Загрузка музыки
        pygame.mixer.music.set_volume(0.5)
        # Словарь музыки
        self._bgm = {
            'menu':   self.menu_music,
            'game':   self.game_music,
            'chase':  self.chase_music,
            'lose':   self.lose_music,
            'win':    self.win_music,
        }

        # Эффекты
        self.sfx = {
            'button':   pygame.mixer.Sound(str("assets/sounds/button02.mp3.flac")),
            'collect':  pygame.mixer.Sound(str("assets/sounds/bookFlip1.ogg")),
            'hit':      pygame.mixer.Sound(str("assets/sounds/link.wav")),
            'exit':     pygame.mixer.Sound(str("assets/sounds/doorClose_2.ogg")),
        }
        for snd in self.sfx.values():
            snd.set_volume(0.7)

    # Методы воспроизведения
    def play_bgm(self, key):
        path = self._bgm.get(key)
        if path:
            pygame.mixer.music.stop()           # остановка текущей музыки (если была)
            pygame.mixer.music.load(str(path))  # загрузка новой музыки
            pygame.mixer.music.play(-1)         # запуск музыки (0 — один раз, -1 — зациклить)

    def stop_bgm(self):
        pygame.mixer.music.stop()

    def play_sfx(self, key):
        snd = self.sfx.get(key)
        if snd:
            snd.play()