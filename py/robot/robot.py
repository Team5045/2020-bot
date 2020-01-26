import wpilib
import ctre
import magicbot
import navx
from components import drivetrain, intake, drivetrainVictors
#targeting
from controllers import alignment_controller

CONTROLLER_LEFT = wpilib.XboxController.Hand.kLeft
CONTROLLER_RIGHT = wpilib.XboxController.Hand.kRight


class SpartaBot(magicbot.MagicRobot):

    drivetrain = drivetrain.Drivetrain
    drivetrain = drivetrainVictors.Drivetrain
    intake = intake.Intake
    #targeting = targeting.Targeting


    def createObjects(self):
        self.drive_controller = wpilib.XboxController(0)
        #self.compressor = wpilib.Compressor()

        self.drivetrain_left_motor_master = ctre.WPI_TalonSRX(1)
        self.drivetrain_left_motor_slave = ctre.WPI_TalonSRX(2)
        #self.drivetrain_left_motor_slave = ctre.WPI_TalonSRX(3)
        #self.drivetrain_left_motor_slave2 = ctre.WPI_VictorSPX(3)
        self.drivetrain_right_motor_master = ctre.WPI_TalonSRX(4)
        self.drivetrain_right_motor_slave = ctre.WPI_TalonSRX(5)
        #self.drivetrain_left_motor_slave = ctre.WPI_TalonSRX(6)
        #self.drivetrain_right_motor_slave2 = ctre.WPI_VictorSPX(6)
        self.drivetrain_shifter_solenoid = wpilib.Solenoid(2)
        self.navx = navx.AHRS.create_spi()

        #intake
        self.intake_roller_motor = ctre.WPI_TalonSRX(7)
        self.intake_arm_solenoid = wpilib.DoubleSolenoid(0,1)


    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        #self.drivetrain.reset_angle_correction()
        pass


    def teleopPeriodic(self):

        #drivetrain
        angle = self.drive_controller.getX(CONTROLLER_RIGHT)
        self.drivetrain.angle_corrected_differential_drive(
            self.drive_controller.getY(CONTROLLER_LEFT), angle)

        if self.drive_controller.getStickButtonReleased(CONTROLLER_LEFT):
            self.drivetrain.shift_toggle()

        #power cell intake
        if self.drive_controller.getAButton():
            self.intake_roller_motor.set(0.75)
        elif self.drive_controller.getBButton():
            self.intake_roller_motor.set(-0.75)
        else:
            self.intake_roller_motor.set(0)

        #intake arm
        if self.drive_controller.getBumperReleased(CONTROLLER_LEFT):
            self.intake.switch()


if __name__ == '__main__':
    wpilib.run(SpartaBot)
