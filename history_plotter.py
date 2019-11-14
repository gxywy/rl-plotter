#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'MICROYU'

import os
import csv
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s %(message)s')

colors = ['b', 'g', 'r', 'c', 'k', 'y', 'm']

class History_Plotter():
    def __init__(self):
        self.exps = []
        self.path = "./result/"

        logging.info("reading data in " + self.path + '...')
        exps_folder = os.listdir(self.path)
        ## 读取每个实验的数据
        for exp_folder in exps_folder:
            if os.path.isdir(self.path + exp_folder):
                exp_info = {'exp_name':exp_folder, 'reward_mean': [], 'reward_std': [], 'loss_mean': [], 'loss_std': [], 'raw_data': []}
                path = "./result/" + exp_folder + "/"
                times_folder = os.listdir(path)
                ## 读取每次实验的数据
                for time_folder in times_folder:
                    if os.path.isdir(path + time_folder):
                        result = {"reward_x":[], 'reward':[], 'loss_x':[], 'loss':[]}
                        data = pd.read_csv(path + time_folder + '/reward.csv', names=["reward_x", "reward"])
                        result['reward_x'] = data.reward_x.tolist()
                        result['reward'] = data.reward.tolist()
                        data = pd.read_csv(path + time_folder + '/loss.csv', names=["loss_x", "loss"])
                        result['loss_x'] = data.loss_x.tolist()
                        result['loss'] = data.loss.tolist()
                        exp_info['raw_data'].append(result)
                ## 根据raw_data计算平均值与方差
                reward_all = []
                loss_all = []
                for item in exp_info['raw_data']:
                    reward_all.append(item['reward'])
                    loss_all.append(item['loss'])
                exp_info['reward_mean'] = np.array(reward_all).T.mean(axis=1)
                exp_info['reward_std'] = np.array(reward_all).T.std(axis=1)
                exp_info['loss_mean'] = np.array(loss_all).T.mean(axis=1)
                exp_info['loss_std'] = np.array(loss_all).T.std(axis=1)
                self.exps.append(exp_info)

    def plot(self, grid=False, show=True, title=None):
        fig = plt.figure(figsize=(12,5))

        ax1 = fig.add_subplot(1,2,1)
        ax1.set(title='Episode Score over Time', xlabel='Episode', ylabel='Episode Score')
        if grid:
            ax1.grid()
        for index in range(len(self.exps)):
            mean = exps[index]['reward_mean']
            std = exps[index]['reward_std']
            ax1.fill_between(exps[index]['raw_data'][0]['reward_x'], mean - std, mean + std, color=colors[index], alpha=0.3)
            ax1.plot(mean, color=colors[index], label=self.exp_name)
        ax1.legend(loc='lower right')

        ax2 = fig.add_subplot(1,2,2)
        ax2.set(title='Running Variance over Time', xlabel='Step', ylabel='Running Variance')
        if grid:
            ax2.grid()
        for index in range(len(self.exps)):
            mean = exps[index]['loss_mean']
            std = exps[index]['loss_std']
            ax2.fill_between(exps[index]['raw_data'][0]['loss_x'], mean - std, mean + std, color=colors[index], alpha=0.3)
            ax2.plot(mean, color=colors[index], label=self.exp_name)
        ax2.legend(loc='lower right')
        
        self._save_result(fig)
        if show:
            plt.show()

    def _save_result(self, fig):
        logging.info("saving data in " + self.path + '...')
        fig.savefig(self.path + 'figure', dpi=400, bbox_inches='tight')