"""
Reinforcement learning maze example.

Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].

This script is the environment part of this example. The RL is in RL_brain.py.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""


import numpy as np
import time
import sys
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk


UNIT = 40   # pixels
MAZE_H = 4  # grid height
MAZE_W = 4  # grid width


class Maze(tk.Tk, object): # 继承自tkinter的Tk类，表示一个迷宫环境
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r'] # 动作空间，包含上下左右四个移动方向
        self.n_actions = len(self.action_space) # 动作数量
        self.title('maze') # 窗口标题
        self.geometry('{0}x{1}'.format(MAZE_W * UNIT, MAZE_H * UNIT)) # 窗口大小，，{0}x{1}表示宽x高，.format用于格式化字符串
        self._build_maze() # 调用_build_maze方法构建迷宫

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                           height=MAZE_H * UNIT,
                           width=MAZE_W * UNIT) # 创建一个画布，指定背景色为白色，宽度和高度分别为迷宫宽度和高度乘以单位长度

        # create grids
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1) # 两个for循环用于在画布上绘制网格线，形成迷宫的格子结构

        # create origin
        origin = np.array([20, 20]) # 原点坐标，表示迷宫左上角第一个格子的中心位置

        # hell
        hell1_center = origin + np.array([UNIT * 2, UNIT])
        self.hell1 = self.canvas.create_rectangle(
            hell1_center[0] - 15, hell1_center[1] - 15,
            hell1_center[0] + 15, hell1_center[1] + 15,
            fill='black')
        # hell
        hell2_center = origin + np.array([UNIT, UNIT * 2])
        self.hell2 = self.canvas.create_rectangle(
            hell2_center[0] - 15, hell2_center[1] - 15,
            hell2_center[0] + 15, hell2_center[1] + 15,
            fill='black')
        # hell_center表示两个洞的位置，分别位于迷宫的(2,1)和(1,2)格子中间。使用create_rectangle方法在画布上绘制两个黑色矩形，表示洞。

        # create oval
        oval_center = origin + UNIT * 2
        self.oval = self.canvas.create_oval(
            oval_center[0] - 15, oval_center[1] - 15,
            oval_center[0] + 15, oval_center[1] + 15,
            fill='yellow') # oval_center表示终点的位置，位于迷宫的(2,2)格子中间。使用create_oval方法在画布上绘制一个黄色圆形，表示终点。

        # create red rect
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red') # 创建红色矩形，表示智能体的初始位置，位于迷宫的(0,0)格子中间。

        # pack all
        self.canvas.pack() # 将画布添加到窗口中进行显示

    def reset(self): # 重置环境的方法
        self.update()
        time.sleep(0.5)
        self.canvas.delete(self.rect)
        origin = np.array([20, 20])
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')
        # return observation
        return self.canvas.coords(self.rect) # 重置环境的方法，首先调用update方法刷新窗口，然后暂停0.5秒。接着删除当前的红色矩形，并重新创建一个新的红色矩形，表示智能体回到初始位置。最后返回智能体的坐标作为初始状态。

    def step(self, action):
        s = self.canvas.coords(self.rect) # 获取当前智能体的坐标作为状态s
        base_action = np.array([0, 0]) # 初始化基本动作为[0,0]
        if action == 0:   # up
            if s[1] > UNIT:
                base_action[1] -= UNIT # 根据动作选择更新基本动作。如果动作是0（上），且当前y坐标大于UNIT，则将基本动作的y分量减去UNIT，实现向上移动。
        elif action == 1:   # down
            if s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:   # right
            if s[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:   # left
            if s[0] > UNIT:
                base_action[0] -= UNIT

        self.canvas.move(self.rect, base_action[0], base_action[1])  # move agent

        s_ = self.canvas.coords(self.rect)  # next state

        # reward function
        if s_ == self.canvas.coords(self.oval):
            reward = 1
            done = True
            s_ = 'terminal'
        elif s_ in [self.canvas.coords(self.hell1), self.canvas.coords(self.hell2)]:
            reward = -1
            done = True
            s_ = 'terminal'
        else:
            reward = 0
            done = False

        return s_, reward, done

    def render(self):
        time.sleep(0.1)
        self.update() # 渲染环境的方法，通过调用update方法刷新窗口，实现动画效果


def update(): # 更新环境的函数
    for t in range(10):
        s = env.reset()
        while True:
            env.render()
            a = 1
            s, r, done = env.step(a)
            if done:
                break # 在这个函数中，首先重置环境，然后在一个循环中不断渲染环境，执行动作，并获取下一个状态、奖励和是否结束的标志。如果结束则跳出循环，开始下一次迭代。

if __name__ == '__main__':
    env = Maze()
    env.after(100, update)
    env.mainloop()