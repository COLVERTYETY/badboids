import pygame as py
import boids
import numpy.random as np
import sys
#import qtrees
import splintercell
# Initialise screen
py.init() # pylint: disable=no-member
WIDTH=800
HEIGHT=700
screen = py.display.set_mode((WIDTH,HEIGHT))
py.display.set_caption('can you see the boids ?')
clock = py.time.Clock()
font = py.font.Font(None, 20)  
boids.font = py.font.Font(None, 20)

boids.boid.SURFACE=screen
boids.boid.generaterandompos(10)
for i in boids.boid.ARRAY:
        i.vx+=np.random_integers(-2,2)
        i.vy+=np.random_integers(-2,2)

splintercell.SHEIGHT=HEIGHT
splintercell.SWIDTH=WIDTH
splintercell.init()
# qtrees.quadtree.SURFACE=screen
# SEED = qtrees.quadtree(0,0,WIDTH,HEIGHT)
# SEED.construct(boids.boid.ARRAY)
# Event loop
done = False
while not done:
    for event in py.event.get():
        if event.type == py.QUIT: # pylint: disable= no-member
                done = True


    screen.fill((0,0,0))
    fps = font.render(str(int(clock.get_fps())), True, py.Color('white'))
    screen.blit(fps,(10,10))
    boids.boid.drawall()

    # SEED = qtrees.quadtree(0,0,WIDTH,HEIGHT)
    # SEED.construct(boids.boid.ARRAY)
    # SEED.recursifdraw()
    clock.tick(30)


    py.display.flip()
py.quit() # pylint: disable=no-member
sys.exit()