#!/usr/bin/env python2

import random
import time
import pygame

class Cell:
    '''
    class Cell
    ----------
    A simple "organism", containing an integer as "genome"

    '''

    def __init__(self, max_genome_length=0xffffff, genome=0):
        '''
        function __init__
        -----------------
        parameters:
        max_genome_length:  integer
        genome:             integer (trucated if > max_genome_length)
        '''
        self.mgl = max_genome_length
        self.genome = genome if genome < self.mgl else genome%self.mgl

    def set_genome(self, genome):
        '''
        function set_genome: set this cell's genome to a new value
        ---------------------------------------------------------
        parameters:
        genome  integer (capped by self.mgl)
        '''
        if genome >= self.mgl:
            self.genome = self.mgl-1
        elif genome < 0:
            self.genome = 0
        else:
            self.genome = genome

    def get_genome(self):
        '''
        function get_genome: return this cell's genome
        ---------------------------------------------
        '''
        return self.genome

    def procreate(self, mutation_rate):
        '''
        function procreate: return a (possibly) mutated version of this cell's genome
        ------------------------------------------------------------------
        parameters:
        mutation_rate   float <= 1  (defines mutation probability: larger number == higher probability)
        '''
        direction = random.choice("nesw")   # as in north (up), east (right), south (down), west (left)
        if random.random() < mutation_rate:
            # prepare XOR bit-toggling by gettin a random power of 2
            # that is <= max_genome_length
            mutation = 2**random.randint(1, len(bin(self.mgl))-3) # -2 bc of leading '0b', and -1 bc of cap
            # randomly choose between:
            # 1) switching one bit of the genome by XOR
            # 2) adding or substracting 1 from genome
            mutation = random.choice(((self.genome ^ mutation), (self.genome + random.choice((-1,1)))))
            return (direction, mutation)
        else: # if not mutated, return genome as-is
            return (direction, self.genome)

class World:
    '''
    class World
    -----------
    A two-dimensional list of cells
    '''
    def __init__(self, max_genome_length, rectsize=5, size_x=30, size_y=10, mutation_rate=0.01):
        '''
        function __init__
        -----------------
        parameters:
        max_genome_length   integer
        size_x, size_y      integers
        mutation_rate       float <= 1  (larger number => higher mutation rate)
        '''
        self.mgl = max_genome_length
        self.optimal_genome = random.randint(0, self.mgl-1)   # initial value of the "fitness functions" goal
        self.change_optimal_at = 100000                     # number of spawned optimal cells before optimums regeneration
        self.change_index = 0                               # counter of spawned optimal cells
        self.rectsize = rectsize
        self.size_x = size_x
        self.size_y = size_y
        self.mr = mutation_rate
        self.screen = pygame.display.set_mode((size_x*rectsize, size_y*rectsize))
        self.clock = pygame.time.Clock()
        '''
        generate worldmap
        '''
        self.worldmap = []
        for row in range(self.size_y):      # append rows
            self.worldmap.append([])
            for col in range(self.size_x):  # append columns
                self.worldmap[row].append(Cell(self.mgl))
        # worldstring for "graphical" representation
        self.worldstring = self.gen_worldstring()
        self.updated_rects = []                             # for pygame.screen updating performance
        self.direction_stat = {'n':0, 'w':0, 's':0, 'e':0}  # direction choice counters
        self.generations = 0                                # generation counters
        
    def run(self):
        while (True):
            self.tic()
            pygame.display.update(self.updated_rects)
            #print self.worldstring
            print "\roptimal: %2x (%i of %i), generations: %i, n: %s, w: %s, s: %s, e: %s" % (
                self.optimal_genome,
                self.change_index,
                self.change_optimal_at,
                self.generations, self.direction_stat['n'],
                self.direction_stat['w'],
                self.direction_stat['s'],
                self.direction_stat['e']
            )
            self.clock.tick_busy_loop(10)
            #time.sleep(0.1)

    def gen_worldstring(self):
        #print "generating worldstring"
        worldstring = ''
        for row in self.worldmap:
            for cell in row:
                worldstring += "%6x" % cell.get_genome()
            worldstring += "\n"
        self.worldstring = worldstring

    def get_worldstring(self):
        return self.worldstring

    def tic(self):
        wm = self.worldmap
        self.updated_rects = []
        for rowkey, row in enumerate(self.worldmap):
            for cellkey, cell in enumerate(row):
                child = cell.procreate(self.mr)
                if child[0] == 'n':
                    rindex = rowkey-1
                    if not rindex < 0:
                        rival_genome = self.worldmap[rindex][cellkey].get_genome()
                        if not abs(self.optimal_genome - rival_genome) < abs(self.optimal_genome - cell.get_genome()):
                            wm[rindex][cellkey].set_genome(child[1])
                            color = child[1]
                            position = cellkey*self.rectsize, rindex*self.rectsize, self.rectsize, self.rectsize
                            self.updated_rects.append(pygame.draw.rect(self.screen, child[1],position))
                    else:
                        pass
                elif child[0] == 'w':
                    cindex = cellkey+1
                    if not cindex >= self.size_x:
                        rival_genome = self.worldmap[rowkey][cindex].get_genome()
                        if not abs(self.optimal_genome - rival_genome) < abs(self.optimal_genome - cell.get_genome()):
                            wm[rowkey][cindex].set_genome(child[1])
                            position = cindex*self.rectsize, rowkey*self.rectsize, self.rectsize, self.rectsize
                            self.updated_rects.append(pygame.draw.rect(self.screen, child[1],position))
                    else:
                        pass
                if child[0] == 's':
                    rindex = rowkey+1
                    if not rindex >= self.size_y:
                        rival_genome = self.worldmap[rindex][cellkey].get_genome()
                        if not abs(self.optimal_genome - rival_genome) < abs(self.optimal_genome - cell.get_genome()):
                            wm[rindex][cellkey].set_genome(child[1])
                            position = cellkey*self.rectsize, rindex*self.rectsize, self.rectsize, self.rectsize
                            self.updated_rects.append(pygame.draw.rect(self.screen, child[1],position))
                    else:
                        pass
                if child[0] == 'e':
                    cindex = cellkey-1
                    if not cindex < 0:
                        rival_genome = self.worldmap[rowkey][cindex].get_genome()
                        if not abs(self.optimal_genome - rival_genome) < abs(self.optimal_genome - cell.get_genome()):
                            wm[rowkey][cindex].set_genome(child[1])
                            position = cindex*self.rectsize, rowkey*self.rectsize, self.rectsize, self.rectsize
                            self.updated_rects.append(pygame.draw.rect(self.screen, child[1],position))
                    else:
                        pass
                self.direction_stat[child[0]] += 1
                if child[1] == self.optimal_genome:
                    self.change_index += 1
                    if self.change_index >= self.change_optimal_at:
                        self.optimal_genome = random.choice(range(self.mgl))
                        self.change_index = 0
        self.worldmap =  wm
        self.gen_worldstring()
        self.generations += 1

if __name__ == '__main__':
    pygame.init()
    earth = World(0x1000000, 5, 200, 100, 0.00001)
    earth.run()
