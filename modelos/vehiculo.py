# modelos/vehiculo.py

# Esta clase representa un vehículo dentro del sistema
class Vehiculo:
    def __init__(self, placa, marca, propietario, hora_entrada, hora_salida=""):
        # Guardamos los datos del vehículo
        self.placa = placa
        self.marca = marca
        self.propietario = propietario
        self.hora_entrada = hora_entrada
        self.hora_salida = hora_salida

    def to_linea(self):
        """
        Convierte el objeto Vehiculo en una línea de texto
        para guardarlo dentro del archivo vehiculos.txt
        """
        return f"{self.placa},{self.marca},{self.propietario},{self.hora_entrada},{self.hora_salida}\n"

    @staticmethod
    def desde_linea(linea):
        """
        Convierte una línea del archivo txt en un objeto Vehiculo
        """
        datos = linea.strip().split(",")

        # Verificamos que existan los 5 datos esperados
        if len(datos) == 5:
            return Vehiculo(
                datos[0],  # placa
                datos[1],  # marca
                datos[2],  # propietario
                datos[3],  # hora_entrada
                datos[4]   # hora_salida
            )

        # Si la línea no tiene el formato correcto, devolvemos None
        return None