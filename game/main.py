import eel
from keras.models import Sequential
from keras.layers import Flatten, Dense
from qlearning4k.games import Catch
from keras.optimizers import *
from agent import Agent
from game import Game

sensor_shape = (30,)
hidden_size = 100
nb_frames = 1

action_count = Game.nb_actions

model = Sequential()
model.add(Flatten(input_shape=(nb_frames, *sensor_shape)))
model.add(Dense(hidden_size))
model.add(Dense(hidden_size))
model.add(Dense(action_count))
model.compile(optimizer='rmsprop', loss="mse")

game = Game()
agent = Agent(model=model)

@eel.expose
def play_game():
    agent.train(game, batch_size=1, nb_epoch=200, epsilon=.1, observe=5, reset_memory=True)
    print('trained')
    agent.play(game)

eel.init('web')
eel.start('main.html')
