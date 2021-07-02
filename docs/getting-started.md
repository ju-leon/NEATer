# Quick Start

In this example, we will solve the CartPole environment from OpenAI.

## Installation

To install the most recent release from PyPI, you should run the command (as root or using sudo as necessary):

````
pip install neater
````

## Evolving
Now we're ready to evolve some networks.
In this example, we'll use the CartPole Environment from OpenAI Gym.

The goal is to balance a pole on a cart by moving the cart left and right.

```python
import gym
import tensorflow as tf
from neater import Agent, Neat

# Specify the environment you want to solve
env = gym.make('CartPole-v1')

# Use the NEAT algorithm with ReLU as activation function
strategy = Neat(population_size=50,
                activation=tf.nn.relu)

# Create an agent with input size of 4, output size of 2
agent = Agent(env, strategy, 4, 2)

# Solve the environment
agent.solve(max_generations=8,
            epoch_len=800,
            discrete=True,
            render=False)

# Have a look what the best genome so far looks like
strategy.plot("cartpole-graph.png")
```

And that's it. The first network is being evolved.

Now we can check on the models performance by applying the model to our environment:

```python
import numpy as np

observation = env.reset()

while True:
    env.render()
    pred = agent.predict(observation)
    
    # This environment only accepts a single discrete value as input
    pred = np.argmax(pred)

    observation, reward, done, info = env.step(pred)
    reward_sum += reward

    # print(reward_sum)
    if done:
        break

env.close()
```

## Saving & Export

Now the model can be saved to be used again at a later point:

```python
# Saving
strategy.save("cartpole.neat")

# Loading
strategy = Neat.load("cartpole.neat", env)
agent = Agent(env, strategy, 4, 2)
```

If you want to deploy your model, you can export it to tensorflow keras:

```
model = strategy.to_keras()
model.summary()
```
## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
