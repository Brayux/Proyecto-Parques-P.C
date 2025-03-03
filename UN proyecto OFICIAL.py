import tkinter as tk
import random

# Definición de constantes para el tablero y los jugadores
TABLERO_FILAS = 15  # Número de filas del tablero
TABLERO_COLUMNAS = 15  # Número de columnas del tablero
FICHAS_POR_JUGADOR = 4  # Cantidad de fichas por jugador
COLORES_JUGADORES = {1: "red", 2: "blue", 3: "green", 4: "yellow"}  # Colores de cada jugador

class Parques:
    """Clase que representa el juego de Parqués utilizando Tkinter."""
    def __init__(self, root):
        """Inicializa la interfaz gráfica y los elementos del juego."""
        self.root = root
        self.root.title("Parqués")  # Título de la ventana
        self.root.geometry("700x700")  # Tamaño de la ventana
        self.root.configure(bg="lightblue")  # Color de fondo

        # Marco que contiene el tablero de juego
        self.tablero_frame = tk.Frame(root, bg="darkgreen", bd=5, relief="ridge")
        self.tablero_frame.grid(row=0, column=0, padx=20, pady=20)
        
        self.casillas = []  # Lista para almacenar las casillas del tablero
        self.fichas = {}  # Diccionario que almacena las fichas de cada jugador
        self.turno_actual = 1  # Variable que controla el turno del jugador actual
        
        self.crear_tablero()  # Llama al método para generar el tablero
        self.inicializar_fichas()  # Llama al método para posicionar las fichas
        
        # Botón para lanzar el dado
        self.boton_dado = tk.Button(root, text="Lanzar dado", command=self.lanzar_dado)
        self.boton_dado.grid(row=1, column=0, pady=10)
        
        # Etiqueta para mostrar el valor del dado
        self.label_dado = tk.Label(root, text="Dado: ")
        self.label_dado.grid(row=2, column=0, pady=5)

        # Etiqueta y entrada para seleccionar la ficha a mover
        self.label_ficha = tk.Label(root, text="Elige ficha (0-3):")
        self.label_ficha.grid(row=3, column=0, pady=5)
        
        self.entry_ficha = tk.Entry(root)
        self.entry_ficha.grid(row=4, column=0, pady=5)
        
    def crear_tablero(self):
        """Crea el tablero de juego usando una matriz de Canvas."""
        for i in range(TABLERO_FILAS):
            fila = []  # Lista para almacenar una fila del tablero
            for j in range(TABLERO_COLUMNAS):
                color = "white"  # Color por defecto de las casillas
                # Define las esquinas como bases de los jugadores
                if (i < 5 and j < 5) or (i < 5 and j >= 10) or (i >= 10 and j < 5) or (i >= 10 and j >= 10):
                    color = "lightgrey"
                # Define el camino principal en amarillo
                elif i == 7 or j == 7:
                    color = "lightyellow"
                
                # Crea un Canvas para representar la casilla
                canvas = tk.Canvas(self.tablero_frame, width=30, height=30, bg=color, highlightthickness=0)
                canvas.grid(row=i, column=j, padx=1, pady=1)
                fila.append(canvas)
            self.casillas.append(fila)  # Agrega la fila al tablero
        
    def inicializar_fichas(self):
        """Posiciona las fichas de cada jugador en sus respectivas bases."""
        posiciones_inicio = {
            1: [(0, 0), (0, 1), (1, 0), (1, 1)],
            2: [(0, 13), (0, 14), (1, 13), (1, 14)],
            3: [(13, 0), (13, 1), (14, 0), (14, 1)],
            4: [(13, 13), (13, 14), (14, 13), (14, 14)],
        }
        
        for jugador, posiciones in posiciones_inicio.items():
            self.fichas[jugador] = []  # Inicializa la lista de fichas para cada jugador
            for fila, columna in posiciones:
                # Crea una etiqueta para representar la ficha
                ficha = tk.Label(self.casillas[fila][columna], text="O", bg=COLORES_JUGADORES[jugador], fg="white")
                ficha.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                self.fichas[jugador].append((ficha, fila, columna))
        
    def lanzar_dado(self):
        """Simula el lanzamiento del dado generando un número aleatorio entre 1 y 6."""
        resultado = random.randint(1, 6)  # Genera un número aleatorio
        self.label_dado.config(text=f"Dado: {resultado}")  # Muestra el resultado en la interfaz
        self.mover_ficha_seleccionada(resultado)  # Llama al método para mover la ficha
        
    def mover_ficha_seleccionada(self, resultado):
        """Mueve la ficha seleccionada según el número obtenido en el dado."""
        try:
            indice = int(self.entry_ficha.get())  # Obtiene el índice de la ficha elegida
            if indice < 0 or indice >= len(self.fichas[self.turno_actual]):  # Verifica que la ficha sea válida
                return
            
            ficha, fila, columna = self.fichas[self.turno_actual][indice]  # Obtiene la ficha y su posición actual
            
            # Calcula la nueva posición de la ficha
            nueva_fila = fila + resultado if fila + resultado < TABLERO_FILAS else TABLERO_FILAS - 1
            nueva_columna = columna  # Mantiene la misma columna (puede modificarse según las reglas reales)
            
            ficha.place_forget()  # Elimina la ficha de la posición actual
            
            # Crea una nueva etiqueta en la nueva posición
            ficha = tk.Label(self.casillas[nueva_fila][nueva_columna], text="O", bg=COLORES_JUGADORES[self.turno_actual], fg="white")
            ficha.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            
            self.fichas[self.turno_actual][indice] = (ficha, nueva_fila, nueva_columna)  # Actualiza la ficha en el diccionario
            
            # Cambia el turno al siguiente jugador
            self.turno_actual = self.turno_actual % 4 + 1  
        except ValueError:
            pass  # Maneja el caso en que el usuario ingrese un valor no válido

if __name__ == "__main__":
    root = tk.Tk()  # Crea la ventana principal de Tkinter
    juego = Parques(root)  # Instancia la clase Parques
    root.mainloop()  # Ejecuta el bucle principal de Tkinter
