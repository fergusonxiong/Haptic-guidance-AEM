import numpy as np
import pygame
import random
import sys, serial, glob
from serial.tools import list_ports
import time
from pysinewave import SineWave
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from height_functions import linear_increase, incremental_increase, exponential_increase

''' DESCRIPTION OF SOME VARIABLE OF THE CODE
xh -> x and y coordinates of the electrovibration device or the mouse otherwise
'''

# VARIABLES OF SIMULATION ON PYGAME
pygame.init() # start pygame
window_dimension = (1540, 800)
#window = pygame.display.set_mode(window_dimension) # create a window (size in pixels)
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
window.fill((255,255,255)) # white background
xc, yc = window.get_rect().center # window center


# Change HERE Seed for different scenarios 
seed = 1  # 8, 24, 42, 56, 64

# Set whether frequency and/or amplitude should change
frequency_on = 1
amplitude_on = 1


# Caption 
pygame.display.set_caption('electrovibration experiment')


# Text
fontTitle = pygame.font.Font('freesansbold.ttf', 45) # printing text font and font size
title = fontTitle.render('Electrovibration experiment', True, (0, 0, 0), (255, 255, 255)) # printing text object
titleRect = title.get_rect()
titleRect.center = (xc, yc-200) 

fontChoice = pygame.font.Font('freesansbold.ttf', 30) # printing text font and font size
textChoice = fontChoice.render('Choose setting:', True, (0, 0, 0), (255, 255, 255)) # printing text object
textChoiceRect = textChoice.get_rect()
textChoiceRect.center = (xc, yc-80) 

fontSetting = pygame.font.Font('freesansbold.ttf', 25) # printing text font and font size
fontSettingCorner = pygame.font.Font('freesansbold.ttf', 20) # printing text font and font size
textSetting1 = fontSetting.render('Linear', True, (0, 0, 0), (255, 255, 255)) # printing text object
textSetting1Corner = fontSettingCorner.render('Linear', True, (0, 0, 0), (255, 255, 255)) # printing text object
textSetting1Rect = textSetting1.get_rect()
textSetting1Rect.center = (xc-250, yc+10) 
fontSettingPress = pygame.font.Font('freesansbold.ttf', 20) # printing text font and font size
textSetting1Choice = fontSettingPress.render('Press \'1\'', True, (0, 0, 0), (255, 255, 255)) # printing text object
textSetting1ChoiceRect = textSetting1Choice.get_rect()
textSetting1ChoiceRect.center = (xc-250, yc+45) 

textSetting2 = fontSetting.render('Incremental', True, (0, 0, 0), (255, 255, 255)) # printing text object
textSetting2Corner = fontSettingCorner.render('Incremental', True, (0, 0, 0), (255, 255, 255)) # printing text object
textSetting2Rect = textSetting2.get_rect()
textSetting2Rect.center = (xc, yc+10)
textSetting2Choice = fontSettingPress.render('Press \'2\'', True, (0, 0, 0), (255, 255, 255)) # printing text object
textSetting2ChoiceRect = textSetting2Choice.get_rect()
textSetting2ChoiceRect.center = (xc, yc+45)

textSetting3 = fontSetting.render('Exponential', True, (0, 0, 0), (255, 255, 255)) # printing text object
textSetting3Corner = fontSettingCorner.render('Exponential', True, (0, 0, 0), (255, 255, 255)) # printing text object
textSetting3Rect = textSetting3.get_rect()
textSetting3Rect.center = (xc+250, yc+10)
textSetting3Choice = fontSettingPress.render('Press \'3\'', True, (0, 0, 0), (255, 255, 255)) # printing text object
textSetting3ChoiceRect = textSetting3Choice.get_rect()
textSetting3ChoiceRect.center = (xc+250, yc+45)

fontTime = pygame.font.Font('freesansbold.ttf', 20) # printing text font and font size
textTime = fontTime.render('Time: ', True, (255, 0, 0)) # printing text object
textTimeRect = textTime.get_rect()
textTimeRect.topleft = (10, 10) 

textTargets = fontTime.render('Targets (' + str(0) + '/' + str(0) +')', True, (0, 0, 0)) # printing text object
textTargetsRect = textTargets.get_rect()
textTargetsRect.midtop = (xc, 10)

textAmplitude = fontTime.render('Amplitude:       ', True, (0, 0, 0)) # printing text object
textAmplitudeRect = textAmplitude.get_rect()
textAmplitudeRect.midbottom = (xc, window_dimension[1]-30)

textFrequency = fontTime.render('Frequency:         ', True, (0, 0, 0)) # printing text object
textFrequencyRect = textFrequency.get_rect()
textFrequencyRect.midbottom = (xc, window_dimension[1]-5)

textScore = fontTitle.render('Score', True, (0, 0, 0), (255, 255, 255)) # printing text object
textScoreRect = textScore.get_rect()
textScoreRect.center = (xc, yc-150) 

fontTable = pygame.font.Font('freesansbold.ttf', 20) # printing text font and font size
textTotalTime = fontTable.render('Total time:', True, (0, 0, 0), (255, 255, 255)) # printing text object
textTotalTimeRect = textTotalTime.get_rect()
textTotalTimeRect.center = (xc, yc-20)  

