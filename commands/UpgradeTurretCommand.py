# commands/UpgradeTurretCommand.py
from commands.commands import Command
import constants as c


class UpgradeTurretCommand(Command):
    def __init__(self, world, turret_group, turret_spritesheets, selected_turret, constants):
        self.world = world
        self.turret_group = turret_group
        self.turret_spritesheets = turret_spritesheets
        self.selected_turret = selected_turret
        self.constants = constants

    def execute(self):
        print("UpgradeTurretCommand execute() called.")
        # Logic to upgrade a turret
        if self.selected_turret and self.world.money >= self.constants.UPGRADE_COST:
            self.selected_turret.upgrade(self.turret_spritesheets)
            self.world.money -= self.constants.UPGRADE_COST
