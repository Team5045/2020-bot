import wpilib
from ctre import WPI_TalonFX
from enum import IntEnum
from wpilib import DoubleSolenoid

class HoodState(IntEnum):
    EXTENDED = 0
    RETRACTED = 1

class Shooter:

    motor = WPI_TalonFX
    hood_solenoid = DoubleSolenoid

    def setup(self):
        #shooter
        self.speed=0.0
        self.stopstart=False

        #hood
        self.state = HoodState.RETRACTED

    def run_shooter(self, speed):
        self.motor.set(speed)
        self.speed = speed

    def switch(self):
        if self.state == HoodState.EXTENDED:
            self.state = HoodState.RETRACTED
        elif self.state == HoodState.RETRACTED:
            self.state = HoodState.EXTENDED

    def extend(self):
        self.state = HoodState.EXTENDED

    def retract(self):
        self.state = HoodState.RETRACTED

    def get_state(self):
        return {
            'hood_state': self.state,
        }

    def execute(self):
        if self.state == HoodState.RETRACTED:
            self.hood_solenoid.set(DoubleSolenoid.Value.kForward)
        elif self.state == HoodState.EXTENDED:
            self.hood_solenoid.set(DoubleSolenoid.Value.kReverse)

        self.run_shooter(self.speed)