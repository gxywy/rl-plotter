# rl-plotter

![PyPI](https://img.shields.io/pypi/v/rl_plotter?style=flat-square) ![GitHub](https://img.shields.io/github/license/gxywy/rl-plotter?style=flat-square) ![GitHub last commit](https://img.shields.io/github/last-commit/gxywy/rl-plotter?style=flat-square)

 This is a simple tool which can plot learning curves easily for reinforcement learning.

## Installation

from PIP

```
pip install rl_plotter
```

from source

```
python3 setup.py install
```

## Examples

First, add a logger in your code (for example: DQN):

```python
from rl_plotter.logger import Logger

def train(name):
    dqn = DQN()
    logger = Logger(name, env_name='PongNoFrameskip-v4', use_tensorboard=False)

    while True:
        s = env.reset()
        while True:
            total_step = logger.add_step()
            a = dqn.select_action(s, EPSILON)
            s_, r, done, info = env.step(a)

            dqn.store_transition(s, a, r, s_)
            episode_reward += r
            
            if dqn.replay_memory.memory_counter > REPLAY_MEMORY_SIZE:
                loss = dqn.learn()
                logger.add_loss(loss.cpu().item())
            if done:
                break
            s = s_
        logger.add_episode()
        logger.add_reward(episode_reward, freq=10)
    logger.finish()
```

After the training or when you are training your agent, you can plot the learning curves in this way:

```
python -m rl_plotter.plotter
```
for help use:
```
python -m rl_plotter.plotter --help
```

The learning curves looks like this:
<div align="center"><img width="400" height="400" src="https://github.com/gxywy/rl-plotter/blob/master/imgs/figure_1.png?raw=true"/></div>
<div align="center"><img width="400" height="400" src="https://github.com/gxywy/rl-plotter/blob/master/imgs/figure_2.png?raw=true"/></div>
<div align="center"><img width="400" height="400" src="https://github.com/gxywy/rl-plotter/blob/master/imgs/figure_3.png?raw=true"/></div>
And you can custom the style of your curves by use parameter of `rl_plotter.plotter`or modifying`rl_plotter.plotter`

## Features
- [x] reinforcement learning plot tools
- [x] timestamp x axis features
- [x] history experiment data plot tools
- [x] x axis formatter features
- [x] multiprocessing algorithm x.monitor  logger
- [x] compatible with [OpenAI-baseline](https://github.com/openai/baselines) monitor data style
- [ ] compatible with [OpenAI-baseline](https://github.com/openai/baselines) progress data style
- [x] custom scalars logger (can be used to analyze any variable in training)
- [ ] ~~basic data plot tools（including ML-Loss plot）~~
- [ ] ~~dynamic plot tools~~