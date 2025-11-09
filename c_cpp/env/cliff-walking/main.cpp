#include <iostream>
#include "cliff_walking.hpp"

using namespace std;

int main() {
    CliffWalkingEnv env; // Create environment with 0% slip probability - deterministic
    int state = env.reset();
    vector<string> actionNames = env.getActionNames();
    std::cout << "Initial State: " << state << std::endl;

    auto [minAction, maxAction] = env.getActionSpace();
    int numActions = maxAction - minAction + 1;

    for (int i = 0; i < 10; ++i) {
        int randAction = rand() % static_cast<int>(numActions);
        cout << "Taking action: " << actionNames[randAction] << endl;
        auto [next_state, reward, done, truncated] = env.step(randAction);
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

