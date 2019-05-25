#!/usr/bin/env python3

"""
Yandex Self-Driving Meetup Challenge.
TASK: Get the plane from the point cloud, the plane should follow these conditions:
 - At least 50% of the points from the cloud are closer than "p" to the plane.
I think that's it. The full condition of the task is in the "condition.html" file.

Reads from stdin, prints result to stdout.
USAGE: cat input3.txt | ./get_plane.py
"""

#pylint:disable=C0103, C0301, W0621

import sys
import math
import random


def plane_equation(p1, p2, p3):
    """
    Gets a plane from 3 points
    :param p1: first point
    :param p2: second point
    :param p3: third point
    :return: (A, B, C, D) from A*x+B*y+C*z+D=0, None if impossible
    """
    a1 = p2[0] - p1[0]
    b1 = p2[1] - p1[1]
    c1 = p2[2] - p1[2]
    a2 = p3[0] - p1[0]
    b2 = p3[1] - p1[1]
    c2 = p3[2] - p1[2]
    a = b1 * c2 - b2 * c1
    b = a2 * c1 - a1 * c2
    c = a1 * b2 - b1 * a2
    # Points are collinear
    if (abs(a) < 1e-6) and (abs(b) < 1e-6) and (abs(c) < 1e-6):
        return None
    # All clear
    d = (- a * p1[0] - b * p1[1] - c * p1[2])
    return (a, b, c, d)


def distance_to_plane(plane, pt):
    """
    Returns distance from the point to the plane
    :param plane: list of plane coefficients (A, B, C, D), can be None
    :param p: point (x, y, z)
    :return: distance fro the point to the plane, float
    """
    if plane is None:
        return None
    d = abs((plane[0] * pt[0] + plane[1] * pt[1] + plane[2] * pt[2] + plane[3]))
    e = (math.sqrt(plane[0] * plane[0] + plane[1] * plane[1] + plane[2] * plane[2]))
    # Not the best assumption, but will work for the task.
    if abs(e) < 1e-10:
        return 1e10
    return d / e


def points_match(plane, p, points, threshold):
    """
    Check if more than 50% of the points match the condition.
    :param plane: plane equation coefficients, [A, B, C, D]
    :param p: maximum distance between point and the plane
    :param points: array of points
    :param treshold: number of points needed to acheive to exit, usually it's total/2
    :return: True if more than treshold points are on or near the plane, False otherwise
    """
    match = 0
    for point in points:
        if distance_to_plane(plane, point) <= p:
            match += 1
        if match >= threshold:
            return True

    return False

def points_percentage(plane, p, points, total):
    """
    Check if more than 50% of the points match the condition.
    :param plane: plane equation coefficients, [A, B, C, D]
    :param p: maximum distance between point and the plane
    :param points: array of points
    :param treshold: number of points needed to acheive to exit, usually it's total/2
    :return: True if more than treshold points are on or near the plane, False otherwise
    """
    match = 0
    for point in points:
        if distance_to_plane(plane, point) <= p:
            match += 1

    return match / total


# ----                                           Read the initial data                                           ---- #
# Maximum distance between point and the plane
p = float(sys.stdin.readline())
# Number of points
points_num = int(sys.stdin.readline())
# Points
points = []
for i in range(0, points_num):
    values = list(map(float, sys.stdin.readline().strip().split('\t')))
    points.append(values)

total = len(points)
threshold = total / 2

# ----                                    Brute force, kinda fails for time limit                                ---- #
"""
for p1 in range(0, total-2):
    for p2 in range(p1+1, total-1):
        for p3 in range(p2+1, total):
            plane_coefs = plane_equation(points[p1], points[p2], points[p3])
            if plane_coefs is None:
                continue
            match = points_match(plane_coefs, p, points, threshold)
            if match:
                print("{0:.6f}".format(plane_coefs[0]),
                      "{0:.6f}".format(plane_coefs[1]),
                      "{0:.6f}".format(plane_coefs[2]),
                      "{0:.6f}".format(plane_coefs[3]))
                sys.exit(0)
            #perc = points_percentage(plane_coefs, p, points, total)
            #print("{0:0.2f}".format(perc*100) + "%")
"""

# ---- Let's try friggin poor man RANSAC instead, like, it's not that hard to find those damn 50% of em points? ---- #
iterations = total # Total number of iterations, let's just hope it'll find the plane before they end.
for i in range(0, iterations):
    # Getting the sample of 3 points from the total set.
    sample = random.sample(range(0, total), 3)

    #pylint:disable=E1126
    #Computing the plane equation
    plane_coefs = plane_equation(points[sample[0]], points[sample[1]], points[sample[2]])
    # pylint:enable=E1126

    # If plane_coefs is None, points are probably collinear or something.
    if plane_coefs is None:
        continue

    # Check if the plane "matches" our condition (more than half of the points are there).
    match = points_match(plane_coefs, p, points, threshold)
    if match:
        print("{0:.6f}".format(plane_coefs[0]),
              "{0:.6f}".format(plane_coefs[1]),
              "{0:.6f}".format(plane_coefs[2]),
              "{0:.6f}".format(plane_coefs[3]))
        sys.exit(0)
