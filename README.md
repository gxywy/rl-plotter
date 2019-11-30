# rl-plotter

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
<img src="https://github.com/gxywy/rl-plotter/blob/master/imgs/screenshot_1.png?raw=true"/>

The learning curves looks like this:

<img src="https://github.com/gxywy/rl-plotter/blob/master/imgs/figure_1.png?raw=true" style="zoom: 33%;" />

<img src="https://github.com/gxywy/rl-plotter/blob/master/imgs/figure_2.png?raw=true" style="zoom: 33%;" />

## To Do

- [x] reinforcement learning plot tools
- [x] timestamp features
- [x] history experiment data plot tools
- [ ] ~~basic data plot tools（including ML-Loss plot）~~
- [ ] ~~dynamic plot tools~~