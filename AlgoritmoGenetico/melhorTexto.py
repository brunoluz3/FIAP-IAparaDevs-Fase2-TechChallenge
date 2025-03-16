import random

# Parâmetros do algoritmo genético
tamanho_populacao = 100
taxa_mutacao = 0.1
num_geracoes = 100

# Define a string objetivo
string_objetivo = "Hello, World!"

# Função para gerar uma solução aleatória
def gerar_solucao():
    solucao = ""
    for _ in range(len(string_objetivo)):
        solucao += chr(random.randint(32, 126))  # Gera um caractere aleatório ASCII imprimível
    return solucao

# Função para calcular o fitness de uma solução
def calcular_fitness(solucao):
    fitness = 0
    for i in range(len(solucao)):
        if solucao[i] == string_objetivo[i]:
            fitness += 1
    return fitness

# Função para selecionar pais para reprodução (roleta viciada)
def selecionar_pais(populacao):
    soma_fitness = sum(calcular_fitness(solucao) for solucao in populacao)
    roleta = []
    acumulador_fitness = 0
    for solucao in populacao:
        fitness = calcular_fitness(solucao)
        probabilidade = fitness / soma_fitness
        roleta.append((solucao, acumulador_fitness + probabilidade))
        acumulador_fitness += probabilidade
    pais = []
    for _ in range(2):
        sorteio = random.random()
        for solucao, limite in roleta:
            if sorteio <= limite:
                pais.append(solucao)
                break
    return pais

# Função para realizar o crossover entre dois pais
def crossover(pai1, pai2):
    ponto_corte = random.randint(1, len(pai1) - 1)
    filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
    filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]
    return filho1, filho2

# Função para realizar a mutação em uma solução
def mutacao(solucao):
    solucao_mutada = ""
    for caractere in solucao:
        if random.random() < taxa_mutacao:
            solucao_mutada += chr(random.randint(32, 126))
        else:
            solucao_mutada += caractere
    return solucao_mutada

# Algoritmo genético
populacao = [gerar_solucao() for _ in range(tamanho_populacao)]
geracao = 0

while geracao < num_geracoes:
    proxima_geracao = []
    for _ in range(tamanho_populacao // 2):
        pai1, pai2 = selecionar_pais(populacao)
        filho1, filho2 = crossover(pai1, pai2)
        proxima_geracao.append(mutacao(filho1))
        proxima_geracao.append(mutacao(filho2))
    populacao = proxima_geracao
    geracao += 1

# Encontra a melhor solução na última geração
melhor_solucao = max(populacao, key=calcular_fitness)

# Imprime a melhor solução encontrada
print("Melhor solução encontrada:", melhor_solucao)
