# Function Approximation implementation for Gym CartPole
#### Simple script to demonstrate function approximation with Gym CartPole simulation https://gymnasium.farama.org/environments/classic_control/cart_pole/
state vector is concatenated with discrete action and RBF was used to transform state-action into feature vector. <br>
Agent was able to learn and reached consistent 500 rewards (steps). <br>
Below is plot of agent rewards during learning process.

<br><br>
<div align="center">
  <img src="../Assets/RBF-Approximation-CartPole-Rewards.png" alt="Learned Rewards" title="Learned rewards" />
  <p>Learned Rewards</p>
</div>
