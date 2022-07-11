from bresenham import *

import numpy as np
import math

calculate_x = lambda r, eP, c: round(r * math.cos(eP)) + c
calculate_y = lambda r, eP, c: round(r * math.sin(eP)) + c
calculate_rad = lambda eP, dA, num, dN :(np.deg2rad(eP) + np.pi - np.deg2rad(dA)/2 + num * np.deg2rad(dA)/(dN-1))

def calculate_for_detector(detectors, padded_image, x_emmiter, y_emmiter):
    new_image_row = []
    for i in detectors:
        lin = bresenham(x_emmiter, y_emmiter, i[0], i[1])
        sumOfRow = 0
        for j in range(len(lin)):
            sumOfRow += padded_image[lin[j][0]][lin[j][1]]

        avg_of_row = sumOfRow/len(lin)
        new_image_row.append(round(avg_of_row, 4))
    return new_image_row


def emitter_detectors_movement(radius, emmiter_pos, center, detector_angle, detector_number):
    detectors = []
    x_emmiter = calculate_x(radius, np.deg2rad(emmiter_pos), center)
    y_emmiter = calculate_y(radius, np.deg2rad(emmiter_pos), center)
        
    # FINDING DETECTOR POSITION
    # for 1 detector
    if detector_number == 1: 
        x_detector = calculate_x(radius, np.deg2rad(emmiter_pos+180.0), center)
        y_detector = calculate_y(radius, np.deg2rad(emmiter_pos+180.0), center)
        detectors.append([x_detector, y_detector])
    # for > 1 detectors
    else:
        for j in range(detector_number):
            rad = calculate_rad(emmiter_pos, detector_angle, j, detector_number)
            x_detector = calculate_x(radius, rad, center)
            y_detector = calculate_y(radius, rad, center)
            detectors.append([x_detector, y_detector])
    return (detectors, x_emmiter, y_emmiter)
