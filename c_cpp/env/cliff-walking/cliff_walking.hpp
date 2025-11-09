/*************************************************************************************************************
 * Cliff Walking Environment
 * This environment simulates the classic Cliff Walking problem in Reinforcement Learning Gym environment.
 * The environment consists of a 4x12 grid where cells 2-11 of bottom row represent a cliff.
 * The agent starts at bottom left cell (4,1) state and must navigate to a goal state bottom right cell (4,12) 
 * while avoiding the cliff.
 * The environment can be configured to be slippery, stochasticity in the agent's movements is set by default 
 * to be 0.00 (deterministic) in class constructor but it can be change to any slipping probability.
 * Client is rewards -1 for each step taken and -10 for falling off the cliff or agent reaching 10000 steps.
 * The episode ends when the agent reaches the goal state or falls off the cliff or reaches 1000 steps.
 *************************************************************************************************************/

#ifndef CLIFF_WALKING_HPP
#define CLIFF_WALKING_HPP

#include <iostream>
#include <vector>

using namespace std;

class CliffWalkingEnv {
    public:
        CliffWalkingEnv(float slipProb = 0.00);
        // get min and max number of states and actions
        pair<int,int> getObservationSpace();
        pair<int,int> getActionSpace();
        vector<string> getActionNames();
        int reset();
        tuple<int, int, bool, bool> step(int action);
    private:
        enum class Actions {
            UP = 0,
            RIGHT = 1,
            DOWN = 2,
            LEFT = 3,
            NUM_ACTIONS = 4    
        };

        int numStates_;
        int currentState_;
        int resetState_;
        float slipProb_;
        int numSteps_;
};
#endif // CLIFF_WALKING_HPP