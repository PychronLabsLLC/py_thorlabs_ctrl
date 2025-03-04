import py_thorlabs_ctrl.kinesis
import clr, time

POLLING_INTERVAL = 250
ENABLE_SLEEP_TIME = 0.1

py_thorlabs_ctrl.kinesis.check_import()
  
from System import String
from System import Decimal

clr.AddReference('System.Collections')
   
clr.AddReference("Thorlabs.MotionControl.GenericMotorCLI")
clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")

import Thorlabs.MotionControl.DeviceManagerCLI
from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI
import Thorlabs.MotionControl.GenericMotorCLI

class Motor:

    """
    Base class for Thorlabs motion controllers. Contains basic functions that apply to most controllers.
    """

    INIT_TIMEOUT = 5000

    def __init__(self, serial_number):
        self.serial_number = str(serial_number)

    def create(self):
        # abstract
        pass

    def get_device(self):
        try:
            device = self.device
        except AttributeError:
            print('device not created!')
            raise

        return device

    def enable(self):
        device = self.get_device()

        device.Connect(self.serial_number)

        if not device.IsSettingsInitialized():
            device.WaitForSettingsInitialized(self.INIT_TIMEOUT)
            
        device.StartPolling(POLLING_INTERVAL)
        time.sleep(ENABLE_SLEEP_TIME)
        device.EnableDevice()
        time.sleep(ENABLE_SLEEP_TIME)

        device.LoadMotorConfiguration(self.serial_number)
        
    def get_serial_number(self):
        device = self.get_device()
        device_info = device.GetDeviceInfo()
        return device_info.SerialNumber
        
    def get_name(self):
        device = self.get_device()
        device_info = device.GetDeviceInfo()
        return device_info.Name

    def get_position(self):
    
        device = self.get_device()

        return Decimal.ToDouble(device.DevicePosition)
        
    def set_velocity(self, max_velocity = None, acceleration = None):
        
        device = self.get_device()
        velocity_params = device.GetVelocityParams()
        max_velocity = Decimal.ToDouble(params.MaxVelocity) if max_velocity == None else max_velocity
        acceleration = Decimal.ToDouble(params.Acceleration) if acceleration == None else acceleration
        
        device.SetVelocityParams(Decimal(max_velocity), Decimal(acceleration))
        
    def is_homed(self):
    
        device = self.get_device()
        return device.Status.IsHomed
        
    def home(self):
    
        device = self.get_device()
        device.Home(0)

    def move_relative(self, dis):
        device = self.get_device()

        device.SetMoveRelativeDistance(Decimal(dis))
        device.MoveRelative(0)

    def move_absolute(self, pos):
        device = self.get_device()

        device.MoveTo(Decimal(pos), 0)
        
    def disable(self):
        device = self.get_device()
        device.DisableDevice()

    def disconnect(self):
        device = self.get_device()

        device.Disconnect()


class KCubeMotor(Motor):

    """
    Base class for K-Cubes.
    """
        
    def set_joystickmode_velocity(self):
    
        device = self.get_device()
        params = device.GetMMIParams()
        try:
            # prior to kinesis 1.14.6
            params.WheelMode = Thorlabs.MotionControl.GenericMotorCLI.Settings.KCubeMMISettings.KCubeWheelMode.Velocity
        except AttributeError:
            try:
                params.JoystickMode = Thorlabs.MotionControl.GenericMotorCLI.Settings.KCubeMMISettings.KCubeJoystickMode.Velocity
            except AttributeError:
                raise AttributeError('cannot find this attribute. APIs have changed. look up latest documentation.')
        device.SetMMIParams(params)
        
    def set_display_intensity(self, intensity):
    
        device = self.get_device()
        params = device.GetMMIParams()
        params.DisplayIntensity = intensity
        device.SetMMIParams(params)
        
    def set_display_timeout(self, timeout):
    
        device = self.get_device()
        params = device.GetMMIParams()
        params.DisplayTimeout = timeout
        device.SetMMIParams(params)
    
        
class TCubeMotor(Motor):

    """
    Base class for K-Cubes.
    """

    pass
        
class KCubeDCServo(KCubeMotor):

    def create(self):
    
        clr.AddReference("ThorLabs.MotionControl.KCube.DCServoCLI")
        from Thorlabs.MotionControl.KCube.DCServoCLI import KCubeDCServo
        
        DeviceManagerCLI.BuildDeviceList()
        self.device = KCubeDCServo.CreateKCubeDCServo(self.serial_number)

class TCubeDCServo(TCubeMotor):

    def create(self):
    
        clr.AddReference("ThorLabs.MotionControl.TCube.DCServoCLI")
        from Thorlabs.MotionControl.TCube.DCServoCLI import TCubeDCServo

        DeviceManagerCLI.BuildDeviceList()
        self.device = TCubeDCServo.CreateTCubeDCServo(self.serial_number)
        
class TCubeStepper(TCubeMotor):

    def create(self):
        
        clr.AddReference("Thorlabs.MotionControl.TCube.StepperMotorCLI")
        from Thorlabs.MotionControl.TCube.StepperMotorCLI import TCubeStepper
        
        DeviceManagerCLI.BuildDeviceList()
        self.device = TCubeStepper.CreateTCubeStepper(self.serial_number)