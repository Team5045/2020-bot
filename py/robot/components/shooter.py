import wpilib
from ctre import WPI_VictorSPX
class Shooter:
    
    motor_master = WPI_VictorSPX
    motor_slave = WPI_VictorSPX

    def setup(self):
        self.speed=0.0
        #set slave motor
        self.motor_slave.set(WPI_VictorSPX.ControlMode.Follower, self.motor_master.getDeviceID())

    def run_shooter(self, speed):
        self.motor_master.set(speed)


    def execute(self):
        self.run_shooter(self.speed)