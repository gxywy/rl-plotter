# rl-plotter

![PyPI](https://img.shields.io/pypi/v/rl_plotter?style=flat-square) ![GitHub](https://img.shields.io/github/license/gxywy/rl-plotter?style=flat-square) ![GitHub last commit](https://img.shields.io/github/last-commit/gxywy/rl-plotter?style=flat-square)

[README](README.md) | [中文文档](README_zh.md)

This is a simple tool which can plot learning curves easily for reinforcement learning (RL)

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

**1. add basic logger**

Add our logger in your code of evaluation (Recommend)

```python
from rl_plotter.logger import Logger
logger = Logger(exp_name="your_exp_name", env_name, seed, locals())
····
logger.update(score=evaluation_score_list, total_steps=current_training_steps)
```

or just use [OpenAI-spinningup](https://github.com/openai/spinningup) to log (Support)

or you can use [OpenAI-baseline](https://github.com/openai/baselines) bench.Monitor (Not Recommend)

```python
env = logger.monitor_env(env)
```

**2. track other variables (Optional)**

if you want to track other variables, you can use our custom_logger:

```python
custom_logger=logger.new_custom_logger(filename, fieldnames=["variable 1", "variable 2", ..., "variable n"])
custom_logger.update(fieldvalues=variable_value_list, total_steps=current_training_steps)
```

**3. plot the results**

After the training or when you are training your agent, you can plot the learning curves in this way:

- switch to log directory or multi log’s parent directory (default: ./)

- run command to plot:

```
rl_plotter --save --show
```

## Example

**1. commonly used commands**

```
rl_plotter --save --show --filter HalfCheetah
rl_plotter --save --show --filter Ant --avg_group --shaded_std
rl_plotter --save --show --filter Swimmer --avg_group --shaded_std --shaded_err
rl_plotter --save --show --filter Walker2d --filename progress.txt --xkey TotalEnvInteracts --ykey AverageEpRet
```

**2. practical examples**

```
rl_plotter --show --save --avg_group --shaded_err --shaded_std
```
<div align="center"><img width="400" height="300" src="https://github.com/gxywy/rl-plotter/blob/master/imgs/figure_1.png?raw=true"/></div>

```
rl_plotter --show --save --avg_group --shaded_err --shaded_std --filename q --filters Walker HalfCheetah --ykey bias real_q --yduel --style default --smooth 0
```
<div align="center"><img width="400" height="300" src="https://github.com/gxywy/rl-plotter/blob/master/imgs/figure_2.png?raw=true"/></div>



**3. more specific usage**

you can find all parameters which can custom the style of your curves using `help`

```
rl_plotter --help
```

```
optional arguments:
-h, --help            show this help message and exit
--fig_length          matplotlib figure length (default: 8)
--fig_width           matplotlib figure width (default: 6)
--style               matplotlib figure style (default: seaborn)
--title               matplotlib figure title (default: None)
--xlabel              matplotlib figure xlabel
--xkey                x-axis key in csv file (default: l)
--ykey                y-axis key in csv file (support multi) (default: r)
--yduel               duel y axis (use if has two ykeys)
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
--borderpad           borderpad of legend (default: 0.5)
--labelspacing        labelspacing of legend (default: 0.5)
--no_legend_group_num don't show num of group in legend
--time                enable this will activate parameters about time
--time_unit           parameters about time, x axis time unit (default: h)
--time_interval       parameters about time, x axis time interval (default: 1)
--xformat             x-axis format
--xlim                x-axis limitation (default: None)
--log_dir             log dir (default: ./)
--filters             filter of dirname
--filename            csv filename
--show                show figure
--save                save figure
--dpi                 figure dpi (default: 400)
```

## Features

- [x] custom logger, style, key, label, x-axis formatter, and so on ...
- [x] filter of directory name
- [x] multi-experiment plotter
- [x] compatible with [OpenAI-baseline](https://github.com/openai/baselines) monitor and [OpenAI-spinningup](https://github.com/openai/spinningup)
- [x] corresponding color for specific experiment
- [x] multi y key & duel y legend

## Citing the Project

If using this repository for your research or publication, please cite:

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

## Acknowledgment

The core of this tools is inspired by [baselines/plot_util.py](https://github.com/openai/baselines/blob/master/baselines/common/plot_util.py)

