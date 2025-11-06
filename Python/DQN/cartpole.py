import numpy as np
import gym
import matplotlib.pyplot as plt
from agent import DQN_Agent

if __name__ == '__main__':
    env = gym.make('CartPole-v1')
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n

    NUM_LOOPS = 20000
    rewards = np.empty(NUM_LOOPS)
    ave_rewards= []
    agent = DQN_Agent(state_size, action_size, 0.99, 1e-3)
    for i in range(NUM_LOOPS):
        r = 0
        state, _ = env.reset()
        agent.reset_state()
        done = False
        deprecate = False

        while not done:
            action = agent.get_action(state)
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            agent.learn((state, action, reward, next_state, done))
            r += reward
            state = next_state
        rewards[i] = r
        rolling_ave = rewards[max(0, i-100): i+1].mean()
        ave_rewards.append(rolling_ave)
        if i%100 == 0:
            print(f"Processed: {i} batches ... rewards: {rolling_ave}")
    plt.plot(ave_rewards)
    plt.show()
