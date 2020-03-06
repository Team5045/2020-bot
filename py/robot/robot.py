import wpilib
import ctre
import magicbot
import navx
from components import shooterFalcon
from wpilib.drive import DifferentialDrive


CONTROLLER_LEFT = wpilib.XboxController.Hand.kLeftHand
CONTROLLER_RIGHT = wpilib.XboxController.Hand.kRightHand


class SpartaBot(magicbot.MagicRobot):

    shooter = shooterFalcon.Shooter

    def createObjects(self):
        self.drive_controller = wpilib.XboxController(0)
        

        #drivetrain
        self.drivetrain_left_motor_master = ctre.WPI_TalonFX(1)
        self.drivetrain_left_motor_slave = ctre.WPI_TalonFX(2)
        self.drivetrain_left_motor_slave2 = ctre.WPI_TalonFX(3)

        self.drivetrain_right_motor_master = ctre.WPI_TalonFX(4)
        self.drivetrain_right_motor_slave = ctre.WPI_TalonFX(5)
        self.drivetrain_right_motor_slave2 = ctre.WPI_TalonFX(6)

        self.left = wpilib.SpeedControllerGroup(self.drivetrain_left_motor_master, self.drivetrain_left_motor_slave, self.drivetrain_left_motor_slave2)
        self.right = wpilib.SpeedControllerGroup(
            self.drivetrain_right_motor_master, self.drivetrain_right_motor_slave, self.drivetrain_right_motor_slave2
        )

        #self.drivetrain = DifferentialDrive(self.left, self.right)
        #self.drivetrain.setExpiration(0.1)

        #shooter
        self.shooter_hood_solenoid = wpilib.DoubleSolenoid(4,5)
        self.shooter_motor = ctre.WPI_TalonFX(11)

    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        #self.drivetrain.setSafetyEnabled(True)
        pass

    def teleopPeriodic(self):

        self.drivetrain_left_motor_master.set(self.drive_controller.getY(CONTROLLER_LEFT))
        self.drivetrain_left_motor_slave.set(self.drive_controller.getY(CONTROLLER_LEFT))
        self.drivetrain_left_motor_slave2.set(self.drive_controller.getY(CONTROLLER_LEFT))

        self.drivetrain_right_motor_master.set(-self.drive_controller.getY(CONTROLLER_RIGHT))
        self.drivetrain_right_motor_slave.set(-self.drive_controller.getY(CONTROLLER_RIGHT))
        self.drivetrain_right_motor_slave2.set(-self.drive_controller.getY(CONTROLLER_RIGHT))

        if self.drive_controller.getAButton():
            self.drivetrain_right_motor_master.set(-1)
            self.drivetrain_right_motor_slave.set(-1)
            self.drivetrain_right_motor_slave2.set(-1)
        

        #self.shooter_motor.set(self.drive_controller.getTriggerAxis(CONTROLLER_RIGHT))

if __name__ == '__main__':
    wpilib.run(SpartaBot)
