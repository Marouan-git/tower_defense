import pygame as pg

class EnemyView(pg.sprite.Sprite):
    def __init__(self, enemy, enemy_image):
        pg.sprite.Sprite.__init__(self)
        self.enemy = enemy
        self.image = enemy_image
        self.rect = self.image.get_rect(center=self.enemy.pos)

    def draw(self, surface):
        # Update rect to match enemy position
        self.rect.center = self.enemy.pos
        surface.blit(self.image, self.rect)