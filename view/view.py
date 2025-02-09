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
        self.master.geometry(f"{self.img_width }x{self.img_height + 100}")

        self.canvas_frame = tk.Frame(self.master)
        self.canvas_frame.grid(row=0, column=0, columnspan=2)

        self.canvas = tk.Canvas(self.canvas_frame, width=self.img_width, height=self.img_height)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        self.button_frame = tk.Frame(self.master)
        self.button_frame.grid(row=1, column=0, pady=5, sticky="ew")

        self.btn_generate = tk.Button(self.button_frame, text="Generar Puntos de entrega", command=self.controller.generate_cities, width=74)
        self.btn_generate.grid(row=0, column=0, padx=5, pady=5)

        self.button_frame_2 = tk.Frame(self.master)
        self.button_frame_2.grid(row=2, column=0, pady=5, sticky="ew")

        self.btn_nn = tk.Button(self.button_frame_2, text="Vecino más cercano", command=self.controller.solve_tsp, width=15)
        self.btn_nn.grid(row=0, column=0, padx=5, pady=5)

        self.btn_local_search = tk.Button(self.button_frame_2, text="Búsqueda Local", command=self.controller.solve_local_search, width=15)
        self.btn_local_search.grid(row=0, column=1, padx=5, pady=5)

        self.btn_genetic = tk.Button(self.button_frame_2, text="Algoritmo Genético", command=self.controller.solve_genetic, width=15)
        self.btn_genetic.grid(row=0, column=2, padx=5, pady=5)

        self.btn_mst = tk.Button(self.button_frame_2, text="MST", command=self.controller.solve_mst, width=15)
        self.btn_mst.grid(row=0, column=3, padx=5, pady=5)


    def update_canvas(self, coordinates):
        self.canvas.delete("all")  
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        for x, y in coordinates:
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="red")

    def animate_solution(self, path, spots, distance, time):
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
            
            # Mostrar el título solo en el último frame
            if frame == len(path) - 1:
                ax.set_title(f"Ruta Óptima del Viajante - Distancia: {distance:.2f} km, Tiempo: {time:.2f} s")

        ani = animation.FuncAnimation(fig, update, frames=len(path), interval=500, repeat=False)
        plt.show()

    def show_message(self, message):
        messagebox.showinfo("Información", message)

    def update_info(self, distance, time):
        self.lbl_distance.config(text=f"Distancia: {distance:.2f} km")
        self.lbl_time.config(text=f"Tiempo: {time:.2f} s")