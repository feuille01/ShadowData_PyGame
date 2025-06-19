import json
import os
import pygame
import xml.etree.ElementTree as ET

# Флаги переворота для Tiled
FLIP_H = 0x80000000  # горизонтальный
FLIP_V = 0x40000000  # вертикальный
FLIP_D = 0x20000000  # диагональный

def load_tiled_map(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def build_gid_map(map_json, map_path):
    gid_map = {}
    base_dir = os.path.dirname(map_path)

    for ts in map_json['tilesets']:
        firstgid = ts['firstgid']
        # определяем путь к изображению тайлсета
        if 'image' in ts:
            tw, th = ts['tilewidth'], ts['tileheight']
            image_path = os.path.join(base_dir, ts['image'])
        else:
            tsx_path = os.path.join(base_dir, os.path.basename(ts['source']))
            tsx = ET.parse(tsx_path).getroot()
            tw = int(tsx.attrib['tilewidth'])
            th = int(tsx.attrib['tileheight'])
            image_elem = tsx.find('image')
            image_path = os.path.join(os.path.dirname(tsx_path), os.path.basename(image_elem.attrib['source']))
        sheet = pygame.image.load(image_path).convert_alpha()
        columns = sheet.get_width() // tw
        rows = sheet.get_height() // th

        # Для каждого тайла в спрайте создаём базовый и перевёрнутые варианты
        for i in range(columns * rows):
            x = (i % columns) * tw
            y = (i // columns) * th
            base_gid = firstgid + i
            # базовый спрайт без переворотов
            image = sheet.subsurface(pygame.Rect(x, y, tw, th)).copy()
            gid_map[base_gid] = image

            # варианты с переворотами
            for mask in (
                    FLIP_H, FLIP_V, FLIP_D,
                    FLIP_H | FLIP_V,
                    FLIP_H | FLIP_D,
                    FLIP_V | FLIP_D,
                    FLIP_H | FLIP_V | FLIP_D,
            ):
                flipped = image
                # диагональный
                if mask & FLIP_D:
                    flipped = pygame.transform.rotate(flipped, 90)
                # горизонтальный/вертикальный флип
                flip_x = bool(mask & FLIP_H)
                flip_y = bool(mask & FLIP_V)
                if flip_x or flip_y:
                    flipped = pygame.transform.flip(flipped, flip_x, flip_y)
                gid_map[base_gid | mask] = flipped
    return gid_map
