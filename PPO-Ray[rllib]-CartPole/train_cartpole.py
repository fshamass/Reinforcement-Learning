import os
import shutil
import ray
from ray import tune
from ray.rllib.algorithms.ppo import PPOConfig

def setup_results_directory(results_dir: str) -> None:
    """Set up the directory for storing training results by removing any existing directory.
    
    Args:
        results_dir (str): Path to the results directory.
    """
    shutil.rmtree(results_dir, ignore_errors=True)

def initialize_ray() -> dict:
    """Initialize Ray and return the context information.
    
    Returns:
        dict: Ray context information, including the dashboard URL.
    """
    ray.shutdown()  # Ensure clean shutdown of any existing Ray instance
    ray_context = ray.init(ignore_reinit_error=True)
    print(f"Ray Dashboard URL: {ray_context.address_info['webui_url']}")
    return ray_context

def configure_ppo() -> PPOConfig:
    """Configure the PPO algorithm with specified hyperparameters.
    
    Returns:
        PPOConfig: Configured PPO algorithm object.
    """
    return (
        PPOConfig()
        .environment("CartPole-v1")  # Set environment to CartPole-v1
        .framework("torch")  # Use PyTorch as the deep learning framework
        .training(
            gamma=0.99,  # Discount factor for future rewards
            lr=0.0001,  # Learning rate for the optimizer
            entropy_coeff=0.02,  # Encourage exploration via entropy regularization
            model={
                "fcnet_hiddens": [512, 512],  # Two hidden layers with 512 units each
                "fcnet_activation": "relu",  # ReLU activation function
            }
        )
        .update_from_dict({
            "train_batch_size": 4096,  # Number of samples per training batch
            "num_sgd_iter": 5,  # Number of SGD iterations per batch
            "sgd_minibatch_size": 64,  # Size of minibatches for SGD
        })
        .api_stack(
            enable_rl_module_and_learner=True,  # Enable new RL module and learner API
            enable_env_runner_and_connector_v2=True  # Enable new environment runner API
        )
        .env_runners(num_env_runners=1)  # Use one environment runner
    )

def run_training(config: PPOConfig, results_dir: str) -> None:
    """Run the PPO training process using Ray Tune.
    
    Args:
        config (PPOConfig): Configured PPO algorithm object.
        results_dir (str): Path to the results directory.
    """
    tuner = tune.Tuner(
        "PPO",
        param_space=config,
        run_config=tune.RunConfig(
            name="cartpole_Training",  # Name of the training run
            storage_path=results_dir,  # Directory to store results
            stop={"training_iteration": 40},  # Stop after 40 iterations
            verbose=1,  # Print progress updates
        ),
    )
    results = tuner.fit()
    print("Training completed. Results saved in:", results_dir)

def main():
    """Main function to orchestrate the PPO training process."""
    # Define paths
    current_dir = os.getcwd()
    results_dir = os.path.join(current_dir, "ray_results")

    # Setup
    setup_results_directory(results_dir)
    initialize_ray()

    # Configure and run training
    config = configure_ppo()
    run_training(config, results_dir)

    # Clean up
    ray.shutdown()

if __name__ == "__main__":
    main()