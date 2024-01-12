# commands/BuildTurretCommand.py
from commands.commands import Command
from Model.Turret.turret import Turret
from View.turret_view import TurretView


class BuildTurretCommand(Command):
    def __init__(self, world, turret_group, turret_view_group, constants, turret_spritesheets, shot_fx):
        self.world = world
        self.turret_group = turret_group
        self.turret_view_group = turret_view_group
        self.constants = constants
        self.turret_spritesheets = turret_spritesheets
        self.shot_fx = shot_fx

    def execute(self, mouse_pos):
        mouse_tile_x = mouse_pos[0] // self.constants.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // self.constants.TILE_SIZE
        mouse_tile_num = (mouse_tile_y * self.constants.COLS) + mouse_tile_x

        if self.world.tile_map[mouse_tile_num] == 7:  # Assuming 7 is the grass tile
            space_is_free = True
            for turret in self.turret_group:
                if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                    space_is_free = False
                    break
            if space_is_free and self.world.money >= self.constants.BUY_COST:
                new_turret = Turret(
                    self.turret_spritesheets, mouse_tile_x, mouse_tile_y, self.shot_fx, self.constants)
                self.turret_group.add(new_turret)
                new_turret_view = TurretView(
                    new_turret, self.turret_spritesheets, self.constants)
                self.turret_view_group.add(new_turret_view)
                self.world.money -= self.constants.BUY_COST
