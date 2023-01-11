# ===============================================================================
# Copyright 2023 ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================
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

class BenchTopStepperController:
    device = None
    def __init__(self, serial_number):
        self.serial_number = serial_number

    def get_device(self):
        try:
            device = self.device
        except AttributeError:
            print('device not created!')
            raise

        return device
    def get_channel(self, idx):
        device = self.get_device()
        return device.GetChannel(idx)

    def create(self):
        clr.AddReference("ThorLabs.MotionControl.Benchtop.StepperMotorCLI")
        from Thorlabs.MotionControl.Benchtop.StepperMotorCLI import BenchtopStepperMotor

        DeviceManagerCLI.BuildDeviceList()
        self.device = BenchtopStepperMotor.CreateBenchtopStepperMotor(self.serial_number)
    def enable(self):
        device = self.get_device()

        device.Connect(self.serial_number)

        for i in range(3):
            channel = device.GetChannel(i+1)
            if not channel.IsSettingsInitialized():
                channel.WaitForSettingsInitialized(self.INIT_TIMEOUT)

            channel.StartPolling(POLLING_INTERVAL)
            time.sleep(ENABLE_SLEEP_TIME)
            channel.EnableDevice()
            time.sleep(ENABLE_SLEEP_TIME)

            channel.LoadMotorConfiguration(self.serial_number)
    def get_position(self, channel):
        channel = self.get_channel(channel)
        return Decimal.ToDouble(channel.DevicePosition)
# ============= EOF =============================================
