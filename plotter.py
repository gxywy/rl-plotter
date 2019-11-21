#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'MICROYU'

import matplotlib.pyplot as plt
import numpy as np
import plot_util as pu
import warnings
warnings.filterwarnings('ignore')

def plot(log_dir='./logs/', average_group=True, split_fn=lambda _: '', shaded_std=True, show=True):
    results = pu.load_results(log_dir)
    pu.plot_results(results, average_group=average_group, split_fn=split_fn, shaded_std=shaded_std)
    plt.savefig(log_dir + 'figure', dpi=400, bbox_inches='tight')
    if show:
        plt.show()

def plot_single(log_dir, smooth_radius=0, show=True):
    results = pu.load_results(log_dir)
    r = results[0]
    plt.plot(np.cumsum(r.monitor.l), pu.smooth(r.monitor.r, radius=0))
    plt.savefig(log_dir + 'figure', dpi=400, bbox_inches='tight')
    if show:
        plt.show()

if __name__ == "__main__":
    plot()