textRestart = fontTable.render('Press \'z\' for restart', True, (0, 0, 0), (255, 255, 255)) # printing text object
textRestartRect = textRestart.get_rect()
textRestartRect.center = (xc, yc+150)


# Clock variables
clock = pygame.time.Clock() # initialise clock
dts = 0.01
FPS = int(1 / dts)


# Set up audio variables
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
#volume.GetVolumeRange()


# VARIABLES ABOUT ELEMENTS OF THE SIMULATION 
# Define number & size of target
target_n = 0  # number of reached targets
target_n_total = 10  # total number of targets
target_radius = 100

# Define min and max value for frequency
min_frequency = 15  # is = 15 Hz
max_frequency = 800  # is = 800 Hz
frequency_range = (max_frequency, min_frequency)
constantFrequency = 400  # in case frequency change is set off

# Define min and max value for amplitude
min_amplitude = 40  # is = 40 percent
max_amplitude = 100  # is = 100 percent
amplitude_range = (min_amplitude, max_amplitude)
constantAmplitude = 100  # in case amplitude change is set off

# Minimum distance to edges/ Area in which target can plots
min_d = 50
x_plot = np.array([min_d, window_dimension[0]-min_d])
y_plot = np.array([min_d, window_dimension[1]-min_d])

# Create a sine wave, with a starting pitch of 12, and a pitch change speed of 40/second.
sinewave = SineWave(pitch = 10, pitch_per_second = 40)
  

run = True
startscreen = True
endscreen = False
setTimer = 0

