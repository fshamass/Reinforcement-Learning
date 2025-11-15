#include "gorge_walking.hpp"


// Constructor implementation
GorgeWalkingEnv::GorgeWalkingEnv(int numRows, int numCols, vector<pair<int,int>> gorge,float slipProb) : 
    numRows_(numRows), numCols_(numCols), slipProb_(slipProb) {
    resetState_ = {(numRows_ - 1), 0};
    goalState_ = {(numRows_ -1), (numCols_ -1)};
    slipProb_ = slipProb;
    currentState_ = resetState_;
    numSteps_ = 0;
    envCells_.resize(numRows_, vector<bool>(numCols_, true));
    for(auto cell:gorge) {
        envCells_[cell.first][cell.second] = false;
    }
}

// Return the initial state
int GorgeWalkingEnv::reset() {
    currentState_ = resetState_;
    numSteps_ = 0;
    return currentState_.first * numCols_ + currentState_.second;
}

pair<int,int> GorgeWalkingEnv::getObservationSpace() {
    return make_pair(0, numRows_ * numCols_ - 1);
}

pair<int,int> GorgeWalkingEnv::getActionSpace() {
    return make_pair(0, static_cast<int>(Actions::NUM_ACTIONS) - 1);
}

vector<string> GorgeWalkingEnv::getActionNames() {
    return {"UP", "RT", "DN", "LT"};
}   

// next_state, reward, done, truncated
tuple<int, int, bool, bool> GorgeWalkingEnv::step(int action) {
    if(action < static_cast<int>(Actions::UP) || action > static_cast<int>(Actions::LEFT)) {
        throw invalid_argument("Invalid action");
    }
    
    int row = currentState_.first;
    int col = currentState_.second;
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
    if ((nextRow >= 0) && (nextRow <= numRows_-1) && (nextCol >= 0) && (nextCol <= numCols_-1)) {
        // Valid move - check for gorge
        if (envCells_[nextRow][nextCol] == false) {
            // Fell off gorge
            currentState_ = resetState_;
            reward = -10;  // Larger penalty for gorge
            done = true;
        } else {
            // Valid move - update state
            currentState_ = {nextRow, nextCol};
        }
    }

    // Check for goal state (bottom-right corner)
    if ((nextRow == goalState_.first) && (nextCol == goalState_.second)) { 
        done = true;  // Episode ends but reward stays -1
    }
    
    // Check for max steps (500 is more reasonable)
    if (++numSteps_ >= 500) {
        truncated = true;
    }
    int flattenedState = currentState_.first * numCols_ + currentState_.second;
    return make_tuple(flattenedState, reward, done, truncated);
}