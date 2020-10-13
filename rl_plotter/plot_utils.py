#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'MICROYU'

import re
import matplotlib.pyplot as plt
import os.path as osp
import json
import os
import numpy as np
import pandas
from glob import glob

def load_csv_results(dir, filename="monitor"):
	import pandas
	monitor_files = (
		glob(osp.join(dir, f"*{filename}.csv"))) # get both csv
	if not monitor_files:
		print("no monitor files of the form found in " + dir)
	dfs = []
	headers = []
	for fname in monitor_files:
		with open(fname, 'rt') as fh:
			if fname.endswith('csv'):
				firstline = fh.readline()
				if not firstline:
					continue
				assert firstline[0] == '#'
				header = json.loads(firstline[1:])
				df = pandas.read_csv(fh, index_col=None)
				headers.append(header)
			else:
				assert 0, 'unreachable'
			df['t'] += header['t_start']
		dfs.append(df)
	df = pandas.concat(dfs)
	df.sort_values('t', inplace=True)
	df.reset_index(inplace=True)
	df['t'] -= min(header['t_start'] for header in headers)
	#df.headers = headers # HACK to preserve backwards compatibility
	return df

def load_results(root_dir_or_dirs="./", filename="monitor"):

	if isinstance(root_dir_or_dirs, str):
		rootdirs = [osp.expanduser(root_dir_or_dirs)]
	else:
		rootdirs = [osp.expanduser(d) for d in root_dir_or_dirs]
	allresults = []
	
	for rootdir in rootdirs:
		assert osp.exists(rootdir), "%s doesn't exist"%rootdir
		for dirname, dirs, files in os.walk(rootdir):
			result = {'dirname' : dirname, "data": None}

			file_re = re.compile(r'(\d+\.)?(\d+\.)?' + filename + r'\.csv')
			if any([f for f in files if file_re.match(f)]):
				result['data'] = pandas.DataFrame(load_csv_results(dirname, filename))

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
	ykey='r',
	xscale=1,
	smooth_radius=0,
	average_group=False,
	shaded_std=True,
	shaded_err=False,
	legend_outside=False,
):
	if style is not None: plt.style.use(style)
	plt.subplots(figsize=(fig_length , fig_width))

	if group_fn is None: group_fn = lambda _ : ''
	groups = list(set(group_fn(result) for result in allresults))
	groups_results = {}

	groups.sort() # very important, determine the corresponding color of result

	for result in allresults:
		group = group_fn(result)
		if group not in groups_results:
			group_info = {'num': 0, 'legend': None, 'x': [], 'y': []}
			groups_results[group] = group_info
		current_group = groups_results[group]
		current_group['num'] += 1

		if xkey == 'l':
			x, y = np.cumsum(result['data'][xkey]), smooth(result['data'][ykey], radius=smooth_radius)
		elif xkey == 't':
			x, y = result['data'][xkey] / xscale, smooth(result['data'][ykey], radius=smooth_radius)
		else:
			x, y = result['data'][xkey], smooth(result['data'][ykey], radius=smooth_radius)

		if x is None: x = np.arange(len(y))
		x, y = map(np.asarray, (x, y))
		if average_group:
			current_group['x'].append(x)
			current_group['y'].append(y)
		else:
			legend, = plt.plot(x, y, color=COLORS[groups.index(group) % len(COLORS)])
			current_group['legend'] = legend

	if average_group:
		for group in sorted(groups):
			current_group = groups_results[group]
			color = COLORS[groups.index(group) % len(COLORS)]

			xlens = [len(x) for x in current_group['x']]
			min_xlen = min(xlens)
			index_min_xlen = xlens.index(min_xlen)

			x = current_group['x'][index_min_xlen]
			ys = [y[:min_xlen] for y in current_group['y']]
			ymean = np.mean(ys, axis=0)
			ystd = np.std(ys, axis=0)
			ystderr = ystd / np.sqrt(len(ys))

			legend, = plt.plot(x, ymean, color=color)
			current_group['legend'] = legend
			if shaded_err:
				plt.fill_between(x, ymean - ystderr, ymean + ystderr, color=color, alpha=.4)
			if shaded_std:
				plt.fill_between(x, ymean - ystd,    ymean + ystd,    color=color, alpha=.2)

	# add legend
	# https://matplotlib.org/users/legend_guide.html
	if any(groups_results.keys()):
		plt.legend(
			[groups_results[key]['legend'] for key in groups_results.keys()],
			['%s (%i)'%(key, groups_results[key]['num']) for key in groups_results.keys()] if average_group else groups_results.keys(),
			loc=2 if legend_outside else None,
			bbox_to_anchor=(1,1) if legend_outside else None)
	# add title
	plt.title(title)
	# add xlabels
	if xlabel is not None: plt.xlabel(xlabel)
	if ylabel is not None: plt.ylabel(ylabel)


if __name__ == "__main__":
	allresults = load_results("./logs", filename="evaluator")
	for result in allresults:
		print(result["dirname"])
	plot_results(allresults, average_group=False, smooth_radius=0)
	#plt.savefig('figure', dpi=400)