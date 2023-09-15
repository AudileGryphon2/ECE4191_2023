#! /usr/bin/env python

from gpiozero import DistanceSensor
from distance_sensor_info import DistanceSensorInfo
import rospy
from std_msgs.msg import Float32


class DistanceSensorCluster: 
    def __init__(self, dist_sensor_info_dict):
        self.dist_sensor_name_to_echo = {}
        self.distance_sensor_pub = {}
        self.dist_sensor_info_dict = dist_sensor_info_dict
        
        self.rate = rospy.Rate(20)
        
        for dist_sensor_name, dist_sensor_info in dist_sensor_info_dict.items():
            self.dist_sensor_name_to_echo[dist_sensor_name] = DistanceSensor(
                max_distance = 4, echo = dist_sensor_info.ECHO, trigger = dist_sensor_info.TRIGGER)
            self.distance_sensor_pub[dist_sensor_name] = rospy.Publisher('ds_' + dist_sensor_name, Float32, queue_size=1)
            # print(self.distance_sensor_pub[dist_sensor_name])
    
    def publish(self):
        for dist_sensor_name, _ in self.dist_sensor_info_dict.items():
            try:
                self.distance_sensor_pub[dist_sensor_name].publish(round(self.dist_sensor_name_to_echo[dist_sensor_name].distance * 100, 4))
            except rospy.ROSInterruptException:
                break
        self.rate.sleep()
    
if __name__ == "__main__":
    rospy.init_node('distance_sensor_cluster')
    
    front_left_dist_sensor = DistanceSensorInfo(name = 'front_left', ECHO = 21, TRIGGER = 20)
    front_right_dist_sensor = DistanceSensorInfo(name = 'front_right', ECHO = 13, TRIGGER = 26)
    # left_dist_sensor = DistanceSensorInfo(name = 'left', ECHO = 16, TRIGGER = 19)
    # right_dist_sensor = DistanceSensorInfo(name = 'right', ECHO = 22, TRIGGER = 10)
    # back_dist_sensor = DistanceSensorInfo(name = 'back', ECHO = 11, TRIGGER = 9)

    # distance_sensor_obj_dict = {'front_left': front_left_dist_sensor, 'front_right': front_right_dist_sensor, 'left': left_dist_sensor, 'right': right_dist_sensor,  'back': back_dist_sensor}
    # distance_sensor_obj_dict = {'front_left': front_left_dist_sensor, 'front_right': front_right_dist_sensor, 'left': left_dist_sensor, 'right': right_dist_sensor}

    distance_sensor_obj_dict = {'front_left': front_left_dist_sensor, 'front_right': front_right_dist_sensor}

    dist_sensor_cls = DistanceSensorCluster(distance_sensor_obj_dict)

    
    while not rospy.is_shutdown(): 
        dist_sensor_cls.publish()