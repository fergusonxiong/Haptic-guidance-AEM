import math
import numpy as np


def linear_increase(frame_dimension, value_range, radius, finger_pos, target_pos):   # Function to create targets gaussians
    
    width = frame_dimension[0]  # Get the width of the frame for the meshgrid
    height = frame_dimension[1] # Get the height of the frame for the meshgrid
    widthSafety = width-50  # because target loc plots with a distance of 50 pixels to edge
    heightSafety = height-50  # because target loc plots with a distance of 50 pixels to edge
    
    # calculate smallest_step
    min_value = value_range[0]
    max_value = value_range[1]
    smallest_step = (max_value-min_value) / (math.sqrt(widthSafety**2 + heightSafety**2))

    # calculate distance
    d = math.sqrt((finger_pos[0]-target_pos[0])**2 + (finger_pos[1]-target_pos[1])**2)

    if d <= radius:
        z = max_value
    else:
        z = (d-radius)*smallest_step
        z = -(z-max_value)
    
    return z


def incremental_increase(frame_dimension, value_range, radius, finger_pos, target_pos):   # Function to create targets gaussians
    
    width = frame_dimension[0]  # Get the width of the frame for the meshgrid
    height = frame_dimension[1] # Get the height of the frame for the meshgrid
    widthSafety = width-50  # because target loc plots with a distance of 50 pixels to edge
    heightSafety = height-50  # because target loc plots with a distance of 50 pixels to edge
    
    # calculate smallest_step
    min_value = value_range[0]
    max_value = value_range[1]
    smallest_step = (max_value-min_value) / (math.sqrt(widthSafety**2 + heightSafety**2))

    # calculate distance
    d = math.sqrt((finger_pos[0]-target_pos[0])**2 + (finger_pos[1]-target_pos[1])**2)
    d_max = math.sqrt((frame_dimension[0]-40)**2 + (frame_dimension[1]-40)**2)
    
    # adjust signal value to value_range
    incremental_list = np.linspace(1.5*radius, d_max, 9)
    stepsize = incremental_list[1]-incremental_list[0]
    z = 0.0
    if d <= 1.5*radius:
        z = max_value
    else:
        for i in incremental_list:
            if d <= i:
                z = (i-(stepsize/2)) * smallest_step  # get mid-point/distance of plateau
                z = -(z-max_value)
                break  # exit incremental_list 
    return z


def exponential_increase(frame_dimension, value_range, radius, finger_pos, target_pos):   # Function to create targets gaussians
    
    width = frame_dimension[0]  # Get the width of the frame for the meshgrid
    height = frame_dimension[1] # Get the height of the frame for the meshgrid
    widthSafety = width-50  # because target loc plots with a distance of 50 pixels to edge
    heightSafety = height-50  # because target loc plots with a distance of 50 pixels to edge
    
    # calculate smallest_step
    value_min = value_range[0]
    value_max = value_range[1]
    
    # calculate distance
    d = math.sqrt((finger_pos[0]-target_pos[0])**2 + (finger_pos[1]-target_pos[1])**2)
    
    if d <= radius:
        z = value_max
    else:    
        # calculate value for defined exponent and base range
        base = 2   # base
        exp_min = 1  # exponent min
        exp_max = 5  # exponent max
        exp_range = (exp_min, exp_max)  # range of exponent
        d_max = math.sqrt((widthSafety-radius)**2 + (heightSafety-radius)**2)  # max distance
        ratio_d = (d-radius)/d_max
        exp = exp_min+(exp_max-exp_min)*(1-ratio_d)  # calculate base for corresponding distance
        result = base**exp
    
        # adjust signal value to value_range/ transform from one intervall to another
        result_min = base**exp_min
        result_max = base**exp_max
        value = ((value_max-value_min)/(result_max-result_min))*result + value_max-((value_max-value_min)/(result_max-result_min))*result_max
        z = value
    
    return z



# CODE TO TEST THE FUNCTIONS
radius = 15
value_range = (1, 10)
frame_dimension = (800, 600)
finger_pos = (0, 0)
target_pos = (650, 200)


# calculate signal value
z_linear = linear_increase(frame_dimension, value_range, radius, finger_pos, target_pos)
z_incremental = incremental_increase(frame_dimension, value_range, radius, finger_pos, target_pos)
z_exponential = exponential_increase(frame_dimension, value_range, radius, finger_pos, target_pos)

#print(z_linear)
#print(z_incremental)
#print(z_expoenential)