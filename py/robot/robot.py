import wpilib
import ctre
import magicbot
import navx
from components import drivetrain, intake, targeting
#targeting
from controllers import alignment_controller
from networktables import NetworkTables

CONTROLLER_LEFT = wpilib.XboxController.Hand.kLeft
CONTROLLER_RIGHT = wpilib.XboxController.Hand.kRight


class SpartaBot(magicbot.MagicRobot):

    drivetrain = drivetrain.Drivetrain
    intake = intake.Intake
    #tower = tower.Tower
    
    #drivetrain = drivetrainVictors.Drivetrain
    targeting = targeting.Targeting


    def createObjects(self):
        NetworkTables.initialize(server='10.50.45.2')
        self.drive_controller = wpilib.XboxController(0)
        #self.compressor = wpilib.Compressor()

        #drivetrain
        self.drivetrain_left_motor_master = ctre.WPI_TalonSRX(4)
        self.drivetrain_left_motor_slave = ctre.WPI_TalonSRX(2)
        self.drivetrain_left_motor_slave2 = ctre.WPI_TalonSRX(3)

        self.drivetrain_right_motor_master = ctre.WPI_TalonSRX(7)
        self.drivetrain_right_motor_slave = ctre.WPI_TalonSRX(8)
        self.drivetrain_right_motor_slave2 = ctre.WPI_TalonSRX(6)

        self.drivetrain_shifter_solenoid = wpilib.Solenoid(2)
        self.navx = navx.AHRS.create_spi()

        #intake
        self.intake_roller_motor = ctre.WPI_VictorSPX(10)
        self.intake_arm_solenoid = wpilib.DoubleSolenoid(0,1)

        #tower
        self.tower_motor = ctre.WPI_VictorSPX(10)
        self.shooter_motor = ctre.WPI_TalonSRX(1)


        self.sd = NetworkTables.getTable("SmartDashboard")
        data = self.targeting.get_data()


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
            -self.drive_controller.getY(CONTROLLER_LEFT), angle)

        if self.drive_controller.getStickButtonReleased(CONTROLLER_LEFT):
            self.drivetrain.shift_toggle()

        #power cell intake
        if self.drive_controller.getBumper(CONTROLLER_RIGHT):
            self.intake_roller_motor.set(0.95)
        if self.drive_controller.getBumper(CONTROLLER_LEFT):
            self.intake_roller_motor.set(-0.95)

        #tower
        '''if self.drive_controller.getYButtonReleased():
            self.tower.move_incremental(35000)
        elif self.drive_controller.getXButtonReleased():
            self.tower.move_incremental(-5000)'''
        
        self.tower_motor.set(self.drive_controller.getTriggerAxis(CONTROLLER_LEFT))
        
        #shooter
        self.tower_motor.set(self.drive_controller.getTriggerAxis(CONTROLLER_RIGHT))
        '''
        if self.drive_controller.getAButton():
            self.shooter_motor.set(0.96)
        else:
            self.shooter_motor.stopMotor()'''


        self.sd.putNumber("tv", data.found)
        #Limelight Test
        if data.found == 1:
            self.intake_roller_motor.set(0.5)

        '''        
        if self.drive_controller.getAButton():
            self.shooter_motor.set(-0.9)
        elif self.drive_controller.getBButton():
            self.shooter_motor.set(-0.65)
        else:
            self.shooter_motor.stopMotor()'''
        

        
        #intake arm
        '''
        if self.drive_controller.getBumperReleased(CONTROLLER_LEFT):
            self.intake.switch()'''


if __name__ == '__main__':
    wpilib.run(SpartaBot)
