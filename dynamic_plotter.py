#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'MICROYU'

import os
import random
import matplotlib.pyplot as plt
import numpy as np

class Dynamic_Plottor():
    def __init__(self, x_data, y_data):
        pass

    def plot(self, x, y):
        plt.ion() # interactive mode on 
        line, = plt.plot(x,y) # plot the data and specify the 2d line
        ax = plt.gca() # get most of the figure elements 

        while True:
            x = np.append(x, new_x)
            y = np.append(y, new_y)
            line.set_xdata(x)
            line.set_ydata(y) # set the curve with new data
            ax.relim() # renew the data limits
            ax.autoscale_view(True, True, True) # rescale plot view
            plt.draw() # plot new figure
            plt.pause(1e-17) # pause to show the figure