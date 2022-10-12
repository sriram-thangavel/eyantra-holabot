#!/usr/bin/env python3

from re import L
import rospy

# publishing to /cmd_vel with msg type: Twist
from geometry_msgs.msg import Twist

# subscribing to /odom with msg type: Odometry
from nav_msgs.msg import Odometry

# for finding sin() cos() 
import math

# Odometry is given as a quaternion, but for the controller we'll need to find the orientaion theta by converting to euler angle
from tf.transformations import euler_from_quaternion

from geometry_msgs.msg import PoseArray


hola_x = 0
hola_y = 0
hola_theta = 0

#desired goals
x_goals = [1, -1, -1, 1, 0]
y_goals = [1, 1, -1, -1, 0]
# theta_goals = [1.2,2.3,3.1,2.3]
theta_goals = [math.pi/4, 3*math.pi/4, -3*math.pi/4, -math.pi/4, 0]


def odometryCb(msg):
	global hola_x, hola_y, hola_theta

	hola_x = msg.pose.pose.position.x
	hola_y = msg.pose.pose.position.y
	q1 = msg.pose.pose.orientation.x
	q2 = msg.pose.pose.orientation.y
	q3 = msg.pose.pose.orientation.z
	q4 = msg.pose.pose.orientation.w
	q = (q1,q2,q3,q4)
	hola_theta = euler_from_quaternion(q)[2]

def task1_goals_Cb(msg):
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


def main():

	rospy.init_node('controller',anonymous=True)

	pub = rospy.Publisher('/cmd_vel',Twist,queue_size=10)
	sub = rospy.Subscriber('/odom',Odometry,odometryCb)

	# declare that the node subscribes to task1_goals along with the other declarations of publishing and subscribing
	rospy.Subscriber('task1_goals', PoseArray, task1_goals_Cb)

	vel = Twist()

	#initalise the required variables to 0

	rate = rospy.Rate(100)

	#desired goal
	# x_d = 7
	# y_d = 9
	# theta_d = 3.14


	#kp value
	kp = 1

	index = 0
	
	while not rospy.is_shutdown():
		
		#errors in global frame
		x = x_goals[index] - hola_x
		y = y_goals[index] - hola_y
		theta = theta_goals[index] - hola_theta

		#error in body frame
		vel_x = x*math.cos(hola_theta)+y*math.sin(hola_theta)
		vel_y = -x*math.sin(hola_theta)+y*math.cos(hola_theta)
		vel_z = theta

		#proprtional controller for velocity
		# vel_x = kp*x
		# vel_y = kp*y
		# vel_z = kp*z

		#publish velocity
		vel.linear.x = kp*vel_x
		vel.linear.y = kp*vel_y
		vel.angular.z = kp*vel_z
		pub.publish(vel)

		rate.sleep()

		print("error x:",round(x,2))
		print("error y:",round(y,2))
		print("error theta:",round(theta,2))


		if round(x,1) == 0 and round(y,1) == 0 and round(theta,1) == 0:
			print("goal reached",round(hola_x,2),round(hola_y,2),round(hola_theta,2))
			rospy.sleep(1.1)

			# if index < len(x_goals):
			# 	index+=1
			# else:
			# 	break
				
		
	




if __name__ == "__main__":
	try:
		main()
	except rospy.ROSInterruptException:
		pass
