import numpy as np
import gym
import matplotlib.pyplot as plt
import random

class Q_Learning_Agent:
    ''' env is list of [num of states, num of actions]
        limits is a list of lists. First list is low limits and 2nd list is high limits
    '''

    def __init__(self, env, limits, num_bins, alpha=0.02, epsilon_decay_rate=0.995, \
                 epsilon_min=0.01, gamma = 0.99) :
        self.grid = self.create_grid(limits, num_bins)
        self.state_size = tuple(len(split) +1 for split in self.grid)
        self.action_size = env[1]
        self.q_table = np.zeros((self.state_size + (self.action_size,)))
        self.alpha = alpha
        self.epsilon = 1.0
        self.epsilon_decay_rate = epsilon_decay_rate
        self.epsilon_min = epsilon_min
        self.gamma = gamma

    def create_grid(self, limits, bins):
        low = limits[0]
        high = limits[1]
        return [np.linspace(l,h,b+1)[1:-1] for l,h,b in zip(low,high,[bins]*len(low))]

    def discretize(self,disc_state):
        return tuple([np.digitize(s,g) for s,g in zip(disc_state,self.grid)])

    def reset_episode(self, state):
        self.last_state = self.discretize(state)
        self.last_action = np.argmax(self.q_table[self.last_state])
        new_epsilon = self.epsilon * self.epsilon_decay_rate
        self.epsilon = max(new_epsilon, self.epsilon_min)
        return self.last_action

    def get_action(self, state):
        rand = np.random.uniform(0,1)
        if(rand < self.epsilon):
            action = random.randint(0, self.action_size - 1)
        else:
            action = np.argmax(self.q_table[state])
        return action

    def act(self, state, reward, mode='train'):
        disc_state = self.discretize(state)
        if mode == 'test':
            action = np.argmax(self.q_table[disc_state])
            return action
        else:
            self.q_table[(self.last_state + (self.last_action,))] += self.alpha * ((reward + self.gamma * max(self.q_table[disc_state])) \
                                                                             - (self.q_table[(self.last_state + (self.last_action,))]))
            action = self.get_action(disc_state)
            self.last_state = disc_state
            self.last_action = action
            return action

if __name__ == '__main__':
    env = gym.make('CartPole-v1')
    env_info = [env.observation_space, env.action_space.n]
    limits = [[-4.8, -5, -0.418, -5],[4.8, 5, 0.418, 5]]
    q_agent = Q_Learning_Agent(env_info, limits, 15)
    episode_reward = 0

    N = 15000
    total_rewards = np.empty(N)
    for i in range(N):
        if(i % 10 == 0):
            print('Round: ', i)
        state, _ = env.reset()
        episode_reward = 0
        action = q_agent.reset_episode(state)
        done = False
        while(not done):
            state, rewards, done, _, _ = env.step(action)
            episode_reward += rewards
            action = q_agent.act(state, rewards)
        total_rewards[i] = episode_reward

    ave_rewards= np.empty(N)
    for t in range(N):
        ave_rewards[t] = total_rewards[max(0, t-100):(t+1)].mean()
    plt.plot(ave_rewards)
    plt.show()
