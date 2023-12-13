import pygame as pg
import constants as c

class TurretView(pg.sprite.Sprite):
    def __init__(self, turret, sprite_sheets):
        pg.sprite.Sprite.__init__(self)
        self.turret = turret
        self.sprite_sheets = sprite_sheets
        self.animation_list = self.load_images()
        self.frame_index = 0

        # Create transparent circle for showing range
        self.range_image = pg.Surface((self.turret.range * 2, self.turret.range * 2), pg.SRCALPHA)
        pg.draw.circle(self.range_image, (128, 128, 128, 100), (self.turret.range, self.turret.range), self.turret.range)

    def load_images(self):
        size = self.sprite_sheets[0].get_height()
        animation_list = []
        for x in range(c.ANIMATION_STEPS):
            temp_img = self.sprite_sheets[self.turret.upgrade_level - 1].subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list

    def draw(self, surface):
        # Determine the image to draw based on frame index
        image = self.animation_list[self.frame_index]
        rotated_image = pg.transform.rotate(image, self.turret.angle - 90)
        rect = rotated_image.get_rect(center=(self.turret.x, self.turret.y))

        # Draw turret and range circle if selected
        surface.blit(rotated_image, rect)
        if self.turret.selected:
            range_rect = self.range_image.get_rect(center=(self.turret.x, self.turret.y))
            surface.blit(self.range_image, range_rect)
    
    def update(self):
        # Logic to update the frame index for animation
        if self.turret.target:
            # Update image based on the animation frame
            if pg.time.get_ticks() - self.turret.update_time > c.ANIMATION_DELAY:
                self.turret.update_time = pg.time.get_ticks()
                self.frame_index += 1
                if self.frame_index >= len(self.animation_list):
                    self.frame_index = 0
                    # Clear target so cooldown can begin
                    self.turret.last_shot = pg.time.get_ticks()
                    self.turret.target = None