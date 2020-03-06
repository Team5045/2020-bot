import wpilib
from enum import IntEnum
from wpilib import Solenoid

HIGH_GEAR = False
LOW_GEAR = True

class Drive:

    shifter_solenoid = Solenoid

    def setup(self):
        self.pending_gear = LOW_GEAR

    def shift_low_gear(self):
        self.pending_gear = LOW_GEAR

    def shift_high_gear(self):
        self.pending_gear = HIGH_GEAR

    def shift_toggle(self):
        if self.pending_gear == HIGH_GEAR:
            self.pending_gear = LOW_GEAR
        else:
            self.pending_gear = HIGH_GEAR
    
    def execute(self):
        # Shifter
        self.shifter_solenoid.set(self.pending_gear)
