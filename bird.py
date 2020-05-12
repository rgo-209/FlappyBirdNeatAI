"""
This is the code for the Bird class used by the
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

# Bird animation images - Scale to 2 times the size
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
             ]


class Bird:
    # Images to show bird position
    IMGS = BIRD_IMGS

    # How much bird will tilt
    MAXIMUM_ROTATION = 25
    # How much to rotate on 1 frame
    ROTATION_SPEED = 20
    # How long to show the bird - Flapping speed
    ANIMATION_FRAME_TIME = 5

    def __init__(self, x, y):
        """
            Initialize the values for bird object.
        :param x: the x coordinate of position of bird
        :param y: the y coordinate of position of bird
        """
        self.x = x
        self.y = y
        self.tilt = 0
        self.tickCount = 0
        self.speed = 0
        self.height = self.y
        self.imgCount = 0
        self.image = self.IMGS[0]

    def jump(self):
        """
            This function makes the bird jump in the air
        :return: None
        """
        self.speed = -10.5
        self.tickCount = 0
        self.height = self.y

    def move(self):
        """
            This function is used to move the bird.
        :return: None
        """
        # Increase the tick count
        self.tickCount += 1

        # The distance to move is determines by the following physics formula
        # dist = u*t + [(1/2) * acc * t^2]
        # where, u = initial velocity, t = time elapsed, acc= accelaration which is 3 here in our case
        distanceToMove =  self.speed*self.tickCount + 1.5*(self.tickCount**2)

        # if bird tries to move down steeply then put limit
        if distanceToMove >=16:
            distanceToMove = 16
        # if bird tries to moves in opposite direction decrease it the distance
        if distanceToMove<0:
            distanceToMove -=2

        # Update the height
        self.y += distanceToMove

        # make the bird tilt at least by maximum rotation
        if distanceToMove<0 or self.y<self.height+50:
            if self.tilt < self.MAXIMUM_ROTATION:
                self.tilt = self.MAXIMUM_ROTATION
        else:
            if self.tilt >-90:
                self.tilt -= self.ROTATION_SPEED


    def draw(self, window):
        """
            This function draws the bird onto the window.
            The image to show depends on the action we want to show
            For wings up: Image bird1.png
            For wings level: Image bird2.png
            For wings down: Image bird3.png
            This creates a flapping effect on screen.
        :param window: Window to draw onto
        :return: None
        """
        self.imgCount += 1

        if   self.imgCount <= self.ANIMATION_FRAME_TIME * 1:
            self.image = self.IMGS[0]
        elif self.imgCount <= self.ANIMATION_FRAME_TIME * 2:
            self.image = self.IMGS[1]
        elif self.imgCount <= self.ANIMATION_FRAME_TIME * 3:
            self.image = self.IMGS[2]
        elif self.imgCount <= self.ANIMATION_FRAME_TIME * 4:
            self.image = self.IMGS[1]
        elif self.imgCount == self.ANIMATION_FRAME_TIME * 4 + 1:
            self.image = self.IMGS[0]
            self.imgCount=0

        # When going down do not flap wings
        if self.tilt <=-80:
            self.image = self.IMGS[1]
            self.imgCount = self.ANIMATION_FRAME_TIME * 2

        # Rotate the bird by tilt angle
        rotatedImage = pygame.transform.rotate(self.image, self.tilt)
        newRectangle = rotatedImage.get_rect(center = self.image.get_rect(topleft = (self.x,self.y)).center)

        # show the position
        window.blit(rotatedImage,newRectangle.topleft)


    def get_mask(self):
        """
            This function return the mask which is later on used to detect the collision.
        :return: None
        """
        return pygame.mask.from_surface(self.image)
