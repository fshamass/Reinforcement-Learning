#ifndef Q_LEARN_HPP
#define Q_LEARN_HPP

#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

class QLearn {
    public:
        QLearn(int numStates, int numActions, float lr=0.02, float gamma=0.99, float minEpsilon=0.01, float decayRate=0.99);
        void reset(int state);
        int  getAction(int state);
        void learn(int reward, int nextState);
        int  forward(int state);
    private:
        vector<vector<float>> qTable_;
        int numActions_;
        float epsilon_;
        float lr_;
        float gamma_;
        float minEpsilon_;
        float decayRate_;
        int lastState_;
        int lastAction_;
};
#endif