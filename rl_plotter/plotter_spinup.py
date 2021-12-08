#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'MICROYU'

import argparse
import matplotlib.pyplot as plt
from rl_plotter import plot_utils as pu


def main():
	parser = argparse.ArgumentParser(description='rl-plotter_spinup')
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
	parser.add_argument('--fig_length', type=int, default=6, 
						help='matplotlib figure length (default: 6)')
	parser.add_argument('--fig_width', type=int, default=6, 
						help='matplotlib figure width (default: 6)')

	parser.add_argument('--title', default=None,
						help='matplotlib figure title (default: None)')
	parser.add_argument('--xlabel', default=None,
						help='matplotlib figure xlabel')
	parser.add_argument('--ylabel', default=None,
						help='matplotlib figure ylabel')
	parser.add_argument('--xkey', default='total_steps',
						help='x-axis key in csv file (default: l)')
	parser.add_argument('--ykey', default=['mean_score'], nargs='+',
						help='y-axis key in csv file (support multi) (default: r)')
	parser.add_argument('--smooth', type=int, default=1,
						help='smooth radius of y axis (default: 1)')
	parser.add_argument('--xlim', type=int, default=None,
						help='x-axis limitation (default: None)')
	
	parser.add_argument('--legend_loc', type=int, default=0,
						help='location of legend')
	parser.add_argument('--legend_outside', action='store_true',
						help='place the legend outside of the figure')
	parser.add_argument('--borderpad', type=float, default=0.5,
						help='borderpad of legend (default: 0.5)')
	parser.add_argument('--labelspacing', type=float, default=0.5,
						help='labelspacing of legend (default: 0.5)')
	parser.add_argument('--font_scale', type=float, default=1,
						help='font_scale of seaborn (default: 1)')
	args = parser.parse_args()
	
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
	datas = []
	for result in allresults:
		result['data'].insert(len(result['data'].columns),'Condition1', pu.default_split_fn(result))
		datas.append(result['data'])
	for value in args.ykey:
		plt.figure()
		pu.plot_data(data=datas, xaxis=args.xkey, value=value, smooth=args.smooth, 
			legend_outside=args.legend_outside,
			legend_loc=args.legend_loc,
			legend_borderpad=args.borderpad,
			legend_labelspacing=args.labelspacing,
			font_scale=args.font_scale)
	plt.title(args.title)
	plt.xlabel(args.xlabel)
	plt.ylabel(args.ylabel)
	fig = plt.gcf()
	fig.set_size_inches((args.fig_length, args.fig_width), forward=False)

	if args.xlim is not None:
		plt.xlim((0, args.xlim))

	if args.save:
		plt.savefig(args.log_dir + 'figure', dpi=args.dpi, bbox_inches='tight')
	if args.show:
		plt.show()


if __name__ == "__main__":
	main()