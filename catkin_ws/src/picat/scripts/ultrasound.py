#!/usr/bin/env python
#encoding: utf8

import sys
import rospy
from picat.msg import UltraSound
from std_msgs.msg import Float32MultiArray, MultiArrayDimension  
from std_msgs.msg import Float32 

class Sonar():
    def __init__(self):
        self.sonar_lb = Float32()
        self.sonar_lf = Float32()
        self.sonar_rb = Float32()
        self.sonar_rf = Float32()
        rospy.Subscriber("/sonar", Float32MultiArray, self.callback)
        self.pub = rospy.Publisher('ultrasound', UltraSound, queue_size=1)

    def callback(self, message):
        self.sonar_lb.data = message.data[0]
        self.sonar_lf.data = message.data[1]
        self.sonar_rb.data = message.data[2]
        self.sonar_rf.data = message.data[3]

    def get_param(self):
        rate = rospy.Rate(10)
        d = UltraSound()
        while not rospy.is_shutdown():
            d.left_forward = self.sonar_lf.data
            d.left_side = self.sonar_lb.data
            d.right_forward = self.sonar_rf.data
            d.right_side = self.sonar_rb.data
            d.sum_all = d.left_forward + d.right_forward
            d.sum_forward = d.left_forward + d.right_forward

            self.pub.publish(d)

        rate.sleep()

if __name__ == '__main__':
    rospy.init_node('ultrasound')
    Sonar().get_param()
