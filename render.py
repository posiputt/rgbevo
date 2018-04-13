#!/usr/bin/env python2

import pygame
from PIL import Image

from debug import cnd_print

DEBUG = False
STATUS = True

'''
class Screen_Renderer:
    def __init__(self, screen_size=(10, 10), pixel_size=10):
        pygame.init()
        self.screen_size = screen_size
        self.pixel_size = pixel_size
        self.screen = pygame.display.set_mode((\
            self.screen_size[0] * self.pixel_size,\
            self.screen_size[1] * self.pixel_size))

    def update_screen(self, pixels):
        """
        take a list of pixel objects and draw them to the screen
        """
        for i, p in enumerate(pixels):
            pos_x, pos_y, color = p.get_pos_x()*self.pixel_size, p.get_pos_y()*self.pixel_size, p.get_genome()
            pygame.draw.rect(self.screen, color, (pos_x, pos_y, self.pixel_size, self.pixel_size))
        pygame.display.flip()
'''

class File_Renderer:
    def __init__(self, size=(10, 10), prefix="rgbevo", mode="RGB", format="png"):
        self.size = size
        self.prefix = prefix
        self.mode = mode
        self.format = format
        
    def write_file(self, pixels, frame_number):
        file_name = "{0}_{1:010d}.{2}".format(self.prefix, frame_number, self.format)
        cnd_print(DEBUG, "executing write_file")
        img = Image.new(self.mode, self.size)
        cnd_print(DEBUG, "created Image object")
        for i, p in enumerate(pixels):
            position = p.get_pos_x(), p.get_pos_y()
            color = p.get_genome()
            img.putpixel(position, color)
        img.save(file_name)
        cnd_print(STATUS, "wrote file '{}'".format(file_name))
