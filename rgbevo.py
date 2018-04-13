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
    
    
def fitness_bitwise (genome, env_genome, max_genome_length):
    """
    calculate fitness by counting matching 
    """
    cnd_print(DEBUG, ">> running: fitness_bitwise({0}, {1}, {2})".format(genome, env_genome, max_genome_length))
    cnd_print(DEBUG, "env genome:\t{0:24b}".format(env_genome))

    fitness = max_genome_length - bin(env_genome ^ genome).count('1')
    #count_1 = bin(env_genome & genome).count('1')    
    #fitness = (count_1/float(max_genome_length))
    cnd_print(DEBUG, "fitness genome\t{0:24b}\t{1:2f}".format(genome, fitness))
    
    return fitness
