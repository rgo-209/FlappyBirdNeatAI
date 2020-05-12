"""
This is the code for the Base class used by the
AI that learns to master the game of Flappy bird.

Rahul Golhar
11th May 2020


This wouldn't have been possible without the guidance from a tutorial that I
referred. The link for the tutorial is :
https://www.youtube.com/watch?v=MMxFDaIOHsE&list=PLzMcBGfZo4-lwGZWXz5Qgta_YNX3_vLS2
I would like to thank Tech with Tim.

"""
import os

import pygame


# Ground/Base image
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))


class Base:
    """
        This class represents the base or the
        ground used in the game.
    """

    # Speed of base movement
    BASE_SPEED = 5

    # Width of the base
    BASE_WIDTH = BASE_IMG.get_width()

    # Image used for the base
    IMG = BASE_IMG

    def __init__(self, y):
        """
            Initialize the base object and assign its position.
        :param y: the height at which to place the base
        """
        self.y = y
        self.x1 = 0
        self.x2 = self.BASE_WIDTH

    def move(self):
        """
            This function is used to move the base.
        :return: None
        """
        # Move the base to the left by speed
        self.x1 -= self.BASE_SPEED
        self.x2 -= self.BASE_SPEED

        # if the base goes out of window then reset its position
        if self.x1 + self.BASE_WIDTH < 0:
            self.x1 = self.x2+self.BASE_WIDTH
        if self.x2 + self.BASE_WIDTH < 0:
            self.x2 = self.x1+self.BASE_WIDTH

    def draw(self, window):
        """
            This function draws the base onto the window.
        :param win: Window to draw onto
        :return: None
        """
        window.blit(self.IMG,(self.x1, self.y))
        window.blit(self.IMG,(self.x2, self.y))