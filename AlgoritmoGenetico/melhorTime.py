"""
Autores: Bruno Luz e Diogo Leal
Conteúdo do trabalho de encerramento da segunda fase do curso de IA para Devs
Esse codigo tem como objetivos a aplicacao pratica de algoritmos geneticos

Case:
    Codificamos um modelo de algortmo genetico que tem como objetivo montar a melhor formacao de uma squad para um projeto de alta complexidade, estamos considerando o seguinte cenário:

    Squad formada por:
        3 devs backend;
        2 devs ios;
        2 devs android;
        2 qas;
        1 tech lead;
        1 project lead

    Populacao inicial: foi formada considerando 3 squads existentes, como valor de comparação, estamos utilizando as ultimas avaliacoes de cada um dos membros dos times;
    Target: como se trata de um projeto complexo, estamos buscando pessoas que foram avaliadas com nota maxima (10) para todos os perfis

    Após a montagem da nova populacao, estamos fazendo uma busca na base atual do membros das squads para entender quais pessoas atendem o resultado apresentado pelo algoritmo

"""

import random
import numpy as np
import pandas as pd

# Definicao do time target
target_team = (10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10)

# Definicao dos parametros do algoritmo
population_size = 11
num_generations = 100

mutation_intensity = 0.001  # % da intesidade de mutacao
mutation_rate = 0.01 # probabilidade de mutacao

json_team_path = "BaseSquads/person.json" #caminho do json com as avaliacoes do time

# Funcao que calcula do fit de um indididuo do time
def calculate_fitness(team):
    return sum(
                abs(
                        team[i] - target_team[i]
                ) for i in range(len(team)
            ))

# Busca a populacao inicial na base de squads
def get_team():
    population = []   
    dataset = pd.read_json(json_team_path)

    for squad in dataset.itertuples():                
        person_temp = [int(person["grade"]) for person in squad.people]        
        population.append(person_temp)
   
    return population

# Aplicao do crossover
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) -1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# Aplicacao da mutacao
def mutate(team, intensity=mutation_intensity, sigma=1):

    mutated_team = list(team)

    for i in range(len(team)):
        if random.random() < mutation_rate:
            mutated_team[i] += round(np.random.normal(0, sigma)) # Gaussian mutation
            
    return list(mutated_team)

# Separacao dos perfis por especialidade
def get_best_team(best_team):    
    dataset = pd.read_json(json_team_path)    
    
    index_backend, index_ios, index_android, index_qa, index_tl, index_pl = split_best_team(best_team)
    
    backend = define_team(index_backend, dataset, "backend")
    ios = define_team(index_ios, dataset, "ios")
    android = define_team(index_android, dataset, "android")
    qa = define_team(index_qa, dataset, "qa")
    tl = define_team(index_tl, dataset, "tl")
    pl = define_team(index_pl, dataset, "pl")

    return backend, ios, android, qa, tl, pl

# Quebra dos indices do time de acordo com cada especialidade
def split_best_team(best_team):
    backend = [best_team[0], best_team[1], best_team[2]]
    ios = [best_team[3], best_team[4]]
    android = [best_team[5], best_team[6]]
    qa = [best_team[7], best_team[8]]
    tl = [best_team[9]]
    pl = [best_team[10]]
    return backend, ios, android, qa, tl, pl

# Busca dos perfis que atendam o resultado do algoritmo
def define_team(best_team, data, title):
    team = []
    control = False
    count_append = 0

    for i in best_team: # Iteracao para controle da quantidade de pessoal para cada tipo de especialidade       
        for squad in data.itertuples():
            for person in squad.people: # Iteracao que varra a base do time para buscar os perfis existentes que atende o resultado do algoritmo
                if count_append < len(best_team):
                    if i == int(person["grade"]) and str(person["title"]) == title:
                        name = person["name"]
                        grade = person["grade"]
                        title = person["title"]

                        team_temp = [name, grade, title]
                        team.append(team_temp)

                        len_before = len(team)   
                        team = remove_duplicate(team) # Tratamento para remoção de itens que possam estar duplicados na lista
                        len_after = len(team)
                        count_append = len(team)                                     
                        
                        if len_before == len_after:
                            control = True
            
            if control:
                control = False
                break      
    
    if len(team) == 0:
        nobody = ["Nobody found", "0", title]
        team.append(nobody)
    
    return list(team)

# Remocao de perfil duplicados da lista do time
def remove_duplicate(team):
    team_without_duplicate = []
    for i in team:
        if i not in team_without_duplicate:
            team_without_duplicate.append(i)

    return team_without_duplicate


if __name__ == '__main__':
    # Bloco main do algoritmo
    population = get_team()
    
    # Lista para controle e impressão do melhor fit e geracao encontrados
    best_fitness_values = []
    best_teams = []
    
    for generation in range(num_generations):
        population = sorted(population, key=calculate_fitness)
    
        best_fitness = calculate_fitness(population[0])
        best_team = population[0]
        best_fitness_values.append(best_fitness)
        best_teams.append(best_team)
    
        print(f"Generation {generation}: Best fitness = {best_fitness}, Best team = {best_team}, Target = {target_team}")    
    
        new_population = [population[0]]  # Em todas as iteracoes estamos mantendo o melhor individuo
        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population[:10], k=2)  # Selecao dos pais entre os 10 melhores indivíduos
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            new_population.extend([child1, child2])
    
        population = new_population
    
    # Exibe o melhor resultado encontrado
    best_team = population[0]
    backend_team, ios_team, android_team, qa_team, tl_team, pl_team = get_best_team(best_team)
    
    print(f"\nBest option: {best_team}")

    # Exibe a lista de pessoal que fazem parte das squad e atendem o resultado gerado pelo algoritmo
    print("\nPeople in the actual team (initial population)")

    print("\nThe best team of backend is:")
    for backend in backend_team:
        print(f"Name: {str(backend[0])} grade: {str(backend[1])}")

    print("\nThe best team of ios is:")
    for ios in ios_team:
        print(f"Name: {str(ios[0])} grade: {str(ios[1])}")

    print("\nThe best team of android is:")
    for android in android_team:
        print(f"Name: {str(android[0])} grade: {str(android[1])}")
    
    print("\nThe best team of qa is:")
    for qa in qa_team:
       print(f"Name: {str(qa[0])} grade: {str(qa[1])}")

    print("\nThe best team of techlead is:")
    for tl in tl_team:
        print(f"Name: {str(tl[0])} grade: {str(tl[1])}")

    print("\nThe best team of project lead is:")
    for pl in pl_team:
       print(f"Name: {str(pl[0])} grade: {str(pl[1])}")