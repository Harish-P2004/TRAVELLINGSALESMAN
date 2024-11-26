import random
import numpy as np
import matplotlib.pyplot as plt

cities = [(0, 0), (1, 5), (5, 6), (8, 3), (2, 4), (6, 8), (3, 7), (9, 5)]


def calculate_distance(city1, city2):
    return np.linalg.norm(np.array(city1) - np.array(city2))


def fitness(tour):
    distance = 0
    for i in range(len(tour)):
        distance += calculate_distance(cities[tour[i]], cities[tour[(i + 1) % len(tour)]])
    return distance


def create_individual():
    individual = list(range(len(cities)))  # List of city indices
    random.shuffle(individual)
    return individual


def create_population(pop_size):
    return [create_individual() for _ in range(pop_size)]


def selection(population, fitnesses, k=3):
    selected = []
    for _ in range(len(population)):
        competitors = random.sample(list(zip(population, fitnesses)), k)
        selected.append(min(competitors, key=lambda x: x[1])[0])
    return selected


def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size
    child[start:end] = parent1[start:end]

    ptr2 = end
    for i in range(end, size + end):
        gene = parent2[i % size]
        if gene not in child:
            child[ptr2 % size] = gene
            ptr2 += 1
    return child


def mutate(individual, mutation_rate=0.1):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(individual)), 2)
        individual[i], individual[j] = individual[j], individual[i]

def genetic_algorithm(pop_size, generations, mutation_rate=0.1):
    population = create_population(pop_size)

    for generation in range(generations):
        fitnesses = [fitness(individual) for individual in population]

       
        selected_population = selection(population, fitnesses)

       
        new_population = []
        for i in range(0, pop_size, 2):
            parent1 = selected_population[i]
            parent2 = selected_population[(i + 1) % pop_size]
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            new_population.append(child1)
            new_population.append(child2)

        population = new_population

        
        if generation % 10 == 0:
            best_fitness = min(fitnesses)
            best_individual = population[fitnesses.index(best_fitness)]
            print(f"Generation {generation}, Best Distance: {best_fitness}, Tour: {best_individual}")

    
    final_fitnesses = [fitness(ind) for ind in population]
    best_individual = population[final_fitnesses.index(min(final_fitnesses))]
    return best_individual, min(final_fitnesses)

def plot_tour(tour):
    x_coords = [cities[city][0] for city in tour] + [cities[tour[0]][0]]
    y_coords = [cities[city][1] for city in tour] + [cities[tour[0]][1]]

    plt.figure(figsize=(8, 6))
    plt.plot(x_coords, y_coords, marker='o', color='b')
    plt.title('Best TSP Tour Found')
    for i, city in enumerate(tour):
        plt.text(cities[city][0], cities[city][1], f'{city}', fontsize=12, color='red')
    plt.show()


population_size = 100
generations = 100
mutation_rate = 0.1


best_tour, best_distance = genetic_algorithm(population_size, generations, mutation_rate)
print(f"Best tour: {best_tour}")
print(f"Best distance: {best_distance}")


plot_tour(best_tour)
