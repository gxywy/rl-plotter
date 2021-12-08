# rl-plotter

![PyPI](https://img.shields.io/pypi/v/rl_plotter?style=flat-square) ![GitHub](https://img.shields.io/github/license/gxywy/rl-plotter?style=flat-square) ![GitHub last commit](https://img.shields.io/github/last-commit/gxywy/rl-plotter?style=flat-square)

[README](README.md) | [中文文档](README_zh.md)

`rl-plotter`是一个可以轻松绘制强化学习算法训练曲线或其它变量的小工具

## 安装

通过pip安装：

```
pip install rl_plotter
```

从源安装：

```
python setup.py install
```

## 用法

**1. 添加基本记录工具**

将我们的记录工具添加到强化学习算法的评估部分 (推荐)

```python
from rl_plotter.logger import Logger
logger = Logger(exp_name="your_exp_name", env_name, seed, locals())
····
logger.update(score=评估得分(list), total_steps=当前训练步数)
```

或者使用 [OpenAI-spinningup](https://github.com/openai/spinningup) 内置的记录工具

也可以使用 [OpenAI-baseline](https://github.com/openai/baselines) bench.Monitor (不推荐)

```python
env = logger.monitor_env(env)
```

**2. 记录其它变量(可选)**

如果你需要记录其它变量，你可以使用自定义logger：

```python
custom_logger=logger.new_custom_logger(filename, fieldnames=["变量 1", "变量 2", ..., "变量 n"])
custom_logger.update(fieldvalues=变量值(list), total_steps=当前训练步数)
```

**3. 绘制结果**

在进行训练的过程中或者训练结束后，你都可以使用下面的方式轻松绘制训练曲线：

- 切换到log目录或多个log的上级目录（默认为当前目录）

- 运行绘制命令：

```
rl_plotter --save --show
```

你也可以使用seaborn内核的绘图工具，获得与[OpenAI-spinningup](https://github.com/openai/spinningup)相同的绘制效果

```
rl_plotter_spinup --save --show
```

## 例子

**1. 常用命令**

```
rl_plotter --save --show --filter HalfCheetah
rl_plotter --save --show --filter Ant --avg_group --shaded_std
rl_plotter --save --show --filter Swimmer --avg_group --shaded_std --shaded_err
rl_plotter --save --show --filter Walker2d --filename progress.txt --xkey TotalEnvInteracts --ykey AverageEpRet
```

**2. 实用例子**

```
rl_plotter --show --save --avg_group --shaded_err --shaded_std
```
<div align="center"><img width="400" height="300" src="https://github.com/gxywy/rl-plotter/blob/master/imgs/figure_1.png?raw=true"/></div>

```
rl_plotter --show --save --avg_group --shaded_err --shaded_std --filename q --filters Walker HalfCheetah --ykey bias real_q --yduel --style default --smooth 0
```
<div align="center"><img width="400" height="300" src="https://github.com/gxywy/rl-plotter/blob/master/imgs/figure_2.png?raw=true"/></div>



**3. 更具体的用法**

你可以使用`help`命令查看所有可以调整与自定义的参数

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

## 特性

- [x] 自定义记录，绘图样式，坐标轴，x轴数据格式等...
- [x] 根据目录与文件名筛选绘图数据
- [x] 多个实验绘制在同一张图中，并自动分组
- [x] 多种绘图内核(第一种为原生matplotlib绘制，第二种为seaborn绘制)
- [x] 兼容 [OpenAI-baseline](https://github.com/openai/baselines) 和[OpenAI-spinningup](https://github.com/openai/spinningup)记录的数据，可以直接绘制曲线
- [x] 可以为每个实验可以设置对应的颜色
- [x] 绘制自定义数据，支持双y轴绘制

## 引用

如果您使用本工具用于您的研究工作，请在相关的论文或出版物中按下方的格式引用：

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

## 致谢

本项目的部分组件参考了[baselines/plot_util.py](https://github.com/openai/baselines/blob/master/baselines/common/plot_util.py)与[spinningup/plot.py](https://github.com/openai/spinningup/blob/master/spinup/utils/plot.py)