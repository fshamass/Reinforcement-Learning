#include <iostream>
#include <deque>
#include <algorithm>
#include "sarsa.hpp"
#include "../../env/gorge-walking/gorge_walking.hpp"

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
    // Create Gorge Walking environment
    vector<pair<int,int>> gorge = 
        {{1,1},{2,1},{3,1},{4,1},{4,2},{4,3},{5,3},{6,3},{0,3},{0,4},{0,5},{1,5},{2,5},{4,5},{5,5},{6,5}};
    int envNumRows = 7;
    int envNumCols = 7; 
    GorgeWalkingEnv env(envNumRows,envNumCols,gorge);

    int numStates = env.getObservationSpace().second - env.getObservationSpace().first + 1;
    int numActions = env.getActionSpace().second - env.getActionSpace().first + 1;
    vector<string> actionNames = env.getActionNames();

    // Create Q-Learning agent with tuned parameters
    Sarsa agent(numStates, numActions,
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
    //Sort Gorge points ascending by rows
    sort(gorge.begin(), gorge.end());
    int index = 0;
    bool done = false;
    int state = env.reset();
    agent.reset(state);
    cout << "----------------------------------" << endl;
    for(int i=0;i<envNumRows;i++) {
        for(int j=0;j<envNumCols;j++) {
            if((i == gorge[index].first) && (j == gorge[index].second)) {
                std::cout << "XX | ";
                if(index < gorge.size()-1)
                    index++;
                continue;
            }
            if((i == envNumRows-1) && (j == envNumCols-1)) {
                std::cout << " G | ";
                continue;
            }
            int state = i * envNumCols + j;
            int action = agent.forward(state);
            std::cout << actionNames[action] << " | ";
        }
        cout << endl;
        cout << "----------------------------------" << endl;
    }
    return 0;
}