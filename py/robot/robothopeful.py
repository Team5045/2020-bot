import wpilib
import ctre
import magicbot
import navx
import wpilib.drive
from wpilib.drive import DifferentialDrive
from wpilib import Solenoid, DoubleSolenoid
from components import shooter, drivetrainFalcon


CONTROLLER_LEFT = wpilib.XboxController.Hand.kLeftHand
CONTROLLER_RIGHT = wpilib.XboxController.Hand.kRightHand


class SpartaBot(magicbot.MagicRobot):
    #shooter = shooter.Shooter()
    #drivetrain = drivetrainFalcon.Drivetrain()

    def createObjects(self):
        self.drive_controller = wpilib.XboxController(0)

        self.drivetrain_left_motor_master = ctre.WPI_TalonSRX(1)
        self.drivetrain_left_motor_slave = ctre.WPI_TalonSRX(2)
        self.drivetrain_left_motor_slave2 = ctre.WPI_TalonSRX(3)

        self.drivetrain_right_motor_master = ctre.WPI_TalonSRX(4)
        self.drivetrain_right_motor_slave = ctre.WPI_TalonSRX(5)
        self.drivetrain_right_motor_slave2 = ctre.WPI_TalonSRX(6)

        self.left = wpilib.SpeedControllerGroup(
            self.drivetrain_left_motor_master, self.drivetrain_left_motor_slave, self.drivetrain_left_motor_slave2
            )
        self.right = wpilib.SpeedControllerGroup(
            self.drivetrain_right_motor_master, self.drivetrain_right_motor_slave, self.drivetrain_right_motor_slave2
        )
        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)
        self.drive.setExpiration(0.1)

        self.shifter_shiftsolenoid = wpilib.Solenoid(1)

        #intake
        self.intake_roller_motor = ctre.WPI_TalonSRX(7)
        self.intake_arm_solenoid = wpilib.DoubleSolenoid(2,3)

        #shooter
        self.motor_master = ctre.WPI_TalonFX(21)
        self.motor_slave = ctre.WPI_TalonFX(20)
        self.hood_solenoid = wpilib.DoubleSolenoid(4,5)

    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        #self.drivetrain.setSafetyEnabled(True)
        self.drive.setSafetyEnabled(False)
        self.intake_arm_solenoid.set(DoubleSolenoid.Value.kReverse)

    def teleopPeriodic(self):
        speed = self.drive_controller.getY(CONTROLLER_LEFT)
        angle = self.drive_controller.getX(CONTROLLER_RIGHT)
        if (abs(angle) > 0.05 or abs(speed) > 0.05):
            self.drive.arcadeDrive(speed, -angle, True) 
        else:
            self.drive.arcadeDrive(0, 0, True)
        
        if self.drive_controller.getStickButtonReleased(CONTROLLER_LEFT):
            self.shifter_shiftsolenoid.set(False)
        if self.drive_controller.getStickButtonReleased(CONTROLLER_RIGHT):
            self.shifter_shiftsolenoid.set(True)

        '''
        #shooter
        if self.drive_controller.getTriggerAxis(CONTROLLER_RIGHT)>0.75:
            self.shooter.run_shooter(self, -0.6)
        else:
            self.motor_master.stopMotor()
            self.motor_slave.stopMotor()
        '''

        if self.drive_controller.getAButton():
            #self.shooter.run_shooter(0.95)
            self.motor_master.set(-0.3)
            self.motor_slave.set(0.3)
        elif self.drive_controller.getXButton():
            #self.shooter.run_shooter(0.5)
            self.motor_master.set(-0.3)
            self.motor_slave.set(0.3)
        else:
            self.motor_master.stopMotor()
            self.motor_slave.stopMotor()

        if self.drive_controller.getBButton():
            #self.shooter.run_shooter(self, 0.35)
            self.motor_master.set(-0.9)
            self.motor_slave.set(0.9)
        else:
            self.motor_master.stopMotor()
            self.motor_slave.stopMotor()


        #shooter hood
        '''
        if self.drive_controller.getStartButtonReleased():
            self.hood_solenoid.set(DoubleSolenoid.Value.kReverse)
        elif self.drive_controller.getBackButtonReleased():
            self.hood_solenoid.set(DoubleSolenoid.Value.kForward)
        '''
        if self.drive_controller.getYButtonReleased():
            self.shooter.switch()
        

        #deploy intake
        '''if self.drive_controller.getYButtonReleased():
            self.intake_arm_solenoid.set(DoubleSolenoid.Value.kForward)
        elif self.drive_controller.getXButtonReleased():
            self.intake_arm_solenoid.set(DoubleSolenoid.Value.kReverse)
        '''



if __name__ == '__main__':
    wpilib.run(SpartaBot)

