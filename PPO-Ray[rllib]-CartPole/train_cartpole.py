import os
import shutil
import ray
from ray import tune
from ray.rllib.algorithms.ppo import PPOConfig

def setup_results_directory(results_dir: str) -> None:
    """Set up the directory for storing training results by removing any existing directory."""
    shutil.rmtree(results_dir, ignore_errors=True)

def initialize_ray() -> dict:
    """Initialize Ray and return the context information."""
    ray.shutdown()  # Ensure clean shutdown of any existing Ray instance
    ray_context = ray.init(ignore_reinit_error=True)
    print(f"Ray Dashboard URL: {ray_context.address_info['webui_url']}")
    return ray_context

def configure_ppo() -> PPOConfig:
    """Configure the PPO algorithm with specified hyperparameters."""
    return (
        PPOConfig()
        .environment("CartPole-v1")
        .framework("torch")
        .training(
            gamma=0.99,
            lr=0.0001,
            entropy_coeff=0.02,
            model={
                "fcnet_hiddens": [256, 256],
                "fcnet_activation": "relu",
            }
        )
        .evaluation(
            evaluation_interval=2,
            evaluation_duration=10,
            evaluation_config={
                "explore": False
            }
        )        
        .update_from_dict({
            "train_batch_size": 4096,
            "num_sgd_iter": 5,
            "sgd_minibatch_size": 64,
        })
        .api_stack(
            enable_rl_module_and_learner=True,
            enable_env_runner_and_connector_v2=True
        )
        .env_runners(num_env_runners=1)
    )

def run_training(config: PPOConfig, results_dir: str) -> None:
    """Run the PPO training process using Ray Tune."""
    tuner = tune.Tuner(
        "PPO",
        param_space=config,
        run_config=tune.RunConfig(
            name="cartpole_Training",
            storage_path=results_dir,
            stop={"training_iteration": 40},
            checkpoint_config=tune.CheckpointConfig(
                checkpoint_frequency=10,  # Save checkpoint every 10 iterations
                checkpoint_at_end=True  # Ensure a checkpoint is saved at the end
            ),
            verbose=1,
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