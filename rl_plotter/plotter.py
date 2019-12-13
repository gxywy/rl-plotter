#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'MICROYU'

import argparse
import warnings
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from rl_plotter import plot_util as pu
warnings.filterwarnings('ignore')

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def default_xy_fn(r):
    x = np.cumsum(r.monitor.l)
    y = pu.smooth(r.monitor.r, radius=10)
    return x,y

def time_xy_fn(r):
    x = r.monitor.t  / 60 / 60
    y = pu.smooth(r.monitor.r, radius=10)
    return x,y

parser = argparse.ArgumentParser(description='plotter')
parser.add_argument('--log_dir', default='./logs/', metavar='DIR',
                    help='log dir (default: ./logs/)')
parser.add_argument('--style', default='seaborn', metavar='STYLE',
                    help='matplotlib figure style (default: seaborn)')
parser.add_argument('--title', default=None, metavar='TITLE',
                    help='matplotlib figure title (default: None)')
parser.add_argument('--xlabel', default=None, metavar='XL',
                    help='matplotlib figure xlabel (default: None)')
parser.add_argument('--xlog', type=str2bool, default=False, 
                    help='use log in x axis scale (default: False)')
parser.add_argument('--xlim', type=int, default=None, 
                    help='matplotlib figure x axis limit (default: None)')
parser.add_argument('--ylabel', default=None, metavar='YL',
                    help='matplotlib figure ylabel (default: None)')
parser.add_argument('--average_group', type=str2bool, default=True,
                    help='if True, will average the curves in the same group and plot the mean. Enables resampling \
                        (if resample = 0, will use 512 steps) (default: False)')
parser.add_argument('--shaded_std', type=str2bool, default=True,
                    help='if True, the shaded region corresponding to standard deviation of the group of curves will be shown (default: True)')
parser.add_argument('--shaded_err', type=str2bool, default=False,
                    help='if True, the shaded region corresponding to error in mean estimate of the group of curves will be shown(default: False)')
parser.add_argument('--legend_outside', type=str2bool, default=False,
                    help='if True, will place the legend outside of the sub-panels (default: 50)')
parser.add_argument('--resample', type=int, default=0,
                    help='if not zero, size of the uniform grid in x direction to resample onto. Resampling is performed via symmetric \
                        EMA smoothing (see the docstring for symmetric_ema). \
                        Default is zero (no resampling). Note that if average_group is True, resampling is necessary; in that case, default \
                        value is 512. (default: 0)')
parser.add_argument('--smooth_step', type=float, default=1.0,
                    help='when resampling (i.e. when resample > 0 or average_group is True), use this EMA decay parameter (in units of the new grid step). (default: 1.0)')
parser.add_argument('--plot_time', type=str2bool, default=False,
                    help='plot time figure (default: False)')

def plot(log_dir, style, title, xlabel, xlog, xlim, ylabel, legend_outside, average_group, shaded_std, shaded_err, 
        resample, smooth_step, show, xy_fn=default_xy_fn, split_fn=lambda _: ''):
    results = pu.load_results(log_dir, enable_monitor=True, enable_progress=False, verbose=False)
    pu.plot_results(results, style=style, title=title, xlabel=xlabel, ylabel=ylabel, legend_outside=legend_outside,
            average_group=average_group, shaded_std=shaded_std, shaded_err=shaded_err, 
            resample=resample, smooth_step=smooth_step, xy_fn=xy_fn, split_fn=split_fn, )
    plt.savefig(log_dir + 'figure', dpi=400, bbox_inches='tight')
    if show:
        if xlog:
            plt.xscale('log')
        if xlim is not None:
            plt.xlim((0, xlim))
        ## get current axis
        ax = plt.gca()
        if xy_fn == time_xy_fn:
            ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
            ax.xaxis.set_major_formatter(ticker.FormatStrFormatter("%dh"))
        elif xy_fn == default_xy_fn:
            ax.xaxis.set_major_formatter(ticker.EngFormatter())
        plt.show()

if __name__ == "__main__":
    args = parser.parse_args()
    
    xy_fn = default_xy_fn
    if args.plot_time:
        xy_fn = time_xy_fn
        if args.xlabel is None:
            args.xlabel = 'Training time'
    else:
        if args.xlabel is None:
            args.xlabel = 'Timesteps'

    if args.ylabel is None:
        args.ylabel = 'Episode Reward'

    plot(args.log_dir, args.style, args.title, args.xlabel, args.xlog, args.xlim, args.ylabel,
        args.legend_outside, args.average_group, args.shaded_std, args.shaded_err, 
        args.resample, args.smooth_step, True, xy_fn=xy_fn)