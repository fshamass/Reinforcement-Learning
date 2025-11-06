import torch
import torch.nn as nn
import gymnasium as gym
import numpy as np

# Define the neural network matching the PPO architecture
class CartPolePolicy(nn.Module):
    def __init__(self):
        super(CartPolePolicy, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(4, 256),  # Input: CartPole observation (4 dimensions)
            nn.ReLU(),
            nn.Linear(256, 256),  # Hidden layer
            nn.ReLU(),
            nn.Linear(256, 2)   # Output: 2 actions (left, right)
        )

    def forward(self, x):
        return self.network(x)

def load_model(weights_path="model_weights.pt"):
    """Load the model weights into the CartPolePolicy network."""
    model = CartPolePolicy()
    model.load_state_dict(torch.load(weights_path))
    model.eval()
    return model

def select_action(model, observation):
    """Select an action using the model for a given observation."""
    # Convert observation to tensor
    obs_tensor = torch.tensor(observation, dtype=torch.float32)
    with torch.no_grad():
        action_logits = model(obs_tensor)
    # Select action with highest logit (deterministic for deployment)
    action = torch.argmax(action_logits).item()
    return action

def test_model(weights_path="model_weights.pt", episodes=5):
    """Test the model in the CartPole-v1 environment."""
    # Load the model
    model = load_model(weights_path)

    # Initialize the environment
    env = gym.make("CartPole-v1")
    total_rewards = []

    for episode in range(episodes):
        observation, _ = env.reset()
        total_reward = 0
        done = False

        while not done:
            action = select_action(model, observation)
            observation, reward, terminated, truncated, _ = env.step(action)
            total_reward += reward
            done = terminated or truncated

        total_rewards.append(total_reward)
        print(f"Episode {episode + 1}: Total Reward = {total_reward}")

    env.close()
    print(f"Average Reward over {episodes} episodes: {np.mean(total_rewards)}")

if __name__ == "__main__":
    test_model()