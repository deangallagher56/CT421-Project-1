import numpy as np
import random

def parse_problem_instances(file_path):
    problem_instances = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                bin_capacity, num_items = map(int, parts)
                weights = next(file).strip().split()
                problem_instances.append((bin_capacity, list(map(int, weights))))
    return problem_instances

def calculate_fitness(solution, items, bin_capacity):
    bins = {}
    for item_index, bin_index in enumerate(solution):
        if bin_index in bins:
            bins[bin_index] += items[item_index]
        else:
            bins[bin_index] = items[item_index]
    penalty = sum([1 for total in bins.values() if total > bin_capacity])
    return -(len(bins) + penalty)

def tournament_selection(population, scores):
    tournament_size = 5
    selected = []
    for _ in range(len(population)):
        tournament = random.sample(list(zip(population, scores)), tournament_size)
        winner = max(tournament, key=lambda x:x[1])
        selected.append(winner[0])
    return selected

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 2)
    return parent1[:crossover_point] + parent2[crossover_point:], parent2[:crossover_point] + parent1[crossover_point:]

def mutate(individual, mutation_rate=0.05):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = random.randint(0, max(individual))
    return individual

def solve_bin_packing_problems(problem_instances):
    results = []
    for bin_capacity, items in problem_instances:
        population_size = 50
        num_generations = 100
        population = [[random.randint(0, len(items) // 2) for _ in items] for _ in range(population_size)]

        for generation in range(num_generations):
            fitness_scores = [calculate_fitness(individual, items, bin_capacity) for individual in population]
            selected_population = tournament_selection(population, fitness_scores)
            next_generation = []
            for i in range(0, population_size, 2):
                parent1, parent2 = selected_population[i], selected_population[i+1]
                child1, child2 = crossover(parent1, parent2)
                next_generation.extend([mutate(child1), mutate(child2)])
            population = next_generation

        final_scores = [calculate_fitness(individual, items, bin_capacity) for individual in population]
        best_solution_index = np.argmax(final_scores)
        best_solution = population[best_solution_index]
        best_fitness = final_scores[best_solution_index]
        unique_bins = len(set(best_solution))
        results.append((unique_bins, best_fitness))
    return results

file_path = "C:\Users\Dean\Downloads\Binpacking-2"
problem_instances = parse_problem_instances(file_path)
results = solve_bin_packing_problems(problem_instances)
print(results)
