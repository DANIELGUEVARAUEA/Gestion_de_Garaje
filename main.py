# main.py

# Importamos tkinter
import tkinter as tk

# Importamos la clase de servicio
from servicios.garaje_servicio import GarajeServicio

# Importamos la interfaz gráfica
from ui.app_tkinter import AppTkinter


def main():
    """
    Función principal que inicia el programa
    """

    # Creamos la ventana principal de tkinter
    root = tk.Tk()

    # Creamos el servicio
    servicio = GarajeServicio()

    # Creamos la aplicación y le enviamos la ventana y el servicio
    AppTkinter(root, servicio)

    # Ejecutamos el ciclo principal de la interfaz
    root.mainloop()


# Este bloque permite ejecutar el programa directamente
if __name__ == "__main__":
    main()