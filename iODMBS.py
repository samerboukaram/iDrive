#Odrive MakerBase
import odrive
import time

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
     

    def EraseConfiguration(self):
  
        #RESTORE DEFAULT BOARD SETTINGS
        try: #Refind Odrive object after loosing it
            print("Erasing Odrive Configurations and restoring defaults")
            self.odrv0.erase_configuration() 
        except:
            self.FindOdrive()

        print("Erase Successfull")


    def SaveConfigurations(self):
        self.odrv0.save_configuration()
        print("Configurations Saved To Odrive")
  

    def Reboot(self):
        try: #Refind Odrive object after loosing it
            print("Rebooting")
            self.odrv0.reboot()
        except:
            print("Odrive Rebooted")
            self.FindOdrive()



    def ConfigureBoard(self):
        self.odrv0.config.brake_resistance = 2 #Bracking resistor 50W 2Ω,
        self.odrv0.config.dc_bus_undervoltage_trip_level = 8 #Min Board Voltage
        self.odrv0.config.dc_bus_overvoltage_trip_level = 56 #Max Board Voltage
        self.odrv0.config.dc_max_positive_current = 50 #Max amps from Battery
        self.odrv0.config.dc_max_negative_current = -3.0 #Max Recharging Current
        self.odrv0.config.max_regen_current = 0 #!!!!!!!
        print("Board has been configured")

    def ConfigureMotor(self, PolePairs):
        self.odrv0.axis0.motor.config.pole_pairs = PolePairs #Pole Pairs
        self.odrv0.axis0.motor.config.motor_type = 0 #MOTOR_TYPE_HIGH_CURRENT (Not gimbal)
        self.odrv0.axis0.motor.config.resistance_calib_max_voltage = 2 #2 by MKR 4 for iDrive
        self.odrv0.axis0.motor.config.calibration_current = 5 #10 by default, 5 by MKR 2 for iDrive smaller motors like 5055,4260
        self.odrv0.axis0.motor.config.current_lim =15 #MaX current for motor  #15 by MKR #25 for iDrive
        self.odrv0.axis0.motor.config.requested_current_range = 20 #motor current sampling range.
        #self.odrv0.axis0.motor.config.direction = 0 #-1 1
        print("Motor has been configured")

        #Motor Calibration
        print("starting Motor calibration...")
        self.odrv0.axis0.requested_state = 4 #AXIS_STATE_MOTOR_CALIBRATION
        #Wait for calibration to finish
        print("Calibrating...")
        while self.odrv0.axis0.current_state != 1: #AXIS_STATE_IDLE
            time.sleep(0.1)

        self.odrv0.axis0.motor.config.pre_calibrated = True
        print("Motor Phase Inductance:", self.odrv0.axis0.motor.config.phase_inductance)
        print("Motor Phase Resistance:", self.odrv0.axis0.motor.config.phase_resistance)
        print("Motor Calibrated")
        self.DumpErrors()
        self.SaveConfigurations()

    def ConfigureEncoder(self, CPR):
        self.odrv0.axis0.encoder.config.mode = 0 #ENCODER_MODE_INCREMENTAL
        self.odrv0.axis0.encoder.config.cpr = CPR #MKR encoder
        self.odrv0.axis0.encoder.config.bandwidth = 3000 # 3000MKR default was 1000
        self.odrv0.axis0.config.calibration_lockin.current = 5 #MKR
        # self.odrv0.axis0.config.can_node_id = 16
        print("Encoder has been configured")

    def ConfigureGains(self):
        self.odrv0.axis0.controller.config.pos_gain = 30 # 30 MKR default is 20
        self.odrv0.axis0.controller.config.vel_gain = 0.02 # 0.02 MKR default is 0.0005
        self.odrv0.axis0.controller.config.vel_integrator_gain = 0.2 # 0.2 MKR default is 0.001
        self.odrv0.axis0.controller.config.vel_limit = 30 #18.25 #maximum speed of the motor, the unit is [turn/s]. # CHECK MKR VALUE
        
        print("Controller Gains were configured")

    def ConfigureTrapTraj(self):

        #OPTIONAL
        #TRAP TRAJ: This mode lets you smoothly accelerate, coast, and decelerate the axis from one position to another.
        #With raw position control, the controller simply tries to go to the setpoint as quickly as possible.

        self.odrv0.axis0.controller.config.input_mode = 5 #INPUT_MODE_TRAP_TRAJ
        self.odrv0.axis0.trap_traj.config.vel_limit = 30
        self.odrv0.axis0.trap_traj.config.accel_limit = 5
        self.odrv0.axis0.trap_traj.config.decel_limit = 5
        print("Trap Traj Configured")




    def CalibrateEncoder(self):
        #ENCODER CALIBRATION
        print("Encoder Offset Float", self.odrv0.axis0.encoder.config.offset_float)
        print("Encoder Offset", self.odrv0.axis0.encoder.config.offset)
        print("Starting Encoder Calibration")
        self.odrv0.axis0.requested_state = 7 #AXIS_STATE_ENCODER_OFFSET_CALIBRATION
        print("Calibrating...")
        while self.odrv0.axis0.current_state != 1: #AXIS_STATE_IDLE
            time.sleep(0.1)

        self.odrv0.axis0.encoder.config.pre_calibrated = True
        self.odrv0.axis0.config.startup_closed_loop_control = True #Automatically enter closed-loop control after power-on.
        print("Encoder Offset Float", self.odrv0.axis0.encoder.config.offset_float)
        print("Encoder Offset", self.odrv0.axis0.encoder.config.offset)

        print("Encoder Calibrated")
        self.DumpErrors()
        self.SaveConfigurations()


    def HallSensorsRandom(self):
        pass
        #SETTINGS THAT SHOULD BE USED WITH HALL SENSORS
        #Current and Encoder Gains
        ####self.odrv0.axis0.motor.config.current_control_bandwidth = 100 #default was 1000
        ####self.odrv0.axis0.encoder.config.calib_scan_distance = 600  #increase config.calib_scan_distance up to a factor of 4 above the default. (default is 50, default was 150 for hall, increased to 600 for 5055) not to have a CPR_POLEPAIRS_MISMATCH 
        #####self.odrv0.axis0.encoder.config.calib_range = 0.03  #default was 0.02
        # self.odrv0.axis0.config.calibration_lockin.ramp_time = 0.4 #MKR
        # self.odrv0.axis0.config.calibration_lockin.ramp_distance = 3.1415927410125732 #MKR
        # self.odrv0.axis0.config.calibration_lockin.accel = 20 #MKR
        # self.odrv0.axis0.config.calibration_lockin.vel = 40 #MKR



    def PassSettings(self):


        self.ConfigureBoard()

        self.ConfigureMotor(7)
        self.ConfigureEncoder(16384)
        self.ConfigureGains()

        # self.ConfigureTrapTraj()

        self.CalibrateEncoder()

        self.SaveConfigurations()
        self.Reboot()
        print('Settings Have been passed')
   

        

    def SetVelocityMode(self):
        self.odrv0.axis0.requested_state = 8 #AXIS_STATE_CLOSED_LOOP_CONTROL
        self.odrv0.axis0.controller.config.control_mode = 2 #CONTROL_MODE_VELOCITY_CONTROL
        
        print(self.odrv0.axis0.current_state)



 
    def SetSpeed(self, RPM):

        self.odrv0.axis0.controller.input_vel = RPM/60 #in turns/sec


if __name__ == '__main__':
    OD = ODESC()
    # OD.Reboot()
    # OD.DumpErrors()
    # OD.EraseConfiguration()
    # OD.PassSettings()

    OD.SetVelocityMode()

    # while True:
    #     OD.SetSpeed(0)
