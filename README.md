# rl-plotter

![PyPI](https://img.shields.io/pypi/v/rl_plotter?style=flat-square) ![GitHub](https://img.shields.io/github/license/gxywy/rl-plotter?style=flat-square) ![GitHub last commit](https://img.shields.io/github/last-commit/gxywy/rl-plotter?style=flat-square)

 This is a simple tool which can plot learning curves easily for reinforcement learning (RL).

## Installation

from PIP

```
pip install rl_plotter
```

from source

```
python setup.py install
```

## Examples

First, add our logger (compatible with [OpenAI-baseline](https://github.com/openai/baselines)) in your code

or just use [OpenAI-baseline](https://github.com/openai/baselines) bench.Monitor (recommended):

```python
from baselines import bench
env = bench.Monitor(env, log_dir)
```

After the training or when you are training your agent, you can plot the learning curves in this way:

```
rl_plotter --save --show
```
for help use:
```
rl_plotter --help
```

and you can find  parameters to custom the style of your curves.

```
optional arguments:
-h, --help            show this help message and exit
--fig_length          matplotlib figure length (default: 6)
--fig_width           matplotlib figure width (default: 6)
--style               matplotlib figure style (default: seaborn)
--title               matplotlib figure title (default: None)
--xlabel              matplotlib figure xlabel
--xkey                x-axis key in csv file (default: l)
--ykey                y-axis key in csv file (default: r)
--smooth              smooth radius of y axis (default: 1)
--ylabel              matplotlib figure ylabel
--avg_group           average the curves in the same group and plot the mean
--shaded_std          shaded region corresponding to standard deviation of the group
--shaded_err          shaded region corresponding to error in mean estimate of the group
--legend_outside      place the legend outside of the figure
--time                enable this will set x_key to t, and activate parameters about time
--time_unit           parameters about time, x axis time unit (default: h)
--time_interval       parameters about time, x axis time interval (default: 1)
--xformat             x-axis format
--xlim                x-axis limitation (default: None)
--log_dir             log dir (default: ./)
--filename            csv filename
--show                show figure
--save                save figure
--dpi                 figure dpi (default: 400)
```

finally, the learning curves looks like this:
<div align="center"><img width="400" height="400" src="https://github.com/gxywy/rl-plotter/blob/master/imgs/figure_1.png?raw=true"/></div>

## Features
- [x] custom logger, style, key, label, interval, and so on ...
- [x] multi-experiment plotter
- [x] x-axis formatter features
- [x] compatible with [OpenAI-baseline](https://github.com/openai/baselines) monitor data style