from abc import ABC, abstractmethod


class TurretFactory(ABC):
    @abstractmethod
    def create_turret(self, tile_x, tile_y, shot_fx, constants):
        pass
