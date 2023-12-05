#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from random import randint
from ar_week5_test.msg import cubic_traj_params,cubic_traj_coeffs
from ar_week5_test.srv import *

def listener():
    # Initialize the ROS node
    rospy.init_node('planner')
    # Subscribe to the 'params' topic
    rospy.Subscriber("params", cubic_traj_params, compute_cubic_coeffs_client)
    # Keep the node running
    rospy.spin()

def compute_cubic_coeffs_client(data):
    # Wait for the 'computer' service to become available
    rospy.wait_for_service('computer')
    # Extract the cubic trajectory parameters from the received message
    params = [data.p0, data.pf, data.v0, data.vf, data.t0, data.tf]
    try:
        # Create a service proxy for the 'computer' service
        compute_cubic_coeffs = rospy.ServiceProxy('computer', compute_cubic_traj)
        # Call the 'computer' service to compute the cubic trajectory coefficients
        resp1 = compute_cubic_coeffs(params[0],params[1],params[2],params[3],params[4],params[5])
        # Publish the computed coefficients
        publish_coeffs(resp1,data.t0,data.tf)
        return resp1
    except rospy.ServiceException as e:
        print("Service call failed: %s" %e)

def publish_coeffs(coeffs,t0,tf):
    coeffslog = [coeffs.a0,coeffs.a1,coeffs.a2,coeffs.a3,t0,tf]
    # Convert the parameters to a list of strings for logging
    coeffs_string = [str(i) for i in coeffslog]
    # Log the generated parameters
    rospy.loginfo(coeffs_string)
    # Publish the generated coeffs parameters
    pub.publish(coeffs.a0,coeffs.a1,coeffs.a2,coeffs.a3,t0,tf)

if __name__ == '__main__':
    pub = rospy.Publisher('coeffs', cubic_traj_coeffs, queue_size=10)
    listener()
