import pygame as pg
import math
from Model.Turret.turret_data import TURRET_DATA


class Turret(pg.sprite.Sprite):
    def __init__(self, sprite_sheets, tile_x, tile_y, shot_fx, constants):
        pg.sprite.Sprite.__init__(self)
        self.upgrade_level = 1
        self.constants = constants

        # Position variables
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.x = (self.tile_x + 0.5) * constants.TILE_SIZE
        self.y = (self.tile_y + 0.5) * constants.TILE_SIZE

        # Sound effect
        self.shot_fx = shot_fx

        # Update time for animations
        self.update_time = pg.time.get_ticks()

        # Initial angle
        self.angle = 90

        # Load initial image
        self.animation_list = self.load_images(sprite_sheets[0])
        self.original_image = self.animation_list[0]

        # Additional turret attributes
        self.range = TURRET_DATA[self.upgrade_level - 1].get("range")
        self.cooldown = TURRET_DATA[self.upgrade_level - 1].get("cooldown")
        self.last_shot = pg.time.get_ticks()
        self.selected = False
        self.target = None

        # Upgrade position of rect attribute
        self.rect = self.original_image.get_rect()
        self.rect.center = (self.x, self.y)

    def load_images(self, sprite_sheet):
        # extract images from spritesheet
        size = sprite_sheet.get_height()
        animation_list = []
        for x in range(self.constants.ANIMATION_STEPS):
            temp_img = sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list

    def update(self, enemy_group, world):
        # if target picked, play firing animation
        if self.target:
            return  # self.play_animation()
        else:
            # search for new target once turret has cooled down
            if pg.time.get_ticks() - self.last_shot > (self.cooldown / world.game_speed):
                self.pick_target(enemy_group)

    def pick_target(self, enemy_group):
        # find an enemy to target
        x_dist = 0
        y_dist = 0
        # check distance to each enemy to see if it is in range
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.target = enemy
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    # damage enemy
                    self.target.health -= self.constants.DAMAGE
                    # play sound effect
                    self.shot_fx.play()
                    break

    # Turret class

    def upgrade(self, sprite_sheets, frame_index=0):
        print("Upgrading turret...")
        print(f"Before upgrade - Upgrade level: {
              self.upgrade_level}, Animation list length: {len(self.animation_list)}")

        self.upgrade_level += 1
        old_range_rect_center = self.range_rect.center if hasattr(
            self, 'range_rect') else self.rect.center

        # Update turret attributes
        self.range = TURRET_DATA[self.upgrade_level - 1].get("range")
        self.cooldown = TURRET_DATA[self.upgrade_level - 1].get("cooldown")

        # Upgrade turret image
        self.animation_list = self.load_images(
            sprite_sheets[self.upgrade_level - 1])
        self.original_image = self.animation_list[frame_index]

        # Upgrade range circle
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100",
                       (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()

        # Center the new range_rect based on the previous position
        self.range_rect.center = old_range_rect_center

        # Center the turret rect based on its position
        self.rect = self.original_image.get_rect()
        self.rect.center = (self.x, self.y)

        print(f"After upgrade - Upgrade level: {
              self.upgrade_level}, Animation list length: {len(self.animation_list)}")
