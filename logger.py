#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'MICROYU'

import os
import random
import time
import logging
import matplotlib.pyplot as plt
import numpy as np
from tensorboardX import SummaryWriter

class Logger():
    def __init__(self, save_dir, use_tensorboard=False):
        self.use_tensorboard = use_tensorboard
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        self.step_counter = 0
        self.episode_counter = 0
        self.rewards = []
        self.losses = []
        self.reward_csv = open(self.save_dir + 'reward.csv', 'w')
        self.loss_csv = open(self.save_dir + 'loss.csv', 'w')
        self.is_learning_start = False

        logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s %(message)s')
        if use_tensorboard:
            self.tf_board_writer = SummaryWriter()
            logging.warn("tensorboardX is enable, please open tensorboard server in current path!")
        logging.info("RL_Plotter initialized successfully!")

    def add_step(self):
        self.step_counter += 1
    
    def add_episode(self):
        self.episode_counter += 1

    def add_reward(self, reward, freq=10):
        self.add_episode()
        self.rewards.append(reward)
        if self.use_tensorboard:
            self.tf_board_writer.add_scalar('Train/reward', reward, self.episode_counter)
        
        if self.episode_counter % 10 == 0:
            logging.info("episodes: %d, mean reward: %.2f, steps: %d, mean loss: %f" % \
                (self.episode_counter, np.mean(self.rewards[-10:]), self.step_counter, np.mean(self.losses[-10])))
        
        if self.episode_counter % freq == 0:
            self.reward_csv.write(str(self.episode_counter) +','+ str(self.rewards[-freq:])+'\n')
            self.reward_csv.flush()
        
        return self.episode_counter

    def add_loss(self, loss):
        self.add_step()
        self.losses.append(loss)
        if self.use_tensorboard:
            self.tf_board_writer.add_scalar('Train/loss', loss, self.step_counter)
        
        if not self.is_learning_start:
            logging.warn("start learning, loss data received.")
            self.is_learning_start = True

        self.loss_csv.write(str(self.step_counter) +','+ str(loss)+'\n')
        self.loss_csv.flush()

        return self.step_counter

    def reset(self):
        self.episode_counter = 0
        self.step_counter = 0
        self.rewards = []
        self.losses = []

    def finish(self):
        self.reward_csv.close()
        self.loss_csv.close()
        self.tf_board_writer.close()