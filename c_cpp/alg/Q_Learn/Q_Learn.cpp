#include "Q_Learn.hpp"

QLearn::QLearn(int numStates, int numActions, float lr, float gamma, float minEpsilon, float decayRate) :
    epsilon_(1.0), numActions_(numActions), lr_(lr), gamma_(gamma), minEpsilon_(minEpsilon), decayRate_(decayRate) {
    qTable_.resize(numStates, vector<float>(numActions, 0.0));
    cout << "Q-Learning agent created with " << numStates << " states and " << numActions << " actions." << std::endl;
}

void QLearn::reset(int state) {
    epsilon_ *= decayRate_;
    epsilon_ = max(epsilon_,minEpsilon_);
    lastState_ = state;
    lastAction_ = -1;
}

int QLearn::getAction(int state) {
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

void QLearn::learn(int reward, int nextState) {
    //Q(s,a) = Q(s,a) + lr * (reward + gamma * max_a` Q(s,a`) - Q(s,a))
    float currentQ = qTable_[lastState_][lastAction_];
    float targetQ = reward + gamma_ * (*max_element(qTable_[nextState].begin(), qTable_[nextState].end()));
    qTable_[lastState_][lastAction_] = currentQ + lr_ *(targetQ - currentQ);
    lastState_ = nextState;
}

int QLearn::forward(int state) {
    auto max_itr = max_element(qTable_[state].begin(), qTable_[state].end());
    int action =  distance(qTable_[state].begin(), max_itr);
    return action;
}
