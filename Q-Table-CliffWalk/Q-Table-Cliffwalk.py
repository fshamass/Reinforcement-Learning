{"metadata":{"kernelspec":{"language":"python","display_name":"Python 3","name":"python3"},"language_info":{"name":"python","version":"3.10.14","mimetype":"text/x-python","codemirror_mode":{"name":"ipython","version":3},"pygments_lexer":"ipython3","nbconvert_exporter":"python","file_extension":".py"},"kaggle":{"accelerator":"none","dataSources":[],"dockerImageVersionId":30775,"isInternetEnabled":false,"language":"python","sourceType":"script","isGpuEnabled":false}},"nbformat_minor":4,"nbformat":4,"cells":[{"cell_type":"code","source":"import numpy as np\nimport gym\nimport matplotlib.pyplot as plt\n\nclass Q_Table:\n    def __init__(self, states, actions, alpha, gamma, eps_decay_rate = 0.9, min_eps = 0.01):\n        self.num_states = states\n        self.num_actions = actions\n        self.alpha = alpha\n        self.gamma = gamma\n        self.eps = 1\n        self.eps_decay_rate = eps_decay_rate\n        self.min_eps = min_eps\n        #self.q_table = np.random.uniform(low=1,high=100, size=(self.num_states,self.num_actions))\n        self.q_table = np.zeros((self.num_states,self.num_actions))\n    \n    def reset_state(self):\n        self.eps *= self.eps_decay_rate\n        self.eps = min(self.eps, self.min_eps)\n        \n    def get_action(self, state):\n        if np.random.uniform() < self.eps:\n            action = np.random.choice([action for action in range(self.num_actions)]) \n        else:\n            action = np.argmax(self.q_table[state])\n        self.last_state = state\n        self.last_action = action\n        return action\n    \n    def act(self, new_state, reward):\n        target = reward+self.gamma*max(self.q_table[new_state])\n        current = self.q_table[self.last_state][self.last_action]\n        current = current + self.alpha *(target - current)\n        self.q_table[self.last_state][self.last_action] = current\n        \n    def get_policy(self):\n        policy = np.array([np.argmax(self.q_table[state]) for state in range(48)]).reshape(4,12)\n        return policy\n        \n    \nif __name__ == '__main__':\n    print('Hello World')\n    env = gym.make('CliffWalking-v0')\n    q_table = Q_Table(env.observation_space.n, env.action_space.n, 0.02, 0.99)\n    N = 5000\n    rewards = np.empty(N)\n    ave_rewards = []\n    \n    for i in range(N):\n        if i%100 == 0:\n            print(\"Processing round: \", i)\n        state, _ = env.reset()\n        q_table.reset_state()\n        done = False\n        reward = 0\n        while not done:\n            action = q_table.get_action(state)\n            new_state, cur_reward, done, _, _ = env.step(action)\n            reward += cur_reward\n            q_table.act(new_state, cur_reward)\n            state = new_state\n        rewards[i] = reward\n        ave_rewards.append(rewards[max(0,i-100):i].mean())\n    plt.plot(ave_rewards)\n    policy = q_table.get_policy()\n    policy[3,1:11] = -1\n    print(\"\\nEstimated Optimal Policy (UP = 0, RIGHT = 1, DOWN = 2, LEFT = 3, N/A = -1):\")\n    print(policy)\n    print(\"Rewards: \",ave_rewards[-1])","metadata":{"_uuid":"8f2839f25d086af736a60e9eeb907d3b93b6e0e5","_cell_guid":"b1076dfc-b9ad-4769-8c92-a6c4dae69d19","execution":{"iopub.status.busy":"2024-09-26T04:28:23.122197Z","iopub.execute_input":"2024-09-26T04:28:23.122645Z","iopub.status.idle":"2024-09-26T04:28:27.796905Z","shell.execute_reply.started":"2024-09-26T04:28:23.122603Z","shell.execute_reply":"2024-09-26T04:28:27.795764Z"},"trusted":true},"execution_count":17,"outputs":[{"name":"stdout","text":"Hello World\nProcessing round:  0\n","output_type":"stream"},{"name":"stderr","text":"/tmp/ipykernel_29/3391524977.py:63: RuntimeWarning: Mean of empty slice.\n  ave_rewards.append(rewards[max(0,i-100):i].mean())\n","output_type":"stream"},{"name":"stdout","text":"Processing round:  100\nProcessing round:  200\nProcessing round:  300\nProcessing round:  400\nProcessing round:  500\nProcessing round:  600\nProcessing round:  700\nProcessing round:  800\nProcessing round:  900\nProcessing round:  1000\nProcessing round:  1100\nProcessing round:  1200\nProcessing round:  1300\nProcessing round:  1400\nProcessing round:  1500\nProcessing round:  1600\nProcessing round:  1700\nProcessing round:  1800\nProcessing round:  1900\nProcessing round:  2000\nProcessing round:  2100\nProcessing round:  2200\nProcessing round:  2300\nProcessing round:  2400\nProcessing round:  2500\nProcessing round:  2600\nProcessing round:  2700\nProcessing round:  2800\nProcessing round:  2900\nProcessing round:  3000\nProcessing round:  3100\nProcessing round:  3200\nProcessing round:  3300\nProcessing round:  3400\nProcessing round:  3500\nProcessing round:  3600\nProcessing round:  3700\nProcessing round:  3800\nProcessing round:  3900\nProcessing round:  4000\nProcessing round:  4100\nProcessing round:  4200\nProcessing round:  4300\nProcessing round:  4400\nProcessing round:  4500\nProcessing round:  4600\nProcessing round:  4700\nProcessing round:  4800\nProcessing round:  4900\n\nEstimated Optimal Policy (UP = 0, RIGHT = 1, DOWN = 2, LEFT = 3, N/A = -1):\n[[ 2  3  1  3  0  1  1  1  1  2  2  2]\n [ 1  0  0  3  1  0  1  2  2  1  2  2]\n [ 1  1  1  1  1  1  1  1  1  1  1  2]\n [ 0 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1  0]]\nRewards:  -13.0\n","output_type":"stream"},{"output_type":"display_data","data":{"text/plain":"<Figure size 640x480 with 1 Axes>","image/png":"iVBORw0KGgoAAAANSUhEUgAAAjwAAAGdCAYAAAAWp6lMAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjcuNSwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy/xnp5ZAAAACXBIWXMAAA9hAAAPYQGoP6dpAAAymUlEQVR4nO3dfXhU9Z3//9fMJDNJIJMEyQ1IuIkoFEWQoGmoWm/yZdTYNXv1xw+tVbCoCwtdEb5AEBbUXYqXVlvqHbquwu62BW2r3eUmmA3gTYlSbgIGBaWgQSAJCJkJIeRm8vn+ETN1JCKUzDnJ5Pm4rnORnPOecz7nA3pe1+d8zhmHMcYIAAAgijntbgAAAECkEXgAAEDUI/AAAICoR+ABAABRj8ADAACiHoEHAABEPQIPAACIegQeAAAQ9WLsbkBn0NLSokOHDikxMVEOh8Pu5gAAgLNgjFFtba369u0rp/PMYzgEHkmHDh1SZmam3c0AAAB/gwMHDqhfv35nrCHwSEpMTJTU2mFer9fm1gAAgLMRCASUmZkZuo6fCYFHCt3G8nq9BB4AALqYs5mOwqRlAAAQ9Qg8AAAg6hF4AABA1CPwAACAqEfgAQAAUY/AAwAAol5UBZ5nn31WAwcOVFxcnHJycrR582a7mwQAADqBqAk8K1eu1IwZM7Rw4UJt27ZNI0aMkM/nU3V1td1NAwAANouawPPUU0/pvvvu0z333KNhw4Zp6dKlSkhI0Msvv2x30wAAgM2iIvA0NjZq69atysvLC61zOp3Ky8tTaWnpafUNDQ0KBAJhCwAAiF5REXiOHj2qYDCo9PT0sPXp6emqrKw8rX7x4sVKSkoKLXxxKAAA0S0qAs+5mjt3rvx+f2g5cOCA3U0CAAARFBVfHtq7d2+5XC5VVVWFra+qqlJGRsZp9R6PRx6Px6rmAWdkjFGwxagpaNQYbFHTl0tjc9uf5q/rgi1qCho1Nf/198bmFgVbjBqaW39uaA6qucWcZ5vO85zO7+Md0ojzbcP59kFrG+z9e2htw3l+/rz/Ldh/Eh3x79Gc77/HTnEO59uG89tBjNOhefnDzq8R53N8247cgdxut7Kzs1VSUqKCggJJUktLi0pKSjRt2jR7G4eodfREg7ZX1Kgp2KKTjUHVNTTrVFNQp5paVN/U+ntDc1DD+yWrqblFgVNNOtXUolNNQTUGW9TSYrS9okZ7j5xQ8DwDCgB0du4YJ4GnI8yYMUMTJkzQ6NGjddVVV+mXv/yl6urqdM8999jdNFisOdiiIyca5K9vUl1DswKnmnWqMdgaShqbVdcQVE19o5qDRvVNQZ1qCup4XaMCp1oDysnGoE6calZWag9d0MPTGmKaW4PMycag6hubVVPfpJqTTWfVnle3fH7O5+B2ORXrcig2xqlYl1Nul1PumC/Xuf66LjbGoRhn63pPjEvumNb1MS7HOR/zqxzn8XGH7Dt26/HP59jnefDzOvZ5fv48ztzePj/PY5/HDs77b7uL/ndyvuf9tx7b5bR3Fk3UBJ7x48fryJEjWrBggSorKzVy5EgVFRWdNpEZnV9zsEVVtQ2q9NcrcKpZX5xoVF1Ds+qbgjp+slEuh0OXpCfqZGNQgVNNOtnQrNqGZh090aiak41655OjHdKO6tqGb61Jio/VkPREeWKd6umJUXysS55Yl+JinfriRKNONDQrxumQO8apxLhYJbhbt8W6nHI5HPLGx6pvcryuHJgid4wzFF7svPACQDRymPO9MRkFAoGAkpKS5Pf75fV67W5OVGsOtsjlbL2gG2MUONWsSv8p1Zxs1LG6Rm3cc0T/s/OQTjYGz/tYvXq41dMTo56eGPXwuBQX62oNJW6XkuPdinE55IlxqocnRknxsUpJcMsT65QnxqmqwCkdPF6vxLhYxcU65YlpDSrx7hj1cLvkjY+VJ8apC5PjFePqlnP/AcB253L9jpoRHljPmNaJtg6H5HI4dLIpqJ6eGAVbjA7V1OvDwwHVnmrWY2t3SzIK1DerMdgiSUpL9OhYXeMZJ9f2TYpTUoJbvXu6lRgXo7hYl3Z+7ldcrFNxMS4lxccqKT5WPeNi1OPLYJOW6FFiXKyu6J+sdG+cRT0BAOjsCDw4a/76Jn16tE4Ha+q1/2id/v3d/TpW1yhJcjqktuzicjq+dRLuV28XJXpi1KunW6k9PerVw624WJfm3jJUfZLiI3YuAIDuhcCDb3T0RINe2/K53vnkiPZWnzjjnJav5ptgi5Hb5VR6kkcXJserT1K8UhLcysnqpW2fHdfF6Ykakp6oC3q6QwEHAIBIIvBAUuvtqd9uPqDyQ379ef8xfVJ9ot06b1yMBqX2VIbXo0vSE3XlwF5yfzmXxV/fJKfDoV493EpN9MjlPH3ire/S09+LBABApBF4uqmWFqNPv6iTJH10uFa/2fyZ/rT3i3Zr7716kG65vI8uSu0pb1zMNz5BxBd0AAA6KwJPN9D85UThHZ/79dae6tY/Pz7Sbu3QjET9f9n91BQ0SoyL0U2XZah3T95KDQDo2gg8UWxbxXH929v7tLb89C9Q/apL+3p1Rf9kff+SNOV9J413wAAAog6BJwodqW3Qf773mX5V8km72+fcNFQtxujKgb10aV+venj4ZwAAiG5c6aJIpf+Ubl7yto5/7SsP/m5EX31+/KQGXtBDjxZcpp4EHABAN8OVLwps3FOtia/8+bT1M/7PJZp6/eB2n5YCAKA7IfB0YcYY/fjf3z/t6ap/ue1S3TK8jy5gsjEAAJIIPF1WVeCUrn18gxqaW0LrJn//Is0ce4li+W4nAADCEHi6GP/JJt327Lv69IuToXVDMxL1Pz+9mqADAMA3IPB0IX85ckI3PvlW2LqX7h6tvGHpNrUIAICugcDTRXx6tC4s7CTFx+o39+Xo0r5JNrYKAICugcDTBfjrm3TdzzdKki7o4dYbU7+nzF4J9jYKAIAuhEkfXcDd//5+6OcX784m7AAAcI4IPJ3c0yWfaMfnfknS0h9nK3tAL5tbBABA10Pg6cSqAqf0ZPHHkqS/v+JC3XRZhs0tAgCgayLwdGKFv98Z+nnBrcNsbAkAAF0bgaeTKj/o14Y9RyRJf/jHMUrp4ba5RQAAdF0Enk7qyTf3SJLGXHSBRvVPsbk1AAB0bQSeTujAsZPa+HHr6M7cm79jc2sAAOj6CDyd0P//QqmMkb6b1UvD+/FiQQAAzheBp5M5Vteow/5TkqQff3eAza0BACA6EHgiqCnYonuXb9G9y7foZGPzWX1mzQeHQz/nD+8TqaYBANCt8NUSEWSM9L8fVUmSmlvMWX3m99s+lyQ9dMtQORyOiLUNAIDuhBGeTqTii5PaXlEjp0MqGHmh3c0BACBqEHg6kT9sbx3dGXNRb6V542xuDQAA0YPA04m8vv2gJOkHI5i7AwBARyLwdBIHa+r12RcnJUm3MFkZAIAOReDpJP68/5gk6fJ+SUqMi7W5NQAARBcCTyfx/peB56qBvWxuCQAA0YfA00n8+dMvA88gAg8AAB2NwNMJ1DcG9ZcjJyRJI/sn29sYAACiEIGnE/ikulbGSL16uJXa02N3cwAAiDoEnk5g22fHJUlD0hN5uzIAABFA4OkE9lTVSpJGDUi2tyEAAEQpAo9FzBm+Susv1XWSpEvSEy1qDQAA3QuBJ4LO9u7UsZONkqS0RL5OAgCASCDwdAJNwRZJkjuGvw4AACKBK2wn0Nj8ZeBx8dcBAEAkcIXtBBjhAQAgsrjCdgJtIzyxLh5JBwAgEgg8nUBjsC3w8NcBAEAk2HaF/fTTTzVp0iQNGjRI8fHxuuiii7Rw4UI1NjaG1e3cuVPXXHON4uLilJmZqccff/y0fb322msaOnSo4uLiNHz4cK1Zs8aq0+gQTcHWZ9a5pQUAQGTYdoXdvXu3Wlpa9MILL2jXrl36xS9+oaVLl+qhhx4K1QQCAY0dO1YDBgzQ1q1b9cQTT+jhhx/Wiy++GKrZtGmT7rjjDk2aNEnbt29XQUGBCgoKVF5ebsdpnbOPq2oVbDGKcTqUGBdjd3MAAIhKDmPO9Eo8az3xxBN6/vnntW/fPknS888/r3nz5qmyslJut1uSVFhYqDfeeEO7d++WJI0fP151dXVatWpVaD/f/e53NXLkSC1duvSsjhsIBJSUlCS/3y+v19th59MUbNHF89ZKknYsHKuk+NjTahav/UgvvLVPvkvT9cJdozvs2AAARLtzuX53qnsofr9fvXr1Cv1eWlqqa6+9NhR2JMnn82nPnj06fvx4qCYvLy9sPz6fT6Wlpd94nIaGBgUCgbDFDg3NQb3wVmu4u2V4H1vaAABAd9BpAs/evXv19NNP6x/+4R9C6yorK5Wenh5W1/Z7ZWXlGWvatrdn8eLFSkpKCi2ZmZkddRrn5M/7j4d+vnpwb1vaAABAd9DhgaewsFAOh+OMS9vtqDYHDx7UTTfdpHHjxum+++7r6CadZu7cufL7/aHlwIEDET9me9755IgkaURmsi7o6bGlDQAAdAcdPkt25syZmjhx4hlrsrKyQj8fOnRI119/vcaMGRM2GVmSMjIyVFVVFbau7feMjIwz1rRtb4/H45HHY3/A+NNfjkqSfvK9gfY2BACAKNfhgSc1NVWpqalnVXvw4EFdf/31ys7O1iuvvCKnM3zAKTc3V/PmzVNTU5NiY1sn/BYXF2vIkCFKSUkJ1ZSUlGj69OmhzxUXFys3N7djTqijfG1q+OfHT6r8YOvcodysC2xoEAAA3Ydtc3gOHjyo6667Tv3799fPf/5zHTlyRJWVlWFzb370ox/J7XZr0qRJ2rVrl1auXKklS5ZoxowZoZoHHnhARUVFevLJJ7V79249/PDD2rJli6ZNm2bHaYU503uT1+1qHZXqkxSnNC/fkg4AQCTZ9uKX4uJi7d27V3v37lW/fv3CtrU9KZ+UlKQ333xTU6dOVXZ2tnr37q0FCxbo/vvvD9WOGTNGv/nNbzR//nw99NBDuvjii/XGG2/osssus/R8ztUHn9dIksaNtmfCNAAA3Umneg+PXSL1Hp7mYIsGt72HZ8FYJSW03pYzxujaJzbowLF6vTLxSl0/NK3DjgkAQHfRZd/D010c8p/SgWP1cjkdyh6YYndzAACIegQeG2yvaH3/zrA+XnnjTn/7MgAA6FgEHhss+9OnkqQhGYn2NgQAgG6CwGODLZ+1jvDEuuh+AACswBXXYg3NwdDP914zyMaWAADQfRB4LLb/aJ0kKTEuRlm9e9jcGgAAugcCj8U+PXpSkpTVu4ccjjO9mhAAAHQUAo/FPjrc+nUS/S9gdAcAAKsQeCz2/v4vJEnDL+y4FxwCAIAzI/BYxHz57aFtc3iuHNjLzuYAANCtEHgi6OtzdOoamlUVaJAkDWLCMgAAliHwWKhtdKdXD7eSE9w2twYAgO6DwGOhz4/XS5IyU+JtbgkAAN0LgcdCh/2tgedCAg8AAJYi8FjoUM2XgSeZwAMAgJUIPBY6VHNKktQnicADAICVCDwWOnKi9Qmt1ESPzS0BAKB7IfBY6HhdoyTpgh48oQUAgJUIPBY69mXgSSHwAABgKQKPRYItRsdOfjnC05PAAwCAlQg8Fjl+skmm9dsl1IuXDgIAYCkCj0VCt7MSYhXjotsBALASV16LfPHlE1oX9OQJLQAArEbgiaCvfnXo0S9HeLidBQCA9Qg8FqkJPaEVa3NLAADofgg8Fjl+skmSlBzPCA8AAFYj8Fikpr51hCeZER4AACxH4LFIzZcjPCnM4QEAwHIEHov461sDT1I8IzwAAFiNwGORuoZmSVIPT4zNLQEAoPsh8FikrrE18PT0uGxuCQAA3Q+BxyJ1DUFJUoKbER4AAKxG4LFI2y2tntzSAgDAcgQeizQ0t0iSEtzc0gIAwGoEHosxwgMAgPUIPBZLIPAAAGA5Ao/FEmK5pQUAgNUIPBHkcIT/Hh/rktPpaL8YAABEDIHHQkxYBgDAHgQeC8VxOwsAAFsQeCwUF0t3AwBgB67AFornlhYAALYg8FgoLobAAwCAHQg8FmKEBwAAe3SKwNPQ0KCRI0fK4XCorKwsbNvOnTt1zTXXKC4uTpmZmXr88cdP+/xrr72moUOHKi4uTsOHD9eaNWssavm58TDCAwCALTpF4Jk9e7b69u172vpAIKCxY8dqwIAB2rp1q5544gk9/PDDevHFF0M1mzZt0h133KFJkyZp+/btKigoUEFBgcrLy608hbPCpGUAAOxh+xV47dq1evPNN/Xzn//8tG2//vWv1djYqJdfflmXXnqpbr/9dv3TP/2TnnrqqVDNkiVLdNNNN2nWrFn6zne+o3/5l3/RqFGj9Mwzz1h5GmclnsfSAQCwha2Bp6qqSvfdd5/+8z//UwkJCadtLy0t1bXXXiu32x1a5/P5tGfPHh0/fjxUk5eXF/Y5n8+n0tLSyDb+b8B7eAAAsIdtgccYo4kTJ2ry5MkaPXp0uzWVlZVKT08PW9f2e2Vl5Rlr2ra3p6GhQYFAIGyxAre0AACwR4dfgQsLC+VwOM647N69W08//bRqa2s1d+7cjm7Ct1q8eLGSkpJCS2ZmpiXHZYQHAAB7xHT0DmfOnKmJEyeesSYrK0vr169XaWmpPB5P2LbRo0frzjvv1PLly5WRkaGqqqqw7W2/Z2RkhP5sr6Zte3vmzp2rGTNmhH4PBAIRCT2Or317aKyLER4AAOzQ4YEnNTVVqamp31r3q1/9Sv/6r/8a+v3QoUPy+XxauXKlcnJyJEm5ubmaN2+empqaFBsbK0kqLi7WkCFDlJKSEqopKSnR9OnTQ/sqLi5Wbm7uNx7b4/GcFrSsEOPim9IBALBDhwees9W/f/+w33v27ClJuuiii9SvXz9J0o9+9CM98sgjmjRpkubMmaPy8nItWbJEv/jFL0Kfe+CBB/T9739fTz75pPLz87VixQpt2bIl7NH1ziLWyQgPAAB26NRX4KSkJL355pvav3+/srOzNXPmTC1YsED3339/qGbMmDH6zW9+oxdffFEjRozQ7373O73xxhu67LLLbGx5+xjhAQDAHraN8HzdwIEDZYw5bf3ll1+ud95554yfHTdunMaNGxeppnWYGObwAABgC67AFop1MsIDAIAdCDwWYoQHAAB7cAW2UCxzeAAAsAWBx0IxPKUFAIAtuAJbiKe0AACwB4HHQtzSAgDAHgQeC3FLCwAAe3AFthC3tAAAsAeBx0KM8AAAYA+uwBZihAcAAHsQeCzEl4cCAGAPrsAWYoQHAAB7EHgsxGPpAADYg8BjISYtAwBgD67AFuKWFgAA9iDwWCiWb0sHAMAWXIEtFONkhAcAADsQeCwUwwgPAAC24ApsIZ7SAgDAHgQeC/GUFgAA9uAKbCFGeAAAsAeBx0IOB4EHAAA7EHgAAEDUI/AAAICoR+ABAABRj8ADAACiHoHHIrxlGQAA+xB4LMIXhwIAYB8Cj0VieekgAAC24SpsEUZ4AACwD4HHInxxKAAA9uEqbJFYJi0DAGAbAo9FnAQeAABsQ+CxiIvAAwCAbQg8FnHyxaEAANiGwGMR8g4AAPYh8FiEER4AAOxD4LEIU3gAALAPgccijPAAAGAfAo9FHAQeAABsQ+CxCLe0AACwD4HHItzSAgDAPgQeizDCAwCAfQg8FuGrJQAAsA+BxyLc0gIAwD62B57Vq1crJydH8fHxSklJUUFBQdj2iooK5efnKyEhQWlpaZo1a5aam5vDajZu3KhRo0bJ4/Fo8ODBWrZsmXUncJYY4AEAwD4xdh7897//ve677z797Gc/0w033KDm5maVl5eHtgeDQeXn5ysjI0ObNm3S4cOHdffddys2NlY/+9nPJEn79+9Xfn6+Jk+erF//+tcqKSnRvffeqz59+sjn89l1aqfhsXQAAOzjMMYYOw7c3NysgQMH6pFHHtGkSZParVm7dq1uvfVWHTp0SOnp6ZKkpUuXas6cOTpy5IjcbrfmzJmj1atXhwWl22+/XTU1NSoqKjqrtgQCASUlJcnv98vr9Z7/yX3FwMLVkqScQb208h9yO3TfAAB0Z+dy/bbtlta2bdt08OBBOZ1OXXHFFerTp49uvvnmsOBSWlqq4cOHh8KOJPl8PgUCAe3atStUk5eXF7Zvn8+n0tLSbzx2Q0ODAoFA2BJpzOEBAMA+tgWeffv2SZIefvhhzZ8/X6tWrVJKSoquu+46HTt2TJJUWVkZFnYkhX6vrKw8Y00gEFB9fX27x168eLGSkpJCS2ZmZoeeW3ucts+WAgCg++rwy3BhYaEcDscZl927d6ulpUWSNG/ePP3whz9Udna2XnnlFTkcDr322msd3awwc+fOld/vDy0HDhyI6PEkRngAALBTh09anjlzpiZOnHjGmqysLB0+fFiSNGzYsNB6j8ejrKwsVVRUSJIyMjK0efPmsM9WVVWFtrX92bbuqzVer1fx8fHtHt/j8cjj8Zz9SXUAAg8AAPbp8MCTmpqq1NTUb63Lzs6Wx+PRnj17dPXVV0uSmpqa9Omnn2rAgAGSpNzcXC1atEjV1dVKS0uTJBUXF8vr9YaCUm5urtasWRO27+LiYuXmdq4JwjyWDgCAfWybWeL1ejV58mQtXLhQb775pvbs2aMpU6ZIksaNGydJGjt2rIYNG6a77rpLO3bs0Lp16zR//nxNnTo1NEIzefJk7du3T7Nnz9bu3bv13HPP6dVXX9WDDz5o16m1ixEeAADsY+t7eJ544gnFxMTorrvuUn19vXJycrR+/XqlpKRIklwul1atWqUpU6YoNzdXPXr00IQJE/Too4+G9jFo0CCtXr1aDz74oJYsWaJ+/frppZde6lTv4JF4Dw8AAHay7T08nYkV7+EZOyxdL949ukP3DQBAd9Yl3sPT3XBLCwAA+xB4LMJ7eAAAsA+XYYswhwcAAPsQeCzCLS0AAOxD4LGIi7wDAIBtCDwW4ZYWAAD2IfBYhLwDAIB9CDwWYQ4PAAD2IfBYhLgDAIB9CDwWYYQHAAD7EHgsQt4BAMA+BB4AABD1CDwWYYQHAAD7EHgsQ+IBAMAuBB6LMMIDAIB9CDwAACDqEXgswgAPAAD2IfBYhFtaAADYh8BjEQdjPAAA2IbAAwAAoh6BBwAARD0Cj0WYwwMAgH0IPBYh7wAAYB8Cj0UcDPEAAGAbAg8AAIh6BB4AABD1CDwW4Y4WAAD2IfBYhBcPAgBgHwKPRRjhAQDAPgQei5B3AACwD4EHAABEPQKPRbilBQCAfQg8AAAg6hF4LMKblgEAsA+BxyLEHQAA7EPgAQAAUY/AYxWGeAAAsA2BxyK8aRkAAPsQeCzCnGUAAOxD4LEIeQcAAPsQeAAAQNQj8FiEW1oAANiHwGMRJi0DAGAfAo9FGOEBAMA+BB6LkHcAALCPrYHn448/1m233abevXvL6/Xq6quv1oYNG8JqKioqlJ+fr4SEBKWlpWnWrFlqbm4Oq9m4caNGjRolj8ejwYMHa9myZRaeBQAA6OxsDTy33nqrmpubtX79em3dulUjRozQrbfeqsrKSklSMBhUfn6+GhsbtWnTJi1fvlzLli3TggULQvvYv3+/8vPzdf3116usrEzTp0/Xvffeq3Xr1tl1WgAAoJNxGGOMHQc+evSoUlNT9fbbb+uaa66RJNXW1srr9aq4uFh5eXlau3atbr31Vh06dEjp6emSpKVLl2rOnDk6cuSI3G635syZo9WrV6u8vDy079tvv101NTUqKio6q7YEAgElJSXJ7/fL6/V26HkOLFwtSfqnGy/WjP9zSYfuGwCA7uxcrt+2jfBccMEFGjJkiP7jP/5DdXV1am5u1gsvvKC0tDRlZ2dLkkpLSzV8+PBQ2JEkn8+nQCCgXbt2hWry8vLC9u3z+VRaWvqNx25oaFAgEAhbIo05PAAA2CfGrgM7HA797//+rwoKCpSYmCin06m0tDQVFRUpJSVFklRZWRkWdiSFfm+77fVNNYFAQPX19YqPjz/t2IsXL9YjjzwSidMCAACdUIeP8BQWFsrhcJxx2b17t4wxmjp1qtLS0vTOO+9o8+bNKigo0A9+8AMdPny4o5sVZu7cufL7/aHlwIEDET2exGPpAADYqcNHeGbOnKmJEyeesSYrK0vr16/XqlWrdPz48dB9t+eee07FxcVavny5CgsLlZGRoc2bN4d9tqqqSpKUkZER+rNt3VdrvF5vu6M7kuTxeOTxeP6W0/ub8eJBAADs0+GBJzU1Vampqd9ad/LkSUmS0xk+yOR0OtXS0iJJys3N1aJFi1RdXa20tDRJUnFxsbxer4YNGxaqWbNmTdg+iouLlZube97n0pEY4QEAwD62TVrOzc1VSkqKJkyYoB07dujjjz/WrFmzQo+ZS9LYsWM1bNgw3XXXXdqxY4fWrVun+fPna+rUqaERmsmTJ2vfvn2aPXu2du/ereeee06vvvqqHnzwQbtOrV3kHQAA7GNb4Ondu7eKiop04sQJ3XDDDRo9erTeffdd/fGPf9SIESMkSS6XS6tWrZLL5VJubq5+/OMf6+6779ajjz4a2s+gQYO0evVqFRcXa8SIEXryySf10ksvyefz2XVqAACgk7HtPTydiRXv4fm/Yy/RtBsu7tB9AwDQnXWJ9/B0Nw4m8QAAYBsCDwAAiHoEHgAAEPUIPAAAIOoReCzCFB4AAOxD4LEIb1oGAMA+BB6LMMIDAIB9CDwWIe8AAGAfAg8AAIh6BB6LcEsLAAD7EHgswqRlAADsQ+CxCCM8AADYh8ADAACiHoEHAABEPQKPRfi2dAAA7EPgsQhxBwAA+xB4AABA1CPwWIQ7WgAA2IfAAwAAoh6BxyIM8AAAYB8Cj0V4SgsAAPsQeCxC3gEAwD4EHouQdwAAsA+BBwAARD0Cj1W4pwUAgG0IPBYh7gAAYB8Cj0UY4AEAwD4EHos4GOMBAMA2BB4AABD1CDwW4ZYWAAD2IfAAAICoR+CxCAM8AADYh8ADAACiHoHHIszhAQDAPgQei/BYOgAA9iHwWIW8AwCAbQg8FiHvAABgHwIPAACIegQeiziYtQwAgG0IPBYh7gAAYB8Cj0UY4AEAwD4EHosQeAAAsA+BxyLG2N0CAAC6LwIPAACIegQei3BLCwAA+0Qs8CxatEhjxoxRQkKCkpOT262pqKhQfn6+EhISlJaWplmzZqm5uTmsZuPGjRo1apQ8Ho8GDx6sZcuWnbafZ599VgMHDlRcXJxycnK0efPmCJwRAADoqiIWeBobGzVu3DhNmTKl3e3BYFD5+flqbGzUpk2btHz5ci1btkwLFiwI1ezfv1/5+fm6/vrrVVZWpunTp+vee+/VunXrQjUrV67UjBkztHDhQm3btk0jRoyQz+dTdXV1pE4NAAB0MQ5jIjuddtmyZZo+fbpqamrC1q9du1a33nqrDh06pPT0dEnS0qVLNWfOHB05ckRut1tz5szR6tWrVV5eHvrc7bffrpqaGhUVFUmScnJydOWVV+qZZ56RJLW0tCgzM1M//elPVVhYeFZtDAQCSkpKkt/vl9fr7YCz/quBhaslSb8cP1IFV1zYofsGAKA7O5frt21zeEpLSzV8+PBQ2JEkn8+nQCCgXbt2hWry8vLCPufz+VRaWiqpdRRp69atYTVOp1N5eXmhmvY0NDQoEAiELQAAIHrZFngqKyvDwo6k0O+VlZVnrAkEAqqvr9fRo0cVDAbbrWnbR3sWL16spKSk0JKZmdkRpwQAADqpcwo8hYWFcjgcZ1x2794dqbZ2mLlz58rv94eWAwcORPyYPKUFAIB9Ys6leObMmZo4ceIZa7Kyss5qXxkZGac9TVVVVRXa1vZn27qv1ni9XsXHx8vlcsnlcrVb07aP9ng8Hnk8nrNqJwAA6PrOKfCkpqYqNTW1Qw6cm5urRYsWqbq6WmlpaZKk4uJieb1eDRs2LFSzZs2asM8VFxcrNzdXkuR2u5Wdna2SkhIVFBRIap20XFJSomnTpnVIOwEAQNcXsTk8FRUVKisrU0VFhYLBoMrKylRWVqYTJ05IksaOHathw4bprrvu0o4dO7Ru3TrNnz9fU6dODY2+TJ48Wfv27dPs2bO1e/duPffcc3r11Vf14IMPho4zY8YM/du//ZuWL1+ujz76SFOmTFFdXZ3uueeeSJ0aAADoYs5phOdcLFiwQMuXLw/9fsUVV0iSNmzYoOuuu04ul0urVq3SlClTlJubqx49emjChAl69NFHQ58ZNGiQVq9erQcffFBLlixRv3799NJLL8nn84Vqxo8fryNHjmjBggWqrKzUyJEjVVRUdNpEZgAA0H1F/D08XYEV7+FZcvtI3TaS9/AAANBRusR7eAAAAKxC4AEAAFGPwAMAAKIegcciDt48CACAbQg8AAAg6hF4AABA1CPwWIQbWgAA2IfAAwAAoh6BBwAARD0Cj0V4SAsAAPsQeAAAQNQj8AAAgKhH4LGIg+e0AACwDYHHIkbd/kvpAQCwDYEHAABEPQKPRbilBQCAfQg8AAAg6hF4AABA1CPwWIQXDwIAYB8CDwAAiHoEHgAAEPUIPBbhjhYAAPYh8AAAgKhH4AEAAFGPwGMRntICAMA+BB4AABD1CDwAACDqEXgAAEDUI/AAAICoR+ABAABRj8BjGR7TAgDALgQeAAAQ9Qg8AAAg6hF4LMKLBwEAsA+BBwAARD0CDwAAiHoEHotwRwsAAPsQeAAAQNQj8AAAgKhH4LGIg8e0AACwDYHHIsYYu5sAAEC3ReABAABRj8BjEW5pAQBgHwIPAACIegQeAAAQ9SIWeBYtWqQxY8YoISFBycnJp23fsWOH7rjjDmVmZio+Pl7f+c53tGTJktPqNm7cqFGjRsnj8Wjw4MFatmzZaTXPPvusBg4cqLi4OOXk5Gjz5s0ROKPzww0tAADsE7HA09jYqHHjxmnKlCntbt+6davS0tL0X//1X9q1a5fmzZunuXPn6plnngnV7N+/X/n5+br++utVVlam6dOn695779W6detCNStXrtSMGTO0cOFCbdu2TSNGjJDP51N1dXWkTg0AAHQxDhPh56WXLVum6dOnq6am5ltrp06dqo8++kjr16+XJM2ZM0erV69WeXl5qOb2229XTU2NioqKJEk5OTm68sorQ0GppaVFmZmZ+ulPf6rCwsKzamMgEFBSUpL8fr+8Xu85nuGZDSxcLUl66e7RyhuW3qH7BgCgOzuX63enmsPj9/vVq1ev0O+lpaXKy8sLq/H5fCotLZXUOoq0devWsBqn06m8vLxQTXsaGhoUCATClkjjIS0AAOzTaQLPpk2btHLlSt1///2hdZWVlUpPDx8VSU9PVyAQUH19vY4ePapgMNhuTWVl5Tcea/HixUpKSgotmZmZHXsyAACgUzmnwFNYWCiHw3HGZffu3efciPLyct12221auHChxo4de86fP1dz586V3+8PLQcOHIj4MQEAgH1izqV45syZmjhx4hlrsrKyzqkBH374oW688Ubdf//9mj9/fti2jIwMVVVVha2rqqqS1+tVfHy8XC6XXC5XuzUZGRnfeEyPxyOPx3NO7Txf3NICAMA+5xR4UlNTlZqa2mEH37Vrl2644QZNmDBBixYtOm17bm6u1qxZE7auuLhYubm5kiS3263s7GyVlJSooKBAUuuk5ZKSEk2bNq3D2gkAALq2cwo856KiokLHjh1TRUWFgsGgysrKJEmDBw9Wz549VV5erhtuuEE+n08zZswIzblxuVyhUDV58mQ988wzmj17tn7yk59o/fr1evXVV7V69erQcWbMmKEJEyZo9OjRuuqqq/TLX/5SdXV1uueeeyJ1an+TfikJdjcBAIDuy0TIhAkTjKTTlg0bNhhjjFm4cGG72wcMGBC2nw0bNpiRI0cat9ttsrKyzCuvvHLasZ5++mnTv39/43a7zVVXXWXee++9c2qr3+83kozf7/8bz/abbfn0C/M/Ow52+H4BAOjuzuX6HfH38HQFkXwPDwAAiIwu+x4eAACASCDwAACAqEfgAQAAUY/AAwAAoh6BBwAARD0CDwAAiHoEHgAAEPUIPAAAIOoReAAAQNQj8AAAgKhH4AEAAFGPwAMAAKIegQcAAES9GLsb0Bm0fWF8IBCwuSUAAOBstV23267jZ0LgkVRbWytJyszMtLklAADgXNXW1iopKemMNQ5zNrEoyrW0tOjQoUNKTEyUw+Ho0H0HAgFlZmbqwIED8nq9Hbpv/BX9bA362Tr0tTXoZ2tEqp+NMaqtrVXfvn3ldJ55lg4jPJKcTqf69esX0WN4vV7+Y7IA/WwN+tk69LU16GdrRKKfv21kpw2TlgEAQNQj8AAAgKhH4Ikwj8ejhQsXyuPx2N2UqEY/W4N+tg59bQ362RqdoZ+ZtAwAAKIeIzwAACDqEXgAAEDUI/AAAICoR+ABAABRj8ATQc8++6wGDhyouLg45eTkaPPmzXY3qVN7++239YMf/EB9+/aVw+HQG2+8EbbdGKMFCxaoT58+io+PV15enj755JOwmmPHjunOO++U1+tVcnKyJk2apBMnToTV7Ny5U9dcc43i4uKUmZmpxx9/PNKn1qksXrxYV155pRITE5WWlqaCggLt2bMnrObUqVOaOnWqLrjgAvXs2VM//OEPVVVVFVZTUVGh/Px8JSQkKC0tTbNmzVJzc3NYzcaNGzVq1Ch5PB4NHjxYy5Yti/TpdRrPP/+8Lr/88tCL1nJzc7V27drQdvo4Mh577DE5HA5Nnz49tI6+7hgPP/ywHA5H2DJ06NDQ9k7fzwYRsWLFCuN2u83LL79sdu3aZe677z6TnJxsqqqq7G5ap7VmzRozb94884c//MFIMq+//nrY9scee8wkJSWZN954w+zYscP83d/9nRk0aJCpr68P1dx0001mxIgR5r333jPvvPOOGTx4sLnjjjtC2/1+v0lPTzd33nmnKS8vN7/97W9NfHy8eeGFF6w6Tdv5fD7zyiuvmPLyclNWVmZuueUW079/f3PixIlQzeTJk01mZqYpKSkxW7ZsMd/97nfNmDFjQtubm5vNZZddZvLy8sz27dvNmjVrTO/evc3cuXNDNfv27TMJCQlmxowZ5sMPPzRPP/20cblcpqioyNLztct///d/m9WrV5uPP/7Y7Nmzxzz00EMmNjbWlJeXG2Po40jYvHmzGThwoLn88svNAw88EFpPX3eMhQsXmksvvdQcPnw4tBw5ciS0vbP3M4EnQq666iozderU0O/BYND07dvXLF682MZWdR1fDzwtLS0mIyPDPPHEE6F1NTU1xuPxmN/+9rfGGGM+/PBDI8n8+c9/DtWsXbvWOBwOc/DgQWOMMc8995xJSUkxDQ0NoZo5c+aYIUOGRPiMOq/q6mojybz11lvGmNZ+jY2NNa+99lqo5qOPPjKSTGlpqTGmNZw6nU5TWVkZqnn++eeN1+sN9e3s2bPNpZdeGnas8ePHG5/PF+lT6rRSUlLMSy+9RB9HQG1trbn44otNcXGx+f73vx8KPPR1x1m4cKEZMWJEu9u6Qj9zSysCGhsbtXXrVuXl5YXWOZ1O5eXlqbS01MaWdV379+9XZWVlWJ8mJSUpJycn1KelpaVKTk7W6NGjQzV5eXlyOp16//33QzXXXnut3G53qMbn82nPnj06fvy4RWfTufj9fklSr169JElbt25VU1NTWF8PHTpU/fv3D+vr4cOHKz09PVTj8/kUCAS0a9euUM1X99FW0x3/GwgGg1qxYoXq6uqUm5tLH0fA1KlTlZ+ff1p/0Ncd65NPPlHfvn2VlZWlO++8UxUVFZK6Rj8TeCLg6NGjCgaDYX+pkpSenq7KykqbWtW1tfXbmfq0srJSaWlpYdtjYmLUq1evsJr29vHVY3QnLS0tmj59ur73ve/psssuk9TaD263W8nJyWG1X+/rb+vHb6oJBAKqr6+PxOl0Oh988IF69uwpj8ejyZMn6/XXX9ewYcPo4w62YsUKbdu2TYsXLz5tG33dcXJycrRs2TIVFRXp+eef1/79+3XNNdeotra2S/Qz35YOdGNTp05VeXm53n33XbubEpWGDBmisrIy+f1+/e53v9OECRP01ltv2d2sqHLgwAE98MADKi4uVlxcnN3NiWo333xz6OfLL79cOTk5GjBggF599VXFx8fb2LKzwwhPBPTu3Vsul+u02elVVVXKyMiwqVVdW1u/nalPMzIyVF1dHba9ublZx44dC6tpbx9fPUZ3MW3aNK1atUobNmxQv379QuszMjLU2NiompqasPqv9/W39eM31Xi93i7xP8eO4Ha7NXjwYGVnZ2vx4sUaMWKElixZQh93oK1bt6q6ulqjRo1STEyMYmJi9NZbb+lXv/qVYmJilJ6eTl9HSHJysi655BLt3bu3S/ybJvBEgNvtVnZ2tkpKSkLrWlpaVFJSotzcXBtb1nUNGjRIGRkZYX0aCAT0/vvvh/o0NzdXNTU12rp1a6hm/fr1amlpUU5OTqjm7bffVlNTU6imuLhYQ4YMUUpKikVnYy9jjKZNm6bXX39d69ev16BBg8K2Z2dnKzY2Nqyv9+zZo4qKirC+/uCDD8ICZnFxsbxer4YNGxaq+eo+2mq6838DLS0tamhooI870I033qgPPvhAZWVloWX06NG68847Qz/T15Fx4sQJ/eUvf1GfPn26xr/p8572jHatWLHCeDwes2zZMvPhhx+a+++/3yQnJ4fNTke42tpas337drN9+3YjyTz11FNm+/bt5rPPPjPGtD6WnpycbP74xz+anTt3mttuu63dx9KvuOIK8/7775t3333XXHzxxWGPpdfU1Jj09HRz1113mfLycrNixQqTkJDQrR5LnzJliklKSjIbN24Me7z05MmToZrJkyeb/v37m/Xr15stW7aY3Nxck5ubG9re9njp2LFjTVlZmSkqKjKpqantPl46a9Ys89FHH5lnn322Wz3GW1hYaN566y2zf/9+s3PnTlNYWGgcDod58803jTH0cSR99SktY+jrjjJz5kyzceNGs3//fvOnP/3J5OXlmd69e5vq6mpjTOfvZwJPBD399NOmf//+xu12m6uuusq89957djepU9uwYYORdNoyYcIEY0zro+n//M//bNLT043H4zE33nij2bNnT9g+vvjiC3PHHXeYnj17Gq/Xa+655x5TW1sbVrNjxw5z9dVXG4/HYy688ELz2GOPWXWKnUJ7fSzJvPLKK6Ga+vp684//+I8mJSXFJCQkmL//+783hw8fDtvPp59+am6++WYTHx9vevfubWbOnGmamprCajZs2GBGjhxp3G63ycrKCjtGtPvJT35iBgwYYNxut0lNTTU33nhjKOwYQx9H0tcDD33dMcaPH2/69Olj3G63ufDCC8348ePN3r17Q9s7ez87jDHm/MeJAAAAOi/m8AAAgKhH4AEAAFGPwAMAAKIegQcAAEQ9Ag8AAIh6BB4AABD1CDwAACDqEXgAAEDUI/AAAICoR+ABAABRj8ADAACiHoEHAABEvf8H2122wl2wDGYAAAAASUVORK5CYII="},"metadata":{}}]}]}