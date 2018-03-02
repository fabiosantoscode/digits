import eel
from keras.models import Sequential
from keras.layers import Flatten, Dense
from qlearning4k.games import Catch
from keras.optimizers import *
from agent import Agent
from game import Game

sensor_grid_length = 30
hidden_size = 100
nb_frames = 10

action_count = 2

model = Sequential()
model.add(Flatten(input_shape=(nb_frames, sensor_grid_length)))
model.add(Dense(hidden_size, activation='relu'))
model.add(Dense(hidden_size, activation='relu'))
model.add(Dense(hidden_size, activation='relu'))
model.add(Dense(action_count))
model.compile(sgd(lr=.2), "mse")

game = Game()
agent = Agent(model=model)

@eel.expose
def play_game():
    agent.train(game, batch_size=10, nb_epoch=1000, epsilon=.1)
    print('trained')
    agent.play(game)

eel.init('web')
eel.start('main.html')
