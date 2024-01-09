# game_controller.py
import pygame as pg
from Model.Enemy.enemy import Enemy
from View.enemy_view import EnemyView
from Model.Turret.turret import Turret
from View.turret_view import TurretView
import constants as c

class GameController:
    def __init__(self, world, world_view, enemy_group, enemy_view_group, turret_group, turret_view_group, enemy_images, turret_spritesheets, shot_fx):
        self.world = world
        self.world_view = world_view
        self.enemy_group = enemy_group
        self.enemy_view_group = enemy_view_group
        self.turret_group = turret_group
        self.turret_view_group = turret_view_group
        self.enemy_images = enemy_images
        self.turret_spritesheets = turret_spritesheets
        self.shot_fx = shot_fx
        self.placing_turrets = False
        self.selected_turret = None
        self.last_enemy_spawn = pg.time.get_ticks()
        self.level_started = False
        self.game_over = False
        self.game_outcome = 0

    def handle_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_mouse_click(pg.mouse.get_pos())

    def handle_mouse_click(self, mouse_pos):
        if self.placing_turrets:
            self.create_turret(mouse_pos)
        else:
            self.select_turret(mouse_pos)

    def create_turret(self, mouse_pos):
        mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
        mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x

        if self.world.tile_map[mouse_tile_num] == 7:  # Assuming 7 is the grass tile
            space_is_free = True
            for turret in self.turret_group:
                if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                    space_is_free = False
                    break
            if space_is_free and self.world.money >= c.BUY_COST:
                new_turret = Turret(self.turret_spritesheets, mouse_tile_x, mouse_tile_y, self.shot_fx)
                self.turret_group.add(new_turret)
                new_turret_view = TurretView(new_turret, self.turret_spritesheets)
                self.turret_view_group.add(new_turret_view)
                self.world.money -= c.BUY_COST
                self.placing_turrets = False



    def select_turret(self, mouse_pos):
        self.clear_selection()
        mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
        for turret in self.turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                self.selected_turret = turret
                turret.selected = True
                break

  

    def clear_selection(self):
        for turret in self.turret_group:
            turret.selected = False

    def update(self):
        if not self.game_over:
            # check if player has lost
            if self.world.health <= 0:
                self.game_over = True
                self.game_outcome = -1  # loss
            # check if player has won
            if self.world.level > c.TOTAL_LEVELS:
                self.game_over = True
                self.game_outcome = 1  # win

            self.spawn_enemies()
            self.check_level_completion()
            self.enemy_group.update(self.world)
            self.turret_group.update(self.enemy_group, self.world)
            for turret_view in self.turret_view_group:
                turret_view.update()
           
            # highlight selected turret
            if self.selected_turret:
                self.selected_turret.selected = True



    def spawn_enemies(self):
        if self.level_started and pg.time.get_ticks() - self.last_enemy_spawn > c.SPAWN_COOLDOWN:
            if self.world.spawned_enemies < len(self.world.enemy_list):
                enemy_type = self.world.enemy_list[self.world.spawned_enemies]
                enemy = Enemy(enemy_type, self.world.waypoints, self.enemy_images)
                self.enemy_group.add(enemy)
                enemy_view = EnemyView(enemy, self.enemy_images[enemy_type])
                self.enemy_view_group.add(enemy_view)
                self.world.spawned_enemies += 1
                self.last_enemy_spawn = pg.time.get_ticks()

    def check_level_completion(self):
        if self.world.check_level_complete():
            self.world.money += c.LEVEL_COMPLETE_REWARD
            self.world.level += 1
            self.level_started = False
            self.last_enemy_spawn = pg.time.get_ticks()
            self.world.reset_level()
            self.world.process_enemies()

    def draw(self, screen):
        self.world_view.draw(screen)
        for enemy_view in self.enemy_view_group:
            if enemy_view.enemy.health > 0:
                enemy_view.draw(screen)
        for turret_view in self.turret_view_group:
            turret_view.draw(screen)

    def start_and_fastforward(self, screen, begin_button, fast_forward_button):
        # check if the level has been started or not
        if self.level_started == False:
            if begin_button.draw(screen):
                self.level_started = True
        else:
            # fast forward option
            self.world.game_speed = 1
            if fast_forward_button.draw(screen):
                self.world.game_speed = 2

    def restart(self):
        self.game_over = False
        self.level_started = False
        self.placing_turrets = False
        self.selected_turret = None
        self.world.process_data()
        self.world.process_enemies()
        # empty groups
        self.enemy_group.empty()
        self.turret_group.empty()
