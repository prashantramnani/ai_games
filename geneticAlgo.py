import runGame
import numpy as np
from game import *

def cal_pop_fitness(new_population):
    fitness = []
    for  i in range(len(new_population)):
        fit = runGame.run_game_with_parameters(new_population[i], display, clock)
        print("fit", fit)
        fitness.append(fit)
    return np.array(fitness)    


def select_mating_pool(population, fitness, num_of_parents_mating):
    parents = np.empty((num_of_parents_mating, population.shape[1]))
    # print("parents shape",parents.shape[0])
    for n in range(num_of_parents_mating):
        max_index = np.where(fitness == np.max(fitness))
        max_index = max_index[0][0]
        parents[n] = population[max_index]
        f=open("neuralNet.txt", "w")
        for i in range(population.shape[1]):
            f.write(str(population[max_index ,i]))
            f.write("\n")
        f.close()
        fitness[max_index] = -99999
    return parents    

def crossover(parents, offspring_size):
    new_population = np.empty(offspring_size)
    for k in range(offspring_size[0]):
        while True:
            parent1 = np.random.randint(0, parents.shape[0] - 1)
            parent2 = np.random.randint(0, parents.shape[0] - 1)

            if parent1 != parent2:
                for j in range(offspring_size[1]):
                    if np.random.uniform(0,1) > 0.5:
                        new_population[k, j] = parents[parent1, j]
                    else:
                        new_population[k, j] = parents[parent2, j]
                break
    return new_population

def mutation(offspring_crossover):
    for k in range(offspring_crossover.shape[0]):
        for _ in range(25):
            j = np.random.randint(0,offspring_crossover.shape[1]-1)
            i = np.random.choice(np.arange(-1,1,0.001), size=(1),replace=False)
            offspring_crossover[k, j] += i
    return offspring_crossover        
