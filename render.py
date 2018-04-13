#!/usr/bin/env python2

import pygame

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
