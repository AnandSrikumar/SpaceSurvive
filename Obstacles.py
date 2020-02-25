import random
import math

def give_picks():
    picks = []
    while len(picks) < 100:
        r_x, r_y = random.randrange(0, 75000), random.randrange(0, 75000)
        picks.append([r_x, r_y, 0])
    return picks


def give_direction(item_points, player_points):
    dx = player_points[0] - item_points[0]
    dy = player_points[1] - item_points[1]
    slope = dy/dx
    if -1 < slope < 1:
        x = 10
        y = slope*x
    else:
        y = 10
        x = y/slope
    angle = math.degrees(math.atan2(dy, dx))
    return [slope, angle]
