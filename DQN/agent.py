import numpy as np
from neural_net import DQNeuralNet
from experience_replay import ReplayBuffer
import torch
import random

class DQN_Agent:
    def __init__(self, state_size, action_size, gamma, tau, eps_decay_rate=0.995, eps_min=0.01):
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma      #discount factor
        self.tau = tau          #rate by which target network parameters are updated
        self.eps_decay_rate = eps_decay_rate
        self.eps_min = eps_min
        self.agent_config()
        self.pred_net = DQNeuralNet(state_size, action_size, self.batch_size)
        self.tar_net =  DQNeuralNet(state_size, action_size, self.batch_size)
        self.replay_buffer = ReplayBuffer(self.buffer_size, self.batch_size)

    #Configurations set by agent - not coming from process that instantiate the agent
    def agent_config(self):
        self.buffer_size = 128000  #replay buffer size
        self.batch_size = 64      #Number of samples to get from replay buffer
        self.eps = 1
        self.learn_cntr = 0
        self.seed = random.seed(0)
        self.learn_threshold = 4  #Threshold by which agent learns from experiences

    def reset_state(self):
        self.eps = max(self.eps * self.eps_decay_rate, self.eps_min)

    #State here is numpy array coming from simulation
    def get_action(self, state):
        if np.random.random() < self.eps:
            return np.random.choice(range(self.action_size))
        else:
            #convert state to 2-D torch tensor
            actions = self.pred_net(state, 'eval')
            action = np.argmax(actions[0])
            return action

    def learn(self, experience):
        if self.batch_size <= self.replay_buffer.push(*experience):
            self.learn_cntr += 1
            #Ensure there are at least batch_size of new samples
            if self.learn_cntr >= self.learn_threshold:
                self.learn_cntr = 0
                #unpack the experience elements
                states, actions, rewards, next_states, dones = self.replay_buffer.sample()
                #Get max Q value for each experience
                next_states_q = self.tar_net(next_states, mode = 'eval')
                next_states_q = np.max(next_states_q, axis=1, keepdims=True)
                targets = rewards + (self.gamma * next_states_q * (1-dones))
                self.pred_net.update(states, actions, targets)
                self.update_target_params()

    def update_target_params(self):
        for target_param, pred_param in zip(self.tar_net.get_model_params(), \
                                            self.pred_net.get_model_params()):
            target_param.data.copy_(self.tau * pred_param.data + (1-self.tau) * target_param.data)


