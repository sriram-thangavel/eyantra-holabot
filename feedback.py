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


######################## IMPORT MODULES ##########################

from symbol import parameters
import numpy				# If you find it required
import rospy 				
from sensor_msgs.msg import Image 	# Image is the message type for images in ROS
from cv_bridge import CvBridge	# Package to convert between ROS and OpenCV Images
import cv2				# OpenCV Library
import math				# If you find it required
from geometry_msgs.msg import Pose2D	# Required to publish ARUCO's detected position & orientation
import matplotlib.pyplot as plt

############################ GLOBALS #############################

aruco_publisher = rospy.Publisher('detected_aruco', Pose2D)
aruco_msg = Pose2D()

##################### FUNCTION DEFINITIONS #######################

# NOTE :  You may define multiple helper functions here and use in your code

def callback(data):
	# Bridge is Used to Convert ROS Image message to OpenCV image
	br = CvBridge()
	rospy.loginfo("receiving camera frame")
	get_frame = br.imgmsg_to_cv2(data, "mono8")		# Receiving raw image in a "grayscale" format
	current_frame = cv2.resize(get_frame, (500, 500), interpolation = cv2.INTER_LINEAR)


	aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_250)
	aruco_parameters = cv2.aruco.DetectorParameters_create()
	corners , ids, rejected_imgpoints = cv2.aruco.detectMarkers(current_frame,aruco_dict,parameters = aruco_parameters)

	x_sum = corners[0][0][0][0]+ corners[0][0][1][0]+ corners[0][0][2][0]+ corners[0][0][3][0]
	y_sum = corners[0][0][0][1]+ corners[0][0][1][1]+ corners[0][0][2][1]+ corners[0][0][3][1]

	mid_x = (corners[0][0][0][0]+ corners[0][0][1][0])/2
	mid_y = (corners[0][0][0][1]+ corners[0][0][1][1])/2
	
	x_centerPixel = x_sum*.25
	y_centerPixel = y_sum*.25

	del_x = x_centerPixel - mid_x
	del_y = y_centerPixel - mid_y
	theta = math.atan2(del_y,del_x)

	


	aruco_msg.x = x_centerPixel
	aruco_msg.y = y_centerPixel
	aruco_msg.theta = theta

	aruco_publisher.publish(aruco_msg)

	# theta = math.atan2()

	# print(x_centerPixel,y_centerPixel)
	# print(theta)
	# print("degree:",math.degrees(theta))
	# rospy.sleep(2)
	# print(ids)
	# print(x_centerPixel)
	# print(y_centerPixel)
	# print(math.degrees(theta))

	# rospy.sleep(19)

	# plt.imshow(current_frame)
	# plt.show()
	# cv2.waitKey(10)

	############ ADD YOUR CODE HERE ############

	# INSTRUCTIONS & HELP : 
	#	-> Use OpenCV to find ARUCO MARKER from the IMAGE
	#	-> You are allowed to use any other library for ARUCO detection, 
	#        but the code should be strictly written by your team and
	#	   your code should take image & publish coordinates on the topics as specified only.  
	#	-> Use basic high-school geometry of "TRAPEZOIDAL SHAPES" to find accurate marker coordinates & orientation :)
	#	-> Observe the accuracy of aruco detection & handle every possible corner cases to get maximum scores !

	############################################
      
def main():
	rospy.init_node('aruco_feedback_node')  
	rospy.Subscriber('overhead_cam/image_raw', Image, callback)
	rospy.spin()
  
if __name__ == '__main__':
  main()
