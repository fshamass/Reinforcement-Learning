import numpy as np
import gym
import matplotlib.pyplot as plt

class Q_Table_Agent:
    def __init__(self, states, actions, alpha, gamma, eps_decay_rate = 0.9, min_eps = 0.01):
        self.num_states = states
        self.num_actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.eps = 1
        self.eps_decay_rate = eps_decay_rate
        self.min_eps = min_eps
        #self.q_table = np.random.uniform(low=1,high=100, size=(self.num_states,self.num_actions))
        self.q_table = np.zeros((self.num_states,self.num_actions))

    def reset_state(self):
        self.eps *= self.eps_decay_rate
        self.eps = min(self.eps, self.min_eps)

    def get_action(self, state):
        if np.random.uniform() < self.eps:
            action = np.random.choice([action for action in range(self.num_actions)])
        else:
            action = np.argmax(self.q_table[state])
        self.last_state = state
        self.last_action = action
        return action

    def act(self, new_state, reward):
        target = reward+self.gamma*max(self.q_table[new_state])
        current = self.q_table[self.last_state][self.last_action]
        current = current + self.alpha *(target - current)
        self.q_table[self.last_state][self.last_action] = current

    def get_policy(self):
        policy = np.array([np.argmax(self.q_table[state]) for state in range(48)]).reshape(4,12)
        return policy


if __name__ == '__main__':
    print('Hello World')
    env = gym.make('CliffWalking-v0')
    q_table_agent = Q_Table_Agent(env.observation_space.n, env.action_space.n, 0.02, 0.99)
    N = 3000
    rewards = np.empty(N)
    ave_rewards = []

    for i in range(N):
        if i%100 == 0:
            print("Processing round: ", i)
        state, _ = env.reset()
        q_table_agent.reset_state()
        done = False
        reward = 0
        while not done:
            action = q_table_agent.get_action(state)
            new_state, cur_reward, done, _, _ = env.step(action)
            reward += cur_reward
            q_table_agent.act(new_state, cur_reward)
            state = new_state
        rewards[i] = reward
        ave_rewards.append(rewards[max(0,i-100):i].mean())
    plt.plot(ave_rewards)
    policy = q_table_agent.get_policy()
    policy[3,1:] = -1
    print("\nEstimated Optimal Policy (UP = 0, RIGHT = 1, DOWN = 2, LEFT = 3, N/A = -1):")
    print(policy)
    print("Rewards: ",ave_rewards[-1])