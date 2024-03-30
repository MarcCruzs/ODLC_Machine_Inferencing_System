#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
import math
from visualization_msgs.msg import Marker
import os

if __name__ == '__main__':
    rospy.init_node("test")

    def callback(msg):
        
        print("marker.x: " + str(msg.pose.position.x))
        print("marker.y: " + str(msg.pose.position.y))

    sub = rospy.Subscriber('/visualization_marker', Marker, callback)

    rospy.spin()