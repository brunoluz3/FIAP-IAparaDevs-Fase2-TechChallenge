import random
import numpy as np

# Definicao do time target
target_team = (10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10)

# Definicao dos parametros do algoritmo
population_size = 6
num_generations = 10

mutation_intensity = 0.001  # % da intesidade de mutacao
mutation_rate = 0.01 # probabilidade de mutacao


# Function to calculate the fitness of an individual team
def calculate_fitness(team):
    # Fitness is the sum of the absolute differences from the target team
    return sum(abs(team[i] - target_team[i]) for i in range(11))

# Generate a random population of teams
def generate_random_population(size):
    return [(random.randint(1, 10), 
             random.randint(1, 10),
             random.randint(1, 10),
             random.randint(1, 10),
             random.randint(1, 10),
             random.randint(1, 10),
             random.randint(1, 10),
             random.randint(1, 10),
             random.randint(1, 10),
             random.randint(1, 10), 
             random.randint(1, 10)) for _ in range(size)]

# Perform one-point crossover
def crossover(parent1, parent2):
    crossover_point = random.randint(1, 9)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


# Perform mutation by changing teams with a specified intensity
def mutate(team, intensity=mutation_intensity, sigma=1):

    mutated_team = list(team)

    for i in range(11):
        if random.random() < mutation_rate:
            mutated_team[i] += round(np.random.normal(0, sigma)) # Gaussian mutation
            
    return tuple(mutated_team)


if __name__ == '__main__':
    # Main genetic algorithm loop
    population = generate_random_population(population_size)
    
    # Lists to store best fitness and generation for plotting
    best_fitness_values = []
    best_teams = []
    
    for generation in range(num_generations):
        population = sorted(population, key=calculate_fitness)
    
        best_fitness = calculate_fitness(population[0])
        best_team = population[0]
        best_fitness_values.append(best_fitness)
        best_teams.append(best_team)
    
        print(f"Generation {generation}: Best fitness = {best_fitness}, Best team = {best_team}, Target = {target_team}")
    
    
    
        new_population = [population[0]]  # Keep the best individual
        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population[:10], k=2)  # Select parents from the top 10 individuals
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            new_population.extend([child1, child2])
    
        population = new_population
    
    # Print the best team found
    best_team = population[0]
    print(f"Best Team: {best_team}")