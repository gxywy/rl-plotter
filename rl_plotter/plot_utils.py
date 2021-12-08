#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'MICROYU'

from datetime import date
import re
import matplotlib.pyplot as plt
import os.path as osp
import json
import os
import numpy as np
import pandas
from glob import glob

COLORS = ([
	# deepmind style
	'#0072B2',
	'#009E73',
	'#D55E00',
	'#CC79A7',
	'#F0E442',
	# built-in color
	'blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'purple', 'pink',
	'brown', 'orange', 'teal',  'lightblue', 'lime', 'lavender', 'turquoise',
	'darkgreen', 'tan', 'salmon', 'gold',  'darkred', 'darkblue',
	# personal color
	'#313695',  # DARK BLUE
	'#74add1',  # LIGHT BLUE
	'#4daf4a',  # GREEN
	'#f46d43',  # ORANGE
	'#d73027',  # RED
	'#984ea3',  # PURPLE
	'#f781bf',  # PINK
	'#ffc832',  # YELLOW
	'#000000',  # BLACK
])

def one_sided_ema(xolds, yolds, low=None, high=None, n=512, decay_steps=1., low_counts_threshold=1e-8):
	'''
	perform one-sided (causal) EMA (exponential moving average)
	smoothing and resampling to an even grid with n points.
	Does not do extrapolation, so we assume
	xolds[0] <= low && high <= xolds[-1]
	Arguments:
	xolds: array or list  - x values of data. Needs to be sorted in ascending order
	yolds: array of list  - y values of data. Has to have the same length as xolds
	low: float            - min value of the new x grid. By default equals to xolds[0]
	high: float           - max value of the new x grid. By default equals to xolds[-1]
	n: int                - number of points in new x grid
	decay_steps: float    - EMA decay factor, expressed in new x grid steps.
	low_counts_threshold: float or int
						  - y values with counts less than this value will be set to NaN
	Returns:
		tuple sum_ys, count_ys where
			xs        - array with new x grid
			ys        - array of EMA of y at each point of the new x grid
			count_ys  - array of EMA of y counts at each point of the new x grid
	'''

	low = xolds[0] if low is None else low
	high = xolds[-1] if high is None else high

	assert xolds[0] <= low, 'low = {} < xolds[0] = {} - extrapolation not permitted!'.format(low, xolds[0])
	assert xolds[-1] >= high, 'high = {} > xolds[-1] = {}  - extrapolation not permitted!'.format(high, xolds[-1])
	assert len(xolds) == len(yolds), 'length of xolds ({}) and yolds ({}) do not match!'.format(len(xolds), len(yolds))


	xolds = xolds.astype('float64')
	yolds = yolds.astype('float64')

	luoi = 0 # last unused old index
	sum_y = 0.
	count_y = 0.
	xnews = np.linspace(low, high, n)
	decay_period = (high - low) / (n - 1) * decay_steps
	interstep_decay = np.exp(- 1. / decay_steps)
	sum_ys = np.zeros_like(xnews)
	count_ys = np.zeros_like(xnews)
	for i in range(n):
		xnew = xnews[i]
		sum_y *= interstep_decay
		count_y *= interstep_decay
		while True:
			if luoi >= len(xolds):
				break
			xold = xolds[luoi]
			if xold <= xnew:
				decay = np.exp(- (xnew - xold) / decay_period)
				sum_y += decay * yolds[luoi]
				count_y += decay
				luoi += 1
			else:
				break
		sum_ys[i] = sum_y
		count_ys[i] = count_y

	ys = sum_ys / count_ys
	ys[count_ys < low_counts_threshold] = np.nan

	return xnews, ys, count_ys

