import sys
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, SCALE, EXIT_HOLD_TIME, LEVEL_PATHS
from utils.tiled_Loader import load_tiled_map, build_gid_map
from models.level import Level
from models.pathfinder import PathFinder
from controllers.game_manager import GameManager
from controllers.input_manager import InputManager
from controllers.entity_factory import init_entities
from views.hud import HUD
from views.game_view import GameView
from controllers.menu import MainMenu, LevelSelectMenu, PauseMenu, GameOverMenu, LevelCompleteMenu, InstructionMenu
from controllers.highscore_manager import HighScoreManager
from controllers.sound_manager import SoundManager
from controllers.mini_games import HackMiniGame


def load_level(idx):
    path = LEVEL_PATHS[idx]
    map_json = load_tiled_map(path)
    gid_map  = build_gid_map(map_json, path)
    return Level(path, gid_map)
GAME_WIDTH = SCREEN_WIDTH // SCALE
GAME_HEIGHT = SCREEN_HEIGHT // SCALE


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Создаём SoundManager и сразу запускаем меню-музыку
    sound = SoundManager()
    sound.play_bgm('menu')
    main_menu = MainMenu(screen, sound)
    instruction_menu = InstructionMenu(screen, sound)
    level_select_menu = LevelSelectMenu(screen, sound)
    pause_menu = PauseMenu(screen, sound)
    game_over_menu = GameOverMenu(screen, sound)
    hack_game = HackMiniGame(screen, sound)

    # Вспомогатели
    game_manager = GameManager()
    input_mgr = InputManager()
    hud = HUD()
    view = GameView(screen, (GAME_WIDTH, GAME_HEIGHT), game_manager, hud)

    while True:
        action = main_menu.run(clock, FPS)
        if action == 'start':
            break
        elif action == 'instructions':
            instruction_menu.run(clock, FPS)

    current_level = level_select_menu.run(clock, FPS)
    level_complete_menu = LevelCompleteMenu(screen, sound, current_level)
    level = load_level(current_level)
    pathfinder = PathFinder(level)
    sound.play_bgm('game')
    # Инициализация всех сущностей через фабрику
    player, documents, enemies, light_sources, exit_points, computers = init_entities(level, pathfinder)
    game_manager.reset()
    elapsed_time = 0.0
    exit_timer = 0.0

    running = True
    paused = False
    game_over = False
    chase_mode = False

    while running:
        dt = clock.tick(FPS) / 1000.0
        elapsed_time += dt

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = not paused

        # если жизни кончились и мы ещё не показали экран поражения
        if player.lives <= 0 and not game_over:
            # запускаем экран Game Over
            action = game_over_menu.run(clock, FPS)
            if action == 'retry':
                # сброс уровня
                game_manager.reset()
                player, documents, enemies, light_sources, exit_points, computers = init_entities(level, pathfinder)
                elapsed_time = 0.0
                game_over = False
            else:  # 'exit' из экрана поражения — возвращаемся в главное меню и ждём выбора
                while True:
                    menu_action = main_menu.run(clock, FPS)
                    if menu_action == 'instructions':
                        instruction_menu.run(clock, FPS)
                    elif menu_action == 'start':
                        current_level = level_select_menu.run(clock, FPS)
                        level = load_level(current_level)
                        pathfinder = PathFinder(level)
                        game_manager.reset()
                        player, documents, enemies, light_sources, exit_points, computers = init_entities(level,
                                                                                                          pathfinder)
                        sound.play_bgm('game')
                        elapsed_time = 0.0
                        game_over = False
                        break  # выходим из цикла и продолжаем игру
                    elif menu_action == 'exit':
                        pygame.quit()
                        sys.exit()
            continue

        if paused:
            action = pause_menu.run(clock, FPS)
            if action == 'continue':
                paused = False
                sound.play_bgm('game')
            elif action == 'instructions':
                # показать инструкцию, остаться в паузе
                instruction_menu.run(clock, FPS)
                continue
            else:  # 'exit'
                sound.play_bgm('menu')
                # возвращаемся к главному меню
                while True:
                    action = main_menu.run(clock, FPS)
                    if action == 'start':
                        break
                    elif action == 'instructions':
                        instruction_menu.run(clock, FPS)
                # и дальше заново выбираем уровень
                current_level = level_select_menu.run(clock, FPS)
                level = load_level(current_level)
                pathfinder = PathFinder(level)
                player, documents, enemies, light_sources, exit_points, computers = init_entities(level, pathfinder)
                game_manager.reset()
                sound.play_bgm('game')
                elapsed_time = 0.0
                paused = False
            continue

        # Ввод
        input_mgr.handle_input(player, level)

        # Логика обновления
        player.update(level, dt)
        for enemy in enemies:
            enemy.update(level, player, dt, sound)

        hack_prompts = []
        keys = pygame.key.get_pressed()
        for comp in computers:
            if not comp.hacked and comp.rect.colliderect(player.rect):
                hack_prompts.append(comp.rect)
                if keys[pygame.K_e]:
                    comp.try_hack(player.rect, hack_game, clock, FPS, sound, player)

        # переключаем музыку в зависимости от chase-флага
        is_chasing = any(e.chasing for e in enemies)
        if is_chasing and not chase_mode:
            sound.play_bgm('chase')
            chase_mode = True
        elif not is_chasing and chase_mode:
            sound.play_bgm('game')
            chase_mode = False

        # Сбор документов
        for doc in documents[:]:
            if doc.collect(player):
                sound.play_sfx('collect')
                player.collect_document()
                documents.remove(doc)

        if player.documents_collected >= 1:
            # активируем точку выхода: при столкновении — завершаем уровень
            on_exit = any(player.rect.colliderect(pt.rect) for pt in exit_points)
            if on_exit:
                exit_timer += dt
            else:
                exit_timer = 0.0
            if exit_timer >= EXIT_HOLD_TIME:
                sound.play_sfx('exit')
                # показываем экран успешного завершения
                score = game_manager.calculate_score(player)

                # экран успешного завершения — рекорд сохраняется внутри него
                action = level_complete_menu.run(clock, FPS, current_level, player.documents_collected, elapsed_time,
                                                 score, player.hacked_computers)

                if action == 'retry':
                    game_manager.reset()
                    player, documents, enemies, light_sources, exit_points, computers = init_entities(level, pathfinder)
                    elapsed_time = 0.0
                    sound.play_bgm('game')
                    running = True
                else:
                    # возвращаемся в главное меню
                    while True:
                        menu_action = main_menu.run(clock, FPS)
                        if menu_action == 'instructions':
                            instruction_menu.run(clock, FPS)
                        elif menu_action == 'start':
                            current_level = level_select_menu.run(clock, FPS)
                            level = load_level(current_level)
                            pathfinder = PathFinder(level)
                            game_manager.reset()
                            player, documents, enemies, light_sources, exit_points, computers = init_entities(level,
                                                                                                              pathfinder)
                            sound.play_bgm('game')
                            elapsed_time = 0.0
                            exit_timer = 0.0
                            break
                        elif menu_action == 'exit':
                            pygame.quit()
                            sys.exit()
                continue

        # Отрисовка сцены
        active_exits = exit_points if player.documents_collected >= 1 else []
        view.draw(player, level, enemies, documents, light_sources, active_exits, elapsed_time, computers, hack_prompts)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
