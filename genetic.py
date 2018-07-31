# genetic algorithm for knapsack problem
# brian djerf 
# july 2018

import numpy
import random
import operator

MAX_WEIGHT = 120
N_HYPOTHESES = 256 # optimal solution likely when > 32
N_GENERATIONS = 8  # should be >= log2(N_HYPOTHESES)
N_ITEMS = 6
CROSSOVER_RATE = 0.5
MUTATION_RATE = 0.05
CULL_RATE = 0.5

# items to be store in backback (weight,value,weight,value,...)
BOXES = [30, 4, 60, 8, 20, 6, 50, 6, 70, 9, 30, 5]

# parallel boolean arrays of items (possible combinations--chromosomes)
# true value => items stored in bp (false => item not stored)
hypotheses = numpy.zeros((N_HYPOTHESES, N_ITEMS))

# start with random population
for i in range (len(hypotheses)):
        for j in range (len(hypotheses[i])):
            hypotheses[i][j] = bool(random.getrandbits(1))

print ("initial candidates:")
print (hypotheses)

# fitness function
# rank by (value - <penalty if over max weight>)
# penalty: 1/5 * <pounds over 120> (but no benefit if under 120)
def rank (hypotheses):

    # current generation
    ranks = numpy.zeros(len(hypotheses))

    weight = 0
    value = 0
    index = 0
    for i in range (len(hypotheses)):
            for j in range (len(hypotheses[i])):
                weight += hypotheses[i][j] * BOXES[index]
                index += 1
                value += hypotheses[i][j] * BOXES[index]
                index += 1
            ranks[i] = value - max((weight - MAX_WEIGHT)/5, 0)
            weight = 0
            value = 0
            index = 0

    # ranked hypothesis (rank bit strings by fitness function on true items)
    r_hypotheses = [k for k, v in sorted(zip(hypotheses, ranks), \
                            key=operator.itemgetter(1),reverse=True)]
    return r_hypotheses;

# recursive genetic algorithm (fringe operations)
def rgenetic (hypotheses):

    # half of combinations reproduce with neighbors
    crossover = numpy.zeros(int(round(len(hypotheses) / 2)))
    n_crossovers = 0

    for i in range (len(crossover)):
            reproduce = numpy.random.choice([0,1], 1, \
                        p=[CROSSOVER_RATE, 1 - CROSSOVER_RATE])
            if reproduce == 1:
                crossover[i] = 1
                n_crossovers += 2

    # represents current generation with crossovers (before culling)
    new_hypotheses = numpy.zeros((len(hypotheses) + n_crossovers, N_ITEMS))

    for i in range (len(new_hypotheses)):
        if i < len(hypotheses):
            new_hypotheses[i] = hypotheses[i]
        else:
            if (i - len(hypotheses)) % 2 == 0:
                if crossover[int(round((i - len(hypotheses))/2))] == 1:
                    # crossover point
                    split = numpy.random.choice([0,1,2,3,4,5], 1)
                    for j in range (len(new_hypotheses[i])):
                        if j < split:
                            new_hypotheses[i][j] = \
                                hypotheses[i - len(hypotheses)][j]
                            new_hypotheses[i + 1][j] = \
                                hypotheses[i - len(hypotheses) + 1][j]
                        else:
                            new_hypotheses[i][j] = \
                                hypotheses[i - len(hypotheses) + 1][j]
                            new_hypotheses[i+1][j] = \
                                hypotheses[i - len(hypotheses)][j]
                        # mutation
                        if j == split:
                            mutate = numpy.random.choice([0,1],1, \
                                p=[MUTATION_RATE, 1 - MUTATION_RATE])
                            if mutate == 1:
                                new_hypotheses[i][j] = not new_hypotheses[i][j]
    
    # rank according to fitness function
    r_hypotheses = rank(new_hypotheses)

    # cull return best ranked combinations
    cutoff = round(int(len(hypotheses)*CULL_RATE))
    return r_hypotheses[0:cutoff];

# recommend running for at least log2(N_HYPOTHESES)
# generations in order to have any candidates at the end
# (assuming a 50% cull rate)
for i in range (N_GENERATIONS):
    new_hypotheses = rgenetic(hypotheses)
    hypotheses = new_hypotheses

print ("best solution found:")
print (hypotheses[0])

for i in range (N_ITEMS):
    if hypotheses[0][i] == 1:
        print ('item {0}: value = {1}, weight = {2}'\
                .format(i + 1, BOXES[2 * i + 1], BOXES[2 * i]))