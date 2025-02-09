import random


class City:
    def __init__(self, width=800, height=600, num_spots=20):
        self.width = width
        self.height = height
        self.num_spots = num_spots
        self.spots = []

    
    def generate_random_points(self):
        """Genera ciudades aleatorias dentro de los límites definidos."""
        self.spots = [(random.randint(50, self.width - 50), random.randint(50, self.height - 50)) for _ in range(20)]

    def get_coordinates(self):
        """Devuelve las coordenadas de las ciudades generadas."""
        return self.spots

