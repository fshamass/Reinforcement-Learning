#include "sarsa.hpp"

Sarsa::Sarsa(int numStates, int numActions, float lr, float gamma, float minEpsilon, float decayRate) :
    epsilon_(1.0), numActions_(numActions), lr_(lr), gamma_(gamma), minEpsilon_(minEpsilon), decayRate_(decayRate) {
    qTable_.resize(numStates, vector<float>(numActions, 0.0));
    cout << "Sarsa agent created with " << numStates << " states and " << numActions << " actions." << std::endl;
}

void Sarsa::reset(int state) {
    epsilon_ *= decayRate_;
    epsilon_ = max(epsilon_,minEpsilon_);
    lastState_ = state;
    lastAction_ = -1;
}

int Sarsa::getAction(int state) {
    float random = static_cast<float>((rand()%100)/100.00);
    int action;
    if(random < epsilon_) {
        action = rand() % numActions_;
    }else {
        auto max_itr = max_element(qTable_[state].begin(), qTable_[state].end());
        action =  distance(qTable_[state].begin(), max_itr);
    }
    lastAction_ = action;
    return action;
}

void Sarsa::learn(int reward, int nextState) {
    // SARSA on-policy update:
    // Q(s,a) = Q(s,a) + lr * (reward + gamma * Q(s',a') - Q(s,a))
    // where a' is drawn from the current policy for nextState.
    int prevState = lastState_;
    int prevAction = lastAction_;

    // Choose next action according to current policy (epsilon-greedy).
    int nextAction = getAction(nextState); // this also sets lastAction_ to nextAction

    float currentQ = qTable_[prevState][prevAction];
    float targetQ = reward + gamma_ * qTable_[nextState][nextAction];
    qTable_[prevState][prevAction] = currentQ + lr_ * (targetQ - currentQ);

    // Advance state (lastAction_ already updated by getAction)
    lastState_ = nextState;
}

int Sarsa::forward(int state) {
    auto max_itr = max_element(qTable_[state].begin(), qTable_[state].end());
    int action =  distance(qTable_[state].begin(), max_itr);
    return action;
}
