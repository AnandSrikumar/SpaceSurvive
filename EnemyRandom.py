import random


class RandomInit:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def place_random_enemy(self):
        side = random.choice([0, 1, 2, 3])
        ranges_x = [0, self.w]
        ranges_y = [0, self.h]
        points = [0, 0]
        if side == 0:
            points[0] = random.randrange(ranges_x[0], ranges_x[1])
            points[1] = -100
        elif side == 2:
            points[0] = random.randrange(ranges_x[0], ranges_x[1])
            points[1] = self.h+100
        elif side == 1:
            points[0] = -100
            points[1] = random.randrange(ranges_y[0], ranges_y[1])

        elif side == 3:
            points[0] = self.w+100
            points[1] = random.randrange(ranges_y[0], ranges_y[1])

        return points

    def get_random_enemy(self, player_x, player_y, boss=-1):
        player_points = [player_x, player_y]
        enem_points = self.place_random_enemy()
        slope = (enem_points[1] - player_points[1])/(enem_points[0] - player_points[0])
        speed = random.choice([10, 20])
        dire = 1
        if enem_points[0] > player_points[0]:
            dire = -1
        sprite = random.choice([0, 1, 2, 3, 4, 5])
        health = [100, 125, 150, 175, 200, 225]
        scores = [50, 100, 150, 200, 250, 300]
        if boss != -1:
            return [enem_points[0], enem_points[1], slope, 30, dire, boss, 1000, 700, 250, 250]
        return [enem_points[0], enem_points[1], slope, speed, dire, sprite, health[sprite], scores[sprite], 80, 80]

    def renew_pos(self, enem_points, player_points):
        slope = (enem_points[1] - player_points[1]) / (enem_points[0] - player_points[0])
        enem_points[2] = slope
        dire = 1
        if enem_points[0] > player_points[0]:
            dire = -1
        enem_points[4] = dire

    def give_random(self, e_list):
        return random.randrange(0, len(e_list))

