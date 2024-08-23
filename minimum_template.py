import pgzrun
from pgzero import screen
from pgzero.actor import Actor

WIDTH = 800
HEIGHT = 600


def draw():
    screen.clear()
    screen.draw.circle((400, 300), 30, 'white')


pgzrun.go()
