import numpy as np


def random_act(state):
    while True:
        y_pos, x_pos = np.random.randint(19), np.random.randint(19)
        if state.is_valid_position(x_pos, y_pos):
            break

    return y_pos, x_pos
