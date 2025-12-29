"""
This part of code is the Q learning brain, which is a brain of the agent.
All decisions are made in here.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""

import numpy as np
import pandas as pd


class QLearningTable:
    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):
        self.actions = actions  # a list
        self.lr = learning_rate # learning rate
        self.gamma = reward_decay # reward decay
        self.epsilon = e_greedy # greedy policy
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64) # initialize q table

    def choose_action(self, observation):
        self.check_state_exist(observation) # check whether the state exists
        # action selection
        if np.random.uniform() < self.epsilon: # exploit policy
            # choose best action
            state_action = self.q_table.loc[observation, :] # get the actions for this state
            # some actions may have the same value, randomly choose on in these actions
            action = np.random.choice(state_action[state_action == np.max(state_action)].index) # choose the action with the highest Q value
        else:
            # choose random action
            action = np.random.choice(self.actions)
        return action

    def learn(self, s, a, r, s_):
        self.check_state_exist(s_) # check whether the next state exists
        q_predict = self.q_table.loc[s, a] # current Q value
        if s_ != 'terminal': # next state is not terminal
            q_target = r + self.gamma * self.q_table.loc[s_, :].max()  # 计算目标Q值，使用贝尔曼方程，考虑当前奖励和下一个状态的最大Q值
        else:
            q_target = r  # next state is terminal
        self.q_table.loc[s, a] += self.lr * (q_target - q_predict)  # update

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table
            self.q_table = pd.concat(
                            [self.q_table,
                             pd.Series([0]*len(self.actions), index=self.q_table.columns, name=state).to_frame().T]
)