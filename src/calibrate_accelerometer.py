#!/usr/bin/env python
"""Released under the MIT License
Copyright 2015, 2016 MrTijn/Tijndagamer
"""

from mpu6050 import mpu6050
from time import sleep, time
import matplotlib.pyplot as plt
import numpy as np
import json

sensor = mpu6050(0x68)

## INPUTS 
file_path = 'calibration_accel.txt'
calibration_time = 40
##

initial_time = time()
time_elapsed = 0


while time_elapsed < calibration_time:
    accel_x = []
    accel_y = []
    accel_z = []

    accel_data = sensor.get_accel_data() 
    
    print('averaged_x', accel_data['x'], 'averaged_y', accel_data['y'], 'averaged_z', accel_data['z'])
    
    accel_x.append(accel_data['x'])
    accel_y.append(accel_data['y'])
    accel_z.append(accel_data['z'])
        
    time_elapsed = int(time() - initial_time)
    
accel_calibration_dict = {'x': np.mean(accel_x), 'y': np.mean(accel_y), 'z': np.mean(accel_z)}
with open(file_path, 'w') as file:
    data_str  = json.dumps(accel_calibration_dict)
    file.write(data_str)