while run:
    '''*********** STARTSCREEN ***********'''
    while startscreen:  
        for event in pygame.event.get(): # interrupt function
            if event.type == pygame.QUIT: # force quit with closing the window
                startscreen = False
                setTimer = 1
                run = False
            elif event.type == pygame.KEYUP:
                if event.key == ord('q'): # force quit with q button
                    startscreen = False
                    setTimer = 1
                    run = False
                if event.key == ord('1'): # select setting 1
                    setTimer = 1
                    setting = 1
                    startscreen = False
                    random.seed(seed)  # repeat same scenario
                    target_pos = np.array([random.randint(x_plot[0], x_plot[1]), random.randint(y_plot[0], y_plot[1])])  # random target pos
                if event.key == ord('2'): # select setting 2
                    setTimer = 1
                    setting = 2
                    startscreen = False
                    random.seed(seed)  # repeat same scenario
                    target_pos = np.array([random.randint(x_plot[0], x_plot[1]), random.randint(y_plot[0], y_plot[1])])  # random target pos
                if event.key == ord('3'): # select setting 3
                    setTimer = 1
                    setting = 3
                    startscreen = False
                    random.seed(seed)  # repeat same scenario
                    target_pos = np.array([random.randint(x_plot[0], x_plot[1]), random.randint(y_plot[0], y_plot[1])])  # random target pos
                
        # real-time plotting
        window.fill((255, 255, 255)) # clear window
        
        # plot text to screen
        window.blit(title, titleRect)
        window.blit(textChoice, textChoiceRect)
        window.blit(textSetting1, textSetting1Rect)
        window.blit(textSetting1Choice, textSetting1ChoiceRect)
        window.blit(textSetting2, textSetting2Rect)
        window.blit(textSetting2Choice, textSetting2ChoiceRect)
        window.blit(textSetting3, textSetting3Rect)
        window.blit(textSetting3Choice, textSetting3ChoiceRect)
        
        pygame.display.flip() # update display
    '''*********** !STARTSCREEN ***********'''    
    
    # quit loop if window has been closed
    if run == False:  
        break
    
    # get mouse position
    mouse_pos = pygame.mouse.get_pos()
    xh = np.clip(np.array(mouse_pos), 0, pygame.display.get_surface().get_width()-1)

    '''************* TASK *************'''
    for event in pygame.event.get(): # interrupt function
        if event.type == pygame.QUIT: # force quit with closing the window
            run = False
        elif event.type == pygame.KEYUP:
            if event.key == ord('q'): # force quit with q button
                run = False
           
    # start timer
    if setTimer == 1:
        timerStart = time.perf_counter()
        setTimer = 0 
        sinewave.play()  # Turn the sine wave on.
    totalTime = round(time.perf_counter()-timerStart, 1) # calculate current time
    
    if setting == 1:
        # define the features of setting 1
        finger_pos = xh
        frequency = linear_increase(window_dimension, frequency_range, target_radius, finger_pos, target_pos)
        frequency = round(frequency, 2)
        amplitude = linear_increase(window_dimension, amplitude_range, target_radius, finger_pos, target_pos)
        amplitude = round(amplitude, 2)
        # change setting choice
        textSettingChoice = textSetting1Corner
        textSettingChoiceRect = textSettingChoice.get_rect()
        textSettingChoiceRect.topright = (window_dimension[0]-10, 10)
    
    if setting == 2:
        # define the features of setting 2
        finger_pos = xh
        frequency = incremental_increase(window_dimension, frequency_range, target_radius, finger_pos, target_pos)
        frequency = round(frequency, 2)
        amplitude = incremental_increase(window_dimension, amplitude_range, target_radius, finger_pos, target_pos)
        amplitude = round(amplitude, 2)
        # change setting choice
        textSettingChoice = textSetting2Corner
        textSettingChoiceRect = textSettingChoice.get_rect()
        textSettingChoiceRect.topright = (window_dimension[0]-10, 10)
    
    if setting == 3:
        # define the features of setting 3
        finger_pos = xh
        frequency = exponential_increase(window_dimension, frequency_range, target_radius, finger_pos, target_pos)
        frequency = round(frequency, 2)
        amplitude = exponential_increase(window_dimension, amplitude_range, target_radius, finger_pos, target_pos)
        amplitude = round(amplitude, 2)
        # change setting choice
        textSettingChoice = textSetting3Corner
        textSettingChoiceRect = textSettingChoice.get_rect()
        textSettingChoiceRect.topright = (window_dimension[0]-10, 10)
        
    # check if target is reached
    if np.sqrt((xh[0]-target_pos[0])**2 + (xh[1]-target_pos[1])**2)<target_radius:
        target_pos = np.array([random.randint(x_plot[0], x_plot[1]), random.randint(y_plot[0], y_plot[1])])  # random target pos
        target_n = target_n+1
        
    # check if number of targets is reached
    if target_n >= target_n_total:
        endscreen = True
        totalTime = round(time.perf_counter()-timerStart, 2)  # calculate final total time
    
    # adjust soundfrequency according to frequency
    if amplitude_on:
        volume.SetMasterVolumeLevelScalar(amplitude/100, None)
    else:
        volume.SetMasterVolumeLevelScalar(constantAmplitude/100, None)
    if frequency_on:
        sinewave.set_frequency(frequency)
    else:
        sinewave.set_frequency(constantFrequency)
    
    # real-time plotting
    window.fill((255,255,255)) # clear window
    
    # plot ouput value
    if amplitude_on:
        textAmplitude = fontTime.render('Amplitude: ' + str(amplitude) + '%', True, (0, 0, 0)) # printing text object
        window.blit(textAmplitude, textAmplitudeRect)
    else:
        textAmplitude = fontTime.render('Amplitude: ' + str(constantAmplitude) + '%', True, (0, 0, 0)) # printing text object
        window.blit(textAmplitude, textAmplitudeRect)
    if frequency_on:
        textFrequency = fontTime.render('Frequency: ' + str(frequency) + 'Hz', True, (0, 0, 0)) # printing text object
        window.blit(textFrequency, textFrequencyRect)
    else:
        textFrequency = fontTime.render('Frequency: ' + str(constantFrequency) + 'Hz', True, (0, 0, 0)) # printing text object
        window.blit(textFrequency, textFrequencyRect)
    
    # plot time
    textTime = fontTime.render('Time: '+ str(totalTime), True, (0, 0, 0))
    window.blit(textTime, textTimeRect)
    
    # plot number of reached targets
    textTargets = fontTime.render('Targets (' + str(target_n) + '/' + str(target_n_total) +')', True, (255, 0, 0)) # printing text object
    window.blit(textTargets, textTargetsRect)
    
    # plot target
    pygame.draw.circle(window, (255, 0, 0), target_pos, target_radius) # draw a red point for target
    
    # plot mouse
    pygame.draw.circle(window, (0, 255, 0), (xh[0], xh[1]), 5) # draw a green point for mouse
    
    window.blit(textSettingChoice, textSettingChoiceRect)
    pygame.display.flip() # update display
    
    '''************* !TASK *************'''
    
    if endscreen:
        sinewave.stop()
        
    if run == False:
        sinewave.stop()
        
    '''*********** ENDSCRREEN ***********'''
    while endscreen:  
        for event in pygame.event.get(): # interrupt function
            if event.type == pygame.QUIT: # force quit with closing the window
                endscreen = False
                run = False
            elif event.type == pygame.KEYUP:
                if event.key == ord('q'): # force quit with q button
                    endscreen = False
                    run = False
                if event.key == ord('z'): # restart button
                    endscreen = False
                    startscreen = True
                    target_n = 0  # reset number of reached targets
        
        # real-time plotting
        window.fill((255,255,255)) # clear window
    
        # plot text to screen
        window.blit(textScore, textScoreRect)
        
        textTotalTime = fontTable.render('Total time: ' + str(totalTime), True, (0, 0, 0), (255, 255, 255)) # printing text object
        textTotalTimeRect = textTotalTime.get_rect()
        textTotalTimeRect.center = (xc, yc-20)  
        window.blit(textTotalTime, textTotalTimeRect)
        
        window.blit(textRestart, textRestartRect)
        
        pygame.display.flip() # update display
    '''*********** !ENDSCREEN ***********'''
    
    # try to keep it real time with the desired step time
    clock.tick(FPS)
    
    if run == False:
        break
    
pygame.quit() # stop pygame