import pygame

def load_animation_strip(path, frame_width):
    # Загружает горизонтальный спрайт-лист и режет его на кадры одинаковой ширины,
    # возвращает список pygame.Surface
    image = pygame.image.load(path).convert_alpha()
    frames = []
    for i in range(image.get_width() // frame_width):
        rect = pygame.Rect(i * frame_width, 0, frame_width, image.get_height())
        frames.append(image.subsurface(rect).copy())
    return frames

def load_image(path):
    return pygame.image.load(path).convert_alpha()