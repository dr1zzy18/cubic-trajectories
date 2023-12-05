#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from random import randint
from ar_week5_test.msg import cubic_traj_params

def points_generator():
    # Initialize the ROS node and create a publisher to publish the trajectory parameters
    pub = rospy.Publisher('params', cubic_traj_params, queue_size=10)
    rospy.init_node('generator')
    # Set the publishing rate to 0.05 Hz
    rate = rospy.Rate(0.05)

    while not rospy.is_shutdown():
         # Generate random values for the trajectory parameters
         p0 = randint(-10,10)
         pf = randint(-10,10)
         v0 = randint(-10,10)
         vf = randint(-10,10)
         t0 = 0
         tf = randint(5,10)
         paramslog = [p0, pf, v0, vf, t0, tf]
         # Convert the parameters to a list of strings for logging
         params_string = [str(i) for i in paramslog]
         # Log the generated parameters
         rospy.loginfo(params_string)
         # Publish the generated trajectory parameters
         pub.publish(p0, pf, v0, vf, t0, tf)
         # Sleep to maintain the publishing rate
         rate.sleep()

if __name__ == '__main__':
    try:
        points_generator()
    except rospy.ROSInterruptException:
        pass
