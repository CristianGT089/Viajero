from tkinter import messagebox
import random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from deap import base, creator, tools, algorithms
import threading

class ProblemSolver:

    def __init__(self):
        self.spots = []

    def set_spots(self, spots):
        self.spots = spots
    
    def solve_tsp(self):
        if not self.spots:
            messagebox.showwarning("Error", "Primero genera los puntos")
            return

        graph = nx.Graph()
        for i in range(len(self.spots)):
            for j in range(i+1, len(self.spots)):
                distance = ((self.spots[i][0] - self.spots[j][0])**2 + (self.spots[i][1] - self.spots[j][1])**2)**0.5
                graph.add_edge(i, j, weight=distance)

        return self.nearest_neighbor(graph)

    def nearest_neighbor(self, graph):
        start = 0  
        path = [start]
        visited = set(path)
        
        while len(path) < len(self.spots):
            last = path[-1]
            neighbors = [(n, graph[last][n]['weight']) for n in graph.neighbors(last) if n not in visited]
            next_city = min(neighbors, key=lambda x: x[1])[0]
            path.append(next_city)
            visited.add(next_city)
        path.append(start)  
        return path
    

    def solve_local_search(self):
        if not self.spots:
            messagebox.showwarning("Error", "Primero genera los puntos")
            return
        
        def swap_2opt(route):
            """Realiza una mutación intercambiando dos nodos al azar"""
            i, j = sorted(random.sample(range(1, len(route) - 1), 2))
            new_route = route[:i] + route[i:j][::-1] + route[j:]
            return new_route

        # Generar ruta inicial aleatoria
        route = list(range(len(self.spots))) + [0]
        best_distance = self.calculate_total_distance(route)

        for _ in range(5000):  # Iteraciones de búsqueda local
            new_route = swap_2opt(route)
            new_distance = self.calculate_total_distance(new_route)
            if new_distance < best_distance:
                route, best_distance = new_route, new_distance

        return route

    
    def solve_genetic(self):
        if not self.spots:
            messagebox.showwarning("Error", "Primero genera los puntos")
            return

        def evaluate(individual):
            return (self.calculate_total_distance(individual),)

        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        toolbox = base.Toolbox()
        toolbox.register("indices", random.sample, range(len(self.spots)), len(self.spots))
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("mate", tools.cxOrdered)
        toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
        toolbox.register("select", tools.selTournament, tournsize=3)
        toolbox.register("evaluate", evaluate)

        pop = toolbox.population(n=100)
        algorithms.eaSimple(pop, toolbox, cxpb=0.7, mutpb=0.2, ngen=100, verbose=False)
        
        best_ind = tools.selBest(pop, k=1)[0]

        return best_ind + [best_ind[0]]


    def solve_mst(self):
        if not self.spots:
            messagebox.showwarning("Error", "Primero genera los puntos")
            return

        graph = nx.Graph()
        for i in range(len(self.spots)):
            for j in range(i+1, len(self.spots)):
                distance = ((self.spots[i][0] - self.spots[j][0])**2 + (self.spots[i][1] - self.spots[j][1])**2)**0.5
                graph.add_edge(i, j, weight=distance)

        mst = nx.minimum_spanning_tree(graph)
        return list(nx.dfs_preorder_nodes(mst, 0)) + [0]
        

    def calculate_total_distance(self, path):
        distance = sum(((self.spots[path[i]][0] - self.spots[path[i+1]][0])**2 +
                        (self.spots[path[i]][1] - self.spots[path[i+1]][1])**2)**0.5
                    for i in range(len(path) - 1))
        return distance

    def solve_held_karp(self):
        if not self.spots:
            messagebox.showwarning("Error", "Primero genera los puntos")
            return

        n = len(self.spots)
        if n > 20:  # Limitar la cantidad de ciudades a un máximo de 20
            messagebox.showwarning("Advertencia", "El número de ciudades es muy alto para Held-Karp. Se recomienda generar menos de 20.")
            return

        dist = [[((self.spots[i][0] - self.spots[j][0])**2 + (self.spots[i][1] - self.spots[j][1])**2)**0.5 for j in range(n)] for i in range(n)]
        
        # Convertir dist a tuplas para evitar el error de "unhashable type"
        dist_tuple = tuple(tuple(row) for row in dist)

        def calculate_held_karp():
            try:
                # Calcular la distancia mínima usando el método 'tsp' de la clase
                shortest_path = self.tsp(dist_tuple, n)

                # Mostrar la distancia mínima
                messagebox.showinfo("Held-Karp", f"Distancia mínima encontrada: {shortest_path}")

                # Obtener el recorrido más corto
                return self.get_shortest_path(dist_tuple, n)


            except RecursionError:
                messagebox.showerror("Error", "La ejecución excedió el límite de recursión. Intente con menos ciudades.")

        # Ejecutar el cálculo en un hilo separado para no bloquear la interfaz
        threading.Thread(target=calculate_held_karp, daemon=True).start()

    def tsp(self, dist, n):
        # Implementación de Held-Karp recursivo sin lru_cache
        def recursive_tsp(mask, pos, dist, n):
            if mask == (1 << n) - 1:
                return dist[pos][0]

            return min(dist[pos][j] + recursive_tsp(mask | (1 << j), j, dist, n) for j in range(n) if not mask & (1 << j))

        # Llamamos a la función recursiva para obtener el resultado
        return recursive_tsp(1, 0, dist, n)

    def get_shortest_path(self, dist, n):
        # Función para reconstruir la ruta óptima usando Held-Karp
        mask = 1
        pos = 0
        path = [pos]

        while mask != (1 << n) - 1:
            next_city = min(
                (j for j in range(n) if not mask & (1 << j)),
                key=lambda j: dist[pos][j] + self.tsp(mask | (1 << j), j)
            )
            path.append(next_city)
            mask |= (1 << next_city)
            pos = next_city

        path.append(0)  # Regresar al punto de inicio
        return path
