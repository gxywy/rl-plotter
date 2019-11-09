#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'MICROYU'

import random
import numpy as np
import matplotlib.pyplot as plt

class RL_Ploter():
    def __init__(self, tensorboard=True, matplot=True, read_history=True):
        self.tensorboard = tensorboard
        self.matplot = matplot
        self.read_history = read_history
        self.step_counter = 0
        self.episode_counter = 0
        self.rewards = []
        self.losses = []

    def plot(self):
        plt.figure(figsize=(20,5))
        plt.subplot(131)
        plt.title('frame %s. reward: %s' % (frame_idx, np.mean(rewards[-10:])))
        plt.plot(rewards)
        plt.subplot(132)
        plt.title('loss')
        plt.plot(losses)
        plt.show()