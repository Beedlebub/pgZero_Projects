import pgzrun
# from pgzero.actor import Actor
# from pgzero import screen

WIDTH = 500
HEIGHT = 500

alien = Actor('alien') # type: ignore
alien.x = 0
alien.y = 50


def draw():
    screen.clear() # type: ignore
    alien.draw()


def update():
    alien.x += 2
    if alien.x > WIDTH:
        alien.x = 0


pgzrun.go()
