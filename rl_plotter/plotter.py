#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'MICROYU'

import argparse
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from rl_plotter import plot_utils as pu


def main():
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
	parser.add_argument('--xkey', default='total_steps',
						help='x-axis key in csv file (default: l)')
	parser.add_argument('--ykey', default=['mean_score'], nargs='+',
						help='y-axis key in csv file (support multi) (default: r)')
	parser.add_argument('--yduel', action='store_true',
						help='=duel y axis (use if has two ykeys)')
	parser.add_argument('--ylabel', default=None,
						help='matplotlib figure ylabel')
	parser.add_argument('--smooth', type=int, default=5,
					help='smooth radius of y axis (default: 5)')
	parser.add_argument('--resample', type=int, default=512,
						help='if not zero, size of the uniform grid in x direction to resample onto. Resampling is performed via symmetric EMA smoothing (see the docstring for symmetric_ema). Default is zero (no resampling). Note that if average_group is True, resampling is necessary; in that case, default value is 512. (default: 512)')
	parser.add_argument('--smooth_step', type=float, default=1.0,
						help='when resampling (i.e. when resample > 0 or average_group is True), use this EMA decay parameter (in units of the new grid step). See docstrings for decay_steps in symmetric_ema or one_sided_ema functions.')
	parser.add_argument('--avg_group', action='store_true',
						help='average the curves in the same group and plot the mean.')
	parser.add_argument('--shaded_std', action='store_true',
						help='shaded region corresponding to standard deviation of the group')
	parser.add_argument('--shaded_err', action='store_true',
						help='shaded region corresponding to error in mean estimate')
	parser.add_argument('--legend_loc', type=int, default=0,
						help='location of legend')
	parser.add_argument('--legend_outside', action='store_true',
						help='place the legend outside of the figure')
	parser.add_argument('--borderpad', type=float, default=0.5,
						help='borderpad of legend (default: 0.5)')
	parser.add_argument('--labelspacing', type=float, default=0.5,
						help='labelspacing of legend (default: 0.5)')
	parser.add_argument('--no_legend_group_num', action='store_true',
						help="don't show num of group in legend")
	
	parser.add_argument('--time', action='store_true',
						help='enable this will activate parameters about time')
	parser.add_argument('--time_unit', default='h',
						help='parameters about time, x axis time unit (default: h)')
	parser.add_argument('--time_interval', type=float, default=1,
						help='parameters about time, x axis time interval (default: 1)')

	parser.add_argument('--xformat', default='',
						help='x-axis format')
	parser.add_argument('--xlim', type=int, default=None,
						help='x-axis limitation (default: None)')
	
	parser.add_argument('--log_dir', default='./',
						help='log dir (default: ./)')
	parser.add_argument('--filters', default=[''], nargs='+',
						help='filters of dirname')
	parser.add_argument('--filename', default='evaluator.csv',
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

	if '.' not in args.filename:
		args.filename = args.filename + '.csv'
	
	# OpenAI baseline's monitor
	if args.filename == 'monitor.csv':
		args.xkey = 'l'
		args.ykey = ['r']
	
	# OpenAI spinup's progress
	if args.filename == 'progress.txt' or args.filename == 'progress.csv':
		args.xkey = 'TotalEnvInteracts'
		if len(args.ykey) == 1:
			args.ykey = ['AverageTestEpRet']
	
	# rl-plotter's evaluator
	if args.filename == 'evaluator.csv':
		args.xkey = 'total_steps'
		if len(args.ykey) == 1:
			args.ykey = ['mean_score']

	if args.save is False:
		args.show = True

	allresults = pu.load_results(args.log_dir, filename=args.filename, filters=args.filters)
	pu.plot_results(allresults,
		fig_length=args.fig_length,
		fig_width=args.fig_width,
		style=args.style,
		title=args.title,
		xlabel=args.xlabel,
		ylabel=args.ylabel,
		xkey=args.xkey,
		ykey=args.ykey,
		yduel=args.yduel,
		xscale=xscale,
		smooth_radius=args.smooth,
		resample=args.resample,
		smooth_step=args.smooth_step,
		average_group=args.avg_group,
		shaded_std=args.shaded_std,
		shaded_err=args.shaded_err,
		legend_outside=args.legend_outside,
		legend_loc=args.legend_loc,
		legend_group_num=not args.no_legend_group_num,
		legend_borderpad=args.borderpad,
		legend_labelspacing=args.labelspacing,
		filename=args.filename)

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
			#ax.xaxis.set_major_formatter(mticker.LogFormatterSciNotation())
			plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0), useMathText=True)
		else:
			plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0), useMathText=False)

	if args.xlim is not None:
		plt.xlim((0, args.xlim))

	if args.save:
		plt.savefig(args.log_dir + 'figure', dpi=args.dpi, bbox_inches='tight')
	if args.show:
		plt.show()
	
	


if __name__ == "__main__":
	main()