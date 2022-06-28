import math
import numpy as np
import matplotlib.pyplot as plt


def linear_increase(frame_dimension, value_range, radius, current_d):   # Function to create targets gaussians
    
    width = frame_dimension[0]  # Get the width of the frame for the meshgrid
    height = frame_dimension[1] # Get the height of the frame for the meshgrid
    widthSafety = width-50  # because target loc plots with a distance of 50 pixels to edge
    heightSafety = height-50  # because target loc plots with a distance of 50 pixels to edge
    
    # calculate smallest_step
    min_value = value_range[0]
    max_value = value_range[1]
    smallest_step = (max_value-min_value) / (math.sqrt(widthSafety**2 + heightSafety**2))

    # calculate distance
    d = current_d

    if d <= radius:
        z = max_value
    else:
        z = (d-radius)*smallest_step
        z = -(z-max_value)
    
    return z


def incremental_increase(frame_dimension, value_range, radius, current_d):   # Function to create targets gaussians
    
    width = frame_dimension[0]  # Get the width of the frame for the meshgrid
    height = frame_dimension[1] # Get the height of the frame for the meshgrid
    widthSafety = width-50  # because target loc plots with a distance of 50 pixels to edge
    heightSafety = height-50  # because target loc plots with a distance of 50 pixels to edge
    
    # calculate smallest_step
    min_value = value_range[0]
    max_value = value_range[1]
    smallest_step = (max_value-min_value) / (math.sqrt(widthSafety**2 + heightSafety**2))

    # calculate distance
    d = current_d
    d_max = math.sqrt((frame_dimension[0]-40)**2 + (frame_dimension[1]-40)**2)
    d_max = round(d_max)
    
    # adjust signal value to value_range
    incremental_list = np.linspace(1.5*radius, d_max, 9)
    stepsize = incremental_list[1]-incremental_list[0]
    z = 0.0
    if d <= 1.5*radius:
        z = max_value
    else:
        for i in incremental_list:
            if d <= i:
                z = (i-radius-(stepsize/2)) * smallest_step  # get mid-point/distance of plateau
                z = -(z-max_value)
                break  # exit incremental_list 
    return z


def exponential_increase(frame_dimension, value_range, radius, current_d):   # Function to create targets gaussians
    
    width = frame_dimension[0]  # Get the width of the frame for the meshgrid
    height = frame_dimension[1] # Get the height of the frame for the meshgrid
    widthSafety = width-50  # because target loc plots with a distance of 50 pixels to edge
    heightSafety = height-50  # because target loc plots with a distance of 50 pixels to edge
    
    # calculate smallest_step
    value_min = value_range[0]
    value_max = value_range[1]
    
    # calculate distance
    d = current_d
    
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



# Calculate graph
frame_dimension = (1540, 800)
target_radius = 80

# Define min and max value for frequency
min_frequency = 800  # is = 500 Hz
max_frequency = 20  # is = 100 Hz
frequency_range = (min_frequency, max_frequency)

# Define min and max value for amplitude
min_amplitude = 20  # is = 10 percent
max_amplitude = 100  # is = 100 percent
amplitude_range = (min_amplitude, max_amplitude)


# calculate max distance:
# (-40 pixel because plotted targets have a safty distnce of 40 to edges)
d_max = math.sqrt((frame_dimension[0]-50)**2 + (frame_dimension[1]-50)**2)
d_max = round(d_max,2)

steps = 200
# x axis values
x = np.linspace(0.0, d_max, num=steps)
# y axis values: frequency & amplitude
y_linear_f = np.zeros(steps)
y_incremental_f = np.zeros(steps)
y_exponential_f = np.zeros(steps)
y_linear_a = np.zeros(steps)
y_incremental_a = np.zeros(steps)
y_exponential_a = np.zeros(steps)

# corresponding y axis values
for count, value in enumerate(x):
    # calculate frequency values
    z_linear_f = linear_increase(frame_dimension, frequency_range, target_radius, value)
    z_incremental_f = incremental_increase(frame_dimension, frequency_range, target_radius, value)
    z_exponential_f = exponential_increase(frame_dimension, frequency_range, target_radius, value)
    y_linear_f[count] = z_linear_f
    y_incremental_f[count] = z_incremental_f
    y_exponential_f[count] = z_exponential_f
    # calculate amplitude values
    z_linear_a = linear_increase(frame_dimension, amplitude_range, target_radius, value)
    z_incremental_a = incremental_increase(frame_dimension, amplitude_range, target_radius, value)
    z_exponential_a = exponential_increase(frame_dimension, amplitude_range, target_radius, value)
    y_linear_a[count] = z_linear_a
    y_incremental_a[count] = z_incremental_a
    y_exponential_a[count] = z_exponential_a



## PLOT graph for linear
# creating graph space for two graphs
graph, (plot1, plot2) = plt.subplots(1, 2)
 
# plot1 graph for frequency
plot1.plot(x, y_linear_f)
plot1.set_title("Linear - Frequency")
plot1.set_ylabel('frequency [Hz]')
plot1.set_xlabel('distance [pixel]')
plot1.invert_xaxis()
 
# plot2 graph for amplitude
plot2.plot(x, y_linear_a)
plot2.set_title("Linear - Amplitude")
plot2.set_ylabel('amplitude [V]')
plot2.set_xlabel('distance [pixel]')
plot2.invert_xaxis()

# display the graph
graph.tight_layout()
plt.show()


## PLOT graph for incremental
# creating graph space for two graphs
graph, (plot1, plot2) = plt.subplots(1, 2)
 
# plot1 graph for frequency
plot1.plot(x, y_incremental_f)
plot1.set_title("Incremental - Frequency")
plot1.set_ylabel('frequency [Hz]')
plot1.set_xlabel('distance [pixel]')
plot1.invert_xaxis()
 
# plot2 graph for amplitude
plot2.plot(x, y_incremental_a)
plot2.set_title("Incremental - Amplitude")
plot2.set_ylabel('amplitude [V]')
plot2.set_xlabel('distance [pixel]')
plot2.invert_xaxis()

# display the graph
graph.tight_layout()
plt.show()


## PLOT graph for exponential
# creating graph space for two graphs
graph, (plot1, plot2) = plt.subplots(1, 2)
 
# plot1 graph for frequency
plot1.plot(x, y_exponential_f)
plot1.set_title("Exponential - Frequency")
plot1.set_ylabel('frequency [Hz]')
plot1.set_xlabel('distance [pixel]')
plot1.invert_xaxis()
 
# plot2 graph for amplitude
plot2.plot(x, y_exponential_a)
plot2.set_title("Exponential - Amplitude")
plot2.set_ylabel('amplitude [V]')
plot2.set_xlabel('distance [pixel]')
plot2.invert_xaxis()

# display the graph
graph.tight_layout()
plt.show()



## PLOT graph for incremental
# plotting the points 
#plt.plot(x, y_incremental)
  
# naming the x axis
#plt.xlabel('distance [pixel]')
# naming the y axis
#plt.ylabel('frequency [Hz]')
  
# giving a title to my graph
#plt.title('Incremental')

# invert axis
#plt.xlim(max(x), min(x))

# function to show the plot
#plt.show()


## PLOT graph for incremental
# plotting the points 
#plt.plot(x, y_exponential)
  
# naming the x axis
#plt.xlabel('distance [pixel]')
# naming the y axis
#plt.ylabel('frequency [Hz]')
  
# giving a title to my graph
#plt.title('Incremental')

# invert axis
#plt.xlim(max(x), min(x))
  
# function to show the plot
#plt.show()