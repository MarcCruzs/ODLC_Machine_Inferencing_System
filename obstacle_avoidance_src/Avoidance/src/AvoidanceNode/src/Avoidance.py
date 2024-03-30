#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
import math
from visualization_msgs.msg import Marker
import os

rospy.init_node('rviz_marker')

rospy.loginfo("my_tutorial_node started!")

marker_pub = rospy.Publisher("/visualization_marker", Marker, queue_size = 2)

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


# goal placeholder
markerUAV = marker
markerUAV.pose.position.x = 2
markerUAV.pose.position.y = 2

# GPS placeholder
markerGOAL = marker
markerGOAL.pose.position.x = 0
markerGOAL.pose.position.y = 0

def callback(msg):
    
    # repelant potential field
    repel_const = 1
    mag = 0
    angle = 0
    length = int((msg.angle_max-msg.angle_min) / msg.angle_increment)
    for i in range(length):
        
        # take the inverse of the distance and rotate the angle of the specific point by 180 (multiply by -1)
        inv_dist = 1/msg.ranges[i]
        neg_ang = -1*(msg.angle_min + msg.angle_increment * i)

        mag =  math.sqrt((inv_dist)**2 + mag**2 + 2 * inv_dist * mag * math.cos(angle - neg_ang))
        angle = angle + math.atan2(inv_dist*math.sin(neg_ang - angle), mag + inv_dist * math.cos(neg_ang - angle))
    
    marker.pose.position.x = repel_const * mag*math.cos(angle)/length
    marker.pose.position.y = repel_const * mag*math.sin(angle)/length

    # attractive potential field

    attract_const = .1 # arbitrary, TO ADJUST, KEEP LOW AND INCREASE BY SMALL AMMOUNTS, CAN EASILY OUTWEIGH REPELANT AND CRASH UAV

    # gradient of hyperboloid centered at goal
    # the gradient of a 3D function at a point is a vector pointing tangent to the function at that point
    # hyperboloid used becasue gradient as dist goes to infinity is linear
    # gets smaller and smaller closer to goal

    # heres my math https://www.wolframalpha.com/input?i2d=true&i=%E2%88%87%5C%2840%29a*Sqrt%5B1%2BPower%5B%5C%2840%29x-Subscript%5Bx%2C1%5D%5C%2841%29%2C2%5D%2BPower%5B%5C%2840%29y-Subscript%5By%2C1%5D%5C%2841%29%2C2%5D%5D%5C%2841%29

    UAV_x = markerUAV.pose.position.x
    UAV_y = markerUAV.pose.position.y
    GOAL_x = markerGOAL.pose.position.x
    GOAL_y = markerGOAL.pose.position.y

    x_diff = (UAV_x - GOAL_x)
    y_diff = (UAV_y - GOAL_y)

    marker.pose.position.x += attract_const * x_diff / math.sqrt(x_diff**2 + y_diff**2)
    marker.pose.position.y += attract_const * y_diff / math.sqrt(x_diff**2 + y_diff**2)

    marker_pub.publish(marker)

sub = rospy.Subscriber('/scan', LaserScan, callback)
# a subscriber for GPS location
# a subscriber for goals

while not rospy.is_shutdown():
  marker_pub.publish(marker)

# rospy.spin()