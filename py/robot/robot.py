import wpilib
import ctre
import magicbot
import navx
from components import drivetrain
#targeting
from controllers import alignment_controller

CONTROLLER_LEFT = wpilib.XboxController.Hand.kLeft
CONTROLLER_RIGHT = wpilib.XboxController.Hand.kRight


class SpartaBot(magicbot.MagicRobot):

    drivetrain = drivetrain.Drivetrain
    #targeting = targeting.Targeting


    def createObjects(self):
        self.drive_controller = wpilib.XboxController(0)
        self.compressor = wpilib.Compressor()

        self.drivetrain_left_motor_master = ctre.WPI_TalonSRX(2)
        self.drivetrain_left_motor_slave = ctre.WPI_TalonSRX(1)
        self.drivetrain_right_motor_master = ctre.WPI_TalonSRX(8)
        self.drivetrain_right_motor_slave = ctre.WPI_TalonSRX(7)
        self.drivetrain_shifter_solenoid = wpilib.Solenoid(2)
        self.navx = navx.AHRS.create_spi()


    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        #self.drivetrain.reset_angle_correction()
        pass


    def teleopPeriodic(self):
        angle = self.drive_controller.getX(CONTROLLER_RIGHT)
        self.drivetrain.angle_corrected_differential_drive(
            self.drive_controller.getY(CONTROLLER_LEFT), angle)

        
        if self.drive_controller.getStickButtonReleased(CONTROLLER_LEFT):
            self.drivetrain.shift_toggle()

        

if __name__ == '__main__':
    wpilib.run(SpartaBot)
