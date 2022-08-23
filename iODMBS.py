#Odrive MakerBase
import odrive


# Configuration Backup

# You can use odrivetool to back up and restore device configurations or transfer the configuration of one ODrive to another one.

#         To save the configuration to a file on the PC, run

#             odrivetool backup-config my_config.json

# To restore the configuration form such a file, run

#     odrivetool restore-config my_config.json

# Note

# The encoder offset calibration is not restored because this would be dangerous if you transfer the calibration values of one axis to another axis.



# #!/usr/bin/env python3
# """
# Example usage of the ODrive python library to monitor and control ODrive devices
# """

# import odrive
# from odrive.enums import *
# import time
# import math

# # Find a connected ODrive (this will block until you connect one)
# print("finding an odrive...")
# my_drive = odrive.find_any()



# # Calibrate motor and wait for it to finish
# print("starting calibration...")
# my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
# while my_drive.axis0.current_state != AXIS_STATE_IDLE:
#     time.sleep(0.1)

# my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL





# # A sine wave to test
# t0 = time.monotonic()
# while True:
#     setpoint = 4.0 * math.sin((time.monotonic() - t0)*2)
#     print("goto " + str(int(setpoint)))
#     my_drive.axis0.controller.input_pos = setpoint
#     time.sleep(0.01)





#SERVER CLASS
class ODESC:

    def __init__(self):

        print("odrive version (on PC):", odrive.__version__)
        self.FindOdrive()

        
    def FindOdrive(self):
        self.odrv0 = odrive.find_any() #Get Odrive Object, find it again if it disapeared.
        print("Connected To Odrive:", self.odrv0.serial_number)

    def DumpErrors(self):
        odrive.utils.dump_errors(self.odrv0)
        odrive.sys.bac

    def EraseConfiguration(self):
  
        #RESTORE DEFAULT BOARD SETTINGS
        try: #Refind Odrive object after loosing it
            print("Erasing Odrive Configurations and restoring defaults")
            self.odrv0.erase_configuration() 
        except:
            self.FindOdrive()
            self.SaveConfigurations()

        print("Calibration Current", self.odrv0.axis0.motor.config.calibration_current)


    def SaveConfigurations(self):
        self.odrv0.save_configuration()
        print("Configurations Saved To Odrive, now rebooting")
        self.Reboot()

    def Reboot(self):
        try: #Refind Odrive object after loosing it
            self.odrv0.reboot()
        except:
            print("Odrive Rebooted")
            self.FindOdrive()


    def PassSettings(self):


        #MAINBOARD PARAMETER CONFIGURATION
        self.odrv0.config.brake_resistance = 2 #The power resistance parameter is 50W 2Ω,
        self.odrv0.config.dc_bus_undervoltage_trip_level = 8
        self.odrv0.config.dc_bus_overvoltage_trip_level = 56
        self.odrv0.config.dc_max_positive_current = 50 #Max amps, of power supply, for over current protection, this was previously not found
        self.odrv0.config.dc_max_negative_current = -3.0 #over current protection
        self.odrv0.config.max_regen_current = 0 #check if this is current to recharege the battery
        print("Board has been configured")
        

        #MOTOR PARAMETER CONFIGURATION
        self.odrv0.axis0.motor.config.pole_pairs = 7 #Pole Pairs
        self.odrv0.axis0.motor.config.motor_type = 0 #MOTOR_TYPE_HIGH_CURRENT (Not gimbal)
        self.odrv0.axis0.motor.config.resistance_calib_max_voltage = 2 #2 by MKR 4 for iDrive
        self.odrv0.axis0.motor.config.calibration_current = 5 #10 by default, 5 by MKR 2 for iDrive smaller motors like 5055,4260
        self.odrv0.axis0.motor.config.current_lim =15 #MaX current for motor  #15 by MKR #25 for iDrive
        self.odrv0.axis0.motor.config.requested_current_range = 20 #motor current sampling range.
        print("Motor has been configured")
        

        #ENCODER PARAMETER CONFIGURATION
        self.odrv0.axis0.encoder.config.mode = 0 #ENCODER_MODE_INCREMENTAL
        self.odrv0.axis0.encoder.config.cpr = 16384 #MKR encoder
        self.odrv0.axis0.encoder.config.bandwidth = 3000 # 3000MKR default was 1000
        self.odrv0.axis0.config.calibration_lockin.current = 5 #MKR
        self.odrv0.axis0.config.calibration_lockin.ramp_time = 0.4 #MKR
        self.odrv0.axis0.config.calibration_lockin.ramp_distance = 3.1415927410125732 #MKR
        self.odrv0.axis0.config.calibration_lockin.accel = 20 #MKR
        self.odrv0.axis0.config.calibration_lockin.vel = 40 #MKR
        print("Encoder has been configured")

        #CONTROLLER PARAMETER CONFIGURATION
        self.odrv0.axis0.controller.config.control_mode = 2 #CONTROL_MODE_VELOCITY_CONTROL
        self.odrv0.axis0.controller.config.vel_limit = 30 #18.25 #maximum speed of the motor, the unit is [turn/s]. # CHECK MKR VALUE
        self.odrv0.axis0.controller.config.pos_gain = 30 # 30 MKR default is 20
        self.odrv0.axis0.controller.config.vel_gain = 0.02 # 0.02 MKR default is 0.0005
        self.odrv0.axis0.controller.config.vel_integrator_gain = 0.2 # 0.2 MKR default is 0.001
        print("Controller has been configured")

        #TRAP TRAJ: NEW WITH MKR  #CHECK IF THIS IS NEEDED FOR velocity control, or just for position control.
        self.odrv0.axis0.controller.config.input_mode = 5 #INPUT_MODE_TRAP_TRAJ
        self.odrv0.axis0.trap_traj.config.vel_limit = 30
        self.odrv0.axis0.trap_traj.config.accel_limit = 5
        self.odrv0.axis0.trap_traj.config.decel_limit = 5
        print("Trap Traj Configured")


        #SETTINGS THAT SHOULD BE USED WITH HALL SENSORS
        #Current and Encoder Gains
        ####self.odrv0.axis0.motor.config.current_control_bandwidth = 100 #default was 1000
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
        print("Motor Calibrated")
        self.SaveConfigurations()


    def CalibrateEncoder(self):
        #ENCODER CALIBRATION
        self.odrv0.axis0.requested_state = 7 #AXIS_STATE_ENCODER_OFFSET_CALIBRATION
        print(self.odrv0.axis0.encoder)
        self.odrv0.axis0.encoder.config.pre_calibrated = True
        self.odrv0.axis0.config.startup_closed_loop_control = True #Automatically enter closed-loop control after power-on.
        print("Encoder Calibrated")
        self.SaveConfigurations()


    def SetSpeed(self, RPM):

        self.odrv0.axis0.controller.input_vel = RPM
        # self.odrv0.axis0.encoder.vel_estimate #get/estimate speed of the motor (turns/s)



if __name__ == '__main__':
    OD = ODESC()
    # OD.Reboot()
    OD.DumpErrors()
    # OD.EraseConfiguration()
    # OD.PassSettings()
    # OD.PrintSettings()
    # OD.CalibrateMotor()
    # OD.CalibrateEncoder()
 