import random
import networkx as nx
from deap import base, creator, tools, algorithms

class ProblemSolver:

    def __init__(self):
        self.spots = []
        self.speed = 50  # Velocidad promedio en km/h

    def set_spots(self, spots):
        self.spots = spots

    def calculate_total_distance(self, path):
        return sum(((self.spots[path[i]][0] - self.spots[path[i+1]][0])**2 +
                    (self.spots[path[i]][1] - self.spots[path[i+1]][1])**2)**0.5
                   for i in range(len(path) - 1))

    def calculate_time(self, distance):
        """Calcula el tiempo estimado del recorrido en horas."""
        return distance / self.speed  

    def solve_tsp(self):
        if not self.spots:
            return None, None, None  

        graph = nx.Graph()
        for i in range(len(self.spots)):
            for j in range(i+1, len(self.spots)):
                distance = ((self.spots[i][0] - self.spots[j][0])**2 +
                            (self.spots[i][1] - self.spots[j][1])**2)**0.5
                graph.add_edge(i, j, weight=distance)

        path = self.nearest_neighbor(graph)
        distance = self.calculate_total_distance(path)
        time = self.calculate_time(distance)
        return path, distance, time

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
            return None, None, None  

        def swap_2opt(route):
            i, j = sorted(random.sample(range(1, len(route) - 1), 2))
            return route[:i] + route[i:j][::-1] + route[j:]

        route = list(range(len(self.spots))) + [0]
        best_distance = self.calculate_total_distance(route)

        for _ in range(5000):
            new_route = swap_2opt(route)
            new_distance = self.calculate_total_distance(new_route)
            if new_distance < best_distance:
                route, best_distance = new_route, new_distance

        time = self.calculate_time(best_distance)
        return route, best_distance, time

    def solve_genetic(self):
        if not self.spots:
            return None, None, None  

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
        best_distance = self.calculate_total_distance(best_ind)
        time = self.calculate_time(best_distance)
        return best_ind + [best_ind[0]], best_distance, time

    def solve_mst(self):
        if not self.spots:
            return None, None, None  

        graph = nx.Graph()
        for i in range(len(self.spots)):
            for j in range(i+1, len(self.spots)):
                distance = ((self.spots[i][0] - self.spots[j][0])**2 +
                            (self.spots[i][1] - self.spots[j][1])**2)**0.5
                graph.add_edge(i, j, weight=distance)

        mst = nx.minimum_spanning_tree(graph)
        path = list(nx.dfs_preorder_nodes(mst, 0)) + [0]
        distance = self.calculate_total_distance(path)
        time = self.calculate_time(distance)
        return path, distance, time

    def get_shortest_path(self, dist, n):
        mask = 1
        pos = 0
        path = [pos]

        while mask != (1 << n) - 1:
            next_city = min(
                (j for j in range(n) if not mask & (1 << j)),
                key=lambda j: dist[pos][j]
            )
            path.append(next_city)
            mask |= (1 << next_city)
            pos = next_city

        path.append(0)  
        distance = sum(dist[path[i]][path[i+1]] for i in range(len(path) - 1))
        time = self.calculate_time(distance)
        return path, distance, time
