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
file_path = 'calibration_gyro_z.txt'
noise_threshold = 0.1
##

with open(file_path, 'r') as file:
    # Read the content of the file into a string
    data_str = file.read()
    
gyro_calibration_dict = json.loads(data_str)
print(gyro_calibration_dict)
z_calib = gyro_calibration_dict['z']
theta = 0

while time_elapsed < 20:    
    tstart = time()

    gyro_z = []
    for idx in range(10): 
        gyro_data = sensor.get_gyro_data() 
        
        gyro_z.append(gyro_data['z'] - z_calib)

    average_gyro_z = np.mean(gyro_z)
    
    if abs(np.mean(gyro_z)) < noise_threshold:
        average_gyro_z = 0
    else: 
        average_gyro_z = np.mean(gyro_z)
        
    print('averaged_z', average_gyro_z)
    
    theta += average_gyro_z*(time()-tstart) 
    print('theta ',theta)
    
    time_elapsed = int(time() - initial_time)
    
z = np.mean(gyro_z)

print("z: ", z)

time_axis = range(1, len(gyro_z) + 1)

plt.plot(time_axis, gyro_z)
plt.show(block = True)
