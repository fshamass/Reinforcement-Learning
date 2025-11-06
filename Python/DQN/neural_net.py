import torch
import numpy as np
import torch.nn as nn
import torch.optim as optim


class DQNeuralNet(nn.Module):
    def __init__(self, state_size, action_size, batch_size):
        super(DQNeuralNet, self).__init__()

        # Define the neural network architecture
        self.network = nn.Sequential(
            nn.Linear(state_size, 16),
            nn.ReLU(),
            nn.Linear(16, 16),
            nn.ReLU(),
            nn.Linear(16, action_size)
        )

        # Define loss and optimizer functions
        self.loss = nn.MSELoss()
        self.optimizer = optim.Adam(self.network.parameters(), lr=5e-4)
        #Initially set network in evaluation mode
        self.network.eval()

        # Set the device to GPU if available, otherwise CPU
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.network.to(self.device)  # Move network to the chosen device
        self.batch_size = batch_size
        self.state_size = state_size
        self.action_size = action_size

    #Retrieve model parameters
    def get_model_params(self):
        return self.network.parameters()

    def forward(self, state, mode='train'):
        # Convert state to torch tensor if it isn't, and move it to the same device
        if not isinstance(state, torch.Tensor):
            state = torch.tensor(state, dtype=torch.float32).to(self.device)
        else:
            state = state.to(self.device)

        # Gradient tracking mode (training)
        if mode == 'train':
            self.network.train()
            ret = self.network(state)  # Return tensor for learning (no conversion to NumPy)
            return ret

        #Inference mode (no gradients) - this could be used for action suggestion on prediction
        #network or batch prediction on target network. Since target network doesn't need backprop
        elif mode == 'eval':
            self.network.eval()
            if state.dim() == 1:
                state = state.unsqueeze(0)
            with torch.no_grad():
                ret = self.network(state)
                # Will return with batch dimension, move to CPU, and convert to NumPy
                ret = ret.cpu().data.numpy()
                return ret
        else:
            raise ValueError(f"Invalid mode: {mode}. Expected 'train' or 'eval'.")

        return None

    def update(self, states, actions, targets):
        #ensure input format to neural network is compatible
        if not isinstance(states, torch.Tensor):
            states = torch.tensor(states, dtype=torch.float32)
        states = states.reshape(self.batch_size,self.state_size).to(self.device)

        if not isinstance(targets, torch.Tensor):
            targets = torch.tensor(targets,dtype=torch.float32)
        targets = targets.reshape(self.batch_size, 1).to(self.device)

        if not isinstance(actions, torch.Tensor):
            actions = torch.tensor(actions,dtype=torch.int64)
        actions = actions.reshape(self.batch_size, 1).to(self.device)

        predictions = self.forward(states, mode='train').gather(dim=1,index=actions)
        loss = self.loss(predictions,targets)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()


