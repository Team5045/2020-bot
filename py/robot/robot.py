import wpilib
import ctre
import magicbot
import navx
from common import rumbler
from components import drivetrain, intake , shooter, #, climb, targeting
#targeting
#from controllers import alignment_controller
from networktables import NetworkTables

CONTROLLER_LEFT = wpilib.XboxController.Hand.kLeft
CONTROLLER_RIGHT = wpilib.XboxController.Hand.kRight


class SpartaBot(magicbot.MagicRobot):

    drivetrain = drivetrain.Drivetrain
    intake = intake.Intake
    shooter = shooter.Shooter
    
    #tower = tower.Tower
    #climb = climb.Climb
    
    #drivetrain = drivetrainVictors.Drivetrain
    #targeting = targeting.Targeting


    def createObjects(self):
        
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
        self.feed_motor = ctre.WPI_TalonSRX(13)
        self.intake_arm_solenoid = wpilib.DoubleSolenoid(4,5)

        #tower
        self.tower_motor = ctre.WPI_TalonSRX(5)
        #self.index_motor = ctre.WPI_TalonSRX(1)

        #shooter
        self.shooter_motor_master = ctre.WPI_VictorSPX(11)
        self.shooter_motor_slave = ctre.WPI_VictorSPX(9)

        #climb
        self.climb_motor_master = ctre.WPI_TalonSRX(12)
        self.climb_motor_slave = ctre.WPI_TalonSRX(1)

       ''' #limelight PID Turning
        self.PIDF = [2.5, 0.002, 10.0, 0.0]
        self.target_pos = self.tx
        self.pending_move = None
        self.target_angle = 0
        self.lock_target = False'''
        self.kP = 0
        self.kI = 0
        self.kD = 0



        #limelight
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
            self.feed_motor.set(0.3)
        elif self.drive_controller.getAButton():
            self.intake.run_roller(-0.85)
            self.feed_motor.set(-0.3)
        else:
            self.feed_motor.stopMotor()
            
        

    #tower
        self.tower_motor.set(self.drive_controller.getTriggerAxis(CONTROLLER_LEFT))
        if self.drive_controller.getBumper(CONTROLLER_LEFT):
            self.tower_motor.set(-0.5)
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
            self.shooter.run_shooter(0.97)
        else:
            self.shooter_motor_master.stopMotor()
            self.shooter_motor_master.stopMotor()
            
    #climb
        '''
        if self.drive_controller.getAButton():
            self.climb_motor_master.set(0.4)
            self.climb_motor_slave.set(0.4)
        elif self.drive_controller.getBButton():
            self.climb_motor_master.set(-0.4)
            self.climb_motor_slave.set(-0.4)
        elif self.drive_controller.getYButton():
            self.climb_motor_master.set(-0.4)
        elif self.drive_controller.getXButton():
            self.climb_motor_slave.set(-0.4)
        else:
            self.climb_motor_master.stopMotor()
            self.climb_motor_slave.stopMotor()       
        ''' 

    #Limelight Test
        '''
        self.sd.putNumber("tv", data.found)
        if self.data.found == 1:
            self.intake_roller_motor.set(0.5)
        '''
        self.llt = NetworkTables.getTable('limelight')
        self.tv = self.llt.getNumber('tv', 0)
        self.tx = self.llt.getNumber('tx', 0)
        if self.drive_controller.getYButton:
            #rumbler.rumble(self.drive_controller.leftRumble, 1)
            #rumbler.rumble(self.drive_controller.rightRumble, 1)
            #self.lmotorpos = self.drivetrain_left_motor_master.get_positon()
            #self.rmotorpos = self.drivetrain_right_motor_master.get_position()
            self.proportional = self.kP
            self.integral_prior = self.kI
            self.derivative = self.kD
            self.iteration_time = 0.1
            self.error_prior = 0
            while self.tv:
                self.error = 0 - self.tx
                self.integral = self.integral + self.error * self.iteration_time
                self.derivative = (self.error - self.error_prior) / self.iteration_time
                self.output = self.kP * self.error + self.kI * self.integral + self.kD * self.derivative
                self.drivetrain_left_motor_master.set(self.output)
                self.drivetrain_right_motor_master.set(-(self.output))
                '''if self.tx > 2:
                    self.drivetrain_left_motor_master.set(-0.5)
                    self.drivetrain_right_motor_master.set(-0.5)
                elif self.tx < -2:
                    self.drivetrain_left_motor_master.set(0.5)
                    self.drivetrain_right_motor_master.set(0.5)
                else:'''


        
    #intake arm deploy
        if self.drive_controller.getYButtonReleased():
            self.intake.switch()


if __name__ == '__main__':
    wpilib.run(SpartaBot)
