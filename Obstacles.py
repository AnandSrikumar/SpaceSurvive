import random
import math

def give_picks(max_x, max_y):
    picks = []
    while len(picks) < 15:
        r_x, r_y = random.randrange(0, max_x), random.randrange(0, max_y)
        picks.append([r_x, r_y, 0])
    return picks


def give_direction(item_points, player_points):
    dx = item_points[0] - player_points[0]
    dy = player_points[1] - item_points[1]
    if dx != 0:
        slope = dy/dx
    if dx == 0:
        slope = 1
    angle = math.degrees(math.atan2(dy, dx))

    return [slope, angle]
