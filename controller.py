#!/usr/bin/env python3

'''
*****************************************************************************************
*
*        		===============================================
*           		    HolA Bot (HB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script should be used to implement Task 0 of HolA Bot (HB) Theme (eYRC 2022-23).
*
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:		[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:		feedback.py
# Functions:
#			[ Comma separated list of functions in this file ]
# Nodes:		Add your publishing and subscribing node


################### IMPORT MODULES #######################

import rospy
import signal		# To handle Signals by OS/user
import sys		# To handle Signals by OS/user

from geometry_msgs.msg import Twist
from geometry_msgs.msg import Wrench		# Message type used for publishing force vectors
from geometry_msgs.msg import PoseArray	# Message type used for receiving goals
from geometry_msgs.msg import Pose2D		# Message type used for receiving feedback

import time
import math		# If you find it useful

from tf.transformations import euler_from_quaternion	# Convert angles

################## GLOBAL VARIABLES ######################

PI = 3.14

x_goals = [50]
y_goals = [350]
theta_goals =  [0]

right_wheel_pub = None
left_wheel_pub = None
front_wheel_pub = None

d = 0.17483

kp = 1
hola_x = 0
hola_y = 0
hola_theta = 0

# vel_x = 0
# vel_y = 0
# vel_z = 0

front_wheel = Wrench()
right_wheel = Wrench()
left_wheel = Wrench()

# vel = Twist()


right_wheel_pub = rospy.Publisher('/right_wheel_force', Wrench, queue_size=10)
front_wheel_pub = rospy.Publisher('/front_wheel_force', Wrench, queue_size=10)
left_wheel_pub = rospy.Publisher('/left_wheel_force', Wrench, queue_size=10)

# pub = rospy.Publisher('/cmd_vel',Twist,queue_size=10)


##################### FUNCTION DEFINITIONS #######################

# NOTE :  You may define multiple helper functions here and use in your code

def signal_handler(sig, frame):
	  
	# NOTE: This function is called when a program is terminated by "Ctr+C" i.e. SIGINT signal 	
	print('Clean-up !')
	cleanup()
	sys.exit(0)

def cleanup():
	pass
	############ ADD YOUR CODE HERE ############

	# INSTRUCTIONS & HELP : 
	#	-> Not mandatory - but it is recommended to do some cleanup over here,
	#	   to make sure that your logic and the robot model behaves predictably in the next run.

	############################################
  
  
def task2_goals_Cb(msg):
	global x_goals, y_goals, theta_goals
	x_goals.clear()
	y_goals.clear()
	theta_goals.clear()

	for waypoint_pose in msg.poses:
		x_goals.append(waypoint_pose.position.x)
		y_goals.append(waypoint_pose.position.y)

		orientation_q = waypoint_pose.orientation
		orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
		theta_goal = euler_from_quaternion (orientation_list)[2]
		theta_goals.append(theta_goal)

def aruco_feedback_Cb(msg):
	global hola_x,hola_y,hola_theta
	hola_x = msg.x
	hola_y = msg.y
	hola_theta = msg.theta
	############ ADD YOUR CODE HERE ############

	# INSTRUCTIONS & HELP : 
	#	-> Receive & store the feedback / coordinates found by aruco detection logic.
	#	-> This feedback plays the same role as the 'Odometry' did in the previous task.

	############################################


def inverse_kinematics(error_x,error_y,error_theta,hola_theta):
	pass
		# global vel_x,vel_y,vel_z

		# #velocity in global frame
		# vel_x_g = kp*error_x
		# vel_y_g = kp*error_y
		# vel_z_g = kp*error_theta
		

		#velocity in body frame
		# vel_x = vel_x_g*math.cos(hola_theta)+vel_y_g*math.sin(hola_theta)
		# vel_y = -vel_x_g*math.sin(hola_theta)+vel_y_g*math.cos(hola_theta)
		# vel_z = vel_z_g

		#publishing velocity
		# vel.linear.x =vel_x
		# vel.linear.y = vel_y
		# vel.angular.z = vel_z
		# pub.publish(vel)

		# body velocity to wheel velocity
		# vel_front_wheel = -d*vel_z + vel_x
		# vel_right_wheel = -d*vel_z + -math.cos(60)*vel_x + -math.sin(60)*vel_y
		# vel_left_wheel = -d*vel_z + -math.cos(60)*vel_x + math.sin(60)*vel_y

		

		# front_wheel.force.x = vel_front_wheel
		# right_wheel.force.x = vel_right_wheel
		# left_wheel.force.x = vel_left_wheel

		# front_wheel_pub.publish(front_wheel)
		# right_wheel_pub.publish(right_wheel)
		# left_wheel_pub.publish(left_wheel)

		# print(vel_front_wheel)
		# print(vel_right_wheel)
		# print(vel_left_wheel)

		# print("))))))))))))))))))))")

		# print(hola_x)
		# print(hola_y)
		# print(hola_theta)

	############ ADD YOUR CODE HERE ############

	# INSTRUCTIONS & HELP : 
	#	-> Use the target velocity you calculated for the robot in previous task, and
	#	Process it further to find what proportions of that effort should be given to 3 individuals wheels !!
	#	Publish the calculated efforts to actuate robot by applying force vectors on provided topics
	############################################


def main():

	rospy.init_node('controller_node')

	signal.signal(signal.SIGINT, signal_handler)

	# NOTE: You are strictly NOT-ALLOWED to use "cmd_vel" or "odom" topics in this task
	#	Use the below given topics to generate motion for the robot.
	# right_wheel_pub = rospy.Publisher('/right_wheel_force', Wrench, queue_size=10)
	# front_wheel_pub = rospy.Publisher('/front_wheel_force', Wrench, queue_size=10)
	# left_wheel_pub = rospy.Publisher('/left_wheel_force', Wrench, queue_size=10)

	right_wheel_pub.publish()

	rospy.Subscriber('detected_aruco',Pose2D,aruco_feedback_Cb)
	rospy.Subscriber('task2_goals',PoseArray,task2_goals_Cb)
	
	rate = rospy.Rate(100)

	############ ADD YOUR CODE HERE ############

	# INSTRUCTIONS & HELP : 
	#	-> Make use of the logic you have developed in previous task to go-to-goal.
	#	-> Extend your logic to handle the feedback that is in terms of pixels.
	#	-> Tune your controller accordingly.
	# 	-> In this task you have to further implement (Inverse Kinematics!)
	#      find three omni-wheel velocities (v1, v2, v3) = left/right/center_wheel_force (assumption to simplify)
	#      given velocity of the chassis (Vx, Vy, W)
	#	   

	index = 0
	while not rospy.is_shutdown():
		
		# Calculate Error from feedback
		#errors in global frame
		error_g_x = abs(x_goals[index] - hola_x)
		error_g_y = abs(y_goals[index] - hola_y)
		error_g_theta = theta_goals[index] - hola_theta

		error_b_x = error_g_x*math.cos(hola_theta) + error_g_y*math.sin(hola_theta)
		error_b_y = -error_g_x*math.sin(hola_theta) + error_g_y*math.cos(hola_theta)
		error_b_theta = error_g_theta

		vel_x = kp * error_b_x
		vel_y = kp * error_b_y
		vel_z = kp * error_b_theta

		vel_front_wheel = -d*vel_z + vel_x
		vel_right_wheel = -d*vel_z + (-math.cos(60)*vel_x) + (-math.sin(60)*vel_y)
		vel_left_wheel = -d*vel_z + (-math.cos(60)*vel_x) + math.sin(60)*vel_y

		front_wheel.force.x = vel_front_wheel
		right_wheel.force.x = vel_right_wheel
		left_wheel.force.x = vel_left_wheel

		front_wheel_pub.publish(front_wheel)
		right_wheel_pub.publish(right_wheel)
		left_wheel_pub.publish(left_wheel)

		print("error_x",error_b_x)
		print("error_y",error_b_y)
		print("error_theta",error_b_theta)

		print("x:",hola_x)
		print("y:",hola_y)
		print("theta:",hola_theta)


		# inverse_kinematics(x,y,theta,hola_theta)
		

		# Change the frame by using Rotation Matrix (If you find it required)

		# Calculate the required velocity of bot for the next iteration(s)
		
		# Find the required force vectors for individual wheels from it.(Inverse Kinematics)

		# Apply appropriate force vectors

		# Modify the condition to Switch to Next goal (given position in pixels instead of meters)

		rate.sleep()

		if -0.04<=vel_x<=0.04:
			vel_x = 0
			
			vel_front_wheel = -d*vel_z + vel_x
			vel_right_wheel = -d*vel_z + (-math.cos(60)*vel_x) + (-math.sin(60)*vel_y)
			vel_left_wheel = -d*vel_z + (-math.cos(60)*vel_x) + math.sin(60)*vel_y

			front_wheel.force.x = vel_front_wheel
			right_wheel.force.x = vel_right_wheel
			left_wheel.force.x = vel_left_wheel

			front_wheel_pub.publish(front_wheel)
			right_wheel_pub.publish(right_wheel)
			left_wheel_pub.publish(left_wheel)
			
		

		if -0.04<=vel_y<=0.04:
			vel_y = 0
			vel_front_wheel = -d*vel_z + vel_x
			vel_right_wheel = -d*vel_z + (-math.cos(60)*vel_x) + (-math.sin(60)*vel_y)
			vel_left_wheel = -d*vel_z + (-math.cos(60)*vel_x) + math.sin(60)*vel_y

			front_wheel.force.x = vel_front_wheel
			right_wheel.force.x = vel_right_wheel
			left_wheel.force.x = vel_left_wheel

			front_wheel_pub.publish(front_wheel)
			right_wheel_pub.publish(right_wheel)
			left_wheel_pub.publish(left_wheel)

		if -0.004<=vel_z<=0.004:
			vel_z = 0
			vel_front_wheel = -d*vel_z + vel_x
			vel_right_wheel = -d*vel_z + (-math.cos(60)*vel_x) + (-math.sin(60)*vel_y)
			vel_left_wheel = -d*vel_z + (-math.cos(60)*vel_x) + math.sin(60)*vel_y

			front_wheel.force.x = vel_front_wheel
			right_wheel.force.x = vel_right_wheel
			left_wheel.force.x = vel_left_wheel

			front_wheel_pub.publish(front_wheel)
			right_wheel_pub.publish(right_wheel)
			left_wheel_pub.publish(left_wheel)
			

		if front_wheel.force.x == 0 and right_wheel.force.x == 0 and left_wheel.force.x == 0:
			print("Goal reached !!!!!")
			rospy.sleep(1)



		# if x_goals[index]-0.5<=hola_x<=x_goals[index]+0.50 and y_goals[index]-0.50<=hola_y<=y_goals[index]+0.50:
		# 	front_wheel.force.x =  0
		# 	front_wheel_pub.publish(front_wheel)
		# 	right_wheel.force.x = 0
		# 	right_wheel_pub.publish(right_wheel)
		# 	left_wheel.force.x = 0
		# 	left_wheel_pub.publish(left_wheel)
			
		

		# if -0.04<=error_b_y<=0.04:
		# 	right_wheel.force.x = 0
		# 	right_wheel_pub.publish(right_wheel)
			

		# if -0.004<=error_b_theta<=0.004:
		# 	left_wheel.force.x = 0
		# 	left_wheel_pub.publish(left_wheel)
			
			

		# if front_wheel.force.x == 0 and left_wheel.force.x == 0 and right_wheel.force.x == 0:
		# 	print("Goal reached !!!!!")
		# 	rospy.sleep(1)

		# if -0.04<=vel_x<=0.04:
		# 	vel.linear.x =  0
		# 	pub.publish(vel)
			
		

		# if -0.04<=vel_y<=0.04:
		# 	vel.linear.y = 0
		# 	pub.publish(vel)
			

		# if -0.004<=vel_z<=0.004:
		# 	vel.angular.z = 0
		# 	pub.publish(vel)
			
			

		# if vel.linear.x == 0 and vel.linear.y == 0 and vel.angular.z == 0:
		# 	print("Goal reached !!!!!")
		# 	rospy.sleep(1)

			

			if index < len(x_goals)-1:
					index += 1

    ############################################

if __name__ == "__main__":
	try:
		main()
	except rospy.ROSInterruptException:
		pass

