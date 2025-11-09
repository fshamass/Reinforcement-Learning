#include <iostream>
#include <deque>
#include "Q_Learn.hpp"
#include "../../env/cliff-walking/cliff_walking.hpp"

void printUsage(const char* programName) {
    std::cout << "Usage: " << programName << " [num_episodes]\n"
              << "  num_episodes: Number of training episodes (default: 100)\n";
}

int main(int argc, char* argv[]) {
    int numEpisodes = 100;  // default value
    
    if (argc > 2) {
        printUsage(argv[0]);
        return 1;
    }
    
    if (argc == 2) {
        try {
            numEpisodes = std::stoi(argv[1]);
            if (numEpisodes <= 0) {
                std::cerr << "Error: Number of episodes must be positive\n";
                return 1;
            }
        } catch (const std::exception& e) {
            std::cerr << "Error: Invalid number of episodes\n";
            printUsage(argv[0]);
            return 1;
        }
    }
    // Create Cliff Walking environment
    CliffWalkingEnv env;
    int numStates = env.getObservationSpace().second - env.getObservationSpace().first + 1;
    int numActions = env.getActionSpace().second - env.getActionSpace().first + 1;
    vector<string> actionNames = env.getActionNames();

    // Create Q-Learning agent with tuned parameters
    QLearn agent(numStates, numActions,
                 0.1,    // learning rate (smaller for more stable learning)
                 0.99,   // gamma (high for long-term rewards)
                 0.01,   // minimum epsilon (for some exploration)
                 0.995); // slower epsilon decay

    std::cout << "Training for " << numEpisodes << " episodes...\n";
    vector<float> aveRewards;
    deque<float> rewardsWindow(100);
    float totalRewards = 0.0;
    for (int episode = 0; episode < numEpisodes; ++episode) {
        int state = env.reset();
        agent.reset(state);
        int steps = 0;
        int rewards = 0;
        while(true) {
            steps++;
            int action = agent.getAction(state);
            auto [nextState, reward, done, truncated] = env.step(action);
            agent.learn(reward, nextState);
            rewards += reward;
            state = nextState;  // Update current state
            if((done) || (truncated)) {
                //cout<< "Episode " << episode + 1 << " rewards: " << rewards << " steps: " << steps << " done: " << done << " truncated: " << truncated << std::endl;
                break;
            }
        }
        if(rewardsWindow.size() >= 100) {
            totalRewards -= rewardsWindow.front();
            rewardsWindow.pop_front();
        }
        rewardsWindow.push_back(rewards);
        totalRewards += rewards;
        float averageReward = totalRewards / rewardsWindow.size();
        cout << "Episode " << episode + 1 << " Average Rewards: " << averageReward << std::endl;
        aveRewards.push_back(averageReward);
    }

    std::cout << "Training completed." << std::endl;
    bool done = false;
    int state = env.reset();
    agent.reset(state);
    cout << "-----------------------------------------------------------" << endl;
    for(int i=0;i<4;i++) {
        for(int j=0;j<12;j++) {
            int s = i*12 + j;
            if((s>=37) && (s<=46)) {
                std::cout << "CL | ";
                continue;
            }
            if(s== 47) {
                std::cout << " X | ";
                continue;
            }
            int action = agent.forward(s);
            std::cout << actionNames[action] << " | ";
        }
        cout << endl;
        cout << "-----------------------------------------------------------" << endl;
    }
    /*
    while(!done) {
        int action = agent.forward(state);
        cout << "State: " << state << " Action: " << actionNames[action] << std::endl;
        auto [nextState, reward, isDone, truncated] = env.step(action);
        state = nextState;
        done = isDone;
    }
    */
    return 0;
}