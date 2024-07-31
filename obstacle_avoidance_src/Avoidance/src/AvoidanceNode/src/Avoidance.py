#! /usr/bin/env python

import math

import rospy
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker

rospy.init_node("rviz_marker")

rospy.loginfo("my_tutorial_node started!")

marker_pub = rospy.Publisher("/visualization_marker", Marker, queue_size=2)

marker = Marker()

marker.header.frame_id = "/map"
marker.header.stamp = rospy.Time.now()

# set shape, Arrow: 0; Cube: 1 ; Sphere: 2 ; Cylinder: 3
marker.type = 2
marker.id = 0

# Set the scale of the marker
marker.scale.x = 1.0
marker.scale.y = 1.0
marker.scale.z = 1.0

# Set the color
marker.color.r = 0.0
marker.color.g = 1.0
marker.color.b = 0.0
marker.color.a = 1.0

# Set the pose of the marker
marker.pose.position.x = 0
marker.pose.position.y = 0
marker.pose.position.z = 0
marker.pose.orientation.x = 0.0
marker.pose.orientation.y = 0.0
marker.pose.orientation.z = 0.0
marker.pose.orientation.w = 1.0


def callback(msg):
    mag = 0
    angle = 0
    for i in range(int((msg.angle_max - msg.angle_min) / msg.angle_increment)):
        inv_dist = 1 / msg.ranges[i]
        neg_ang = -1 * (msg.angle_min + msg.angle_increment * i)

        mag = math.sqrt((inv_dist) ** 2 + mag**2 + 2 * inv_dist * mag * math.cos(angle - neg_ang))
        angle = angle + math.atan2(inv_dist * math.sin(neg_ang - angle), mag + inv_dist * math.cos(neg_ang - angle))

    marker.pose.position.x = mag * math.cos(angle)
    marker.pose.position.y = mag * math.sin(angle)
    marker_pub.publish(marker)


# rospy.init_node('scan_values')
sub = rospy.Subscriber("/scan", LaserScan, callback)
rospy.spin()
