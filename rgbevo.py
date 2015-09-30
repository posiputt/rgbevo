#!/usr/bin/env python2

import random
import time

class cell:
    def __init__(self, max_genome_length=0xffffff, genome=0):
        self.mgl = max_genome_length
        self.genome = genome if genome < self.mgl else genome%self.mgl

    def set_genome(self, genome):
        if genome >= self.mgl:
            self.genome = self.mgl-1
        elif genome < 0:
            self.genome = 0
        else:
            self.genome = genome

    def get_genome(self):
        return self.genome

    def procreate(self, mutation_rate):
        direction = random.choice("nwse")
        if random.random() < mutation_rate:
            mutation = random.choice((1,-1))
            return (direction, self.genome + mutation)
        else:
            return (direction, self.genome)

class world:
    def __init__(self, max_genome_length, size_x=30, size_y=10, mutation_rate=0.01):
        self.mgl = max_genome_length
        self.optimal_genome = 0xf
        self.change_optimal_at = 300000
        self.change_index = 0
        self.size_x = size_x
        self.size_y = size_y
        self.mr = mutation_rate
        self.worldmap = []
        for row in range(self.size_y):
            self.worldmap.append([])
            for col in range(self.size_x):
                self.worldmap[row].append(cell(self.mgl))
        self.worldstring = self.gen_worldstring()
        self.direction_stat = {'n':0, 'w':0, 's':0, 'e':0}
        self.generations = 0
        
    def run(self):
        while (True):
            self.tic()
            print self.worldstring
            print "optimal: %2x (%i of %i), generations: %i\nn: %s, w: %s, s: %s, e: %s" % (
                self.optimal_genome,
                self.change_index,
                self.change_optimal_at,
                self.generations, self.direction_stat['n'],
                self.direction_stat['w'],
                self.direction_stat['s'],
                self.direction_stat['e']
            )
            time.sleep(0.1)

    def gen_worldstring(self):
        #print "generating worldstring"
        worldstring = ''
        for row in self.worldmap:
            for cell in row:
                worldstring += "%2x" % cell.get_genome()
            worldstring += "\n"
        self.worldstring = worldstring

    def get_worldstring(self):
        return self.worldstring

    def tic(self):
        wm = self.worldmap
        for rowkey, row in enumerate(self.worldmap):
            for cellkey, cell in enumerate(row):
                child = cell.procreate(self.mr)
                if child[0] == 'n':
                    rindex = rowkey-1
                    if not rindex < 0:
                        rival_genome = self.worldmap[rindex][cellkey].get_genome()
                        if not abs(self.optimal_genome - rival_genome) < abs(self.optimal_genome - cell.get_genome()):
                            wm[rindex][cellkey].set_genome(child[1])
                    else:
                        pass
                elif child[0] == 'w':
                    cindex = cellkey+1
                    if not cindex >= self.size_x:
                        rival_genome = self.worldmap[rowkey][cindex].get_genome()
                        if not abs(self.optimal_genome - rival_genome) < abs(self.optimal_genome - cell.get_genome()):
                            wm[rowkey][cindex].set_genome(child[1])
                    else:
                        pass
                if child[0] == 's':
                    rindex = rowkey+1
                    if not rindex >= self.size_y:
                        rival_genome = self.worldmap[rindex][cellkey].get_genome()
                        if not abs(self.optimal_genome - rival_genome) < abs(self.optimal_genome - cell.get_genome()):
                            wm[rindex][cellkey].set_genome(child[1])
                    else:
                        pass
                if child[0] == 'e':
                    cindex = cellkey-1
                    if not cindex < 0:
                        rival_genome = self.worldmap[rowkey][cindex].get_genome()
                        if not abs(self.optimal_genome - rival_genome) < abs(self.optimal_genome - cell.get_genome()):
                            wm[rowkey][cindex].set_genome(child[1])
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
    earth = world(0x10, 75, 40, 0.00001)
    earth.run()
    time.sleep(1)
    while(True):
        earth.tic()
        print earth.get_worldstring()
        
