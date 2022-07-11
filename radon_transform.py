from detectors import *
import streamlit as st
from skimage.exposure import rescale_intensity
import numpy as np

@st.cache
def radon_transform(image, steps_number, alpha, detector_number, detector_angle):

    # calculating measures of image and paddings
    height = image.shape[0]
    width = image.shape[1]
    diagonal = math.sqrt(height ** 2 + width ** 2)
    padding_height = math.ceil(diagonal - height) + 2
    padding_width = math.ceil(diagonal - width) + 2
    
    # creating new square image with paddings to avoid lossing data
    padded_image = np.zeros((height + padding_height, width + padding_width))
    padded_image[math.ceil(padding_height/2):(math.ceil(padding_height/2)+height), 
    math.ceil(padding_width/2):math.ceil(padding_width/2)+width] = image
    
    center = padded_image.shape[0] // 2
    radius = diagonal / 2
    new_image = []
    
    # simulating emmiter movement
    for emmiter_pos in np.arange(0.0, (float(steps_number)*alpha), alpha):# emmiter_pos in degress!!!
        detectors, x_emmiter, y_emmiter = emitter_detectors_movement(radius, emmiter_pos, center, detector_angle, detector_number)      
        new_image.append(calculate_for_detector(detectors, padded_image, x_emmiter, y_emmiter))
        
    return new_image

@st.cache
def reverse_radon_transform(image, steps_number, alpha, detector_number, detector_angle, sinogram, filtered = False):
    # calculating measures of image and paddings
    height = image.shape[0]
    width = image.shape[1]
    diagonal = math.sqrt(height ** 2 + width ** 2)
    padding_height = math.ceil(diagonal - height) + 2
    padding_width = math.ceil(diagonal - width) + 2   
    partial_reverse_images = []
    iterator = 0
    
    # creating new square image with paddings to avoid lossing data
    padded_image = np.zeros((height + padding_height, width + padding_width))

    center = padded_image.shape[0] // 2
    radius = diagonal / 2
    
    # simulating emmiter movement
    for emmiter_pos in np.arange(0.0, (float(steps_number) * alpha), alpha):# emmiter_pos w stopniach!!!
        detectors, x_emmiter, y_emmiter = emitter_detectors_movement(radius, emmiter_pos, center, detector_angle, detector_number)      
        i = int(emmiter_pos//alpha)
        k = 0
        for detector in detectors:
            x_pos, y_pos = detector[0], detector[1]
            lin = bresenham(x_emmiter, y_emmiter, x_pos, y_pos)
            for pos in range(len(lin)):
                padded_image[int(lin[pos][0])][int(lin[pos][1])] += (sinogram[i][k])
            k += 1

        if iterator % 10 == 0:
            if filtered:
                partial_reverse_images.append(rescale_intensity(padded_image, in_range=(0, 255), out_range=(0, 255)))
            else:
                partial_reverse_images.append(rescale_intensity(padded_image))

        iterator += 1  

    if filtered:
        partial_reverse_images.append(rescale_intensity(padded_image, in_range=(0, 255), out_range=(0, 255)))
    else:
        partial_reverse_images.append(rescale_intensity(padded_image))
        
    return padded_image[math.ceil(padding_height/2):(math.ceil(padding_height/2)+height), 
                        math.ceil(padding_width/2):math.ceil(padding_width/2)+width],partial_reverse_images


