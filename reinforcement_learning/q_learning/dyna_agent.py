import random
from more_itertools import all_equal

from utils import ActionContainer, Coordinate
import maze

actions = ActionContainer(up=Coordinate(0, 1), right=Coordinate(1, 0), down=Coordinate(0, -1), left=Coordinate(-1, 0))
exp_rate = 0.2 # chance of taking a random action instead of the greedy one
learning_rate = 0.1
random_updates = episodes = model = Q_values = None

def choose_action(state):
    if random.random() <= exp_rate or all_equal(Q_values[state]): 
        return random.choice(actions)
    return max(actions, key=lambda a: Q_values[state][a])

def compute_Q_value(state, action, next_state, reward):
    return learning_rate * (reward + max(Q_values[next_state].values()) - Q_values[state][action])

def randomly_update_Q_values():
    # update the Q-value for random previous state/action combos
    for _ in range(random_updates):
        r_state = random.choice(list(model.keys()))
        r_action = random.choice(list(model[r_state].keys()))
        r_reward, r_next_state = model[r_state][r_action]
        Q_values[r_state][r_action] += compute_Q_value(r_state, r_action, r_next_state, r_reward)

def play():
    steps_per_episode = []
    for _ in range(episodes):
        state = maze.start
        actions_taken = 0
        """
        continually choose actions, either the best available or a random until the goal is reached.
        The Q-value of each state/action-combo is correlated with its distance from the goal.
        """
        while not state == maze.goal:
            actions_taken += 1
            
            # get action, get its resulting state, get the reward for the state
            action = choose_action(state)
            next_state = maze.get_next_state(state, action)
            reward = maze.get_reward(next_state)
                
            # update Q-values and model, then go to next state
            Q_values[state][action] += compute_Q_value(state, action, next_state, reward)
            model[state][action] = (reward, next_state)
            state = next_state

            # Reinforce the learning process
            randomly_update_Q_values()
        
        steps_per_episode.append(actions_taken)
    
    return steps_per_episode
