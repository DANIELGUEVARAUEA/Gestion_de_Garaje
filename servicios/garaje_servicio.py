# servicios/garaje_servicio.py

# Importamos la clase Vehiculo del paquete modelos
from modelos.vehiculo import Vehiculo

# Importamos os para verificar si el archivo existe
import os

# Importamos datetime para trabajar con fecha y hora actual
from datetime import datetime


# Esta clase contiene la lógica del sistema
class GarajeServicio:
    def __init__(self, nombre_archivo="vehiculos.txt"):
        # Lista privada donde se almacenan los vehículos
        self._vehiculos = []

        # Nombre del archivo txt donde se guardarán los datos
        self.nombre_archivo = nombre_archivo

        # Al iniciar el programa, cargamos los vehículos guardados
        self.cargar_desde_archivo()

    def agregar_vehiculo(self, placa, marca, propietario):
        """
        Agrega un vehículo nuevo al sistema.
        La hora de entrada se genera automáticamente.
        La hora de salida queda vacía al inicio.
        """
        # Obtenemos la hora actual del sistema
        hora_entrada = datetime.now().strftime("%H:%M:%S")

        # Creamos un objeto Vehiculo
        vehiculo = Vehiculo(placa, marca, propietario, hora_entrada, "")

        # Lo agregamos a la lista interna
        self._vehiculos.append(vehiculo)

        # Guardamos la lista actualizada en el archivo txt
        self.guardar_en_archivo()

        # Retornamos el vehículo creado
        return vehiculo

    def registrar_salida(self, placa):
        """
        Busca un vehículo por placa y registra su hora de salida.
        Si ya tiene salida, no la vuelve a registrar.
        """
        # Recorremos todos los vehículos almacenados
        for vehiculo in self._vehiculos:
            # Si encontramos la placa buscada
            if vehiculo.placa == placa:
                # Verificamos si aún no tiene hora de salida
                if vehiculo.hora_salida == "":
                    # Guardamos la hora actual como hora de salida
                    vehiculo.hora_salida = datetime.now().strftime("%H:%M:%S")

                    # Guardamos cambios en el archivo
                    self.guardar_en_archivo()

                    # Devolvemos el vehículo actualizado
                    return vehiculo

                # Si ya tenía hora de salida, devolvemos None
                return None

        # Si no se encontró el vehículo, devolvemos None
        return None

    def listar_vehiculos(self):
        """
        Retorna la lista de vehículos registrados
        """
        return self._vehiculos

    def guardar_en_archivo(self):
        """
        Guarda todos los vehículos en el archivo vehiculos.txt
        """
        with open(self.nombre_archivo, "w", encoding="utf-8") as archivo:
            # Recorremos cada vehículo y lo escribimos en una línea
            for vehiculo in self._vehiculos:
                archivo.write(vehiculo.to_linea())

    def cargar_desde_archivo(self):
        """
        Carga los vehículos desde el archivo txt si existe
        """
        # Verificamos si el archivo ya existe
        if os.path.exists(self.nombre_archivo):
            with open(self.nombre_archivo, "r", encoding="utf-8") as archivo:
                # Leemos línea por línea
                for linea in archivo:
                    vehiculo = Vehiculo.desde_linea(linea)

                    # Si la línea fue convertida correctamente, la agregamos
                    if vehiculo:
                        self._vehiculos.append(vehiculo)