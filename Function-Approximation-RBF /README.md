# Function Approximation implementation for Gym CartPole
#### Simple script to demonstrate function approximation with Gym CartPole simulation https://gymnasium.farama.org/environments/classic_control/cart_pole/
RBF was used to transform state into feature vector. Then discrete action is concatenated with state and vector for prediction.
Agent was able to learn and reached consistent 500 rewards (steps).
Below is plot of agent rewards during learning process.

<br><br>
<div align="center">
  <img src="../Assets/RBF-Approximation-CartPole-Rewards.png" alt="Learned Rewards" title="Learned rewards" />
  <p>Learned Rewards</p>
</div>
