import pgzrun
from pgzero import screen
from pgzero.actor import Actor

WIDTH = 200
HEIGHT = 200

alien = Actor('alien')
alien.pos = (0, 50)


def draw():
    screen.clear() # type: ignore
    alien.draw()


def update():
    if keyboard.right: # type: ignore
        alien.x = alien.x + 2
    elif keyboard.left: # type: ignore
        alien.x = alien.x - 2


pgzrun.go()
