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


class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        # 定义动作空间
        self.action_space = ['u', 'd', 'r', 'l']
        self.n_actions = len(self.action_space)
        self.title('maze')
        self.geometry('{0}x{1}'.format(MAZE_W * UNIT, MAZE_H * UNIT))
        self._build_maze()

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                           height=MAZE_H * UNIT,
                           width=MAZE_W * UNIT)

        # create grids
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

        # 原点(0,0) -> 左上角
        origin = np.array([20, 20])

        # hell (障碍物)
        hell1_center = origin + np.array([UNIT * 2, UNIT])
        self.hell1 = self.canvas.create_rectangle(
            hell1_center[0] - 15, hell1_center[1] - 15,
            hell1_center[0] + 15, hell1_center[1] + 15,
            fill='black')

        hell2_center = origin + np.array([UNIT, UNIT * 2])
        self.hell2 = self.canvas.create_rectangle(
            hell2_center[0] - 15, hell2_center[1] - 15,
            hell2_center[0] + 15, hell2_center[1] + 15,
            fill='black')

        # 终点 (2,2)
        oval_center = origin + np.array([UNIT * 2, UNIT * 2])
        self.oval = self.canvas.create_oval(
            oval_center[0] - 15, oval_center[1] - 15,
            oval_center[0] + 15, oval_center[1] + 15,
            fill='yellow')

        # 创建红色方块（智能体）
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')

        self.canvas.pack()

    def reset(self):
        self.update()
        time.sleep(0.5)
        self.canvas.delete(self.rect)
        origin = np.array([20, 20])
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')
        # 返回初始状态 (0,0)
        return (0, 0)

    def step(self, action):
        # 当前像素坐标
        s = self.canvas.coords(self.rect)  # [x1, y1, x2, y2]
        col = int((s[0] - 5) // UNIT)   # 格子列索引
        row = int((s[1] - 5) // UNIT)   # 格子行索引

        # 动作对应的坐标变化
        if action == 0 and row > 0:        # up
            row -= 1
        elif action == 1 and row < MAZE_H-1:  # down
            row += 1
        elif action == 2 and col < MAZE_W-1:  # right
            col += 1
        elif action == 3 and col > 0:      # left
            col -= 1

        # 移动像素
        new_x = col * UNIT + 20
        new_y = row * UNIT + 20
        self.canvas.coords(self.rect,
            new_x - 15, new_y - 15,
            new_x + 15, new_y + 15)

        # 奖励与终止判断
        if (row, col) == (2, 2):   # 到达终点
            reward, done = 1, True
        elif (row, col) in [(1, 2), (2, 1)]:  # 陷阱
            reward, done = -1, True
        else:
            reward, done = 0, False

        return (row, col), reward, done

    def render(self):
        time.sleep(0.3)
        self.update()


def update(n_round):
    for episode in range(n_round):
        s = env.reset()
        while True:
            env.render()
            a = np.random.choice([0,1,2,3])   # 随机动作
            s_, r, done = env.step(a)
            print("round:" + str(episode) +" " + f"state:{s} action:{a} -> state':{s_}, reward:{r}")
            s = s_
            if done:
                break

if __name__ == '__main__':
    n_round = 10
    env = Maze()
    env.after(100, update(n_round))
    env.mainloop()