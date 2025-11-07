#include <iostream>
#include "cliff-walking.hpp"

using namespace std;

int main() {
    CliffWalkingEnv env; // Create environment with 0% slip probability - deterministic
    int state = env.reset();
    vector<string> actionNames = {"UP", "RIGHT", "DOWN", "LEFT"};
    std::cout << "Initial State: " << state << std::endl;

    for (int i = 0; i < 10; ++i) {
        int randAction = rand() % static_cast<int>(CliffWalkingEnv::Actions::NUM_ACTIONS);
        CliffWalkingEnv::Actions action = static_cast<CliffWalkingEnv::Actions>(randAction);
        cout << "Taking action: " << actionNames[randAction] << endl;
        auto [next_state, reward, done, truncated] = env.step(action);
        std::cout << "Step " << i + 1 << ": Next State: " << next_state 
                  << ", Reward: " << reward 
                  << ", Done: " << done 
                  << ", Truncated: " << truncated << std::endl;
        if (done || truncated) {
            break;
        }
    }

    return 0;
}

