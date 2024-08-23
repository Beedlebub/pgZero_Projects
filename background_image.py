import pgzrun
from pgzero import screen
from pgzero.actor import Actor

WIDTH = 500
HEIGHT = 500

alien = Actor('alien')
alien.x = 0
alien.y = 50

background = Actor('background')


def draw():
    screen.clear() # type: ignore
    background.draw()
    alien.draw()


def update():
    alien.x += 2
    if alien.x > WIDTH:
        alien.x = 0


pgzrun.go()
