import wpilib
from ctre import WPI_TalonFX
from wpilib import DoubleSolenoid


class Shooter:

    motor_master = WPI_TalonFX
    motor_slave = WPI_TalonFX
    hood_solenoid = DoubleSolenoid

    state = False

    def setup(self):
        #shooter
        self.speed=0.0

        #set slave motor
        self.motor_slave.set(WPI_TalonFX.ControlMode.Follower,
                                  self.motor_master.getDeviceID())
        self.motor_master.setInverted(True)

        #hood
        self.state = False

    def run_shooter(self, speed):
        self.motor_master.set(speed)
        self.speed = speed
    
    def switch(self):
        print("switch")
        if self.state == False:
            self.state = True
        elif self.state == True:
            self.state = False

    def extend(self):
        self.state = True

    def retract(self):
        self.state = False

    def get_state(self):
        return {
            'hood_state': self.state,
        }

    def execute(self):
        print("execute")
        if self.state == True:
            self.hood_solenoid.set(DoubleSolenoid.Value.kForward)
        elif self.state == False:
            self.hood_solenoid.set(DoubleSolenoid.Value.kReverse)

        if self.enable:
            self.run_shooter(self.speed)
        else:
            self.run_shooter(0)
