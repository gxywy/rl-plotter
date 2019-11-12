#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'MICROYU'

import random
import matplotlib.pyplot as plt
import numpy as np
from tensorboardX import SummaryWriter

colors = ['b', 'g', 'r', 'c', 'k', 'y', 'm']

class RL_Dataset():
    def __init__(self, rewards, losses):
        pass

class RL_Ploter():
    def __init__(self, exp_name, use_tensorboard=True):
        self.use_tensorboard = use_tensorboard
        self.exp_name = exp_name
        self.step_counter = 0
        self.episode_counter = 0
        self.rewards = []
        self.losses = []
        self.history_dataset = []
        if use_tensorboard:
            self.tf_board_writer = SummaryWriter()
            print("[Info] tensorboardX is enable, please open tensorboard server in current path.")

    def append_rewards(self, reward):
        self.episode_counter += 1
        self.rewards.append(reward)
        if self.use_tensorboard:
            self.tf_board_writer.add_scalar('Train/reward', reward, self.episode_counter)

    def append_losses(self, loss):
        self.step_counter += 1
        self.losses.append(loss)
        if self.use_tensorboard:
            self.tf_board_writer.add_scalar('Train/loss', loss, self.step_counter)

    def reset(self):
        self.episode_counter = 0
        self.step_counter = 0
        self.rewards = self.losses = []
    
    def load_history(self):
        pass

    def save_result(self):
        plt.savefig('haha.png', dpi=400, bbox_inches='tight')
        pass
    
    def smooth_curve(self, points, factor=0.9):
        smoothed_points = []
        for point in points:
            if smoothed_points:
                previous = smoothed_points[-1]
                smoothed_points.append(previous * factor + point * (1 - factor))
            else:
                smoothed_points.append(point)
        return smoothed_points

    def plot_result_multi(self):
        reward_mean = np.mean(self.rewards)
        reward_std = np.std(self.rewards)

        plt.xkcd()
        
        fig = plt.figure(figsize=(12,5))
        ax1 = fig.add_subplot(1,2,1)
        ax1.set_xlabel('Episode')
        ax1.set_ylabel('Episode Reward')
        ax1.set_title('Episode Reward over Time')
        
        ax1.plot(self.smooth_curve(self.rewards), label=self.exp_name)
        ax1.fill_between(np.arange(self.episode_counter), self.rewards - reward_std, self.rewards + reward_std, alpha=0.1)
        #ax1.plot(self.rewards, 'g', linewidth=3, alpha=0.1)
        ax1.legend(loc='upper left')

        ax2 = fig.add_subplot(1,2,2)
        ax2.set_xlabel('Step')
        ax2.set_ylabel('Running Variance')
        ax2.set_title('Running Variance over Time')
        ax2.plot(self.losses, label=self.exp_name)
        ax2.legend(loc='upper left')

        #plt.legend(handles=[l1, l2], labels=['up', 'down'],  loc='best')
        #plt.set_autoscale_on(True)
        #plt.autoscale_view(True,True,True)
        
        plt.tight_layout()
        plt.show()
    
    def plot_result_single(self, is_smoothing=True, reward_figure=True, loss_figure=True):
        pass


class Simple_Ploter():
    def __init__(self, x_data, y_data):
        pass


class Dynamic_Plotor():
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