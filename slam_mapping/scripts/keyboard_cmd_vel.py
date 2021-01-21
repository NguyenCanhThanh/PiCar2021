#!/usr/bin/env python
#keyboard_cmd_vel.py

import rospy
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse

class Key():
    def __init__(self): 
        self.cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    def wait_for_subscribers(self):
        i = 0
        while not rospy.is_shutdown() and self.cmd_vel.get_num_connections() == 0:
            if i == 4:
                print("Waiting for subscriber to connect to {}".format(self.cmd_vel.name))
            rospy.sleep(0.5)
            i += 1
            i = i % 5
        if rospy.is_shutdown():
            raise Exception("Got shutdown request before subscribers connected")

    def send_vel(self):
        vel = Twist()
        direction = raw_input('k: forward, j: backward, h: left, l: right, return: stop > ')
        if 'k' in direction: vel.linear.x = 0.15
        if 'j' in direction: vel.linear.x = -0.15
        if 'h' in direction: vel.angular.z = 3.14/4
        if 'l' in direction: vel.angular.z = -3.14/4
        print(vel)
        self.cmd_vel.publish(vel)

if __name__ == '__main__':
    rospy.init_node('keyboard_cmd_vel')
    K = Key()
    rate = rospy.Rate(10)

    #K.wait_for_subscribers()
    while not rospy.is_shutdown():
        K.send_vel()
        rate.sleep()