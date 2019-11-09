#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'MICROYU'

import random
import matplotlib.pyplot as plt
import numpy as np
from tensorboardX import SummaryWriter

class RL_Dataset():
    def __init__(self, rewards, losses):
        pass

class RL_Ploter():
    def __init__(self, use_tensorboard=True):
        self.use_tensorboard = use_tensorboard
        self.step_counter = 0
        self.episode_counter = 0
        self.rewards = []
        self.losses = []
        self.history_dataset = []
        if use_tensorboard:
            self.tf_board_writer = SummaryWriter()
            print("[Info] tensorboardX is enable, please open tensorboard client in current path.")

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
        pass

    def plot_result_multi(self, is_smoothing=True):
        plt.figure(figsize=(20,5))
        plt.subplot(131)
        plt.title('frame %s. reward: %s' % (self.episode_counter, np.mean(rewards[-10:])))
        plt.plot(rewards)
        plt.subplot(132)
        plt.title('loss')
        plt.plot(losses)
        plt.show()
    
    def plot_result_single(self, is_smoothing=True, reward_figure=True, loss_figure=True):
        pass

class Simple_Ploter():
    def __init__(self, x_data, y_data):
        pass


class Dynamic_Plotor():
    def __init__(self, x_data, y_data):
        pass