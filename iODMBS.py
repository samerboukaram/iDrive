#Odrive MakerBase
import odrive


#SERVER CLASS
class ODESC:

    def __init__(self):

        print("odrive version (on PC):", odrive.__version__)
        self.odrv0 = odrive.find_any() #Get Odrive Object
        print(self.odrv0.serial_number)
        

    def EraseConfiguration(self):
  
        #RESTORE DEFAULT BOARD SETTINGS
        self.odrv0.erase_configuration() #rest board to default settings
        # self.Reboot() #check if reboot is required with makerdrive

    def PassSettings(self):


        #MAINBOARD PARAMETER CONFIGURATION
        self.odrv0.config.brake_resistance = 2 #The power resistance parameter is 50W 2Ω,
        self.odrv0.config.dc_bus_undervoltage_trip_level = 8
        self.odrv0.config.dc_bus_overvoltage_trip_level = 56
        #THIS WAS PREVIOUSLY NOT FOUND # self.odrv0.config.dc_max_positive_current = 50 #Max amps, of power supply, for over current protection
        self.odrv0.config.dc_max_negative_current = -2.0 #over current protection
        self.odrv0.config.max_regen_current = 0
        # self.odrv0.save_configuration()
        

        #MOTOR PARAMETER CONFIGURATION
        self.odrv0.axis0.motor.config.pole_pairs = 7 #Pole Pairs
        self.odrv0.axis0.motor.config.motor_type = 0 #MOTOR_TYPE_HIGH_CURRENT (Not gimbal)
        self.odrv0.axis0.motor.config.resistance_calib_max_voltage = 4 #2 by MKR
        self.odrv0.axis0.motor.config.calibration_current = 2 #10 by default, 2 for smaller motors like 5055,4260
        self.odrv0.axis0.motor.config.current_lim =25 #MaX current for motor
        self.odrv0.axis0.motor.config.requested_current_range = 20 #motor current sampling range.
        # self.odrv0.save_configuration()
        

        #ENCODER PARAMETER CONFIGURATION
        self.odrv0.axis0.encoder.config.mode = 0 #ENCODER_MODE_INCREMENTAL
        self.odrv0.axis0.encoder.config.cpr = 16384
        self.odrv0.axis0.encoder.config.bandwidth = 3000 #default was 1000
        self.odrv0.axis0.config.calibration_lockin.current = 5
        self.odrv0.axis0.config.calibration_lockin.ramp_time = 0.4
        self.odrv0.axis0.config.calibration_lockin.ramp_distance = 3.1415927410125732
        self.odrv0.axis0.config.calibration_lockin.accel = 20
        self.odrv0.axis0.config.calibration_lockin.vel = 40
        # self.odrv0.save_configuration()

        #CONTROLLER PARAMETER CONFIGURATION
        self.odrv0.axis0.controller.config.control_mode = 2 #CONTROL_MODE_VELOCITY_CONTROL
        self.odrv0.axis0.controller.config.vel_limit = 30 #18.25 #maximum speed of the motor, the unit is [turn/s]. #Default is 20000
        self.odrv0.axis0.controller.config.pos_gain = 30 #default is 20
        self.odrv0.axis0.controller.config.vel_gain = 0.02 #default is 0.0005
        self.odrv0.axis0.controller.config.vel_integrator_gain = 0.2 #default is 0.001

        #NEW WITH MKR  #CHECK IF THIS IS NEEDED FOR velocity control, or just for position control.
        self.odrv0.axis0.controller.config.input_mode = 5 #INPUT_MODE_TRAP_TRAJ
        self.odrv0.axis0.trap_traj.config.vel_limit = 30
        self.odrv0.axis0.trap_traj.config.accel_limit = 5
        self.odrv0.axis0.trap_traj.config.decel_limit = 5


        #THESE SETTINGS WERE NOT USED
        #Current and Encoder Gains
        ####self.odrv0.axis0.motor.config.current_control_bandwidth = 100 #default was 1000
        #Encoder Calibration settings
        ####self.odrv0.axis0.encoder.config.calib_scan_distance = 600  #increase config.calib_scan_distance up to a factor of 4 above the default. (default is 50, default was 150 for hall, increased to 600 for 5055) not to have a CPR_POLEPAIRS_MISMATCH 
        #####self.odrv0.axis0.encoder.config.calib_range = 0.03  #default was 0.02

        self.SaveConfigurations()
        print('Settings Have been passed')
   

    def PrintSettings(self):
        print("Priniting Settings")
        #MotherBoard ODESC Configurations
        print("Brake Resistance", self.odrv0.config.brake_resistance)

        #Motor
        print("Pole Pairs", self.odrv0.axis0.motor.config.pole_pairs)
        print("Motor Type", self.odrv0.axis0.motor.config.motor_type)
        print("Resistance Calibration Max Voltage", self.odrv0.axis0.motor.config.resistance_calib_max_voltage)
        print("Calibration Current", self.odrv0.axis0.motor.config.calibration_current)
        print("Current Limit", self.odrv0.axis0.motor.config.current_lim)
      

        #Encoder and Control Modes
        print("Encoder Mode", self.odrv0.axis0.encoder.config.mode)
        print("Control Mode", self.odrv0.axis0.controller.config.control_mode)
        print("Encoder CPR", self.odrv0.axis0.encoder.config.cpr)

        #Motor Calibration
        print("Motor Precalibrated", self.odrv0.axis0.motor.config.pre_calibrated)

      
    def CalibrateMotor(self):
        #MOTOR CALIBRATION
        self.odrv0.axis0.requested_state = 4 #AXIS_STATE_MOTOR_CALIBRATION
        print(self.odrv0.axis0.motor)
        self.odrv0.axis0.motor.config.pre_calibrated = True


    def CalibrateEncoder(self):
        #ENCODER CALIBRATION
        self.odrv0.axis0.requested_state = 7 #AXIS_STATE_ENCODER_OFFSET_CALIBRATION
        print(self.odrv0.axis0.encoder)
        self.odrv0.axis0.encoder.config.pre_calibrated = True
        self.odrv0.axis0.config.startup_closed_loop_control = True #Automatically enter closed-loop control after power-on.

    def SaveConfigurations(self):
        self.odrv0.save_configuration()

    def Reboot(self):
        self.odrv0.reboot()


    def SetSpeed(self, RPM):

        self.odrv0.axis0.controller.input_vel = RPM
        # self.odrv0.axis0.encoder.vel_estimate #get/estimate speed of the motor (turns/s)



if __name__ == '__main__':
    OD = ODESC()
    # OD.EraseConfiguration()
    # OD.PassSettings()
    OD.PrintSettings()
    # OD.CalibrateMotor()
    # OD.CalibrateEncoder()
    # OD.SaveConfigurations()
