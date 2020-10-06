from collections import defaultdict
import matplotlib.pyplot as plt

import maze
import dyna_agent

# based off of https://towardsdatascience.com/reinforcement-learning-model-based-planning-methods-5e99cae0abb8

def set_up_agent(random_updates, episodes):
    dyna_agent.random_updates = random_updates
    dyna_agent.episodes = episodes
    dyna_agent.model = defaultdict(dict)
    dyna_agent.Q_values = {
        (r, c): {a: 0 for a in dyna_agent.actions}
        for c in range(maze.cols)
        for r in range(maze.rows) 
    }

n_episodes = 50
plt.figure(figsize=[10, 6])
for steps in (0, 5, 50):
    set_up_agent(steps, n_episodes)
    num_steps_used = dyna_agent.play()
    plt.plot(range(n_episodes), num_steps_used, label=f"steps={steps}")

plt.legend()
plt.show()