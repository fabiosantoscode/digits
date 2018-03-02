import math
from collections import namedtuple

RayMatch = namedtuple('RayMatch', 'collided, dist_x, dist_y, mx, my, horiz, normal')

track = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1,(2),0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

class TrackObject:
    def __init__(self, track):
        self.track = track

    def is_occupied(self, x, y):
        try:
            return self.track[math.floor(y)][math.floor(x)] is 0
        except IndexError:
            return True

    def ray_cast(self, start_x, start_y, end_x, end_y):
        dx, dy = (end_x - start_x, end_y - start_y)
        mx = math.floor(start_x)
        my = math.floor(start_y)
        delta_x = math.sqrt(1 + (dy ** 2) / (dx ** 2))
        delta_y = math.sqrt(1 + (dx ** 2) / (dy ** 2))
        collided = False

        if dx < 0:
            step_x = -1
            dist_x = (0 - mx) * delta_x
        else:
            step_x = 1
            dist_x = (mx + 1 - 0) * delta_x

        if dy < 0:
            step_y = -1
            dist_y = (0 - my) * delta_y
        else:
            step_y = 1
            dist_y = (my + 1 - 0) * delta_y

        for iter in range(50):
            if dist_x < dist_y:
                dist_x += delta_x
                mx += step_x
                horiz = True
                normal = math.pi if step_x > 0 else 0
            else:
                dist_y += delta_y
                my += step_y
                horiz = False
                normal = math.pi * (1/3) if step_y > 0 else math.pi / 2

            if self.is_occupied(x, y):
                collided = True
                break

        return RayMatch(collided, dist_x, dist_y, mx, my, horiz, normal)

track_object = TrackObject(track)

