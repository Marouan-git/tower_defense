import pygame as pg
import json
from Model.Enemy.enemy import Enemy
from Model.world import World
from Model.Turret.turret import Turret
from View.button import Button
from View.world_view import WorldView
from View.turret_view import TurretView
from View.enemy_view import EnemyView
from Constants.constants import GameConstants
from Controller.game_controller import GameController
from Factory.TurretFactory import TurretFactory
from Factory.create_turret import BasicTurretFactory


def main():
    # initialise pygame
    pg.init()

    # create clock
    clock = pg.time.Clock()

    constants = GameConstants()

    # create game window
    screen = pg.display.set_mode(
        (constants.SCREEN_WIDTH + constants.SIDE_PANEL, constants.SCREEN_HEIGHT))
    pg.display.set_caption("MS Defence")

    # game variables
    game_over = False
    game_outcome = 0  # -1 is loss & 1 is win
    level_started = False
    # last_enemy_spawn = pg.time.get_ticks()
    placing_turrets = False
    selected_turret = None

    # load images
    # map
    map_image = pg.image.load('levels/level.png').convert_alpha()
    # turret spritesheets
    turret_spritesheets = []
    for x in range(1, constants.TURRET_LEVELS + 1):
        turret_sheet = pg.image.load(
            f'assets/images/turrets/turret_{x}.png').convert_alpha()
        turret_spritesheets.append(turret_sheet)
    # individual turret image for mouse cursor
    cursor_turret = pg.image.load(
        'assets/images/turrets/cursor_turret.png').convert_alpha()
    # enemies
    enemy_images = {
        "weak": pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha(),
        "medium": pg.image.load('assets/images/enemies/enemy_2.png').convert_alpha(),
        "strong": pg.image.load('assets/images/enemies/enemy_3.png').convert_alpha(),
        "elite": pg.image.load('assets/images/enemies/enemy_4.png').convert_alpha()
    }
    # buttons
    buy_turret_image = pg.image.load(
        'assets/images/buttons/buy_turret.png').convert_alpha()
    cancel_image = pg.image.load(
        'assets/images/buttons/cancel.png').convert_alpha()
    upgrade_turret_image = pg.image.load(
        'assets/images/buttons/upgrade_turret.png').convert_alpha()
    begin_image = pg.image.load(
        'assets/images/buttons/begin.png').convert_alpha()
    restart_image = pg.image.load(
        'assets/images/buttons/restart.png').convert_alpha()
    fast_forward_image = pg.image.load(
        'assets/images/buttons/fast_forward.png').convert_alpha()
    # gui
    heart_image = pg.image.load("assets/images/gui/heart.png").convert_alpha()
    coin_image = pg.image.load("assets/images/gui/coin.png").convert_alpha()
    logo_image = pg.image.load("assets/images/gui/logo.png").convert_alpha()

    # load sounds
    shot_fx = pg.mixer.Sound('assets/audio/shot.wav')
    shot_fx.set_volume(0.5)

    bg_music = pg.mixer.Sound('assets/audio/backsound.wav')
    bg_music.set_volume(0.2)  # Adjust the volume as needed
    bg_music.play(-1)  # -1 means the music will loop indefinitely

    pg.mixer.music.get_busy()

    # load json data for level
    with open('levels/level.tmj') as file:
        world_data = json.load(file)

    # load fonts for displaying text on the screen
    text_font = pg.font.SysFont("Consolas", 24, bold=True)
    large_font = pg.font.SysFont("Consolas", 36)

    # function for outputting text onto the screen

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    def display_data():
        # draw panel
        pg.draw.rect(screen, "grey10", (constants.SCREEN_WIDTH,
                                        0, constants.SIDE_PANEL, constants.SCREEN_HEIGHT))
        pg.draw.rect(screen, "grey0", (constants.SCREEN_WIDTH,
                                       0, constants.SIDE_PANEL, 400), 2)
        screen.blit(logo_image, (constants.SCREEN_WIDTH, 400))
        # display data
        draw_text("LEVEL: " + str(world.level), text_font,
                  "grey100", constants.SCREEN_WIDTH + 10, 10)
        screen.blit(heart_image, (constants.SCREEN_WIDTH + 10, 35))
        draw_text(str(world.health), text_font, "grey100",
                  constants.SCREEN_WIDTH + 50, 40)
        screen.blit(coin_image, (constants.SCREEN_WIDTH + 10, 65))
        draw_text(str(world.money), text_font, "grey100",
                  constants.SCREEN_WIDTH + 50, 70)

    # Create World instance
    world = World(world_data, constants)
    world.process_data()
    world.process_enemies()

    # Create WorldView instance
    world_view = WorldView(world, map_image)

    # create groups
    enemy_group = pg.sprite.Group()
    enemy_view_group = pg.sprite.Group()
    turret_group = pg.sprite.Group()
    # Create a group for turret views
    turret_view_group = pg.sprite.Group()

    # create buttons
    turret_button = Button(constants.SCREEN_WIDTH + 30,
                           120, buy_turret_image, True)
    cancel_button = Button(constants.SCREEN_WIDTH +
                           50, 180, cancel_image, True)
    upgrade_button = Button(constants.SCREEN_WIDTH + 5,
                            180, upgrade_turret_image, True)
    begin_button = Button(constants.SCREEN_WIDTH + 60, 300, begin_image, True)
    restart_button = Button(310, 300, restart_image, True)
    fast_forward_button = Button(
        constants.SCREEN_WIDTH + 50, 300, fast_forward_image, False)

    # Initialize GameController
    game_controller = GameController(world, world_view, enemy_group, enemy_view_group,
                                     turret_group, turret_view_group, enemy_images, turret_spritesheets, shot_fx, constants, BasicTurretFactory())

    # game loop
    run = True
    while run:

        clock.tick(constants.FPS)

        #########################
        # UPDATING SECTION
        #########################

        game_controller.update()

        #########################
        # DRAWING SECTION
        #########################

        game_controller.draw(screen)

        display_data()

        if game_controller.game_over == False:
            game_controller.start_and_fastforward(
                screen, begin_button, fast_forward_button)
            # draw buttons
            # button for placing turrets
            # for the "turret button" show cost of turret and draw the button
            draw_text(str(constants.BUY_COST), text_font,
                      "grey100", constants.SCREEN_WIDTH + 215, 135)
            screen.blit(coin_image, (constants.SCREEN_WIDTH + 260, 130))
            if turret_button.draw(screen):
                game_controller.placing_turrets = True
            # if placing turrets then show the cancel button as well
            if game_controller.placing_turrets == True:
                # show cursor turret
                cursor_rect = cursor_turret.get_rect()
                cursor_pos = pg.mouse.get_pos()
                cursor_rect.center = cursor_pos
                if cursor_pos[0] <= constants.SCREEN_WIDTH:
                    screen.blit(cursor_turret, cursor_rect)
                if cancel_button.draw(screen):
                    game_controller.placing_turrets = False
            # if a turret is selected then show the upgrade button
            if game_controller.selected_turret:
                # if a turret can be upgraded then show the upgrade button
                if game_controller.selected_turret.upgrade_level < constants.TURRET_LEVELS:
                    # show cost of upgrade and draw the button
                    draw_text(str(constants.UPGRADE_COST), text_font,
                              "grey100", constants.SCREEN_WIDTH + 215, 195)
                    screen.blit(
                        coin_image, (constants.SCREEN_WIDTH + 260, 190))
                    if upgrade_button.draw(screen):
                        if game_controller.world.money >= constants.UPGRADE_COST:
                            game_controller.selected_turret.upgrade(
                                turret_spritesheets)
                            game_controller.world.money -= constants.UPGRADE_COST
        else:
            pg.draw.rect(screen, "dodgerblue",
                         (200, 200, 400, 200), border_radius=30)
            if game_controller.game_outcome == -1:
                draw_text("GAME OVER", large_font, "grey0", 310, 230)
            elif game_controller.game_outcome == 1:
                draw_text("YOU WIN!", large_font, "grey0", 315, 230)

            # restart level

            if restart_button.draw(screen):
                game_controller.world = World(world_data, constants)
                game_controller.restart()

        # event handler
        for event in pg.event.get():
            # quit program
            if event.type == pg.QUIT:
                run = False

            # mouse click
        # mouse click
            if not game_controller.game_over:
                if not game_controller.turret_selected_this_event:
                    game_controller.handle_events(event)
                    game_controller.turret_selected_this_event = True
                else:
                    game_controller.turret_selected_this_event = False

        # update display
        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()
