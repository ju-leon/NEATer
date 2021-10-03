# from torch.nn.modules import activation
from neater import Agent, Neat
import tensorflow as tf
import gym

import numpy as np
# from tqdm import tqdm
import timeit
import matplotlib.pyplot as plt


env = gym.make('Breakout-ram-v0')

print(env.observation_space)
print(env.action_space)

strategy = Neat(population_size=100,
                max_genetic_distance=5,
                p_mutate_connection=0.4,
                p_mutate_node=0.3,
                p_mutate_bias=0.01,
                p_mutate_weight_random=0.01,
                p_mutate_weight_shift=0.01,
                p_mutate_toggle_node=0.3,
                p_mutate_toggle_connection=0.3,
                p_mutation=0.5,
                activation=tf.nn.relu
                )

agent = Agent(env, strategy, 128, 4, discrete=True)

starttime = timeit.default_timer()
H = agent.solve(max_generations=5,  # 3
                epoch_len=300,
                increase_rate=10,
                stat_intervall=1,
                render=False)

print("Execution Time: ", timeit.default_timer() - starttime)

strategy.plot("graph.png")

#model = strategy.to_keras()

#model.summary()
#tf.keras.utils.plot_model(model, "mini_resnet.png", show_shapes=True)

# for layer in model.layers:
#    print(layer.get_config(), layer.get_weights())

strategy.save("test.neat")

# agent = Agent(env, strategy, 4, 2, discrete=True)

# agent.save("test.neat")

# agent.load("test.neat")

# print(net)
observation = env.reset()

print(observation)
print(observation.shape)

reward_sum = 0
while True:
    env.render()
    # pred_tf = np.array(model.predict(observation.reshape(1, -1))).flatten()
    pred_nt = np.array(agent.predict(observation))

    # print(pred_tf)
    # print(pred_nt)
    # print("---")
    # assert np.array_equal(pred_tf, pred_nt)

    pred = pred_nt
    pred = np.argmax(pred)

    observation, reward, done, info = env.step(pred)
    reward_sum += reward

    if done:
        print(reward_sum)
        print("DONE")
        break

env.close()
