import numpy as np
import Actions as ac
import os

actions = []
actions.append([ac.ACT_MOVE, 100, 500])
actions.append([ac.ACT_OPEN_LASER])
actions.append([ac.ACT_WORK, 500, 400])
actions.append([ac.ACT_WORK, 900, 600])
actions.append([ac.ACT_WORK, 500, 1200])
actions.append([ac.ACT_WORK, 100, 500])
actions.append([ac.ACT_CLOSE_LASER])
actions.append([ac.ACT_MOVE, 0, 0])
np.save(os.path.join('cache', 'cube.npy'), actions)
