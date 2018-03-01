import numpy as np
import random
import math
import eel
import time
from track import track_object as track

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
        self.reset()

    def reset(self):
        self.runner = find_runner(track)
        self.speed = 0.3
        self.ended = False
        self.sensor_matrix = self.get_sensor_matrix()
        self.result = None
        self.steps = 0

    @property
    def is_won(self):
        return self.steps >= 100

    def is_over(self):
        return self.ended

    def get_sensor_matrix(self, all=False, as_bools=False):
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
                    if as_bools:
                        sensors.append(int(not self.track.is_occupied(sens_x, sens_y)))
                    else:
                        sensors.append((sens_x, sens_y))

        if all:
            assert len(sensors) == 30, "len sensors is %d" % len(sensors)
        return sensors

    def get_score(self):
        return len(self.get_sensor_matrix(all=False))

    def get_frame(self):
        return np.array(self.get_sensor_matrix(all=True, as_bools=True))

    def continuous_play(self, network):
        max = float('inf')
        if hasattr(self, 'max_episode_steps'):
            max = self.max_episode_steps
        step = 0
        while step < max and not self.ended:
            step += 1
            action = random.choice([-1, 1])
            reward = self.step(action)
            print('action: ', action, 'reward:', reward)
            self.display()

    def display(self):
        eel.drawGame(self.to_json())
        time.sleep(0.1)

    nb_actions = 2

    def action_space(self):
        return [-1, 1]

    def play(self, action):
        assert action in self.action_space(), "expected action to be -1 or 1, was {}".format(action)
        self.steps += 1
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

        reward = len(self.get_sensor_matrix(all=False))

        return self.get_as_state(), reward, self.ended

    def to_json(self):
        return {
            'track': self.track.track,
            'runner': self.runner,
            'sensorMatrix': self.sensor_matrix
        }

