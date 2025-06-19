import pygame, sys, time
from settings import PIXEL_FONT_PATH


class HackMiniGame:
    def __init__(self, screen, sound):
        self.screen = screen
        self.sound = sound
        self.font_big = pygame.font.Font(PIXEL_FONT_PATH, 48)
        self.font_small = pygame.font.Font(PIXEL_FONT_PATH, 28)

        self.goal_clicks = 10
        self.time_limit = 3.0  # секунды


    def run(self, clock, fps):
        clicks = 0
        start_time = time.time()
        success = False

        while True:
            now = time.time()
            elapsed = now - start_time
            remaining = max(0, self.time_limit - elapsed)

            if clicks >= self.goal_clicks:
                success = True
                break
            if elapsed >= self.time_limit:
                break

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN and e.key == pygame.K_e:
                    self.sound.play_sfx('button')
                    clicks += 1

            self.screen.fill((10,10,10))
            msg = self.font_big.render(f"Взлом: нажмите «E» {self.goal_clicks} раз!", True, (255,255,0))
            timer = self.font_small.render(f"Осталось времени: {remaining:.1f} секунд", True, (255,255,255))
            count = self.font_small.render(f"Нажатий: {clicks}/{self.goal_clicks}", True, (200,200,200))

            self.screen.blit(msg, ((self.screen.get_width()-msg.get_width())//2, 100))
            self.screen.blit(timer, ((self.screen.get_width()-timer.get_width())//2, 200))
            self.screen.blit(count, ((self.screen.get_width()-count.get_width())//2, 250))

            pygame.display.flip()
            clock.tick(fps)

        return success
