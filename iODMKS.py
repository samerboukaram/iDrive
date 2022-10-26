#Odrive MakerBase
import odrive
import time

# ODRIVE ENUMS
# https://github.com/odriverobotics/ODrive/blob/master/tools/odrive/enums.py

'''CONFIGURATIONS BACKUP

# You can use odrivetool to back up and restore device configuration
#  or transfer the configuration of one ODrive to another one.

#To save the configuration to a file on the PC, run
#             odrivetool backup-config my_config.json

# To restore the configuration form such a file, run
#           odrivetool restore-config my_config.json

# Note
# The encoder offset calibration is not restored because this would be dangerou
#  if you transfer the calibration values of one axis to another axis.

'''



#SERVER CLASS
class ODESC:

    def __init__(self):

        print("odrive version on PC:", odrive.__version__)
        self.FindOdrive()

        print("firmware version on board", self.GetFirmwareVersion())


    def GetFirmwareVersion(self):
        FWVersion = (str(self.odrv0.fw_version_major)
            + "." + str(self.odrv0.fw_version_minor)
            + "." + str(self.odrv0.fw_version_revision)
            + ".post" + str(self.odrv0.fw_version_unreleased))
        print(FWVersion)

        
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

    def ConfigureMotor(self, Axis, PolePairs,MaxSVoltage,KV):
        if Axis == 0: Axis = self.odrv0.axis0
        if Axis == 1: Axis = self.odrv0.axis1

        Axis.motor.config.pole_pairs = PolePairs #Pole Pairs
        Axis.motor.config.motor_type = 0 #MOTOR_TYPE_HIGH_CURRENT (Not gimbal)
        Axis.motor.config.resistance_calib_max_voltage = 5 #MaxSVoltage/2 #2 by MKS 4 for iDrive #it is standardized to S/2
        Axis.motor.config.calibration_current =10 #10 for 6354, 5 by MKS 2 for iDrive smaller motors like 5055,4260 #Standardized to S
        Axis.motor.config.current_lim = 50 #25 #MaxSVoltage*3.65 #MaX current for motor  #15 by MKS #25 for iDrive
        Axis.motor.config.requested_current_range = MaxSVoltage*3.65+5 #20 for MKS motor current sampling range.
        #Axis.motor.config.direction = 0 #-1 1
        Axis.controller.config.vel_limit = MaxSVoltage*980*3.65/60 #30 for MKS #18.25 #maximum speed of the motor, the unit is [turn/s]. # CHECK MKS VALUE
        print("Motor has been configured")

        #Motor Calibration
        print("starting Motor calibration...")
        Axis.requested_state = 4 #AXIS_STATE_MOTOR_CALIBRATION
        #Wait for calibration to finish
        print("Calibrating...")
        while Axis.current_state != 1: #AXIS_STATE_IDLE
            time.sleep(0.1)

        Axis.motor.config.pre_calibrated = True
        print("Motor Phase Inductance:", Axis.motor.config.phase_inductance)
        print("Motor Phase Resistance:", Axis.motor.config.phase_resistance)
        print("Motor Calibrated")
        self.DumpErrors()
        self.SaveConfigurations()

    def ConfigureEncoder(self, Axis, CPR):
        if Axis == 0: Axis = self.odrv0.axis0
        if Axis == 1: Axis = self.odrv0.axis1

        Axis.encoder.config.mode = 0 #ENCODER_MODE_INCREMENTAL
        Axis.encoder.config.cpr = CPR #MKS encoder
        Axis.encoder.config.bandwidth = 3000 # 3000MKS default was 1000
        Axis.encoder.config.calib_scan_distance = 50 #how much the motor rotates for calibration
        #               default was 50 increased  not to have CPR Mismatch
        Axis.config.calibration_lockin.current = 5 #MKS
        # Axis.config.can_node_id = 16
        print("Encoder has been configured")

    def ConfigureGains(self, Axis):
        if Axis == 0: Axis = self.odrv0.axis0
        if Axis == 1: Axis = self.odrv0.axis1

        # Axis.controller.config.pos_gain = 30 # 30 MKS default is 20
        # print(Axis.controller.config.vel_gain)
        Axis.controller.config.vel_gain = 0.1 # 0.02 MKS default is 0.0005 #Higher values better for low speeds
        Axis.controller.config.vel_integrator_gain = 10 # 0.2 MKS default is 0.001

        # 0.1 5 good
        
     
        print("Controller Gains were configured")


    def EncoderSignalSearch(self, Axis):
        if Axis == 0: Axis = self.odrv0.axis0
        if Axis == 1: Axis = self.odrv0.axis1
        
        Axis.encoder.config.use_index = True

        Axis.requested_state = 6 #AXIS_STATE_ENCODER_INDEX_SEARCH
        print("Finding Encoder Index...")
        while Axis.current_state != 1: #AXIS_STATE_IDLE
            time.sleep(0.1)
        print("Index Signal Found!!")

        # Axis.config.startup_encoder_index_search = True #This searches for the index on each startup
        

    def CalibrateEncoder(self, Axis):
        if Axis == 0: Axis = self.odrv0.axis0
        if Axis == 1: Axis = self.odrv0.axis1

        #ENCODER CALIBRATION
        print("Encoder Offset Float", Axis.encoder.config.offset_float)
        print("Encoder Offset", Axis.encoder.config.offset)
        print("Starting Encoder Calibration")
        Axis.requested_state = 7 #AXIS_STATE_ENCODER_OFFSET_CALIBRATION
        print("Calibrating...")
        while Axis.current_state != 1: #AXIS_STATE_IDLE
            time.sleep(0.1)

        # Axis.encoder.config.pre_calibrated = True   #this option will go Back to false if INDEX signal search was not done
        Axis.config.startup_encoder_offset_calibration = True #start encoder calibration after powering
        # Axis.config.startup_closed_loop_control = True #Automatically enter closed-loop control after power-on.
     	

        print("Encoder Offset Float", Axis.encoder.config.offset_float)
        print("Encoder Offset", Axis.encoder.config.offset)

        print("Encoder Calibrated")
        self.DumpErrors()
        self.SaveConfigurations()


    def HallSensorsSettings(self, Axis): #Not Configured, just draft
        if Axis == 0: Axis = self.odrv0.axis0
        if Axis == 1: Axis = self.odrv0.axis1

        pass
        #SETTINGS THAT SHOULD BE USED WITH HALL SENSORS
        #Current and Encoder Gains
        #Axis.motor.config.current_control_bandwidth = 100 #default was 1000
        #Axis.encoder.config.calib_scan_distance = 600  #increase config.calib_scan_distance up to a factor of 4 above the default. (default is 50, default was 150 for hall, increased to 600 for 5055) not to have a CPR_POLEPAIRS_MISMATCH 
        #Axis.encoder.config.calib_range = 0.03  #default was 0.02
        # Axis.config.calibration_lockin.ramp_time = 0.4 #MKS
        # Axis.config.calibration_lockin.ramp_distance = 3.1415927410125732 #MKS
        # Axis.config.calibration_lockin.accel = 20 #MKS
        # Axis.config.calibration_lockin.vel = 40 #MKS


    def PassSettings(self, Axis):


        self.ConfigureBoard()

        #Small motor
        # self.ConfigureMotor(Axis = 0,PolePairs = 7, MaxSVoltage = 4, KV = 980)
        self.ConfigureMotor(Axis = Axis,PolePairs = 7, MaxSVoltage = 5, KV = 60)
        self.ConfigureEncoder(Axis = Axis, CPR = 16384)
        self.ConfigureGains(Axis)

        # self.EncoderSignalSearch(Axis) #added to save encoder calibration
        self.CalibrateEncoder(Axis)

        self.SaveConfigurations()
        # self.Reboot()
        print('Settings Have been passed')

   
    #POSITION CONTROL
    def SetPositionMode(self, Axis):
        if Axis == 0: Axis = self.odrv0.axis0
        if Axis == 1: Axis = self.odrv0.axis1

        Axis.controller.config.control_mode = 3 #CONTROL_MODE_POSITION_CONTROL
     
        #Configure Trap Traj
        Axis.controller.config.input_mode = 5 #INPUT_MODE_TRAP_TRAJ
        Axis.trap_traj.config.vel_limit = 20
        Axis.trap_traj.config.accel_limit = 5
        Axis.trap_traj.config.decel_limit = 5
        # Axis.controller.config.inertia = 0 #Optional
        # Axis.config.motor.current_soft_max = <Float> #Optional
       
        
        print("Trap Traj Configured")

        #Lock Axis		
        Axis.requested_state = 8 #AXIS_STATE_CLOSED_LOOP_CONTROL		
  
        
      

    def SetPosition(self, Axis, Position):
        if Axis == 0: Axis = self.odrv0.axis0
        if Axis == 1: Axis = self.odrv0.axis1

        Axis.controller.input_pos = Position

    def SetPositionIncremental(self, Axis, Increment):
        if Axis == 0: Axis = self.odrv0.axis0
        if Axis == 1: Axis = self.odrv0.axis1

        #Move incremental
        Axis.controller.move_incremental(Increment, from_goal_point = False)
        # To set the goal relative to the current actual position, use from_goal_point = False
        # To set the goal relative to the previous destination, use from_goal_point = True
        

    def ReleaseAxis(self, Axis):
        if Axis == 0: Axis = self.odrv0.axis0
        if Axis == 1: Axis = self.odrv0.axis1

        Axis.requested_state = 1 #AXIS_STATE_IDLE

        
    #VELOCITY CONTROL (including RAMPED)
    def SetVelocityMode(self, Axis):
        if Axis == 0: Axis = self.odrv0.axis0
        if Axis == 1: Axis = self.odrv0.axis1

        Axis.controller.config.control_mode = 2 #CONTROL_MODE_VELOCITY_CONTROL
        
        # #RAMPED VELOCITY CONTROL #Lets you set the acceleration
        # Axis.controller.config.vel_ramp_rate = 5 #default 0.5 #acceleration in turn/s^2
        # Axis.controller.config.input_mode = 2 #INPUT_MODE_VEL_RAMP
        
        Axis.requested_state = 8 #AXIS_STATE_CLOSED_LOOP_CONTROL
        print(Axis.current_state)

    def SetSpeed(self, Axis, RPM):
        if Axis == 0: Axis = self.odrv0.axis0
        if Axis == 1: Axis = self.odrv0.axis1
        
        Axis.controller.input_vel = RPM/60 #in turns/sec

    def GetCurrent(self, Axis):
        if Axis == 0: Axis = self.odrv0.axis0
        if Axis == 1: Axis = self.odrv0.axis1
        
        CommandedCurrent = round(Axis.motor.current_control.Iq_setpoint,2)
        MeasuredCurrent = round(Axis.motor.current_control.Iq_measured,2)

        
        #Encoder position 
        Turns = Axis.encoder.pos_estimate #[turns] 
        # Counts = Axis.encoder.pos_est_counts #[counts]

        #View rotational velocity with 
        TurnsPerSec = round(Axis.encoder.vel_estimate,2) #[turn/s] 
        # CountsPerSec = Axis.encoder.vel_est_counts #[count/s]

        # print(MeasuredCurrent, round(CommandedCurrent-MeasuredCurrent,2),TurnsPerSec*60)
        return MeasuredCurrent


