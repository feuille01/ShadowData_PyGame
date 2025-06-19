import pygame
import sys
from controllers.highscore_manager import HighScoreManager
from settings import (
    MAIN_MENU_BG, PAUSE_OVERLAY, LEVEL_PATHS, LEVEL_SELECT_BG, INSTRUCTION_BG,
    PAUSE_BG, GAME_OVER_BG, LEVEL_COMPLETE_BG, PIXEL_FONT_PATH
)


class MainMenu:
    def __init__(self, screen, sound):
        self.screen = screen
        self.sound = sound
        w, h = screen.get_size()
        self.bg = pygame.image.load(MAIN_MENU_BG).convert()
        self.font = pygame.font.Font(PIXEL_FONT_PATH, 24)

        # кнопки
        btn_w, btn_h = 340, 70
        pad = 15                    # Отступ между кнопками
        cx, cy = w // 2, h // 2     # Центр экрана

        self.btn_start = pygame.Rect(cx - btn_w // 2, cy - btn_h - pad * 2, btn_w, btn_h)
        self.btn_instr = pygame.Rect(cx - btn_w // 2, cy, btn_w, btn_h)
        self.btn_exit = pygame.Rect(cx - btn_w // 2, cy + btn_h + pad * 2, btn_w, btn_h)


    def run(self, clock, fps):
        self.sound.play_bgm('menu')
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:  # Нажатие левой кнопки мыши
                    mx, my = e.pos
                    if self.btn_start.collidepoint(mx, my):
                        self.sound.play_sfx('button')
                        return 'start' # стартуем игру
                    if self.btn_instr.collidepoint(mx, my):
                        self.sound.play_sfx('button')
                        return 'instructions'
                    if self.btn_exit.collidepoint(mx, my):
                        self.sound.play_sfx('button')
                        pygame.quit()
                        sys.exit()
            self.screen.blit(self.bg, (0, 0))

            mouse_pos = pygame.mouse.get_pos()

            for rect, label in [
                (self.btn_start, 'Начать игру'),
                (self.btn_instr, 'Инструкция'),
                (self.btn_exit, 'Выход из игры')
            ]:
                is_hover = rect.collidepoint(mouse_pos)

                bg_color = (255, 255, 200) if is_hover else (200, 200, 160)
                border_color = (20, 30, 80)

                pygame.draw.rect(self.screen, bg_color, rect)
                pygame.draw.rect(self.screen, border_color, rect, 6)

                txt = self.font.render(label, True, (10, 10, 60))
                tx = rect.x + (rect.width - txt.get_width()) // 2
                ty = rect.y + (rect.height - txt.get_height()) // 2
                self.screen.blit(txt, (tx, ty))

            pygame.display.flip()
            clock.tick(fps)


class LevelSelectMenu:
    def __init__(self, screen, sound):
        self.screen = screen
        self.sound  = sound
        w, h = screen.get_size()
        self.bg = pygame.image.load(LEVEL_SELECT_BG).convert()
        self.font = pygame.font.Font(PIXEL_FONT_PATH, 24)

        # кнопки
        btn_w, btn_h = 340, 70
        gap = 35
        total_h = len(LEVEL_PATHS) * btn_h + (len(LEVEL_PATHS)-1)*gap
        start_y = (h - total_h)//2
        self.buttons = []

        for i in range(len(LEVEL_PATHS)):
            x = (w - btn_w)//2
            y = start_y + i*(btn_h + gap)
            rect = pygame.Rect(x, y, btn_w, btn_h)
            self.buttons.append(rect)


    def run(self, clock, fps):
        self.sound.play_bgm('menu')
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    mx, my = e.pos
                    for idx, rect in enumerate(self.buttons):
                        if rect.collidepoint(mx, my):
                            self.sound.play_sfx('button')
                            return idx  # выбранный уровень (0-2)

            self.screen.blit(self.bg, (0, 0))
            mouse_pos = pygame.mouse.get_pos()

            for i, rect in enumerate(self.buttons):
                is_hover = rect.collidepoint(mouse_pos)
                bg_color = (255, 255, 200) if is_hover else (200, 200, 160)
                border_color = (10, 20, 60)
                pygame.draw.rect(self.screen, bg_color, rect)
                pygame.draw.rect(self.screen, border_color, rect, 4)

                label = self.font.render(f"Уровень {i + 1}", True, (10, 10, 60))
                tx = rect.x + (rect.w - label.get_width())//2
                ty = rect.y + (rect.h - label.get_height())//2
                self.screen.blit(label, (tx,ty))

            pygame.display.flip()
            clock.tick(fps)


class InstructionMenu:
    def __init__(self, screen, sound):
        self.screen = screen
        self.sound  = sound

        w, h = screen.get_size()
        self.bg = pygame.image.load(INSTRUCTION_BG).convert()

        self.font_title = pygame.font.Font(PIXEL_FONT_PATH, 36)
        self.font_text = pygame.font.Font(PIXEL_FONT_PATH, 18)

        # Кнопка возврата
        btn_w, btn_h = 200, 50
        x = (w - btn_w)//2
        y = h - btn_h - 40
        self.btn_back = pygame.Rect(x, y, btn_w, btn_h)

        # Текст инструкции
        self.lines = [
            "Ваша задача - проникнуть в секретные офисы корпораций,",
            "собрать важные документы, избегая патрулирующих охранников.", "",
            "Используйте свои навыки скрытности,",
            "взламывайте компьютеры и собирайте важные документы,",
            "чтобы выполнить миссию и выбраться непойманным.", "",
            "Управление: "
            "W-A-S-D — для движения.",
            "Соберите не менее одного документа, чтобы разблокировать точку выхода!",
            "Если враг вас заметил - он начнёт погоню,",
            "каждая секунда в зоне видимости врага - отнимает жизнь"
        ]


    def run(self, clock, fps):
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if self.btn_back.collidepoint(e.pos):
                        self.sound.play_sfx('button')
                        return
                if e.type == pygame.KEYDOWN and e.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    self.sound.play_sfx('button')
                    return

            self.screen.blit(self.bg, (0, 0))

            # затемнение
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            self.screen.blit(overlay, (0, 0))

            # заголовок
            title = self.font_title.render("Инструкция", True, (255,255,0))
            self.screen.blit(title, ((self.screen.get_width()-title.get_width())//2, 40))

            # текст
            y = 120
            for line in self.lines:
                shadow = self.font_text.render(line, True, (0, 0, 0))
                self.screen.blit(shadow, (62, y + 2))
                # Основной текст
                surf = self.font_text.render(line, True, (255, 255, 255))
                self.screen.blit(surf, (60, y))
                y += 40

            # кнопка назад
            mouse_pos = pygame.mouse.get_pos()
            is_hover = self.btn_back.collidepoint(mouse_pos)
            bg_color = (255, 255, 200) if is_hover else (200, 200, 160)
            border_color = (10, 20, 60)
            text_color = (10, 10, 60)

            pygame.draw.rect(self.screen, bg_color, self.btn_back)
            pygame.draw.rect(self.screen, border_color, self.btn_back, 4)

            txt = self.font_text.render("Назад", True, text_color)
            tx = self.btn_back.x + (self.btn_back.width - txt.get_width()) // 2
            ty = self.btn_back.y + (self.btn_back.height - txt.get_height()) // 2
            self.screen.blit(txt, (tx, ty))

            pygame.display.flip()
            clock.tick(fps)


class PauseMenu:
    def __init__(self, screen, sound):
        self.screen = screen
        self.sound = sound
        self.bg = pygame.image.load(PAUSE_BG).convert()
        w, h = screen.get_size()

        # затемненный фон
        self.overlay = pygame.Surface((w, h))
        self.overlay.set_alpha(PAUSE_OVERLAY)

        # шрифт
        self.font = pygame.font.Font(PIXEL_FONT_PATH, 20)

        # кнопки
        btn_w, btn_h = 340, 70
        gap = 30  # отступ между кнопками
        cx = w // 2
        total_height = 3 * btn_h + 2 * gap
        start_y = (h - total_height) // 2

        self.btn_continue = pygame.Rect(cx - btn_w // 2, start_y, btn_w, btn_h)
        self.btn_instr = pygame.Rect(cx - btn_w // 2, start_y + btn_h + gap, btn_w, btn_h)
        self.btn_exit = pygame.Rect(cx - btn_w // 2, start_y + 2 * (btn_h + gap), btn_w, btn_h)


    def run(self, clock, fps):
        self.sound.play_bgm('menu')
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    return 'continue'
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    mx, my = e.pos
                    if self.btn_continue.collidepoint(mx, my):
                        self.sound.play_sfx('button')
                        return 'continue'
                    if self.btn_instr.collidepoint(mx, my):
                        self.sound.play_sfx('button')
                        return 'instructions'
                    elif self.btn_exit.collidepoint(mx, my):
                        self.sound.play_sfx('button')
                        return 'exit'

            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(self.overlay, (0, 0))

            # кнопки
            mouse_pos = pygame.mouse.get_pos()
            buttons = [
                (self.btn_continue, 'Продолжить'),
                (self.btn_instr,    'Инструкция'),
                (self.btn_exit,     'Главное меню')
            ]

            for rect, label in buttons:
                is_hover = rect.collidepoint(mouse_pos)
                bg_color = (255, 255, 200) if is_hover else (200, 200, 160)
                border_color = (10, 20, 60)
                text_color = (10, 10, 60)

                pygame.draw.rect(self.screen, bg_color, rect)
                pygame.draw.rect(self.screen, border_color, rect, 4)

                txt = self.font.render(label, True, text_color)
                tx = rect.x + (rect.width - txt.get_width()) // 2
                ty = rect.y + (rect.height - txt.get_height()) // 2
                self.screen.blit(txt, (tx, ty))

            pygame.display.flip()
            clock.tick(fps)


class GameOverMenu:
    def __init__(self, screen, sound):
        self.screen = screen
        self.sound = sound
        self.bg = pygame.image.load(GAME_OVER_BG).convert()
        w, h = screen.get_size()

        # затемнённый фон
        self.overlay = pygame.Surface((w, h))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(200)

        # шрифты
        self.title_font = pygame.font.Font(PIXEL_FONT_PATH, 48)
        self.text_font = pygame.font.Font(PIXEL_FONT_PATH, 22)

        # кнопки
        btn_w, btn_h = 300, 60
        pad = 20
        cx, cy = w//2, h//2 + 50
        self.btn_retry = pygame.Rect(cx - btn_w//2, cy - btn_h - pad, btn_w, btn_h)
        self.btn_menu  = pygame.Rect(cx - btn_w//2, cy + pad, btn_w, btn_h)


    def run(self, clock, fps):
        self.sound.play_bgm('lose')
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    self.sound.play_sfx('button')
                    return 'exit'
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    mx, my = e.pos
                    if self.btn_retry.collidepoint(mx, my):
                        self.sound.play_sfx('button')
                        return 'retry'
                    if self.btn_menu.collidepoint(mx, my):
                        self.sound.play_sfx('button')
                        return 'exit'

            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(self.overlay, (0, 0))

            # заголовок
            title = self.title_font.render("Задание провалено!", True, (255, 0, 0))
            tx = (self.screen.get_width() - title.get_width()) // 2
            ty = self.screen.get_height()//2 - 200
            self.screen.blit(title, (tx, ty))

            sub = self.text_font.render("Вас заметили!", True, (255, 0, 0))
            sx = (self.screen.get_width() - sub.get_width()) // 2
            self.screen.blit(sub, (sx, ty + title.get_height() + 45))

            # Кнопки
            mouse_pos = pygame.mouse.get_pos()
            for rect, label in [
                (self.btn_retry, "Заново"),
                (self.btn_menu, "Главное меню")
            ]:
                is_hover = rect.collidepoint(mouse_pos)
                bg_color = (255, 255, 200) if is_hover else (200, 200, 160)
                border_color = (10, 20, 60)
                text_color = (10, 10, 60)

                pygame.draw.rect(self.screen, bg_color, rect)
                pygame.draw.rect(self.screen, border_color, rect, 4)

                txt = self.text_font.render(label, True, text_color)
                tx = rect.x + (rect.width - txt.get_width()) // 2
                ty = rect.y + (rect.height - txt.get_height()) // 2
                self.screen.blit(txt, (tx, ty))

            pygame.display.flip()
            clock.tick(fps)


class LevelCompleteMenu:
    def __init__(self, screen, sound, level_idx):
        self.screen = screen
        self.sound = sound
        self.bg = pygame.image.load(LEVEL_COMPLETE_BG).convert()
        self.hs_mgr = HighScoreManager()

        w, h = screen.get_size()
        # затемнённый фон
        self.overlay = pygame.Surface((w, h))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(200)

        # шрифты
        self.title_font = pygame.font.Font(PIXEL_FONT_PATH, 48)
        self.stat_font = pygame.font.Font(PIXEL_FONT_PATH, 22)
        self.btn_font = pygame.font.Font(PIXEL_FONT_PATH, 22)

        # кнопки
        btn_w, btn_h = 300, 60
        pad = 20
        cx, cy = w // 2, h // 2 + 80
        self.btn_retry = pygame.Rect(cx - btn_w // 2, cy - btn_h - pad, btn_w, btn_h)
        self.btn_menu = pygame.Rect(cx - btn_w // 2, cy + pad, btn_w, btn_h)


    def run(self, clock, fps, level_idx, docs_collected, elapsed_time, score, hacked_computers):
        w, h = self.screen.get_size()
        # подготовка строк статистики
        minutes = int(elapsed_time) // 60
        seconds = int(elapsed_time) % 60
        time_str = f"{minutes:02}:{seconds:02}"
        stats1 = f"Документы: {docs_collected}"
        stats2 = f"Время: {time_str}"
        stats3 = f"Очки: {score}"
        stats4 = f"Взломано компьютеров: {hacked_computers}"

        # Сохраняем рекорд
        player_name = "Player"
        self.hs_mgr.add_record(level_idx, player_name, score, docs_collected, time_str, hacked_computers)
        records = self.hs_mgr.get_records(level_idx)

        self.sound.play_bgm('win')

        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    self.sound.play_sfx('button')
                    return 'exit'
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    mx, my = e.pos
                    if self.btn_retry.collidepoint(mx, my):
                        self.sound.play_sfx('button')
                        return 'retry'
                    if self.btn_menu.collidepoint(mx, my):
                        self.sound.play_sfx('button')
                        return 'exit'

            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(self.overlay, (0, 0))

            # Заголовок
            title = self.title_font.render("Уровень пройден!", True, (0, 255, 0))
            tx = (w - title.get_width()) // 2
            ty = h // 2 - 350
            self.screen.blit(title, (tx, ty))

            # Статистика
            stat1 = self.stat_font.render(stats1, True, (255, 255, 255))
            stat2 = self.stat_font.render(stats2, True, (255, 255, 255))
            stat3 = self.stat_font.render(stats3, True, (255, 255, 255))
            stat4 = self.stat_font.render(stats4, True, (255, 255, 255))
            sx1 = (w - stat1.get_width()) // 2
            sx2 = (w - stat2.get_width()) // 2
            sx3 = (w - stat3.get_width()) // 2
            sx4 = (w - stat4.get_width()) // 2
            self.screen.blit(stat1, (sx1, ty + 280))
            self.screen.blit(stat2, (sx2, ty + 220))
            self.screen.blit(stat3, (sx3, ty + 160))
            self.screen.blit(stat4, (sx4, ty + 100))

            # Заголовок таблицы рекордов
            hs_header = self.stat_font.render("Лучшие результаты:", True, (255, 215, 0))
            hx = (w - hs_header.get_width()) // 30
            hy = ty + 155
            self.screen.blit(hs_header, (hx, hy))

            # Список рекордов
            hs_font = pygame.font.Font(PIXEL_FONT_PATH, 16)
            x = w // 20
            y0 = hy + hs_header.get_height() + 40
            line_height = 50

            for idx, rec in enumerate(records, start=1):    # записываем в rec и далее достаём по ключу
                line1 = f"{idx}. Очки: {rec['score']}, время: {rec['time']}"
                line2 = f"Документы: {rec['documents']}, взлом: {rec.get('hacked', 0)}"
                # рендер строк
                txt1 = hs_font.render(line1, True, (255, 255, 255))
                txt2 = hs_font.render(line2, True, (200, 200, 200))
                # координаты отрисовки
                y_offset = y0 + (idx - 1) * line_height * 1.6
                self.screen.blit(txt1, (x, y_offset))
                self.screen.blit(txt2, (x + 25, y_offset + 35))

            # Кнопки
            mouse_pos = pygame.mouse.get_pos()
            for rect, label in [(self.btn_retry, "Заново"), (self.btn_menu, "Главное меню")]:
                is_hover = rect.collidepoint(mouse_pos)
                bg_color = (255, 255, 200) if is_hover else (200, 200, 160)
                border_color = (10, 20, 60)
                text_color = (10, 10, 60)

                pygame.draw.rect(self.screen, bg_color, rect)
                pygame.draw.rect(self.screen, border_color, rect, 4)

                txt = self.btn_font.render(label, True, text_color)
                tx_b = rect.x + (rect.width - txt.get_width()) // 2
                ty_b = rect.y + (rect.height - txt.get_height()) // 2
                self.screen.blit(txt, (tx_b, ty_b))

            pygame.display.flip()
            clock.tick(fps)