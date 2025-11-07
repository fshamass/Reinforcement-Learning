#include "cliff-walking.hpp"


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

// next_state, reward, done, truncated
tuple<int, int, bool, bool> CliffWalkingEnv::step(Actions action) {
    int row = currentState_ / 12;
    int col = currentState_ % 12;
    int reward = 0;
    bool done = false;
    bool truncated = false;

    float randProb = static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
    if (randProb < slipProb_) {
        // Slippery logic (random movement) - Randomly select action
        int slip = rand() % static_cast<int>(Actions::NUM_ACTIONS);
        action = static_cast<Actions>(slip);
    }

    numSteps_++;
    currentState_ = -1;
    //Check for out of bounds and update position
    switch (action) {
        case Actions::UP: // up
            row -= 1;
            break;
        case Actions::RIGHT: // right
            col += 1;
            break;
        case Actions::DOWN: // down
            row += 1;
            break;
        case Actions::LEFT: // left
            col -= 1;
            break;
    }
    if((row < 0) || (row > 3) || (col < 0) || (col > 11)) {
        currentState_ = resetState_;
        reward = -10;
    }else {
        // Check for cliff
        if (row == 3 && col > 0 && col < 11) {
            currentState_ = resetState_;
            reward = -10;
        }
    }
    if(currentState_ != resetState_) {
        currentState_ = row * 12 + col;
        reward = -1;
    }
    if(currentState_ == 3 * 12 + 11) {
        done = true; // Reached goal
    }
    if(numSteps_ >= 1000) {
        truncated = true; // Max steps reached
    }

    return make_tuple(currentState_, reward, done, truncated); // Normal step
}
