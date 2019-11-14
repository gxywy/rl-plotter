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

exps = []
path = "./result/"
exps_folder = os.listdir(path)
## 读取每个实验的数据
for exp_folder in exps_folder:
    if os.path.isdir(path + exp_folder):
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
        exps.append(exp_info)