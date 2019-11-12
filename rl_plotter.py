#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'MICROYU'

import os
import random
import matplotlib.pyplot as plt
import numpy as np
from tensorboardX import SummaryWriter

class RL_Plotter():
    def __init__(self, exp_name, use_tensorboard=False):
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

    def add_rewards(self, reward, log=True):
        self.episode_counter += 1
        self.rewards.append(reward)
        if self.use_tensorboard:
            self.tf_board_writer.add_scalar('Train/reward', reward, self.episode_counter)
        #print("[info] episode:" )

    def add_losses(self, loss, log=True):
        self.step_counter += 1
        self.losses.append(loss)
        if self.use_tensorboard:
            self.tf_board_writer.add_scalar('Train/loss', loss, self.step_counter)

    def reset(self):
        self.episode_counter = 0
        self.step_counter = 0
        self.rewards = self.losses = []

    def _save_result(self, fig):
        save_dir = './result/'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        fig.savefig(save_dir + self.exp_name, dpi=400, bbox_inches='tight')

        csv_file = open(save_dir + self.exp_name + '_reward.csv', 'w')
        for index in range(self.episode_counter):
            csv_file.write(str(index)+','+str(self.rewards[index])+'\n')
            csv_file.flush()
        csv_file.close()

        csv_file = open(save_dir + self.exp_name + '_loss.csv', 'w')
        for index in range(self.step_counter):
            csv_file.write(str(index)+','+str(self.losses[index])+'\n')
            csv_file.flush()
        csv_file.close()
    
    def _smooth_curve(self, points, factor):
        smoothed_points = []
        for point in points:
            if smoothed_points:
                previous = smoothed_points[-1]
                smoothed_points.append(previous * factor + point * (1 - factor))
            else:
                smoothed_points.append(point)
        return smoothed_points

    def plot_result_multi(self, reward_smooth=0.9, loss_smooth=0.9, grid=False, show=True):
        fig = plt.figure(figsize=(12,5))

        ax1 = fig.add_subplot(1,2,1)
        ax1.set(title='Episode Reward over Time', xlabel='Episode', ylabel='Episode Reward')
        if grid:
            ax1.grid()
        ax1.plot(self.rewards, color='#1f77b4', alpha=0.3)
        ax1.plot(self._smooth_curve(self.rewards, reward_smooth), color='#1f77b4', label=self.exp_name)
        ax1.legend(loc='lower right')

        ax2 = fig.add_subplot(1,2,2)
        ax2.set(title='Running Variance over Time', xlabel='Timestep', ylabel='Running Variance')
        if grid:
            ax2.grid()
        ax2.plot(self.losses, color="#1f77b4", alpha=0.3)
        ax2.plot(self._smooth_curve(self.losses, loss_smooth), color='#1f77b4', label=self.exp_name)
        ax2.legend(loc='lower right')
        
        self._save_result(fig)
        if show:
            plt.show()
    
    def plot_reward(self, smooth=0.9, grid=False, show=True):
        fig, ax = plt.subplots()
        ax.set(title='Episode Reward over Time', xlabel='Episode', ylabel='Episode Reward')
        if grid:
            ax.grid()
        ax.plot(self.rewards, color='#1f77b4', alpha=0.3)
        ax.plot(self._smooth_curve(self.rewards, smooth), color='#1f77b4', label=self.exp_name)
        ax.legend(loc='lower right')

        self._save_result(fig)
        if show:
            plt.show()
    
    def plot_loss(self, smooth=0.9, grid=False, show=True):
        fig, ax = plt.subplots()
        ax.set(title='Running Variance over Time', xlabel='Timestep', ylabel='Running Variance')
        if grid:
            ax.grid()
        ax.plot(self.losses, color="#1f77b4", alpha=0.3)
        ax.plot(self._smooth_curve(self.losses, smooth), color='#1f77b4', label=self.exp_name)
        ax.legend(loc='lower right')
        
        self._save_result(fig)
        if show:
            plt.show()