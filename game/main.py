import eel
from keras.models import Sequential
from keras.layers import Flatten, Dense
from qlearning4k.games import Catch
from keras.optimizers import *
from agent import Agent

grid_size = 10
hidden_size = 100
nb_frames = 1

action_count = 3

model = Sequential()
model.add(Flatten(input_shape=(nb_frames, grid_size, grid_size)))
model.add(Dense(hidden_size, activation='relu'))
model.add(Dense(hidden_size, activation='relu'))
model.add(Dense(action_count))
model.compile(sgd(lr=.2), "mse")

catch = Catch(grid_size)
agent = Agent(model=model)

@eel.expose
def play_game():
    agent.train(catch, batch_size=10, nb_epoch=1000, epsilon=.1)
    print('trained')
    # agent.play(catch)

eel.init('web')
eel.start('main.html')
