#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'MICROYU'

import csv
import os
import json, time
import numpy as np

color2num = dict(
    gray=30,
    red=31,
    green=32,
    yellow=33,
    blue=34,
    magenta=35,
    cyan=36,
    white=37,
    crimson=38
)

def colorize(string, color, bold=False, highlight=False):
    """
    Colorize a string.

    This function was originally written by John Schulman.
    """
    attr = []
    num = color2num[color]
    if highlight: num += 10
    attr.append(str(num))
    if bold: attr.append('1')
    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)


class Logger():
    def __init__(self, log_dir="./logs", exp_name=None, env_name=None, seed=0):
        num_exps = 0
        self.log_dir = f"./{log_dir}/{exp_name}_{env_name}_seed{seed}"
        while True:
            if os.path.exists(f"{self.log_dir}-{str(num_exps)}/"):
                num_exps += 1
            else:
                self.log_dir += f"-{str(num_exps)}/"
                os.makedirs(self.log_dir)
                break
        self.csv_file = open(self.log_dir + '/evaluator.csv', 'w', encoding='utf8')
        header={"t_start": time.time(), 'env_id' : env_name, 'exp_name': exp_name, 'seed': seed}
        header = '# {} \n'.format(json.dumps(header))
        self.csv_file.write(header)
        self.logger = csv.DictWriter(self.csv_file, fieldnames=('mean_score', 'total_steps', 'std_score', 'max_score', 'min_score'))
        self.logger.writeheader()
        self.csv_file.flush()

    def monitor_env(self, env):
        from baselines import bench
        env = bench.Monitor(env, self.log_dir, allow_early_resets=True)
        return env

    def update(self, score, total_steps):
        '''
            Score is a list
        '''
        avg_score = np.mean(score)
        std_score = np.std(score)
        max_score = np.max(score)
        min_score = np.min(score)

        print(colorize(f"\nEvaluation over {len(score)} episodes after {total_steps}:", 'yellow', bold=True))
        print(colorize(f"Avg: {avg_score:.3f} Std: {std_score:.3f} Max: {max_score:.3f} Min: {min_score:.3f}\n", 'yellow', bold=True))
        
        epinfo = {"mean_score": avg_score, "total_steps": total_steps, "std_score": std_score, "max_score": max_score, "min_score": max_score}
        self.logger.writerow(epinfo)
        self.csv_file.flush()

class CustomLogger():
    def __init__(self, log_dir="./logs", exp_name=None, env_name=None, seed=0, filename="logger.csv", fieldnames=[]):
        self.fieldnames = ["total_steps"] + fieldnames
        num_exps = 0
        self.log_dir = f"./{log_dir}/{exp_name}_{env_name}_seed{seed}"
        while True:
            if os.path.exists(f"{self.log_dir}-{str(num_exps)}/"):
                num_exps += 1
            else:
                self.log_dir += f"-{str(num_exps)}/"
                os.makedirs(self.log_dir)
                break
        self.csv_file = open(self.log_dir + '/' + filename, 'w', encoding='utf8')
        header={"t_start": time.time(), 'env_id' : env_name, 'exp_name': exp_name, 'seed': seed}
        header = '# {} \n'.format(json.dumps(header))
        self.csv_file.write(header)
        self.logger = csv.DictWriter(self.csv_file, fieldnames=(self.fieldnames))
        self.logger.writeheader()
        self.csv_file.flush()

    def update(self, fieldvalues, total_steps):

        print(colorize(f"\nCustomLogger with fileds: {self.fieldnames}", 'yellow', bold=True))
        print(colorize(f"total_steps: {total_steps}, fieldvalues: {fieldvalues}\n", 'yellow', bold=True))
        
        epinfo = {}
        fieldvalues = [total_steps] + fieldvalues
        for filedname, filedvalue in zip(self.fieldnames, fieldvalues):
                epinfo.update({filedname: filedvalue})
        self.logger.writerow(epinfo)
        self.csv_file.flush()