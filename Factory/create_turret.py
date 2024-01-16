from Model.Turret.turret import Turret
from Factory.TurretFactory import TurretFactory


class BasicTurretFactory(TurretFactory):
    def create_turret(self, turretSpritesheets, tile_x, tile_y, shot_fx, constants):
        return Turret(turretSpritesheets, tile_x, tile_y, shot_fx, constants)
