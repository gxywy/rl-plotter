#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'MICROYU'

import argparse
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from rl_plotter import plot_utils as pu


if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='plotter')
	parser.add_argument('--fig_length', type=int, default=6, 
						help='matplotlib figure length (default: 6)')
	parser.add_argument('--fig_width', type=int, default=6, 
						help='matplotlib figure width (default: 6)')
	parser.add_argument('--style', default='seaborn',
						help='matplotlib figure style (default: seaborn)')
	parser.add_argument('--title', default=None,
						help='matplotlib figure title (default: None)')
	parser.add_argument('--xlabel', default=None,
						help='matplotlib figure xlabel')
	parser.add_argument('--xkey', default='l',
						help='x-axis key in csv file (default: l)')
	parser.add_argument('--ykey', default='r',
						help='y-axis key in csv file (default: r)')
	parser.add_argument('--smooth', type=int, default=0,
						help='smooth radius of y axis (default: 1)')
	parser.add_argument('--ylabel', default=None,
						help='matplotlib figure ylabel')
	parser.add_argument('--avg_group', action='store_true',
						help='average the curves in the same group and plot the mean.')
	parser.add_argument('--shaded_std', action='store_true',
						help='shaded region corresponding to standard deviation of the group')
	parser.add_argument('--shaded_err', action='store_true',
						help='shaded region corresponding to error in mean estimate')
	parser.add_argument('--legend_outside', action='store_true', default=False,
						help='place the legend outside of the figure')
	
	parser.add_argument('--time', action='store_true',
						help='enable this will set x_key to t, and activate parameters about time')
	parser.add_argument('--time_unit', default='h',
						help='parameters about time, x axis time unit (default: h)')
	parser.add_argument('--time_interval', type=float, default=1,
						help='parameters about time, x axis time interval (default: 1)')

	parser.add_argument('--xformat', default='eng',
						help='x-axis format')
	parser.add_argument('--xlim', type=int, default=None,
						help='x-axis limitation (default: None)')
	
	parser.add_argument('--log_dir', default='./logs/',
						help='log dir (default: ./logs/)')
	parser.add_argument('--filename', default='monitor',
						help='csv filename')
	parser.add_argument('--show', action='store_true',
						help='show figure')
	parser.add_argument('--save', action='store_true',
					help='save figure')
	parser.add_argument('--dpi', type=int, default=400,
						help='figure dpi (default: 400)')
	args = parser.parse_args()

	xscale = 1
	if args.time:
		if args.xlabel is None:
			args.xlabel = 'Training time'
		args.xkey = 't'
		if args.time_unit == 'h': 
			xscale = 60 * 60
			args.time_interval = 2
		elif args.time_unit == 'min': 
			xscale = 60
			args.time_interval = 20
	else:
		if args.xlabel is None:
			args.xlabel = 'Timesteps'
	
	if args.ylabel is None:
		args.ylabel = 'Episode Reward'

	allresults = pu.load_results(args.log_dir, filename=args.filename)
	pu.plot_results(allresults,
		fig_length=args.fig_length,
		fig_width=args.fig_width,
		style=args.style,
		title=args.title,
		xlabel=args.xlabel,
		ylabel=args.ylabel,
		xkey=args.xkey,
		ykey=args.ykey,
		xscale=xscale,
		smooth_radius=args.smooth,
		average_group=args.avg_group,
		shaded_std=args.shaded_std,
		shaded_err=args.shaded_err,
		legend_outside=args.legend_outside)

	ax = plt.gca() # get current axis
	if args.time:
		if args.time_unit == 'h' or args.time_unit == 'min':
			ax.xaxis.set_major_locator(mticker.MultipleLocator(args.time_interval))
		ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%d" + args.time_unit))
	else:
		if args.xformat == 'eng':
			ax.xaxis.set_major_formatter(mticker.EngFormatter())
		elif args.xformat == 'log':
			ax.xaxis.set_major_formatter(mticker.LogFormatter())
		elif args.xformat == 'sci':
			ax.xaxis.set_major_formatter(mticker.LogFormatterSciNotation())

	if args.xlim is not None:
		plt.xlim((0, args.xlim))
	
	if args.save:
		plt.savefig(args.log_dir + 'figure', dpi=args.dpi, bbox_inches='tight')
	if args.show:
		plt.show()