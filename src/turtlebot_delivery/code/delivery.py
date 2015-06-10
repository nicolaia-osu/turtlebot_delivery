#!/usr/bin/env python

import roslib#; roslib.load_manifest('turtlebot_delivery')
import rospy
import time
import actionlib
from std_msgs.msg import String
from move_base_msgs.msg import *

def callback(msg):

    str_params = msg.data.split(',')

    for str in str_params:
        print(str)

    # construct goals
    pickup_goal = MoveBaseGoal()
    pickup_goal.target_pose.header.frame_id = 'map'

    delivery_goal = MoveBaseGoal()
    delivery_goal.target_pose.header.frame_id = 'map'

    home_goal = MoveBaseGoal()
    home_goal.target_pose.header.frame_id = 'map'
    home_goal.target_pose.pose.position.x = -1.814
    home_goal.target_pose.pose.position.y = -10.761
    home_goal.target_pose.pose.position.z = 0.000
    home_goal.target_pose.pose.orientation.x = 0.000
    home_goal.target_pose.pose.orientation.y = 0.000
    home_goal.target_pose.pose.orientation.z = 0.644
    home_goal.target_pose.pose.orientation.w = 0.765


    if str_params[0] == "PR2":
        pickup_goal.target_pose.pose.position.x = 1.138
        pickup_goal.target_pose.pose.position.y = -5.808
        pickup_goal.target_pose.pose.position.z = 0.000
        pickup_goal.target_pose.pose.orientation.x = 0.000
        pickup_goal.target_pose.pose.orientation.y = 0.000
        pickup_goal.target_pose.pose.orientation.z = -0.321
        pickup_goal.target_pose.pose.orientation.w = 0.947
    elif str_params[0] == "Baxter":
        pickup_goal.target_pose.pose.position.x = 0.060
        pickup_goal.target_pose.pose.position.y = -8.548
        pickup_goal.target_pose.pose.position.z = 0.000
        pickup_goal.target_pose.pose.orientation.x = 0.000
        pickup_goal.target_pose.pose.orientation.y = 0.000
        pickup_goal.target_pose.pose.orientation.z = 0.058
        pickup_goal.target_pose.pose.orientation.w = 0.998
    else:
        print("unknown pickup goal!")

    if str_params[1] == "Austin's Desk":
        delivery_goal.target_pose.pose.position.x = 0.772
        delivery_goal.target_pose.pose.position.y = 0.049
        delivery_goal.target_pose.pose.position.z = 0.00
        delivery_goal.target_pose.pose.orientation.x = 0.00
        delivery_goal.target_pose.pose.orientation.y = 0.00
        delivery_goal.target_pose.pose.orientation.z = 0.988
        delivery_goal.target_pose.pose.orientation.w = 0.156
    elif str_params[1] == "Matt's Desk":
        delivery_goal.target_pose.pose.position.x = 3.598
        delivery_goal.target_pose.pose.position.y = 0.879
        delivery_goal.target_pose.pose.position.z = 0.000
        delivery_goal.target_pose.pose.orientation.x = 0.000
        delivery_goal.target_pose.pose.orientation.y = 0.000
        delivery_goal.target_pose.pose.orientation.z = -0.011
        delivery_goal.target_pose.pose.orientation.w = 1.000
    else:
        print("unknown delivery goal!")
    
    # create the action client
    client = actionlib.SimpleActionClient("move_base", MoveBaseAction)

    print("waiting for server")

    # wait for server
    client.wait_for_server(rospy.Duration(10))

    print("got server")

    # send the goal and wait for completion
    print("sending pickup goal")
    client.send_goal(pickup_goal)
    client.wait_for_result()

    # print result
    print client.get_result()

    print("pickup goal finished")

    # wait for item
    time.sleep(10)

    # send the goal and wait for completion
    print("sending delivery goal")
    client.send_goal(delivery_goal)
    client.wait_for_result()

    # print result
    print client.get_result()
    print("goal delivery finished")

    # wait for pickup
    time.sleep(10)

    # send the goal and wait for completion
    print("sending home goal")
    client.send_goal(home_goal)
    client.wait_for_result()

    # print result
    print client.get_result()
    print("goal home finished")


if __name__ == '__main__':
    rospy.init_node('delivery')

    print("in main")

    # A subscriber for the laser data
    sub = rospy.Subscriber('/delivery_command', String, callback)

    rospy.spin()