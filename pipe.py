"""
This is the code for the Pipe class used by the
AI that learns to master the game of Flappy bird.

Rahul Golhar
11th May 2020


This wouldn't have been possible without the guidance from a tutorial that I
referred. The link for the tutorial is :
https://www.youtube.com/watch?v=MMxFDaIOHsE&list=PLzMcBGfZo4-lwGZWXz5Qgta_YNX3_vLS2
I would like to thank Tech with Tim.

"""
import os
import random
import pygame


# Window size to display
WINDOW_WIDTH = 480
WINDOW_HEIGHT =640

# Pipe image
PIPE_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "pipe.png")),  (int(WINDOW_WIDTH/7), int(WINDOW_HEIGHT)))

class PipeObj:
    """
        This class is used to represent a pipe used in the game.
    """
    # Gap between 2 pipes
    GAP = 200
    # Speed of pipe movement
    PIPE_SPEED = 5

    def __init__(self, x):
        """
            Initialize the values for the pipe class.
        :param x:   the x coordinate of the pipe
        """
        self.x = x
        self.height = 0
        self.top = 0
        self.buttom = 0

        # for upside down pipe
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        # for upward pipe
        self.PIPE_BOTTOM = PIPE_IMG

        # if the pipe has gone out of the screen then this value is false
        self.passed = False
        # set the height of the pipe randomly
        self.setHeight()

    def setHeight(self):
        """
            This function is used to randomly set the height of the pipes.
        :return: None
        """
        # Generate a random number to use for height
        self.height= random.randrange(50, 300)
        # set position of top
        self.top = self.height - self.PIPE_TOP.get_height()
        # set position of bottom
        self.bottom = self.height + self.GAP

    def move(self):
        """
            This function is used to move a pipe on screen.
        :return: None
        """
        # decrease the position by the value of speed
        self.x -= self.PIPE_SPEED

    def draw(self, window):
        """
            This function draws the pipe onto the window.
        :param win: Window to draw onto
        :return: None
        """
        window.blit(self.PIPE_TOP, (self.x, self.top))
        window.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        """
            This function is used to determine the collision of
            the bird and the pipe.
        :param bird: the bird to be checked for collision with pipe
        :return: True if bird has collided else return false
        """
        # get the mask of bird object
        bird_Mask = bird.get_mask()
        # get the mask of top pipe
        top_Mask = pygame.mask.from_surface(self.PIPE_TOP)
        # get the mask of bottom pipe
        bottom_Mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        # check how far the masks are from each other
        top_offset = (self.x - bird.x , self.top - round(bird.y))
        bottom_offset = (self.x - bird.x , self.bottom - round(bird.y))

        # If the masks overlap then it will return the point of collision with bottom pipe
        bottom_point = bird_Mask.overlap(bottom_Mask, bottom_offset)

        # If the masks overlap then it will return the point of collision with top pipe
        top_point = bird_Mask.overlap(top_Mask, top_offset)

        # If there is collision return true else return false
        if top_point or bottom_point:
            return True
        return False