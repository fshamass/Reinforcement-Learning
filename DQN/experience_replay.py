import torch
import numpy as np
import random
from collections import namedtuple

Transition = namedtuple('Transition', field_names=['state', 'action', 'reward', 'next_state', 'done'])

class ReplayBuffer:
    def __init__(self, capacity, batch_size):
        self.capacity = capacity
        self.buffer = []
        self.index = 0
        self.batch_size = batch_size
        self.size = 0
        self.seed = random.seed(0)


    def push(self,*args):
        transition = Transition(*args)
        if len(self.buffer) < self.capacity:
            self.buffer.append(transition)
        else:
            self.buffer[self.index] = transition
        self.index = (self.index + 1) % self.capacity
        self.size = min(len(self.buffer), self.capacity)
        return self.size

    def sample(self):
        experiences =  random.sample(self.buffer, min(self.size, self.batch_size))

        states = np.vstack([experience.state for experience in experiences])
        actions = np.vstack([experience.action for experience in experiences])
        rewards = np.vstack([experience.reward for experience in experiences])
        next_states = np.vstack([experience.next_state for experience in experiences])
        dones = np.vstack([experience.done for experience in experiences])
        return (states, actions, rewards, next_states, dones)
