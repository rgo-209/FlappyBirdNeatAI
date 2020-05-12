"""
This is the code for the fitness function used by the
AI that learns to master the game of Flappy bird.

Rahul Golhar
11th May 2020


This wouldn't have been possible without the guidance from a tutorial that I
referred. The link for the tutorial is :
https://www.youtube.com/watch?v=MMxFDaIOHsE&list=PLzMcBGfZo4-lwGZWXz5Qgta_YNX3_vLS2
I would like to thank Tech with Tim.

"""

import os
import neat
import pygame

from base import Base
from bird import Bird
from pipe import PipeObj

pygame.init()
# set the window name
pygame.display.set_caption('Flappy Bird AI by Rahul Golhar')

# Initialize the pygame font
pygame.font.init()


# Initialize generations to zero
GEN = 0

# Window size to display
WINDOW_WIDTH = 480
WINDOW_HEIGHT =640

# This is the font to be used for the texts we will show.
SCORE_FONT = pygame.font.SysFont("comicsans", 30 )

# Background image
BACKGROUND_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "bg.png")),
                                        (WINDOW_WIDTH, WINDOW_HEIGHT))

def drawWindow(win, birds, pipes, base, score, gen):
    """
    This function is used to draw the give objects onto
    a window at a given instance of time.
    :param win:     Window Object
    :param birds:   List of birds alive
    :param pipes:   list of pipes visible on screen
    :param base:    the ground/base object
    :param score:   the current score
    :param gen:     the current generation
    :return: None
    """
    # Put on the background first
    win.blit(BACKGROUND_IMG, (0, 0))

    # Draw the pipes on screen
    for pipe in pipes:
        pipe.draw(win)

    # Show the score
    text = SCORE_FONT.render("Score: "+str(score),1,(255,0,0,0))
    win.blit(text, (WINDOW_WIDTH - 10 -text.get_width(), 10 ))

    # Show the current generation
    text = SCORE_FONT.render("Generation: "+str(gen),1,(255,0,0,0))
    win.blit(text, ( 10, 10 ))
    # Show no of birds that are currently alive
    text = SCORE_FONT.render("Alive: "+str(len(birds)),1,(255,0,0,0))
    win.blit(text, ( 10, 30 ))

    # Show name of creator
    tag = SCORE_FONT.render("rgo_209",1,(0,0,0,0))
    win.blit(tag, ( 10, 550 ))


    # Draw the base on screen
    base.draw(win)

    # Draw all the birds that are currently alive
    for bird in birds:
        bird.draw(win)

    # Update the screen
    pygame.display.update()



def fitnessFunction(genomes, config):
    """
    This is the fitness function to be used for
    determining performances of the birds.
    :param genomes: it is a list of neural net
                    genomes.
    :param config:  the config object for neat
    :return: None
    """
    global GEN

    # Update the generation
    GEN += 1
    # List of neural net objects used
    neuralNets = []
    # List of all genomes used
    genomeList = []
    # List of bird objects used
    birds = []

    # Generate the list of birds, genomes using neural nets
    for _, genome in genomes:
        # set neural network
        neuralNet = neat.nn.FeedForwardNetwork.create(genome, config)
        neuralNets.append(neuralNet)

        # add bird at initial position (150,260)
        birds.append(Bird(150,260))

        # Let the fitness be initially 0
        genome.fitness = 0

        # add the genome to the list of all genomes
        genomeList.append(genome)

    # generate the game window
    os.environ['SDL_VIDEO_WINDOW_POS'] = '80, 60'
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # initial score will be 0
    score = 0

    # set base at height of 575
    base = Base(575)

    # add a pipe along the X axis at a distance of 300 from origin
    pipes = [PipeObj(300)]

    # initially run will be true
    run =True
    # create a clock object
    clock = pygame.time.Clock()

    while(run):
        # set the frame speed for the clock object
        clock.tick(30)
        # check whether the used asked to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        # Initial index of pipes be 0
        pipeIndex = 0

        # add a pipe if the bird has passed it
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > (pipes[0].x + pipes[0].PIPE_TOP.get_width()):
                pipeIndex = 1
        else:
            run = False
            break
        # now check the position and assign the action to do for every bird
        for x, bird in enumerate(birds):
            # make 1 move and update new values
            bird.move()
            # add a fitness of 0.1 for every frame the bird is alive
            genomeList[x].fitness += 0.1

            # get the neural net output using 3 input for the first layer
            # 1st  = the height at which the bird is right now
            # 2nd  = the distance between bird and the top pipe
            # 3rd  = the distance between bird and the bottom pipe
            neuralNetOutput = neuralNets[x].activate((bird.y, abs(bird.y - pipes[pipeIndex].height),
                                                                  abs(bird.y - pipes[pipeIndex].bottom)))
            # the bird will jump only if the output
            # of neural net is more than 0.5
            if neuralNetOutput[0] > 0.5:
                bird.jump()

        # this array store the pipes that need to be removed
        rem = []

        add_pipe = False
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    # if the bird collides with  a pipe
                    # remove all its data from all 3 arrays
                    # storing its bird object, neural net object
                    # and the genome associated with it
                    genomeList[x].fitness -= 1
                    birds.pop(x)
                    neuralNets.pop(x)
                    genomeList.pop(x)
                if not pipe.passed and pipe.x < bird.x:
                    # if the bird doesn't hit a pipe
                    # then we need to add a new pipe
                    # when the bird passes the current pipe
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width()<0:
                # when the pipe goes out of window just remove it
                rem.append(pipe)
            # let the pipe make a move
            pipe.move()

        # if the bird passed a pipe then increase its score by 1
        if add_pipe:
            score += 1
            for g in genomeList:
                g.fitness += 5
            # when the bird passes a pipe
            # generate another pipe
            pipes.append(PipeObj(460))

        # remove the pipes that went off the screen
        for r in rem:
            pipes.remove(r)

        # check whether any of the bird has hit the ground
        for x, bird in enumerate(birds):
            if bird.y +bird.image.get_height() >= 640 or bird.y <=0:
                # if the bird collides with  a ground
                # remove all its data from all 3 arrays
                # storing its bird object, neural net object
                # and the genome associated with it
                birds.pop(x)
                neuralNets.pop(x)
                genomeList.pop(x)

        # let the pipe make a move
        base.move()

        # draw the current state onto a screen
        drawWindow(win, birds, pipes, base, score, GEN)
