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
        solution = self.solver.solve_tsp()
        self.view.animate_solution(solution, self.city.get_coordinates())  # Enviar solo los datos necesarios

    def solve_local_search(self):
        solution = self.solver.solve_local_search()
        self.view.animate_solution(solution, self.city.get_coordinates())

    def solve_genetic(self):
        solution = self.solver.solve_genetic()
        self.view.animate_solution(solution, self.city.get_coordinates())

    def solve_mst(self):
        solution = self.solver.solve_mst()
        self.view.animate_solution(solution, self.city.get_coordinates())

    