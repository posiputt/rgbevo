#!/usr/bin/env python2

DEBUG = True

import random
from debug import cnd_print
    
def mutate_bitwise(genome, max_genome_length):
    """
    switch a single bit in a binary int, then return
    """
    """
    exception wenn genome > 2**max_genome_length
    wie geht das noch?
    """
    cnd_print(DEBUG, ">> running: mutate_bitwise({0}, {1})".format(genome, max_genome_length))
    cnd_print(DEBUG, "original value:\t{0:8d} ({0:24b})".format(genome))
    
    switch_bit = random.randint(0, max_genome_length-1)
    cnd_print(DEBUG, "switching bit:\t{0:8d} ({1:24b})".format(switch_bit, 2**switch_bit))
    
    mutated_genome = genome ^ 2**switch_bit
    cnd_print(DEBUG, "mutated value:\t{0:8d} ({0:24b})".format(mutated_genome))
    
    return mutated_genome
    
    
def fitness_bitwise(genome, env_genome, max_genome_length):
    """
    calculate fitness by counting matching bits 
    """
    cnd_print(DEBUG, ">> running: fitness_bitwise({0:06x}, {1:06x}, {2})".format(genome, env_genome, max_genome_length))
    cnd_print(DEBUG, "env genome:\t{0:06x}".format(env_genome))

    fitness = max_genome_length - bin(env_genome ^ genome).count('1')
    #count_1 = bin(env_genome & genome).count('1')    
    #fitness = (count_1/float(max_genome_length))
    cnd_print(DEBUG, "fitness genome\t{0:06x}\t{1:2d}".format(genome, fitness))
    
    return fitness


def pick_winner(genomes, env_genome, max_genome_length):
    """
    randomly choose winner from a list of competitors
    weighted by fitness
    """
    candidates = []
    for g in genomes:
        fitness = fitness_bitwise(g, env_genome, max_genome_length)
        for i in range(fitness):
            candidates.append(g)
        #cnd_print(DEBUG, "weighted candidates list:\n {}".format(candidates))
    
    return random.choice(candidates)

