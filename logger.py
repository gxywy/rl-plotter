#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'MICROYU'

import csv
import os
import json
import random
import time
import logging
import matplotlib.pyplot as plt
import numpy as np

class Logger():
    def __init__(self, exp_name, env_name=None, use_tensorboard=False):
        self.save_dir = "./logs/" + exp_name + "/"
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        self.csv_file = open(self.save_dir + 'monitor.csv', 'w')
        header={"t_start": time.time(), 'env_id' : env_name}
        header = '# {} \n'.format(json.dumps(header))
        self.csv_file.write(header)
        self.logger = csv.DictWriter(self.csv_file, fieldnames=('r', 'l', 't'))
        self.logger.writeheader()
        self.csv_file.flush()

        self.step_counter = 0
        self.episode_counter = 0
        self.steps = []
        self.rewards = []
        self.losses = []

        self.use_tensorboard = use_tensorboard
        self.is_learning_start = False
        self.start_time = time.time()
        
        logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s %(message)s')
        logging.info(exp_name + " start !")

        if use_tensorboard:
            from tensorboardX import SummaryWriter
            self.tf_board_writer = SummaryWriter()
            logging.warn("tensorboardX is logger enable, please open tensorboard server in current path!")

    def add_step(self):
        self.step_counter += 1
        return np.sum(self.steps)
    
    def add_episode(self):
        self.steps.append(self.step_counter)
        self.step_counter = 0
        self.episode_counter += 1
        return self.episode_counter

    def add_reward(self, reward, freq=10):
        self.rewards.append(reward)
        total_step = np.sum(self.steps)

        if self.use_tensorboard:
            self.tf_board_writer.add_scalar('Train/reward', reward, total_step)
        
        if self.episode_counter % freq == 0:
            logging.info("episodes: %d, mean reward: %.2f, steps: %d, mean loss: %f" % \
                (self.episode_counter, np.mean(self.rewards[-freq:]), total_step, np.mean(self.losses[-freq:])))
        
        epinfo = {"r": reward, "l": self.steps[-1], "t": time.time() - self.start_time}
        self.logger.writerow(epinfo)
        self.csv_file.flush()

    def add_loss(self, loss):
        self.losses.append(loss)
        total_step = np.sum(self.steps)

        if self.use_tensorboard:
            self.tf_board_writer.add_scalar('Train/loss', loss, total_step)
        
        if not self.is_learning_start:
            logging.warn("start learning, loss data received.")
            self.is_learning_start = True

        #self.csv_file.write(str(total_step) +','+ str(loss)+'\n')
        #self.csv_file.flush()

    def reset(self):
        self.episode_counter = 0
        self.step_counter = 0
        self.rewards = []
        self.losses = []

    def finish(self):
        self.csv_file.close()
        self.reset()
        if self.use_tensorboard:
            self.tf_board_writer.close()