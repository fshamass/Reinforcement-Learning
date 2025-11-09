#include "cliff_walking.hpp"


// Constructor implementation
CliffWalkingEnv::CliffWalkingEnv(float slipProb) {
    numStates_ = 48; // Example number of states
    resetState_ = 3 * 12 + 0;
    slipProb_ = slipProb;
    currentState_ = resetState_;
    numSteps_ = 0;
}

//Return the initial state
int CliffWalkingEnv::reset() {
    currentState_ = resetState_;
    numSteps_ = 0;
    return currentState_;
}

pair<int,int> CliffWalkingEnv::getObservationSpace() {
    return make_pair(0, numStates_ - 1);
}

pair<int,int> CliffWalkingEnv::getActionSpace() {
    return make_pair(0, static_cast<int>(Actions::NUM_ACTIONS) - 1);
}

vector<string> CliffWalkingEnv::getActionNames() {
    return {"UP", "RT", "DN", "LT"};
}   

// next_state, reward, done, truncated
tuple<int, int, bool, bool> CliffWalkingEnv::step(int action) {
    if(action < static_cast<int>(Actions::UP) || action > static_cast<int>(Actions::LEFT)) {
        throw invalid_argument("Invalid action");
    }
    
    int row = currentState_ / 12;
    int col = currentState_ % 12;
    int nextRow = row;
    int nextCol = col;
    bool done = false;
    bool truncated = false;
    
    // Calculate next position
    switch (static_cast<Actions>(action)) {
        case Actions::UP:    nextRow = row - 1; break;
        case Actions::RIGHT: nextCol = col + 1; break;
        case Actions::DOWN:  nextRow = row + 1; break;
        case Actions::LEFT:  nextCol = col - 1; break;
        default: break;
    }
    
    // Default reward is -1 per step
    int reward = -1;
    
    // Check bounds - if invalid, stay in current state
    if (nextRow >= 0 && nextRow <= 3 && nextCol >= 0 && nextCol <= 11) {
        // Valid move - check for cliff
        if (nextRow == 3 && nextCol > 0 && nextCol < 11) {
            // Fell off cliff
            currentState_ = resetState_;
            reward = -10;  // Larger penalty for cliff
            done = true;
        } else {
            // Valid move - update state
            currentState_ = nextRow * 12 + nextCol;
        }
    }
    // else: Invalid move - stay in current state, still get -1 reward
    
    // Check for goal state (bottom-right corner)
    if (currentState_ == 47) {  // 3 * 12 + 11
        done = true;  // Episode ends but reward stays -1
    }
    
    // Check for max steps (500 is more reasonable)
    if (++numSteps_ >= 500) {
        truncated = true;
    }
    
    return make_tuple(currentState_, reward, done, truncated);
}