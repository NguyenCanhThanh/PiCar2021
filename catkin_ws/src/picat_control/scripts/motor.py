#!/usr/bin/env python
#encoding: utf8

import sys
import rospy
import math
from picat.msg import MotorFreqs
from picat.srv import PutMotorFreqs
from geometry_msgs.msg import Twist
from std_msgs.msg import UInt16MultiArray, Int16MultiArray, Float32, Int16, Float64

class Motor():
    def __init__(self):
        self.motor = rospy.Publisher("/motor", Int16MultiArray, queue_size= 1)
        self.sub_pulse = rospy.Subscriber('pub_pulse', Int16MultiArray, self.calback_pulse)
        self.sub_raw = rospy.Subscriber('motor_raw', MotorFreqs, self.callback_raw_freq)
        self.sub_cmd_vel = rospy.Subscriber('cmd_vel', Twist, self.callback_cmd_vel)
        self.sub_srv_tm = rospy.Service('timed_motion', PutMotorFreqs, self.callback_tm)

        self.pulse1 = Int16()
        self.pulse2 = Int16()
        self.error1 = Float32()
        self.error2 = Float32()
        self.vel1 = Float64()
        self.vel2 = Float64()
        self.last_error1 = 0
        self.last_error2 = 0
        self.kp = 15
        self.kd = 0.005
        self.ki = 0.5
        self.last_time = rospy.Time.now()
        self.using_cmd_vel = False

    def set_raw_freq(self,left_hz,right_hz):
        m = Int16MultiArray()
        m.data.append(left_hz)
        m.data.append(right_hz)
        self.motor.publish(m)

    def calback_pulse (self, message):
        self.pulse1.data = message.data[0]
        self.pulse2.data = message.data[1]

    def callback_raw_freq(self,message):
        self.set_raw_freq(message.left, message.right)

    def callback_cmd_vel(self,message):
        self.vel1 = (2*message.linear.x - message.angular.z)/2
        self.vel2 = (2*message.linear.x + message.angular.z)/2

        self.using_cmd_vel = True
        self.last_time = rospy.Time.now()

    def callback_tm(self,message):
        self.set_raw_freq(message.left, message.right)
        rospy.sleep(message.duration)
        self.set_raw_freq(0, 0)


    def pid(self, error, last_error):       
        error_d = error - last_error
        error_i = error

        if error_i >= 50:
            error_i = 50
        elif error_i <= -50:
            error_i = -50

        temp = self.kp*error + self.ki*error_i + self.kd*error_d
        last_error = error

        if temp >= 255:
            temp = 255
        elif temp <=-255:
            temp = -255
        
        return temp

if __name__ == '__main__':
    rospy.init_node('motor_freq')
    m = Motor()
    
    rate = rospy.Rate(1)
    pw1 = 0
    pw2 = 0
    while not rospy.is_shutdown():
        if m.using_cmd_vel:
            m.error1 = m.vel1 - m.pulse1.data/30
            m.error2 = m.vel2 - m.pulse2.data/30
            pw1 = pw1 + m.pid(m.error1, m.last_error1)
            pw2 = pw2 + m.pid(m.error2, m.last_error2)
            print(pw1, pw2) 
            m.set_raw_freq(pw1, pw2)
        if m.using_cmd_vel and rospy.Time.now().to_sec() - m.last_time.to_sec() >= 1.0:
            m.set_raw_freq(0,0)
            m.using_cmd_vel = False
        rate.sleep()
