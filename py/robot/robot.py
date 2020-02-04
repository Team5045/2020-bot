import wpilib
import ctre
import magicbot
import navx
from components import drivetrain, intake#, shooter , targeting
#targeting
#from controllers import alignment_controller
#from networktables import NetworkTables

CONTROLLER_LEFT = wpilib.XboxController.Hand.kLeft
CONTROLLER_RIGHT = wpilib.XboxController.Hand.kRight


class SpartaBot(magicbot.MagicRobot):

    drivetrain = drivetrain.Drivetrain
    intake = intake.Intake
    #shooter = shooter.Shooter
    #tower = tower.Tower
    
    #drivetrain = drivetrainVictors.Drivetrain
    #targeting = targeting.Targeting


    def createObjects(self):
        #NetworkTables.initialize(server='10.50.45.2')
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
        self.tower_motor = ctre.WPI_TalonSRX(5)
        self.index_motor = ctre.WPI_TalonSRX(1)

        #shooter
        self.shoot_motor_master = ctre.WPI_VictorSPX(11)
        self.shoot_motor_slave = ctre.WPI_VictorSPX(9)

        #limelight
        #self.sd = NetworkTables.getTable("SmartDashboard")
        #self.data = self.targeting.get_data()


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

    #intake
        if self.drive_controller.getBumper(CONTROLLER_RIGHT):
            self.intake.run_roller(0.85)
        if self.drive_controller.getBumper(CONTROLLER_LEFT):
            self.intake.run_roller(-0.85)

    #tower
        self.tower_motor.set(self.drive_controller.getTriggerAxis(CONTROLLER_LEFT))

        '''if self.drive_controller.getYButtonReleased():
            self.tower.move_incremental(35000)
        elif self.drive_controller.getXButtonReleased():
            self.tower.move_incremental(-5000)

        if self.drive_controller.getXButton():
            self.index_motor.set(0.8)
        else:
            self.index_motor.stopMotor()'''
        
    #shooter
        if self.drive_controller.getTriggerAxis(CONTROLLER_RIGHT)>0.4:
            self.shoot_motor_master.set(0.95)
            self.shoot_motor_slave.set(0.95)
        else:
            self.shoot_motor_master.stopMotor()
            self.shoot_motor_slave.stopMotor()
        

    #Limelight Test
        '''
        self.sd.putNumber("tv", data.found)
        if self.data.found == 1:
            self.intake_roller_motor.set(0.5)
        '''

        
    #intake arm deploy
        '''
        if self.drive_controller.getBumperReleased(CONTROLLER_LEFT):
            self.intake.switch()
        '''


if __name__ == '__main__':
    wpilib.run(SpartaBot)
