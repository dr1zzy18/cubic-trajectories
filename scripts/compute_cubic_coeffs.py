#!/usr/bin/env python
import rospy
import numpy as np
from numpy.linalg import inv
from ar_week5_test.srv import compute_cubic_traj,compute_cubic_trajResponse


def handle_compute_cubic_coeffs(req):
    # Create the matrix of coefficients for the cubic polynomial
    matrix = np.array([[1.,req.t0,req.t0**2,req.t0**3],
                [0.,1.,2*req.t0,3*(req.t0**2)],
                [1.,req.tf,req.tf**2,req.tf**3],
                [0.,1.,2*req.tf,3*(req.tf**2)]])
    # Create the vector of known values
    vec = np.array([req.p0,req.v0,req.pf,req.vf])
    # Calculate the inverse of matrix
    matrix_inv = inv(matrix)
    # Solve for the coefficients of the cubic polynomial
    c = matrix_inv.dot(vec)
    return c[0],c[1],c[2],c[3]

def compute_cubic_coeffs():
    # Initialize the ROS node and create a service to compute the cubic trajectory coefficients
    rospy.init_node('computer')
    s = rospy.Service('computer', compute_cubic_traj, handle_compute_cubic_coeffs)
    # Spin the node
    rospy.spin()

if __name__ == "__main__":
    compute_cubic_coeffs()