def symmetric_ema(xolds, yolds, low=None, high=None, n=512, decay_steps=1., low_counts_threshold=1e-8):
	'''
	perform symmetric EMA (exponential moving average)
	smoothing and resampling to an even grid with n points.
	Does not do extrapolation, so we assume
	xolds[0] <= low && high <= xolds[-1]
	Arguments:
	xolds: array or list  - x values of data. Needs to be sorted in ascending order
	yolds: array of list  - y values of data. Has to have the same length as xolds
	low: float            - min value of the new x grid. By default equals to xolds[0]
	high: float           - max value of the new x grid. By default equals to xolds[-1]
	n: int                - number of points in new x grid
	decay_steps: float    - EMA decay factor, expressed in new x grid steps.
	low_counts_threshold: float or int
						  - y values with counts less than this value will be set to NaN
	Returns:
		tuple sum_ys, count_ys where
			xs        - array with new x grid
			ys        - array of EMA of y at each point of the new x grid
			count_ys  - array of EMA of y counts at each point of the new x grid
	'''
	xs, ys1, count_ys1 = one_sided_ema(xolds, yolds, low, high, n, decay_steps, low_counts_threshold=0)
	_,  ys2, count_ys2 = one_sided_ema(-xolds[::-1], yolds[::-1], -high, -low, n, decay_steps, low_counts_threshold=0)
	ys2 = ys2[::-1]
	count_ys2 = count_ys2[::-1]
	count_ys = count_ys1 + count_ys2
	ys = (ys1 * count_ys1 + ys2 * count_ys2) / count_ys
	ys[count_ys < low_counts_threshold] = np.nan
	return xs, ys, count_ys

def load_csv_results(dir, filename="monitor.csv"):
	import pandas
	monitor_files = (
		glob(osp.join(dir, f"*{filename}")))
	if not monitor_files:
		print("no files of the form found in " + dir)
	dfs = []
	headers = []
	for fname in monitor_files:
		with open(fname, 'rt') as fh:
			firstline = fh.readline()
			if not firstline:
				continue
			if filename == 'monitor.csv' or firstline[0] == '#':
				assert firstline[0] == '#'
				header = json.loads(firstline[1:])
				headers.append(header)
				df = pandas.read_csv(fh, index_col=None, sep=",|\t", engine='python')
			else:
				fh.seek(0)
				df = pandas.read_csv(fh, index_col=None, sep=",|\t", engine='python')
			if filename=="monitor.csv":
				df['t'] += header['t_start']
		dfs.append(df)
	df = pandas.concat(dfs)
	if filename=="monitor.csv":
		df.sort_values('t', inplace=True)
	df.reset_index(inplace=True)
	if filename=="monitor.csv":
		df['t'] -= min(header['t_start'] for header in headers)
	#df.headers = headers # HACK to preserve backwards compatibility
	return df

def load_results(root_dir_or_dirs="./", filename="monitor.csv", filters=['']):

	if isinstance(root_dir_or_dirs, str):
		rootdirs = [osp.expanduser(root_dir_or_dirs)]
	else:
		rootdirs = [osp.expanduser(d) for d in root_dir_or_dirs]
	allresults = []
	
	for rootdir in rootdirs:
		assert osp.exists(rootdir), "%s doesn't exist"%rootdir
		for dirname, dirs, files in os.walk(rootdir):
			for filter in filters:
				if filter in dirname:
					result = {'dirname' : dirname, "data": None}

					file_re = re.compile(r'(\d+\.)?(\d+\.)?' + filename)
					if any([f for f in files if file_re.match(f)]):
						csv_result = load_csv_results(dirname, filename)
						if csv_result is not None:
							result['data'] = pandas.DataFrame(csv_result)

					if result['data'] is not None:
						allresults.append(result)
	return allresults


def smooth(y, radius, mode='two_sided', valid_only=False):
	'''
	Smooth signal y, where radius is determines the size of the window
	mode='twosided':
		average over the window [max(index - radius, 0), min(index + radius, len(y)-1)]
	mode='causal':
		average over the window [max(index - radius, 0), index]
	valid_only: put nan in entries where the full-sized window is not available
	'''
	assert mode in ('two_sided', 'causal')
	if len(y) < 2*radius+1:
		return np.ones_like(y) * y.mean()
	elif mode == 'two_sided':
		convkernel = np.ones(2 * radius+1)
		out = np.convolve(y, convkernel,mode='same') / np.convolve(np.ones_like(y), convkernel, mode='same')
		if valid_only:
			out[:radius] = out[-radius:] = np.nan
	elif mode == 'causal':
		convkernel = np.ones(radius)
		out = np.convolve(y, convkernel,mode='full') / np.convolve(np.ones_like(y), convkernel, mode='full')
		out = out[:-radius+1]
		if valid_only:
			out[:radius] = np.nan
	return out

