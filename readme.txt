read me for genetic algorithm
brian djerf

the assignment is contained in "genetic.py"
which produces a number of random combinations
(of items stored and not stored) as the initial 
input for the algorithm. the items are from a 
predetermined list, each with a value and a weight. 
the goal is to maximize the total value of the 
items in the backpack, without exceeding the 
maximum weight.

the initial combinations crossover at a specified
rate, with crossovers occasionally being slightly
mutated. the new population is culled according
to a fitness function and returned, either to
be run again as the next generation or to be outputted
as the best solutions found so far, depending
on the number of generations chosen to be run.

all key variables including maximum weight,
number of hypotheses, rates of fringe 
operations, and the array of items itself
can be altered at the top of the script

run with "python3 genetic.py"