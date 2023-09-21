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

initial_time = time()
time_elapsed = 0

## INPUTS 
file_path = 'calibration_accel.txt'
noise_threshold = 0.1
##

with open(file_path, 'r') as file:
    # Read the content of the file into a string
    data_str = file.read()
    
accel_calibration_dict = json.loads(data_str)
print(accel_calibration_dict)

x_calib = accel_calibration_dict['x']
y_calib = accel_calibration_dict['y']
z_calib = accel_calibration_dict['z']
theta = 0

while time_elapsed < 20:    
    tstart = time()

    accel_x = []
    accel_y = []
    accel_z = []
    
    for idx in range(10): 
        accel_data = sensor.get_accel_data() 
        
        accel_x.append(accel_data['x'] - x_calib)
        accel_y.append(accel_data['y'] - y_calib)
        accel_z.append(accel_data['z'] - z_calib)

    average_gyro_x = np.mean(accel_x)
    average_gyro_y = np.mean(accel_y)
    average_gyro_z = np.mean(accel_z)
    
    
    if abs(np.mean(accel_x)) < noise_threshold:
        average_gyro_x = 0
    else: 
        average_gyro_x = np.mean(accel_x)
        
    if abs(np.mean(accel_y)) < noise_threshold:
        average_gyro_y = 0
    else: 
        average_gyro_y = np.mean(accel_y)
        
    if abs(np.mean(accel_z)) < noise_threshold:
        average_gyro_z = 0
    else: 
        average_gyro_z = np.mean(accel_z)
        
        
    print('averaged_x', average_gyro_x, 'averaged_y', average_gyro_y, 'averaged_z', average_gyro_z)
        
    time_elapsed = int(time() - initial_time)
    

