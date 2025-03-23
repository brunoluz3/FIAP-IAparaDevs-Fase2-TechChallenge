# FIAP-IAparaDevs-Fase2-TechChallenge 
 
## Usando algoritmos geneticos para montagem de squads

Esse repositório contém um projeto em python que utiliza algoritmos genéticos para estrutura squads (equipes ágeis), utilizando como base um arquivos JSON com as útimas avaliações dos times atuais.

## Resumo
Esse projeto tem como objetivo montar um time ágil de alta performance, utilizando como base, a busca por um individuo (squad) onde todos os seus genes (membros) seráo classificados como nota 10. Para avaliação inicial, criamos a primeira população com base nas squads atuais e em resultados reais das últimas avaliação de cada componente dos times, a partir disso, utilizamos o cruzamento genético e a mutação para buscarmos novas combinações genéticas que permitam gerarmos um novo individuo.

## Arquivos
Esse projeto contém 7 arquivos, porém, alguns foram utilizados como PoC (prova de conceito), para uso da aplicação são necessário:

- **BaseSquads/person.json**: Arquivo onde podemos consultar/inserir os dados das squads atuais, essa informação será utilizada em 2 momentos, no primeiro para montar a primeira população, ou seja, a partir desse individuo geraremos as mutações e cruzamentos para gerar novas squads e após isso, com base no resultado gerado, vamos utilizar essa base novamente para consultar se temos pessoas nos times que poderiam migrar para uma nova squad que visa alta performance.

- **melhorTime.py**: Nesse arquivos temos os métodos baseados em algoritmos genéticos que são responsáveis por calcular o fitness dos individuos, fazer o cruzamento genético, aplicar o fator de mutação e gerar os novos individuos

- **SugestaoMelhorTime.py**: Nesse arquivos temos a aplicação dos arquivos anterior, utilizando o pygame como interface para visualização dos resultados, além disso, é possivel acompanhar a quantidade de gerações que foram realizadas até o momento que alcançamos o resultado ideal

- **requirements.txt**: Documento que descreve todas as libs e verões usadas no projeto

## Como usar

Para executar o projeto: 
- Atualize o arquivo JSON com os dados das suas squads
- Ajuste as variavies:
    - target_team: Quatidade de pessoas e resultados esperados para cada um dos membros do time
    - population_size: Tamanho da população que será utilizado durante todo o processo de criação de novos individuos



## Dependências

- Python 3.X
- Pygame (para interface de visuaização)

O projeto foi criado utilizando uma ambiente local com as seguintes libs:

- contourpy==1.3.1
- cycler==0.12.1
- fonttools==4.56.0
- kiwisolver==1.4.8
- matplotlib==3.10.1
- numpy==2.2.4
- packaging==24.2
- pandas==2.2.3
- pillow==11.1.0
- pygame==2.6.1
- pyparsing==3.2.1
- python-dateutil==2.9.0.post0
- pytz==2025.1
- six==1.17.0
- tzdata==2025.2

'''Para instalar as dependencias, utilize o comando: pip install -r requirements.txt'''

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE)