def default_split_fn(r):
	# match name between slash and -<digits> at the end of the string
	# (slash in the beginning or -<digits> in the end or either may be missing)
	match = re.search(r'[^/-]+(?=(-\d+)?\Z)', r['dirname'])
	if match:
		return match.group(0)

def plot_results(
	allresults,
	group_fn=default_split_fn,
	fig_length=6,
	fig_width=6,
	style=None,
	title=None,
	xlabel=None,
	ylabel=None,
	xkey='l',
	ykey=['r'],
	yduel=False,
	xscale=1,
	smooth_radius=0,
	resample=0,
	smooth_step=1.0,
	average_group=False,
	shaded_std=True,
	shaded_err=False,
	legend_outside=False,
	legend_loc=0,
	legend_group_num=True,
	legend_borderpad=1.0,
	legend_labelspacing=1.0,
	filename="monitor.csv"
):
	default_samples = 512
	if average_group:
		resample = resample or default_samples

	if style is not None: plt.style.use(style)
	_, plt1 = plt.subplots(figsize=(fig_length , fig_width))

	if group_fn is None: group_fn = lambda _ : ''
	groups_raw = list(set(group_fn(result) for result in allresults))
	
	# handle n-ykey
	if len(ykey) > 1:
		groups = []
		for group in groups_raw:
			for key in ykey:
				groups.append(group + "_" + key)
	else:
		groups = groups_raw
		
	groups_results = {}
	groups.sort() # very important, determine the corresponding color of result

	# handle dual y
	if len(ykey) == 2 and yduel:
		plt2 = plt1.twinx()

	for result in allresults:
		group_raw = group_fn(result)
	
		for key in ykey: # handle n-ykey
			if len(ykey) > 1:
				group = group_raw + "_" + key
			else:
				group = group_raw

			if (ykey[0] in group or len(ykey) != 2) or not yduel: # handle dual y
				pltt = plt1
			else:
				pltt = plt2
			
			if group not in groups_results:
				group_info = {'num': 0, 'legend': None, 'x': [], 'y': [], 'ykey': key}
				groups_results[group] = group_info
			current_group = groups_results[group]
			current_group['num'] += 1
			
			if filename == 'monitor.csv' and xkey == 'l' :
				x, y = np.cumsum(result['data'][xkey]), smooth(result['data'][key], radius=smooth_radius)
			elif filename == 'monitor.csv' and xkey == 't':
				x, y = result['data'][xkey] / xscale, smooth(result['data'][key], radius=smooth_radius)
			else:
				x, y = result['data'][xkey], smooth(result['data'][key], radius=smooth_radius)

			if x is None: x = np.arange(len(y))
			x, y = map(np.asarray, (x, y))
			if average_group:
				current_group['x'].append(x)
				current_group['y'].append(y)
			else:
				if resample:
					x, y, counts = symmetric_ema(x, y, x[0], x[-1], resample, decay_steps=smooth_step)
					legend, = pltt.plot(x, y, color=COLORS[groups.index(group) % len(COLORS)])
					# handle dual y label
				if ylabel is not None:
					if yduel:
						pltt.set_ylabel(current_group['ykey'])
					else:
						pltt.set_ylabel(ylabel)
				current_group['legend'] = legend
			
	if average_group:
		for group in sorted(groups):
			current_group = groups_results[group]
			if not any(current_group):
				continue
			color = COLORS[groups.index(group) % len(COLORS)]
			origxs = [x for x in current_group['x']]
			minxlen = min(map(len, origxs))
			def allequal(qs):
				return all((q==qs[0]).all() for q in qs[1:])
			if resample:
					low  = max(x[0] for x in origxs)
					high = min(x[-1] for x in origxs)
					usex = np.linspace(low, high, resample)
					ys = []
					for (x, y) in zip(current_group['x'], current_group['y']):
						ys.append(symmetric_ema(x, y, low, high, resample, decay_steps=1.0)[1])
			else:
				assert allequal([x[:minxlen] for x in origxs]),\
					'If you want to average unevenly sampled data, set resample=<number of samples you want>'
				usex = origxs[0]
				ys = [xy[1][:minxlen] for xy in current_group]
			ymean = np.mean(ys, axis=0)
			ystd = np.std(ys, axis=0)
			ystderr = ystd / np.sqrt(len(ys))

			# handle dual y
			if (ykey[0] in group or len(ykey) != 2) or not yduel:
				pltt = plt1
			else:
				pltt = plt2
			legend, = pltt.plot(usex, ymean, color=color)
			# handle dual y label
			if ylabel is not None:
				if yduel:
					pltt.set_ylabel(current_group['ykey'])
				else:
					pltt.set_ylabel(ylabel)
			
			current_group['legend'] = legend
			if shaded_err:
				pltt.fill_between(usex, ymean - ystderr, ymean + ystderr, color=color, alpha=.4)
			if shaded_std:
				pltt.fill_between(usex, ymean - ystd,    ymean + ystd,    color=color, alpha=.2)

	# add legend
	# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html
	if any(groups_results.keys()):
		if legend_group_num:
			plt.legend(
					[groups_results[key]['legend'] for key in groups_results.keys()],
					['%s (%i)'%(key.replace('without', 'w/o').replace('_', '-'), groups_results[key]['num']) for key in groups_results.keys()] if average_group else groups_results.keys(),
					loc=9 if legend_outside else legend_loc, bbox_to_anchor = (0.5,-0.1) if legend_outside else (1,1) if legend_outside else None, borderpad=legend_borderpad, labelspacing=legend_labelspacing, ncol=len(groups_results.keys()) if legend_outside else 1)
		else:
			plt.legend(
					[groups_results[key]['legend'] for key in groups_results.keys()],
					['%s'%(key.replace('without', 'w/o').replace('_', '-')) for key in groups_results.keys()] if average_group else groups_results.keys(),
					loc=9 if legend_outside else legend_loc, bbox_to_anchor = (0.5,-0.1) if legend_outside else (1,1) if legend_outside else None, borderpad=legend_borderpad, labelspacing=legend_labelspacing, ncol=len(groups_results.keys()) if legend_outside else 1)
	# add title
	plt.title(title)
	# add xlabels
	if xlabel is not None: plt.xlabel(xlabel)


