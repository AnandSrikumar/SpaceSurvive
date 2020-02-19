import random


def give_picks():
    picks = []
    while len(picks) < 100:
        r_x, r_y = random.randrange(0, 75000), random.randrange(0, 75000)
        picks.append([r_x, r_y, 0])
    return picks
