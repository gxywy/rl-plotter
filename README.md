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

## Usage

Add our logger in your code of evaluation

```python
from rl_plotter.logger import Logger
logger = Logger(exp_name="your_exp_name", env_name, seed)
····
logger.update(score=evaluation_score_list, total_steps=current_training_steps)
```

or you can use [OpenAI-baseline](https://github.com/openai/baselines) bench.Monitor:

```python
env = logger.monitor_env(env)
```

if you want to track other variables:

```python
custom_logger=logger.new_custom_logger(filename, fieldnames=["variable 1", "variable 2", ..., "variable n"])
custom_logger.update(fieldvalues=variable_value_list, total_steps=current_training_steps)
```



After the training or when you are training your agent, you can plot the learning curves in this way:

- switch to log directory (default: ./)

- run command to plot:

```
rl_plotter --save --show
```



more general commands in practice:

```
rl_plotter --save --show --avg_group --shaded_std
rl_plotter --save --show --avg_group --shaded_std --time
rl_plotter --save --show --avg_group --shaded_std --shaded_err
```



for help:

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
--ylabel              matplotlib figure ylabel
--smooth              smooth radius of y axis (default: 10)
--resample            if not zero, size of the uniform grid in x direction
                      to resample onto. Resampling is performed via
                      symmetric EMA smoothing (see the docstring for
                      symmetric_ema). Default is zero (no resampling). Note
                      that if average_group is True, resampling is
                      necessary; in that case, default value is 512.
                      (default: 512)
--smooth_step         when resampling (i.e. when resample > 0 or
					  average_group is True), use this EMA decay parameter
                      (in units of the new grid step). See docstrings for
                      decay_steps in symmetric_ema or one_sided_ema functions. 
                      (default: 1.0)
--avg_group           average the curves in the same group and plot the mean
--shaded_std          shaded region corresponding to standard deviation of the group
--shaded_err          shaded region corresponding to error in mean estimate of the group
--legend_loc          location of legend
--legend_outside      place the legend outside of the figure
--no_legend_group_num don't show num of group in legend
--time                enable this will set x_key to t, and activate parameters about time
--time_unit           parameters about time, x axis time unit (default: h)
--time_interval       parameters about time, x axis time interval (default: 1)
--xformat             x-axis format
--xlim                x-axis limitation (default: None)
--log_dir             log dir (default: ./)
--filter              filter of dirname
--filename            csv filename
--show                show figure
--save                save figure
--dpi                 figure dpi (default: 400)
```



finally, the learning curves looks like this:

<div align="center"><img width="400" height="400" src="https://github.com/gxywy/rl-plotter/blob/master/imgs/figure_1.png?raw=true"/></div>


## Features

- [x] custom logger, style, key, label, interval, and so on ...
- [x] filter of directory name
- [x] multi-experiment plotter
- [x] x-axis formatter features
- [x] compatible with [OpenAI-baseline](https://github.com/openai/baselines) monitor data style
- [x] corresponding color for specific experiment

## Citing the Project

To cite this repository in publications:

```
@misc{rl-plotter,
  author = {Xiaoyu Gong},
  title = {RL-plotter: A plotter for reinforcement learning},
  year = {2020},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/gxywy/rl-plotter}},
}
```