def plot_data(data, xaxis='total_steps', value="mean_score", condition="Condition1", smooth=1, 
        legend_outside=False,
        legend_loc=0,
        legend_borderpad=1.0,
        legend_labelspacing=1.0,
        font_scale=1.5,
        **kwargs):
    import seaborn as sns
    if smooth > 1:
        """
        smooth data with moving window average.
        that is,
            smoothed_y[t] = average(y[t-k], y[t-k+1], ..., y[t+k-1], y[t+k])
        where the "smooth" param is width of that window (2k+1)
        """
        y = np.ones(smooth)
        for datum in data:
            x = np.asarray(datum[value])
            z = np.ones(len(x))
            smoothed_x = np.convolve(x,y,'same') / np.convolve(z,y,'same')
            datum[value] = smoothed_x
    if isinstance(data, list):
        data = pandas.concat(data, ignore_index=True)
    
    data.sort_values(by='Condition1', axis=0)

    sns.set(style="darkgrid", font_scale=font_scale)
    sns.lineplot(data=data, x=xaxis, y=value, hue=condition, ci='sd', **kwargs)
    handles, labels = plt.gca().get_legend_handles_labels()

    plt.legend(
        handles[1:],
        ['%s'%(key.replace('without', 'w/o').replace('_', '-')) for key in labels[1:]],
        loc=9 if legend_outside else legend_loc, bbox_to_anchor = (0.5,-0.1) if legend_outside else (1,1) if legend_outside else None, borderpad=legend_borderpad, labelspacing=legend_labelspacing, ncol=len(labels)-1 if legend_outside else 1)

    xscale = np.max(np.asarray(data[xaxis])) > 5e3
    if xscale:
        # Just some formatting niceness: x-axis scale in scientific notation if max x is large
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

    plt.tight_layout(pad=0.5)


if __name__ == "__main__":
	# allresults = load_results("./logs", filename="evaluator.csv")
	# for result in allresults:
	# 	print(result["dirname"])
	# plot_results(allresults, average_group=False, smooth_radius=0)
	# plt.show()

    # allresults = load_results("./", filename="evaluator.csv")
    # datas = []
    # for result in allresults:
    #     result['data'].insert(len(result['data'].columns),'Condition1', default_split_fn(result))
    #     datas.append(result['data'])
    # plt.figure()
    # fig = plt.gcf()
    # fig.set_size_inches((16, 9), forward=False)

    # plot_data(data=datas)
    # plt.show()
    pass
    