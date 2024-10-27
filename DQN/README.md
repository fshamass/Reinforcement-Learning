# Deep Q-Network (DQN) Implementation with Gym CartPole

This project implements a Deep Q-Network (DQN) to train an agent in the CartPole environment from OpenAI's Gymnasium. The main objective is to achieve a stable training performance, tuning hyperparameters to optimize the agent's ability to balance the pole effectively.

**Environment:** [CartPole-v1](https://gymnasium.farama.org/environments/classic_control/cart_pole/)

## Project Overview

Initially, the agent demonstrated rapid progress, reaching rewards over 250 due to Q-value overestimation. However, as training continued, rewards declined, and the agent gradually improved through further learning cycles. Around the 4000th epoch, the agent achieved the maximum reward of 500 across three consecutive evaluation points (each point representing a rolling average of 100 episodes), indicating consistent performance across roughly 300 episodes with rewards of 500 or close to it.

While this indicated promising stability, the agent's learning became less consistent beyond this point, likely due to the continuous soft updates applied to the target network. Soft updates caused the agent to keep refining its policy even after reaching optimal performance, leading to periods of suboptimal policy shifts and recovery phases.

The agent achieved maximum rewards across five consecutive evaluation points around the 10,000th epoch, confirming the stability achieved through earlier training. Unsure of the optimal stopping point, the training session was extended to 20,000 epochs to observe longer-term patterns.

## Exploration Strategy

Exploration was decayed at the episode level, rather than per action within episodes, as action-level decay destabilized the learning process significantly. By decaying exploration across episodes, the agent was able to achieve improved stability and maintain a more reliable policy.

## Key Observations
- **Q-value Overestimation**: Rapid initial success in rewards indicated overestimation of Q-values.
- **Training Stability**: Reached a consistent performance (reward of 500) around 4000 epochs, with occasional fluctuations due to soft updates.
- **Exploration Decay**: Episode-level decay provided stability, while action-level decay destabilized learning.

---


<div align="center">
  <br>
  <img src="../Assets/DQN-CartPole.png" alt="Learned Policy" title="Learned Policy" />
  <p>Learned Policy</p>
</div>

