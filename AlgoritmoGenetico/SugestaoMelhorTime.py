import pygame
import matplotlib
import pylab
import matplotlib.backends.backend_agg as agg
from melhorTime import *
import os
import random
import itertools


#Inicializacao da janela
window_size = (1000, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Melhor formação de squad")
clock = pygame.time.Clock()

#Variaveis globais
FPS = 10
target_team = (10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10)

# Definicao dos parametros do algoritmo
population_size = 11

#Metodo para desenhar gráfico
def draw_plot(x, y, x_label, y_label):
    fig = pylab.figure(figsize=[4, 6], dpi=100)
    ax = fig.gca()
    ax.plot(x, y)

    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_argb()

    size = canvas.get_width_height()
    surf = pygame.image.fromstring(raw_data, size, "ARGB")
    screen.blit(surf, (0,0))

def draw_text (text, x_position, y_position, color=(255, 255, 255), font_size=35, font="Arial"):
    pygame.font.init()
    font = pygame.font.SysFont(font, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x_position, y_position)
    screen.blit(text_surface, text_rect)

def draw_team(team, position, title, x, y, font_size=15):    
    # Print o cabecalho 
    draw_text(title, x, y+position, font_size=font_size)

    # Faz uma varreduara nos membros do time para apresentar os dados
    for member in team:        
        position += 15
        person = ""
        if str(member[1]) == "":
            person = str(member[0])
        else:
            person = f"Name: {str(member[0])} grade: {str(member[1])}"

        draw_text(person, x, y+position, font_size=font_size)


pygame.init()
generation_counter = itertools.count(start=1)  # iniciando a contagem por 1

# Inicia o inviduo squad com base em dados historicos armazenados em um JSON
population = get_team()

# Lista para controle e impressão do melhor fit e geracao encontrados
best_fitness_values = []
best_teams = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False  # Quit the game when the 'q' key is pressed
            elif event.key == pygame.K_KP1:                
                print(target_team)

    
    i = next(generation_counter)
    population = sorted(population, key=calculate_fitness)

    best_fitness = calculate_fitness(population[0])
    best_team = population[0]
    best_fitness_values.append(best_fitness)
    best_teams.append(best_team)

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

    # Limpa os preenchimentos de tela anteriores
    screen.fill((0,0,0))

    # Preencher os resultados na tela
    draw_plot(list(range(len(best_fitness_values))), best_fitness_values, "Generation", "Fitness") 

    draw_text(f"Best Solution: {best_team}", 450, window_size[1]-500, font_size=15)
    draw_text(f"Target       : {tuple(target_team)}", 450, window_size[1]-500+15, font_size=15)
    
    # Mostra na tela se alguma das pessoas que faz parte do time atualmente atende os requisitos para participar da squad
    #Backend 
    draw_team(backend_team, 30, "Backend", 450, window_size[1]-450, font_size=15)
    #iOS 
    draw_team(ios_team, 105, "iOS", 450, window_size[1]-450, font_size=15)
    #Android 
    draw_team(android_team, 165, "Android", 450, window_size[1]-450, font_size=15)
    #QA 
    draw_team(qa_team, 225, "QA", 450, window_size[1]-450, font_size=15)
    #Techlead 
    draw_team(tl_team, 285, "Techlead", 450, window_size[1]-450, font_size=15)
    #Pjectlead 
    draw_team(pl_team, 330, "Projectlead", 450, window_size[1]-450, font_size=15)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
