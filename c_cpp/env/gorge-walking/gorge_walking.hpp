/*****************************************************************************************************************
 * Gorge Walking Environment (generalized)
 *
 * This environment extends the classic OpenAI Gym "CliffWalking" example and provides a flexible, configurable 
 * grid-world where an agent must navigate from a start (bottom left) cell to a goal (bottom right) cell
 * while avoiding a configurable "gorge" region. The key differences and capabilities are:
 *
 * - Flexible grid size: the environment can be instantiated with arbitrary number of rows and columns
 *   instead of the fixed 4x12 layout used in the classic example.
 * - Configurable gorge: the gorge (danger) cells are supplied as a list of coordinates and may form any
 *   contiguous or non-contiguous shape the user requires (not limited to a single row slice).
 * - Slippery / stochastic dynamics: an optional slip probability can be provided to make actions
 *   stochastic (agent's intended action may be replaced by a random action with given probability).
 * - Reward / termination semantics: by default the environment follows the familiar pattern of small
 *   negative step reward (encouraging shorter paths) and a larger negative penalty for entering gorge
 *   cells. Episode termination occurs when the agent reaches the goal or falls into the gorge; a max-step
 *   truncation is also applied to prevent infinite episodes.
 *
 * The public API provides observation / action space queries, a `reset()` returning the initial state, and
 * a `step(action)` method returning the (next_state, reward, done, truncated) tuple (gym-like semantics).
 *
 * This header documents the environment interface; check the implementation (.cpp) for precise reward
 * magnitudes and default parameter values.
 ****************************************************************************************************************/

#ifndef GORGE_WALKING_HPP
#define GORGE_WALKING_HPP

#include <iostream>
#include <vector>

using namespace std;

class GorgeWalkingEnv {
    public:
        GorgeWalkingEnv(int numRows, int numCols, vector<pair<int,int>> gorge, float slipProb = 0.00);
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

        int numRows_;
        int numCols_;
        pair<int,int> currentState_;
        pair<int,int> resetState_;
        pair<int,int> goalState_;
        float slipProb_;
        int numSteps_;
        vector<vector<bool>> envCells_;
};
#endif // gorge_WALKING_HPP