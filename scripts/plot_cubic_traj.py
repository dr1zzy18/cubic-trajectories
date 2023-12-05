#!/usr/bin/env python
import rospy
from std_msgs.msg import String,Float64
from random import randint
import numpy as np
from ar_week5_test.msg import cubic_traj_params,cubic_traj_coeffs


def callback(data):
    # Log message indicating the callback has been triggered
    rospy.loginfo("plotter callback")
    # Extract cubic coefficients a0, a1, a2, and a3 from the message
    a = [data.a0,data.a1,data.a2,data.a3]
    # Extract start and end times from the message
    t = [data.t0,data.tf]
    # Set the rate at which to publish the trajectory positions, velocities, and accelerations
    rate = rospy.Rate(10)
    # Compute the trajectory accelerations, positions, and velocities based on the cubic coefficients.
    for i in np.arange(0,int(t[1]), 0.1):
        acceleration = 2*a[2] + 6*a[3]*i
        position = a[0] + a[1]*i + a[2]*(i**2) + a[3]*(i**3)
        velocity = a[1] + 2*a[2]*i + 3*a[3]*(i**2)
        # Publish the computed accelerations, positions, and velocities to their respective topics.
        pub_acceleration.publish(acceleration)
        pub_position.publish(position)
        pub_velocity.publish(velocity)
        # Sleep to maintain the publishing rate
        rate.sleep()


def listener():
    # Subscribe to the "coeffs" topic with messages of type cubic_traj_coeffs and register the callback function
    rospy.Subscriber("coeffs", cubic_traj_coeffs, callback)
    # Spin the node
    rospy.spin()

if __name__ == "__main__":
    # Initialize the node with the name "plotter"
    rospy.init_node('plotter')
    # Create publishers for the trajectory accelerations, positions, and velocities
    pub_acceleration = rospy.Publisher('trajAcc', Float64, queue_size=10)
    pub_position = rospy.Publisher('trajPos', Float64, queue_size=10)
    pub_velocity = rospy.Publisher('trajVel', Float64, queue_size=10)
    listener()
