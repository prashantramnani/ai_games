import random
import numpy as np
import geneticAlgo
from neuralNet import *

num_weights = n_x*n_h + n_h*n_h2 + n_h2*n_y 

num_generations = 1000
sol_per_population = 50
num_parents_mating = 12

pop_size = (sol_per_population, num_weights)

new_population = np.random.choice(np.arange(-1,1,step=0.01),size = pop_size, replace=True)
print("new",new_population.shape)

for generation in range(num_generations):
        
    print('##############Generation:'+str(generation)+'#########')

    fitness = geneticAlgo.cal_pop_fitness(new_population)
    print("fitness" , fitness)
    print('#######  fittest chromosome in gneneration ' + str(generation) +' is having fitness value:  ', np.max(fitness))

    parents = geneticAlgo.select_mating_pool(new_population,fitness,num_parents_mating)
    # print("parents", parents)
    offspring_crossover = geneticAlgo.crossover(parents, pop_size[0] - num_parents_mating, num_weights)
    # print("offspring_crossover", offspring_crossover)
    mutated_population = geneticAlgo.mutation(offspring_crossover)

    new_population[0:parents.shape[0]] = parents
    new_population[parents.shape[0]:pop_size[0]] = mutated_population
