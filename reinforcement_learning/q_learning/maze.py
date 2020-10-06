import numpy as np

from utils import Coordinate

rows = 6
cols = 9
start = Coordinate(2, 0)
goal = Coordinate(0, 8)
blocks = [(1, 2), (2, 2), (3, 2), (0, 7), (1, 7), (2, 7), (4, 5)]

maze = np.zeros((rows, cols))
for b in blocks:
    maze[b] = -1

def get_next_state(state, action):
    s = Coordinate(state.x + action.x, state.y + action.y)
    if s.x in range(rows) and s.y in range(cols) and s not in blocks:
        return s
    return state

def get_reward(state):
    return state == goal

maze_translation = lambda v: {1: '*', -1: 'z', 0: '0'}[v]
def show_maze(state=start):
    maze[state] = 1
    for i in range(0, rows):
        print('-------------------------------------')
        out = '| ' + " | ".join(map(maze_translation, maze[i])) + ' |'
        print(out)
    print('-------------------------------------')
