from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class View:
    def __init__(self, master, controller):
        self.controller = controller  # Guardamos referencia al controlador

        self.bg_image = Image.open("map.png")
        self.img_width, self.img_height = self.bg_image.size
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        self.master = master
        self.master.title("Optimización del Viajante")
        self.master.geometry(f"{self.img_width + 340}x{self.img_height + 50}")

        self.canvas_frame = tk.Frame(self.master)
        self.canvas_frame.grid(row=0, column=0)

        self.canvas = tk.Canvas(self.canvas_frame, width=self.img_width, height=self.img_height)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        self.button_frame = tk.Frame(self.master)
        self.button_frame.grid(row=1, column=0, pady=5, sticky="ew")

        self.btn_generate = tk.Button(self.button_frame, text="Generar Puntos de entrega", command=self.controller.generate_cities, width=25)
        self.btn_generate.pack(side=tk.LEFT, padx=5)

        self.btn_nn = tk.Button(self.button_frame, text="Vecino más cercano", command=self.controller.solve_tsp, width=25)
        self.btn_nn.pack(side=tk.LEFT, padx=5)

        self.btn_local_search = tk.Button(self.button_frame, text="Búsqueda Local", command=self.controller.solve_local_search, width=25)
        self.btn_local_search.pack(side=tk.LEFT, padx=5)

        self.btn_genetic = tk.Button(self.button_frame, text="Algoritmo Genético", command=self.controller.solve_genetic, width=25)
        self.btn_genetic.pack(side=tk.LEFT, padx=5)

        self.btn_mst = tk.Button(self.button_frame, text="MST (Árbol de Expansión Mínima)", command=self.controller.solve_mst, width=25)
        self.btn_mst.pack(side=tk.LEFT, padx=5)

    def update_canvas(self, coordinates):
        self.canvas.delete("all")  
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        for x, y in coordinates:
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="red")

    def animate_solution(self, path, spots):
        fig, ax = plt.subplots(figsize=(self.img_width / 100, self.img_height / 100))  # Mantiene la proporción

        bg_image = plt.imread("map.png")  # Carga la imagen sin rotarla
        ax.imshow(bg_image, extent=[0, self.img_width, 0, self.img_height])  

        graph = nx.Graph()
        pos = {i: (spots[i][0], self.img_height - spots[i][1]) for i in range(len(spots))}  # Invertir Y

        nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=500, ax=ax)

        edges = []
        def update(frame):
            if frame > 0:
                u, v = path[frame-1], path[frame]
                graph.add_edge(u, v)
                edges.append((u, v))
            ax.clear()
            ax.imshow(bg_image, extent=[0, self.img_width, 0, self.img_height])  
            nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=500, ax=ax)
            nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color='red', width=2, ax=ax)

        ani = animation.FuncAnimation(fig, update, frames=len(path), interval=500, repeat=False)
        plt.title("Ruta Óptima del Viajante")
        plt.show()

    def show_message(self, message):
        messagebox.showinfo("Información", message)
