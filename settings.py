# Константы

# Экран
SCREEN_WIDTH = 1440 # Ширина окна игры в пикселях
SCREEN_HEIGHT = 1000  # Высота окна игры в пикселях

# Частота кадров
FPS = 60

# Размер тайла
TILE_SIZE = 16
SCALE = 2
DOCUMENT_SIZE = 10  # размер картинки документа

# Игровые параметры
PLAYER_LIVES = 3  # Начальное количество жизней игрока
PLAYER_SPEED = 1
ENEMY_SPEED = 0.5
DEFAULT_LIGHT_RADIUS = 100  # Радиус освещения (в пикселях)
ENEMY_FOV = 80              # Угол конуса зрения врага в градусах
ENEMY_VISION_RADIUS = 60    # Длина конуса зрения врага в градусах
DETECTION_TIME = 1.0
CHASE_TIMEOUT = 3.5

COLOR_WHITE = (255, 255, 255)

# Шрифт
PIXEL_FONT_PATH = "assets/font/PressStart2P-Regular.ttf"

# Пути к уровням
LEVEL_PATHS = [
    "assets/maps/level1.json",
    "assets/maps/level2.json",
    "assets/maps/level3.json",
]

# Спрайты игрока
SPRITE_WALK_UP    = "assets/businessman1/businessman1_walk_up.png"
SPRITE_WALK_DOWN  = "assets/businessman1/businessman1_walk_down.png"
SPRITE_WALK_LEFT  = "assets/businessman1/businessman1_walk_left.png"
SPRITE_WALK_RIGHT = "assets/businessman1/businessman1_walk_right.png"

SPRITE_IDLE_UP    = "assets/businessman1/businessman1_idle_up.png"
SPRITE_IDLE_DOWN  = "assets/businessman1/businessman1_idle_down.png"
SPRITE_IDLE_LEFT  = "assets/businessman1/businessman1_idle_left.png"
SPRITE_IDLE_RIGHT = "assets/businessman1/businessman1_idle_right.png"

# Спрайты врага
SPRITE_ENEMY_WALK_UP    = "assets/enemy/enemy_walk_up.png"
SPRITE_ENEMY_WALK_DOWN  = "assets/enemy/enemy_walk_down.png"
SPRITE_ENEMY_WALK_LEFT  = "assets/enemy/enemy_walk_left.png"
SPRITE_ENEMY_WALK_RIGHT = "assets/enemy/enemy_walk_right.png"

SPRITE_ENEMY_IDLE_UP    = "assets/enemy/enemy_idle_up.png"
SPRITE_ENEMY_IDLE_DOWN  = "assets/enemy/enemy_idle_down.png"
SPRITE_ENEMY_IDLE_LEFT  = "assets/enemy/enemy_idle_left.png"
SPRITE_ENEMY_IDLE_RIGHT = "assets/enemy/enemy_idle_right.png"

# Спрайты документа и замочка на компьютере
SPRITE_DOCUMENT = "assets/sprites/document.png"
SPRITE_COMPUTER = "assets/sprites/computer.png"
COMPUTER_SCALE = 0.023  # Размер замочка (взлом)

SPRITE_LIFE = "assets/sprites/eye.png"  # Спрайт значка жизней
LIFE_ICON_SIZE = TILE_SIZE * 1.5        # Размер значка жизней

SPRITE_EXIT = "assets/sprites/exit.png" # Спрайт картинки выхода
EXIT_SIZE = TILE_SIZE * 2               # Размер картинки выхода
EXIT_HOLD_TIME = 1.0                    # время удержания на выходе в сек

# Меню
MAIN_MENU_BG = "assets/background/ShadowData_background.png"
LEVEL_SELECT_BG = "assets/background/level_select.png"
PAUSE_BG = "assets/background/pause_bg.png"
INSTRUCTION_BG = "assets/background/instruction_bg.png"
GAME_OVER_BG = "assets/background/game_over.png"
LEVEL_COMPLETE_BG = "assets/background/level_complete.png"
PAUSE_OVERLAY = 60  # прозрачность фона паузы