if __name__ == '__main__':

    OD = ODESC()
    # OD.Reboot()
    OD.DumpErrors()
    # OD.EraseConfiguration()
    # OD.PassSettings(0)
    # OD.PassSettings(1)

    # OD.ConfigureMotor(Axis = 0,PolePairs = 7, MaxSVoltage = 5, KV = 100)
    # OD.ConfigureEncoder(Axis = 0, CPR = 16384)
    # OD.ConfigureGains(Axis = 0)

    # OD.ConfigureMotor(Axis = 1,PolePairs = 7, MaxSVoltage = 5, KV = 140)
    # OD.ConfigureEncoder(Axis = 1, CPR = 16384)
    # OD.ConfigureGains(Axis = 1)

        
    # OD.odrv0.axis0.encoder.config.use_index = True
    # OD.odrv0.axis1.encoder.config.use_index = True

    # OD.odrv0.axis0.requested_state = 6 #AXIS_STATE_ENCODER_INDEX_SEARCH
    # OD.odrv0.axis1.requested_state = 6 #AXIS_STATE_ENCODER_INDEX_SEARCH


    # OD.EncoderSignalSearch(1) #added to save encoder calibration
    # OD.EncoderSignalSearch(0) #added to save encoder calibration

    # OD.CalibrateEncoder(Axis)

    # OD.SaveConfigurations()



    # OD.SetVelocityMode(0)
    # OD.SetVelocityMode(1)
    # OD.SetSpeed(Axis = 0, RPM = 20)
    # OD.ReleaseAxis(0)
    # OD.SetSpeed(Axis = 1, RPM = 100)

    # Get motor current
    # while True:
        # print(OD.GetCurrent(0)+OD.GetCurrent(1))
    # import iPS4

    # PS4 = iPS4.PS4Controller()

    # while True:
    #     PS4.GetValues()
    #     RPM = -int(PS4.LeftStickUD*1000/10)
    #     OD.SetSpeed(Axis = 0, RPM = 42+RPM)


    # OD.SetPositionMode(0)
    # for i in range(20):
    #     OD.SetPosition(Axis= 0, Position = -0.1*i)
    #     time.sleep(1)
    # OD.SetPositionIncremental(Axis = 0, Increment = 50)
    # OD.ReleaseAxis(Axis = 0)
     

 



#SINE WAVE EXAMPLE

# import odrive
# from odrive.enums import *
# import time
# import math

# # A sine wave to test
# t0 = time.monotonic()
# while True:
#     setpoint = 4.0 * math.sin((time.monotonic() - t0)*2)
#     print("goto " + str(int(setpoint)))
#     my_drive.axis0.controller.input_pos = setpoint
#     time.sleep(0.01)

