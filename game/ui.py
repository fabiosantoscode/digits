import eel
from track import track_object as track
from game import Game

@eel.expose
def play_game():
    game = Game(track)
    game.play()

eel.init('web')
eel.start('main.html')

