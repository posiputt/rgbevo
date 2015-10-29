#!/usr/bin/env python2

import random
import pygame
import sys

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
            ''' 
            mutation = 2**random.randint(1, len(bin(self.mgl))-3) # -2 bc of leading '0b', and -1 bc of cap
            '''
            '''
            mutation = 2** random.choice((7,15,23))
            '''
            
            mutation = 2** random.randint(0,23)
                
            # randomly choose between:
            # 1) switching one bit of the genome by XOR
            # 2) adding or substracting 1 from genome
            mutation = random.choice((
                    (self.genome ^ mutation),
                    (self.genome + random.choice((-1, 1, -256, 256, -65536, 65536)))
                    ))
            '''
            mutation = self.genome + random.choice((-1,1,-10,10,-100,100,-1000,1000,-10000,10000))
            '''
            '''
            mutation = self.genome + random.choice((-0x1,0x1,-0x100,0x100,-0x10000,0x10000))
            '''
            if mutation < 0:
                mutation = 0
            elif mutation > 0xffffff:
                mutation = 0xffffff
            return (direction, mutation)
        else: # if not mutated, return genome as-is
            return (direction, self.genome)

class World:
    '''
    class World
    -----------
    A two-dimensional list of cells
    '''
    def __init__(self, max_genome_length, rectsize=5, size=(10, 10), mutation_rate=0.01):
        '''
        function __init__
        -----------------
        parameters:
        max_genome_length   integer
        size_x, size_y      integers
        mutation_rate       float <= 1  (larger number => higher mutation rate)
        '''
        self.mgl = max_genome_length
        self.optimal_genome = random.randint(0, self.mgl-1) # initial value of the "fitness functions" goal
        print "%06x" % self.optimal_genome
        self.change_optimal_at = size[0] * size[1]          # number of spawned optimal cells before optimums regeneration
        self.change_index = 0                               # counter of spawned optimal cells
        self.rectsize = rectsize
        self.size_x = size[0]
        self.size_y = size[1]
        self.mr = mutation_rate
        self.screen = pygame.display.set_mode((self.size_x*self.rectsize, self.size_y*self.rectsize))
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
        '''
        function run
        ------------
        no parameters
        main loop of this class
        '''
        while (True):
            self.tick()
            pygame.display.update(self.updated_rects)   # update pygame window
            '''
            # deprecated CLI 'graphics'
            print self.worldstring
            print "optimal: %06x (%i of %i), generations: %i, changes: %i" % (
                self.optimal_genome,
                self.change_index,
                self.change_optimal_at,
                self.generations,
                len(self.updated_rects)
            )
            '''
            self.updated_rects = []
            self.clock.tick_busy_loop(20)

    def gen_worldstring(self):
        '''
        function gen_worldstring (DEPRECATED)
        -------------------------------------
        no parameters
        read wordlmap, convert into single string
        '''
        print "generating worldstring"
        worldstring = ''
        for row in self.worldmap:
            for cell in row:
                worldstring += "%6x" % cell.get_genome()
            worldstring += "\n"
        self.worldstring = worldstring

    def get_worldstring(self):
        return self.worldstring

    def tick(self):
        '''
        function tick
        -------------
        no parameters
        go through every cell in worldmap,
        let it procreate
        let it fight for neighboring cell
        if applicable, write new genome into
        neighboring cell
        '''
        wm = self.worldmap
        for rowkey, row in enumerate(self.worldmap):
            for cellkey, cell in enumerate(row):
                child = cell.procreate(self.mr)
                this_genome = child[1]
                diff_this = abs(self.optimal_genome - this_genome)
                diff_quotient = 1.0
                rindex = 0
                cindex = 0
                if child[0] == 'n':
                    rindex = rowkey - 1
                    cindex = cellkey
                elif child[0] == 'w':
                    rindex = rowkey
                    cindex = cellkey - 1
                elif child[0] == 's':
                    rindex = rowkey + 1
                    cindex = cellkey
                elif child[0] == 'e':
                    rindex = rowkey
                    cindex = cellkey + 1
                if not rindex < 0 and not rindex >= self.size_y and not cindex < 0 and not cindex >= self.size_x:
                    rival_genome = self.worldmap[rindex][cindex].get_genome()
                    if rival_genome == this_genome:
                        continue
                    diff_rival = abs(self.optimal_genome - rival_genome)
                    if diff_rival == 0:
                        diff_quotient = 1.0 - 5.960464832810452e-08
                        #print "nay",
                    elif diff_this == 0:
                        diff_quotient = 5.960464832810452e-08
                        #print "yay",
                    elif diff_rival > diff_this:
                        diff_quotient = float(diff_this) / (float(diff_rival))
                    elif diff_rival < diff_this:
                        diff_quotient = 1.0 - (float(diff_rival) / (float(diff_this)))
                    victory = random.random()
                    if victory > diff_quotient:
                        #print diff_rival, diff_this, diff_quotient, victory
                        #print "%06x wins over %06x" % (this_genome, rival_genome)
                        wm[rindex][cindex].set_genome(child[1])
                        color = child[1]
                        position = cindex*self.rectsize, rindex*self.rectsize, self.rectsize, self.rectsize
                        self.updated_rects.append(pygame.draw.rect(self.screen, child[1],position))
                else:
                    pass
                self.direction_stat[child[0]] += 1
                if child[1] == self.optimal_genome:
                    self.change_index += 1
                    # print self.change_index, self.change_optimal_at
                    if self.change_index >= self.change_optimal_at:
                        self.optimal_genome = random.choice(range(self.mgl))
                        print "%06x" % self.optimal_genome
                        self.change_index = 0
        self.worldmap =  wm
        # self.gen_worldstring()
        self.generations += 1

