import pygame

class InputManager:
    # Обработка пользовательского ввода
    def handle_input(self, player, level):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        # Горизонтальное движение
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1
        # Вертикальное движение
        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1

        # Выполняем движение, если есть направление
        if dx != 0 or dy != 0:
            player.move(dx, dy, level)
