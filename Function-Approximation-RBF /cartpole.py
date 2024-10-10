import numpy as np
import gym
import matplotlib.pyplot as plt
from sklearn.kernel_approximation import RBFSampler

class Approximator_Agent:
    ''' Generic funtion approximator agent. It uses RBF for state-action approximation.
        samples: randomly collected samples from env. It is used to fit RFB sampler for better state represntation
        alpha: learning rate
        gamma: discount factor
        eps_decay_rate: rate at which eps to be decayed.
        eps_min: min eps value beyond which no decay is performed.
    '''
    def __init__(self, num_actions, samples, alpha, gamma, eps_decay_rate = 0.995, eps_min = 0.01):
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.eps = 1
        self.eps_decay_rate = eps_decay_rate
        self.eps_min = eps_min
        self.featurizer = RBFSampler()
        self.featurizer.fit(samples)
        self.w = np.zeros(self.featurizer.n_components)

    def reset_state(self, state):
        self.eps = 1
        self.last_state = state

    def predict(self, state, action):
        sa = np.concatenate((state, [action]))
        x = self.featurizer.transform([sa])[0]
        return self.w @ x

    def grad(self, state, action):
        sa = np.concatenate((state, [a]))
        x = self.featurizer.transform([sa])[0]
        return x

    def check_all_actions(self,state):
        res = [self.predict(state, action) for action in range(self.num_actions)]
        return res

    def get_action(self, state):
        rand = np.random.random()
        if(rand < self.eps):
            return np.random.choice(self.num_actions)
        else:
            return np.argmax(self.check_all_actions(state))

    def learn(self, state, action, reward):
        self.eps *= self.eps_decay_rate
        self.eps = min(self.eps, self.eps_min)
        cur_pred = self.predict(self.last_state, action)
        target = reward + self.gamma * np.max(self.check_all_actions(state))
        grad = self.grad(self.last_state, action)
        self.w += self.alpha * (target - cur_pred) * grad
        self.last_state = state

def collect_random_samples(env, n):
    samples = []
    for i in range(n):
        s, _ = env.reset()
        done = False
        truncate = False
        while not (done or truncate):
            a = env.action_space.sample()
            sa = np.concatenate((s,[a]));
            samples.append(sa)
            s,r,done,truncate,_ = env.step(a)
    return samples

if __name__ == '__main__':
    env = gym.make('CartPole-v1')
    #collect random samples for RBF fitting
    samples = collect_random_samples(env,10000)
    approx_agent = Approximator_Agent(env.action_space.n,samples,0.02, 0.99)

    training_iterations = 20000
    rewards = np.empty(training_iterations)
    ave_rewards = np.empty(training_iterations)
    for i in range(training_iterations):
        s, _ = env.reset()
        approx_agent.reset_state(s)
        done = False
        truncate = False
        reward = 0
        while not(done or truncate):
            a = approx_agent.get_action(s)
            s,r,done,truncate, _ = env.step(a)
            approx_agent.learn(s,a,r)
            reward += r
        rewards[i] = reward
        if i % 100 == 0:
            print("Iteration: ", i , ' rewards: ', reward)
    for t in range(training_iterations):
        ave_rewards[t] = rewards[max(0,t-100):i].mean()

    plt.plot(ave_rewards)
    plt.show()
