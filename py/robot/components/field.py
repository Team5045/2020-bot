<<<<<<< HEAD
from enum import IntEnum
import wpilib
from networktables import NetworkTables


class Field:

    def execute(self):
        robot_table = NetworkTables.getTable('robot')
        robot_table.putValue('time', wpilib.Timer.getMatchTime())
=======
from enum import IntEnum
import wpilib
from networktables import NetworkTables


class Field:

    def execute(self):
        robot_table = NetworkTables.getTable('robot')
        robot_table.putValue('time', wpilib.Timer.getMatchTime())
>>>>>>> fdf0f5284e4d91a69f880b411c853646250e6fd6
