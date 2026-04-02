# ui/app_tkinter.py

# Importamos tkinter para crear la interfaz gráfica
import tkinter as tk

# Importamos ttk para usar Treeview (tabla)
# Importamos messagebox para mostrar mensajes al usuario
from tkinter import ttk, messagebox


# Clase principal de la interfaz gráfica
class AppTkinter:
    def __init__(self, root, servicio):
        # Guardamos la ventana principal
        self.root = root

        # Guardamos el servicio recibido por inyección de dependencias
        self.servicio = servicio

        # Configuración de la ventana
        self.root.title("Sistema de Registro de Vehículos DG")
        self.root.geometry("950x600")
        self.root.resizable(False, False)

        # Llamamos al método que crea todos los controles visuales
        self.crear_widgets()

        # Cargamos en la tabla los vehículos guardados en el archivo
        self.cargar_tabla()

    def crear_widgets(self):
        """
        Crea todos los componentes de la interfaz:
        etiquetas, cajas de texto, botones y tabla
        """

        # Título principal
        titulo = tk.Label(
            self.root,
            text="Sistema Garaje DG",
            font=("Arial", 18, "bold")
        )
        titulo.pack(pady=10)

        # Frame para agrupar el formulario
        frame_formulario = tk.Frame(self.root)
        frame_formulario.pack(pady=10)

        # ---------------- CAMPOS DEL FORMULARIO ----------------

        # Etiqueta y caja de texto para la placa
        tk.Label(frame_formulario, text="Placa:", font=("Arial", 12)).grid(
            row=0, column=0, padx=10, pady=5, sticky="e"
        )
        self.entry_placa = tk.Entry(frame_formulario, width=30)
        self.entry_placa.grid(row=0, column=1, padx=10, pady=5)

        # Etiqueta y caja de texto para la marca
        tk.Label(frame_formulario, text="Marca:", font=("Arial", 12)).grid(
            row=1, column=0, padx=10, pady=5, sticky="e"
        )
        self.entry_marca = tk.Entry(frame_formulario, width=30)
        self.entry_marca.grid(row=1, column=1, padx=10, pady=5)

        # Etiqueta y caja de texto para el propietario
        tk.Label(frame_formulario, text="Propietario:", font=("Arial", 12)).grid(
            row=2, column=0, padx=10, pady=5, sticky="e"
        )
        self.entry_propietario = tk.Entry(frame_formulario, width=30)
        self.entry_propietario.grid(row=2, column=1, padx=10, pady=5)

        # ---------------- BOTONES ----------------

        # Frame para agrupar los botones
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)

        # Botón para agregar un vehículo
        btn_agregar = tk.Button(
            frame_botones,
            text="Agregar vehículo",
            width=18,
            command=self.agregar_vehiculo
        )
        btn_agregar.grid(row=0, column=0, padx=10)

        # Botón para registrar salida del vehículo seleccionado
        btn_registrar_salida = tk.Button(
            frame_botones,
            text="Registrar salida",
            width=18,
            command=self.registrar_salida
        )
        btn_registrar_salida.grid(row=0, column=1, padx=10)

        # Botón para limpiar los campos del formulario
        btn_limpiar = tk.Button(
            frame_botones,
            text="Limpiar",
            width=18,
            command=self.limpiar_campos
        )
        btn_limpiar.grid(row=0, column=2, padx=10)

        # ---------------- TABLA ----------------

        # Definimos las columnas de la tabla
        columnas = ("placa", "marca", "propietario", "hora_entrada", "hora_salida")

        # Creamos la tabla
        self.tabla = ttk.Treeview(
            self.root,
            columns=columnas,
            show="headings",
            height=12
        )

        # Encabezados de las columnas
        self.tabla.heading("placa", text="Placa")
        self.tabla.heading("marca", text="Marca")
        self.tabla.heading("propietario", text="Propietario")
        self.tabla.heading("hora_entrada", text="Hora Entrada")
        self.tabla.heading("hora_salida", text="Hora Salida")

        # Tamaño y alineación de las columnas
        self.tabla.column("placa", width=120, anchor="center")
        self.tabla.column("marca", width=150, anchor="center")
        self.tabla.column("propietario", width=180, anchor="center")
        self.tabla.column("hora_entrada", width=150, anchor="center")
        self.tabla.column("hora_salida", width=150, anchor="center")

        # Mostramos la tabla en pantalla
        self.tabla.pack(pady=15)

    def agregar_vehiculo(self):
        """
        Toma los datos escritos en el formulario y registra el vehículo
        """

        # Obtenemos los valores escritos por el usuario
        placa = self.entry_placa.get().strip()
        marca = self.entry_marca.get().strip()
        propietario = self.entry_propietario.get().strip()

        # Validamos que no existan campos vacíos
        if not placa or not marca or not propietario:
            messagebox.showwarning("Campos vacíos", "Complete todos los campos.")
            return

        # Llamamos al servicio para crear y guardar el vehículo
        vehiculo = self.servicio.agregar_vehiculo(placa, marca, propietario)

        # Insertamos el vehículo nuevo en la tabla
        self.tabla.insert("", "end", values=(
            vehiculo.placa,
            vehiculo.marca,
            vehiculo.propietario,
            vehiculo.hora_entrada,
            vehiculo.hora_salida
        ))

        # Mostramos mensaje al usuario
        messagebox.showinfo("Éxito", "Vehículo registrado correctamente.")

        # Limpiamos los campos
        self.limpiar_campos()

    def registrar_salida(self):
        """
        Registra la hora de salida del vehículo seleccionado en la tabla
        """

        # Obtenemos la fila seleccionada
        seleccion = self.tabla.selection()

        # Si no hay ninguna fila seleccionada, mostramos advertencia
        if not seleccion:
            messagebox.showwarning("Sin selección", "Seleccione un vehículo de la tabla.")
            return

        # Recuperamos la información de la fila seleccionada
        item = self.tabla.item(seleccion[0])
        valores = item["values"]

        # La placa está en la primera columna
        placa = valores[0]

        # Llamamos al servicio para registrar la salida
        vehiculo_actualizado = self.servicio.registrar_salida(placa)

        # Si devuelve None, es porque ya tenía salida o no se encontró
        if vehiculo_actualizado is None:
            messagebox.showinfo("Aviso", "Ese vehículo ya tiene hora de salida registrada.")
            return

        # Actualizamos la fila de la tabla con la nueva hora de salida
        self.tabla.item(seleccion[0], values=(
            vehiculo_actualizado.placa,
            vehiculo_actualizado.marca,
            vehiculo_actualizado.propietario,
            vehiculo_actualizado.hora_entrada,
            vehiculo_actualizado.hora_salida
        ))

        # Mostramos mensaje de confirmación
        messagebox.showinfo("Éxito", "Hora de salida registrada correctamente.")

    def limpiar_campos(self):
        """
        Limpia las cajas de texto del formulario
        """
        self.entry_placa.delete(0, tk.END)
        self.entry_marca.delete(0, tk.END)
        self.entry_propietario.delete(0, tk.END)

    def cargar_tabla(self):
        """
        Carga los vehículos guardados en el archivo txt dentro de la tabla
        """
        for vehiculo in self.servicio.listar_vehiculos():
            self.tabla.insert("", "end", values=(
                vehiculo.placa,
                vehiculo.marca,
                vehiculo.propietario,
                vehiculo.hora_entrada,
                vehiculo.hora_salida
            ))