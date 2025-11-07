#ifndef CLIFF_WALKING_HPP
#define CLIFF_WALKING_HPP

#include <iostream>
#include <vector>

using namespace std;

class CliffWalkingEnv {
    public:
        enum class Actions {
            UP = 0,
            RIGHT = 1,
            DOWN = 2,
            LEFT = 3,
            NUM_ACTIONS = 4    
        };

        CliffWalkingEnv(float slipProb = 0.00);
        int reset();
        tuple<int, int, bool, bool> step(Actions action);
    private:
        int numStates_;
        int currentState_;
        int resetState_;
        float slipProb_;
        int numSteps_;
};
#endif // CLIFF_WALKING_HPP