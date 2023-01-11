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



from flask import Flask

app = Flask(__name__)


import py_thorlabs_ctrl.kinesis
py_thorlabs_ctrl.kinesis.init(r'C:\Program Files\Thorlabs\Kinesis')
# change this to your own installation path
from py_thorlabs_ctrl.kinesis.motor import Motor
# tcube = TCubeDCServo(83854669)
# tcube.create()
# tcube.enable()
# tcube.is_homed()
# tcube.get_position()

xmotor = Motor(83854669)
xmotor.create()
xmotor.enable()
xmotor.is_homed()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/position/<axis>')
def get_position(axis):

    resp = {axis: {'position': xmotor.get_position()}}
    return resp
# ============= EOF =============================================
