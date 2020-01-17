from ctre import WPI_TalonSRX
from magicbot import tunable
from enum import IntEnum
from wpilib import Solenoid
from constants import TALON_TIMEOUT

class IntakeState(IntEnum):
    EXTENDED = 0
    RETRACTED = 1


class Intake:
    roller_motor = WPI_TalonSRX
    arm_solenoid = Solenoid

    def setup(self):
        self.state = IntakeState.RETRACTED
        self.roller_motor.setInverted(True)
        self.roller_motor.setSensorPhase(True)

        self.speed = 0.0

    def switch(self):
        if self.state == IntakeState.EXTENDED:
            self.state = IntakeState.RETRACTED
        elif self.state == IntakeState.RETRACTED:
            self.state = IntakeState.EXTENDED

    def extend(self):
        self.state = ClawState.EXTENDED

    def retract(self):
        self.state = ClawState.RETRACTED

    def run_intake(self, speed):
        self.roller_motor.set(speed)

    def get_state(self):
        return {
            'arm_state': self.state,
        }

    def execute(self):
        if self.state == IntakeState.RETRACTED:
            self.solenoid.set(Solenoid.Value.KForward)
        elif self.state == IntakeState.EXTENDED:
            self.solenoid.set(Solenoid.Value.kReverse)

        self.run_intake(self.speed)
    