# !!! WORK IN PROGRESS !!!

![neater](figures/neater.png)

# NEATer - a faster NEAT implementation

**NEATer** is a neater implementation of neat-python, **focused on speed and ease of use**. The genectic crossovers and mutations are entirely written in C++ to increase computation speed. NEATer provides a convienent Python interface and is fully compatible with **OpenAI** environments.

**Installation:**

```shell
pip install git+https://github.com/ju-leon/NEATer.git
```

**Quick and simple setup:**

```python
import neat
from neat.network_pool import NeatOptimizer
import gym

env = gym.make('CartPole-v1')
st = Neat(population_size=300)
opt = NeatOptimizer(env, 4, 2, st)

opt.solve(max_generations=10,
          epoch_len=800,
          discrete=True,
          render=False)
```

