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
        # self.optimal_genome = self.mgl
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
        
    def run(self):
        while (True):
            self.tic()
            print self.worldstring
            print "n: %s\tw: %s\ts: %s\te: %s" % (self.direction_stat['n'], self.direction_stat['w'], self.direction_stat['s'], self.direction_stat['e'])
            time.sleep(0.1)

    def gen_worldstring(self):
        #print "generating worldstring"
        worldstring = ''
        for row in self.worldmap:
            for cell in row:
                worldstring += "%x" % cell.get_genome()
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
                        rival_genome = wm[rindex][cellkey].get_genome()
                        if not rival_genome > cell.get_genome():
                            wm[rindex][cellkey].set_genome(child[1])
                    else:
                        pass
                elif child[0] == 'w':
                    cindex = cellkey+1
                    if not cindex >= self.size_x:
                        wm[rowkey][cindex].set_genome(child[1])
                    else:
                        pass
                if child[0] == 's':
                    rindex = rowkey+1
                    if not rindex >= self.size_y:
                        wm[rindex][cellkey].set_genome(child[1])
                    else:
                        pass
                if child[0] == 'e':
                    cindex = cellkey-1
                    if not cindex < 0:
                        wm[rowkey][cindex].set_genome(child[1])
                    else:
                        pass
                self.direction_stat[child[0]] += 1
        self.worldmap =  wm
        self.gen_worldstring()

if __name__ == '__main__':
    earth = world(0x10, 70, 30, 0.01)
    earth.run()
    time.sleep(1)
    while(True):
        earth.tic()
        print earth.get_worldstring()
        
