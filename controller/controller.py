import tkinter as tk

from model.city import City
from model.solvers import ProblemSolver
from view.view import View

class Controller:

    def __init__(self):
        self.root = tk.Tk()
        self.solver = ProblemSolver()
        self.view = View(self.root, self)
        self.city = City(self.view.img_width, self.view.img_height, 20)

        self.root.mainloop()

    def generate_cities(self):
        self.city.generate_random_points()
        self.solver.set_spots(self.city.get_coordinates())
        self.view.update_canvas(self.city.get_coordinates())  # Enviar solo datos, no el objeto

    def solve_tsp(self):
        route, distance, time = self.solver.solve_tsp()
        if route:
            self.view.animate_solution(route, self.city.get_coordinates())  # Enviar solo los datos necesarios
            print(f"Ruta: {route}, Distancia: {distance:.2f}, Tiempo estimado: {time:.2f} horas")
        else:
            print("No hay puntos para calcular")

    def solve_local_search(self):
        route, distance, time = self.solver.solve_local_search()
        if route:
            self.view.animate_solution(route, self.city.get_coordinates())
            print(f"Ruta: {route}, Distancia: {distance:.2f}, Tiempo estimado: {time:.2f} horas")
        else:
            print("No hay puntos para calcular")

    def solve_genetic(self):
        route, distance, time = self.solver.solve_genetic()
        if route:
            self.view.animate_solution(route, self.city.get_coordinates())
            print(f"Ruta: {route}, Distancia: {distance:.2f}, Tiempo estimado: {time:.2f} horas")
        else:
            print("No hay puntos para calcular")

    def solve_mst(self):
        route, distance, time = self.solver.solve_mst()
        if route:
            self.view.animate_solution(route, self.city.get_coordinates())
            print(f"Ruta: {route}, Distancia: {distance:.2f}, Tiempo estimado: {time:.2f} horas")
        else:
            print("No hay puntos para calcular")

    