if __name__ == '__main__':
    indicators = '--help', '-h', '--world-size', '-ws', '--rect-size', '-rs', '--mutation-rate', '-m'
    worldsize = [50, 50]
    rectsize = 10
    mutation_rate = 0.1
    for index, a in enumerate(sys.argv):
        if a in indicators:
            if a == '--help' or a == '-h':
                rtfm =  "\nrgbevo - a silly, colorful evolution sim.\n" \
                        "-----------------------------------------\n" \
                        "options:\n" \
                        "--------\n" \
                        "--help, -h:\t\tshow this manual, quit\n" \
                        "--world-size 120x100:\tset world size to " \
                        "X = 120, Y = 100 rectangles\n" \
                        "\t\t\tshort form: --ws 120x100\n" \
                        "--rect-size 10:\t\tset rectangle size to 10px squared\n" \
                        "\t\t\tshort form: -rs 10\n" \
                        "--mutation-rate 0.1:\tset mutation rate to 0.1\n" \
                        "\t\t\tshort form: -m 0.1\n" \
                        "\t\t\thigher rate means mutations more common\n" \
                        "\t\t\tshouldn't be >1\n"
                quit(rtfm)
            elif a == '--world-size' or a == '-ws':
                worldsize = sys.argv[index+1].split('x')
                if len(worldsize) != 2:
                    quit('try something like "--world-size 20x20"')
                else:
                    worldsize[0] = int(worldsize[0])
                    worldsize[1] = int(worldsize[1])
            elif a == '--rect-size' or a == '-rs':
                rectsize = int(sys.argv[index+1])
            elif a == '--mutation-rate' or a == '-m':
                mutation_rate = float(sys.argv[index+1])
            else:
                pass
    arg_echo = "Initializing world with these properties:\nworld-size: %ix%i\nrect-size: %i\nmutation-rate: %f\n" % (
            worldsize[0], worldsize[1],
            rectsize,
            mutation_rate
    )
    print arg_echo
    pygame.init()
    earth = World(0x1000000, rectsize=rectsize, size=worldsize, mutation_rate=mutation_rate)
    earth.run()
