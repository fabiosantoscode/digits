import _pickle as pickle
import random
import math
import eel
import time
from track import track_object as track

try:
    classifier = pickle.load(open('network.pickle', 'rb'))
except IOError:
    print('You should run network.py to create the classifier')
    exit()

def find_runner(track):
    x = 0
    y = 0
    for row_no, track_row in enumerate(track.track):
        for col_no, entity in enumerate(track_row):
            if entity == 2:
                x, y = col_no, row_no

    return (x, y, 0.1)

turn_speed = 0.3

class Game(object):
    def __init__(self, track):
        self.track = track
        self.runner = find_runner(track)
        self.speed = 0.3
        self.ended = False
        self.sensor_matrix = self.get_sensor_matrix()
        self.result = None

    def get_sensor_matrix(self, all=False):
        runner_x, runner_y, runner_angle = self.runner
        sine, cosine = math.sin(runner_angle), math.cos(runner_angle)
        sensors = []

        for x in map(lambda x: x / 2, range(0, 6)):
            for y in map(lambda x: x / 2, range(-2, 3)):
                sens_x, sens_y = (
                    x * cosine - y * sine,
                    y * cosine + x * sine
                )

                sens_x, sens_y = (sens_x + runner_x, sens_y + runner_y)

                if all or not self.track.is_occupied(sens_x, sens_y):
                    sensors.append((sens_x, sens_y))

        return sensors

    def play(self):
        eel.drawGame(self.to_json())
        while not self.ended:
            action = random.choice([-1, 1])
            reward = self.advance(action)
            print('action: ', action, 'reward:', reward)
            eel.drawGame(self.to_json())
            time.sleep(0.1)

    def advance(self, action):
        x, y, angle = self.runner
        angle += action * turn_speed
        dx, dy = math.cos(angle) * self.speed, math.sin(angle) * self.speed
        x += dx
        y += dy
        self.sensor_matrix = self.get_sensor_matrix()

        if self.track.is_occupied(x, y):
            self.ended = True
        else:
            self.runner = (x, y, angle)

        return len(self.get_sensor_matrix(all=False))

    def to_json(self):
        return {
            'track': self.track.track,
            'runner': self.runner,
            'sensorMatrix': self.sensor_matrix
        }


game = Game(track)
