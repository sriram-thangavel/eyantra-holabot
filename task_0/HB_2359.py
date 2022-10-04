#! /usr/bin/env python3

# '''
# *****************************************************************************************
# *
# *        		===============================================
# *           		    HolA Bot (HB) Theme (eYRC 2022-23)
# *        		===============================================
# *
# *  This script should be used to implement Task 0 of HolA Bot (KB) Theme (eYRC 2022-23).
# *
# *  This software is made available on an "AS IS WHERE IS BASIS".
# *  Licensee/end user indemnifies and will keep e-Yantra indemnified from
# *  any and all claim(s) that emanate from the use of the Software or
# *  breach of the terms of this agreement.
# *
# *****************************************************************************************
# '''

# # Team ID:			[ HB_2359 ]
# # Author List:		[Sriram Thangavel, Sree Harish, Akshith, Prasannakumar]
# # Filename:			task_0.py
# # Functions:
# # 				[posecallback(),main(),semi_circle(),rightangle_turn(),straight() ]
# # Nodes:		 	vel_pub  pose_sub


# ####################### IMPORT MODULES #######################
import math
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

# ##############################################################


# ################# ADD GLOBAL VARIABLES HERE #################

x = 0
y = 0
theta = 0
change_distance = 0


# ##############################################################


def main():
    global x,y
    
    rospy.init_node('turtle_test1',anonymous=True)

  
    pose_sub = rospy.Subscriber('turtle1/pose',Pose,posecallback)
    Rate = rospy.Rate(5)

 
    vel_pub = rospy.Publisher('turtle1/cmd_vel',Twist,queue_size=10)

    vel = Twist()


    semi_circle(vel,vel_pub)
    rightangle_turn(vel,vel_pub)
    straight(vel,vel_pub)
    print("Done!!")

    


# ################# ADD UTILITY FUNCTIONS HERE #################

def posecallback(pose_data):
    global x,y,theta
    x = round(pose_data.x,2)
    y = round(pose_data.y,2)
    theta = round(pose_data.theta,2)


def semi_circle(vel,vel_pub):
    global change_distance,theta
    theta0 = theta

    while not rospy.is_shutdown():

        del_theta = abs(theta-theta0)
        theta0 = theta


        change_distance += del_theta


        if (change_distance >= 3.14):
            break

        vel.linear.x = 1
        vel.angular.z = 1
        vel_pub.publish(vel)
        print("My turtleBot is: Moving in circle!")
        print(theta)

    

def rightangle_turn(vel,vel_pub):
    vel.linear.x = 0
    vel.angular.z = 3.14/2
    vel_pub.publish(vel)
    print("My turtleBot is: Rotating!")
    print(theta)
    rospy.sleep(1.01)
    

  
def straight(vel,vel_pub):
    global change_distance,x,y
    change_distance = 0
    x0 = x
    y0 = y

    while not rospy.is_shutdown():
        distance = math.sqrt(pow(x-x0,2)+pow(y-y0,2))
       
        x0 = x
        y0 = y
        change_distance += round(distance,2)
        

        if (change_distance >= 2.00):
            vel.linear.x = 0
            vel_pub.publish(vel)
            break

        vel.angular.z = 0
        vel.linear.x = 1
        vel_pub.publish(vel)
        rospy.sleep(1)
        print("My turtleBot is: Moving straight!!!")
        print(theta)
        
    
    
    
# ##############################################################


# ######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS PART #########
if __name__ == "__main__":
    try:
        print("------------------------------------------")
        print("         Python Script Started!!          ")
        print("------------------------------------------")
        main()

    except:
        print("------------------------------------------")
        traceback.print_exc(file=sys.stdout)
        print("------------------------------------------")
        sys.exit()

    finally:
        print("------------------------------------------")
        print("    Python Script Executed Successfully   ")
        print("------------------------------------------")
     

    




