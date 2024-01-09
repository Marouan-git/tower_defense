class WorldView():
    def __init__(self, world, map_image):
        self.world = world
        self.map_image = map_image

    def draw(self, surface):
        surface.blit(self.map_image, (0, 0))