"""
This is the code for an AI that learns to master the game of Flappy bird.
Rahul Golhar
11th May 2020


This wouldn't have been possible without the guidance from a tutorial that I
referred. The link for the tutorial is :
https://www.youtube.com/watch?v=MMxFDaIOHsE&list=PLzMcBGfZo4-lwGZWXz5Qgta_YNX3_vLS2
I would like to thank Tech with Tim.

"""

import neat
import os

from fitnessFunction import fitnessFunction


def main():
    """
        This is the main function to run the algorithm.
        It creates a population and calls the fitness
        function on it.
    :return: None
    """
    # set the local directory to be used for finding config file
    localDirectory = os.path.dirname(__file__)

    # Set the path for config file
    configPath = os.path.join(localDirectory,"config-feedforward.txt")

    # set the config variable for neat
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,neat.DefaultSpeciesSet, neat.DefaultStagnation,configPath)

    # get the population
    population = neat.Population(config)

    # add a neat reporter for the population
    population.add_reporter(neat.StdOutReporter(True))
    statistics = neat.StatisticsReporter()
    population.add_reporter(statistics)

    winner = population.run(fitnessFunction,50)

    print(winner)

if __name__ == "__main__":
    main()