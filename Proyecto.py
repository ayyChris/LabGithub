import tkinter as tk
from tkinter import END, messagebox, ttk
import pyodbc
import datetime
from tkinter import ttk
import re
import decimal

login_window = None


# Función para conectarse a la base de datos
def conectar_bd(username, password):
    conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=localhost;DATABASE=AgenciaVehiculos1;UID={username};PWD={password}"
    try:
        conexion = pyodbc.connect(conn_str)
        print("Conexión a la base de datos establecida correctamente.")
        return conexion
    except pyodbc.Error as e:
        print("Error de pyodbc:", e)
        return None


# Función para obtener el rol del usuario desde la base de datos
def obtener_rol_usuario(conexion, username):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT IS_MEMBER('administrador') AS es_administrador")
        row = cursor.fetchone()
        if row:
            if row.es_administrador == 1:
                return "administrador"
            else:
                return "usuario"
        else:
            return None
    except pyodbc.Error as e:
        print("Error de pyodbc:", e)
        return None


def mostrar_vista_inventario(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM view_InventarioVehiculos")
        datos_inventario = cursor.fetchall()

        # Crear una ventana para mostrar los datos
        vista_window = tk.Tk()
        vista_window.title("Vista de Inventario de Vehículos")

        # Crear un Treeview para mostrar los datos en forma de tabla
        tree = ttk.Treeview(vista_window)
        tree["columns"] = (
            "ID",
            "Placa",
            "Tipo",
            "Marca",
            "Modelo",
            "Año",
            "Precio",
            "Estado",
            "Dirección",
            "Ciudad",
            "País",
        )

        # Configurar las columnas
        tree.column("#0", width=0, stretch=tk.NO)  # Espacio en blanco
        tree.column("ID", width=50, anchor=tk.CENTER)
        tree.column("Placa", width=100, anchor=tk.CENTER)
        tree.column("Tipo", width=100, anchor=tk.CENTER)
        tree.column("Marca", width=100, anchor=tk.CENTER)
        tree.column("Modelo", width=100, anchor=tk.CENTER)
        tree.column("Año", width=70, anchor=tk.CENTER)
        tree.column("Precio", width=70, anchor=tk.CENTER)
        tree.column("Estado", width=100, anchor=tk.CENTER)
        tree.column("Dirección", width=150, anchor=tk.CENTER)
        tree.column("Ciudad", width=100, anchor=tk.CENTER)
        tree.column("País", width=100, anchor=tk.CENTER)

        # Encabezados
        tree.heading("#0", text="", anchor=tk.CENTER)
        tree.heading("ID", text="ID", anchor=tk.CENTER)
        tree.heading("Placa", text="Placa", anchor=tk.CENTER)
        tree.heading("Tipo", text="Tipo", anchor=tk.CENTER)
        tree.heading("Marca", text="Marca", anchor=tk.CENTER)
        tree.heading("Modelo", text="Modelo", anchor=tk.CENTER)
        tree.heading("Año", text="Año", anchor=tk.CENTER)
        tree.heading("Precio", text="Precio", anchor=tk.CENTER)
        tree.heading("Estado", text="Estado", anchor=tk.CENTER)
        tree.heading("Dirección", text="Dirección", anchor=tk.CENTER)
        tree.heading("Ciudad", text="Ciudad", anchor=tk.CENTER)
        tree.heading("País", text="País", anchor=tk.CENTER)

        # Crear estilo para el Treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12))

        # Insertar datos en el Treeview
        for fila in datos_inventario:
            # Convertir el precio a un número flotante si es un objeto Decimal
            fila = list(fila)
            fila[6] = (
                float(fila[6]) if isinstance(fila[6], decimal.Decimal) else fila[6]
            )

            tree.insert("", tk.END, values=fila)

        tree.pack(expand=True, fill="both")
        vista_window.mainloop()

    except pyodbc.Error as e:
        print("Error de pyodbc:", e)
        messagebox.showerror("Error", "No se pudo mostrar la vista de inventario.")


def mostrar_vista_ventas(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM view_VentasDetalles")
        datos_ventas = cursor.fetchall()

        # Crear una ventana para mostrar los datos
        ventas_window = tk.Tk()
        ventas_window.title("Vista de Detalles de Ventas")

        # Crear un Treeview para mostrar los datos en forma de tabla
        tree = ttk.Treeview(ventas_window)
        tree["columns"] = (
            "ID Venta",
            "Fecha",
            "Nombre Cliente",
            "Apellido Cliente",
            "Marca",
            "Modelo",
            "Año",
            "Precio Venta",
            "Método Pago",
        )

        # Configurar las columnas
        tree.column("#0", width=0, stretch=tk.NO)  # Espacio en blanco
        tree.column("ID Venta", width=100, anchor=tk.CENTER)
        tree.column("Fecha", width=150, anchor=tk.CENTER)
        tree.column("Nombre Cliente", width=150, anchor=tk.CENTER)
        tree.column("Apellido Cliente", width=150, anchor=tk.CENTER)
        tree.column("Marca", width=100, anchor=tk.CENTER)
        tree.column("Modelo", width=100, anchor=tk.CENTER)
        tree.column("Año", width=70, anchor=tk.CENTER)
        tree.column("Precio Venta", width=100, anchor=tk.CENTER)
        tree.column("Método Pago", width=150, anchor=tk.CENTER)

        # Encabezados
        tree.heading("#0", text="", anchor=tk.CENTER)
        tree.heading("ID Venta", text="ID Venta", anchor=tk.CENTER)
        tree.heading("Fecha", text="Fecha", anchor=tk.CENTER)
        tree.heading("Nombre Cliente", text="Nombre Cliente", anchor=tk.CENTER)
        tree.heading("Apellido Cliente", text="Apellido Cliente", anchor=tk.CENTER)
        tree.heading("Marca", text="Marca", anchor=tk.CENTER)
        tree.heading("Modelo", text="Modelo", anchor=tk.CENTER)
        tree.heading("Año", text="Año", anchor=tk.CENTER)
        tree.heading("Precio Venta", text="Precio Venta", anchor=tk.CENTER)
        tree.heading("Método Pago", text="Método Pago", anchor=tk.CENTER)

        # Crear estilo para el Treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12))

        # Insertar datos en el Treeview
        for fila in datos_ventas:
            # Convertir la fecha a una cadena formateada
            fila = list(fila)
            fila[1] = (
                fila[1].strftime("%Y-%m-%d %H:%M:%S") if fila[1] else ""
            )  # Assuming fecha is at index 1
            tree.insert("", tk.END, values=tuple(fila))

        tree.pack(expand=True, fill="both")
        ventas_window.mainloop()

    except pyodbc.Error as e:
        print("Error de pyodbc:", e)
        messagebox.showerror("Error", "No se pudo mostrar la vista de ventas.")


def obtener_ubicaciones(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT idUbicacion, dirección FROM Inventario.Ubicaciones")
        ubicaciones = cursor.fetchall()
        print("Datos de ubicaciones:", ubicaciones)
        return ubicaciones
    except pyodbc.Error as e:
        print("Error de pyodbc:", e)
        return []


# Función para ejecutar el procedimiento almacenado con datos ingresados por el usuario
def ejecutar_procedimiento(
    conexion, placa, tipo, marca, modelo, año, precio, estado, ubicacion
):
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "EXEC sp_AñadirVehiculoInventario ?,?,?,?,?,?,?,?",
            (placa, tipo, marca, modelo, año, precio, estado, ubicacion),
        )
        conexion.commit()
        print("Procedimiento almacenado ejecutado correctamente.")
    except pyodbc.Error as e:
        print("Error de pyodbc:", e)
    except Exception as e:
        print("Error inesperado:", e)


import random


def obtener_datos(
    conexion, placa, tipo, marca, modelo, año, precio, estado, ubicacion_var
):
    try:
        ubicacion_seleccionada = ubicacion_var.get()
        if ubicacion_seleccionada:
            # Separar el ID de la ubicación del nombre
            id_ubicacion = int(ubicacion_seleccionada.split(":")[0])
        else:
            # Si no se selecciona ninguna ubicación, elegir una aleatoria entre 1 y 6
            id_ubicacion = random.randint(1, 6)
        # Ejecutar el procedimiento almacenado con el ID de ubicación
        ejecutar_procedimiento(
            conexion, placa, tipo, marca, modelo, año, precio, estado, id_ubicacion
        )
    except pyodbc.Error as e:
        print("Error de pyodbc:", e)
    except Exception as e:
        print("Error inesperado:", e)


def mostrar_ingreso_vehiculos(conexion):
    ventana_ingreso = tk.Tk()
    ventana_ingreso.title("Ingresar Vehículo")

    # Ajustar tamaño de la ventana
    ventana_ingreso.geometry("300x400")

    # Crear estilo para los campos de texto
    style = ttk.Style()
    style.configure("TEntry", font=("Arial", 12))

    # Etiquetas y campos de entrada para los datos del vehículo
    tk.Label(ventana_ingreso, text="Placa:").grid(row=0, column=0, padx=5, pady=5)
    entry_placa = ttk.Entry(ventana_ingreso, style="TEntry")
    entry_placa.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(ventana_ingreso, text="Tipo:").grid(row=1, column=0, padx=5, pady=5)
    entry_tipo = ttk.Entry(ventana_ingreso, style="TEntry")
    entry_tipo.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(ventana_ingreso, text="Marca:").grid(row=2, column=0, padx=5, pady=5)
    entry_marca = ttk.Entry(ventana_ingreso, style="TEntry")
    entry_marca.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(ventana_ingreso, text="Modelo:").grid(row=3, column=0, padx=5, pady=5)
    entry_modelo = ttk.Entry(ventana_ingreso, style="TEntry")
    entry_modelo.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(ventana_ingreso, text="Año:").grid(row=4, column=0, padx=5, pady=5)
    entry_año = ttk.Entry(ventana_ingreso, style="TEntry")
    entry_año.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(ventana_ingreso, text="Precio:").grid(row=5, column=0, padx=5, pady=5)
    entry_precio = ttk.Entry(ventana_ingreso, style="TEntry")
    entry_precio.grid(row=5, column=1, padx=5, pady=5)

    tk.Label(ventana_ingreso, text="Estado:").grid(row=6, column=0, padx=5, pady=5)
    entry_estado = ttk.Entry(ventana_ingreso, style="TEntry")
    entry_estado.grid(row=6, column=1, padx=5, pady=5)

    tk.Label(ventana_ingreso, text="Ubicación:").grid(row=7, column=0, padx=5, pady=5)
    ubicacion_var = tk.StringVar()
    ubicacion_menu = ttk.Combobox(
        ventana_ingreso, textvariable=ubicacion_var, state="readonly", width=20
    )
    ubicacion_menu.grid(row=7, column=1, padx=5, pady=5)
    ubicaciones = obtener_ubicaciones(conexion)
    ubicacion_menu["values"] = [f"{id_}: {nombre}" for id_, nombre in ubicaciones]

    # Función para ingresar el vehículo y cerrar la ventana
    def ingresar_vehiculo():
        obtener_datos(
            conexion,
            entry_placa.get(),
            entry_tipo.get(),
            entry_marca.get(),
            entry_modelo.get(),
            entry_año.get(),
            entry_precio.get(),
            entry_estado.get(),
            ubicacion_var,
        )
        ventana_ingreso.destroy()  # Cerrar la ventana después de ingresar el vehículo

    # Crear estilo para el botón
    style.configure("TButton", font=("Arial", 12), padding=5)

    # Botón para ejecutar el procedimiento almacenado con los datos ingresados
    btn_ingresar = ttk.Button(
        ventana_ingreso,
        text="Ingresar Vehículo",
        command=ingresar_vehiculo,
        style="TButton",
    )
    btn_ingresar.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

    ventana_ingreso.mainloop()


# Función para mostrar la interfaz principal


def mostrar_interfaz_principal(conexion):
    global root
    root = tk.Tk()
    root.title("Menú administrador")
    root.geometry("400x300")  # Establecer el tamaño de la ventana

    style = ttk.Style()
    style.theme_use("clam")

    # Crear estilo para el botón
    style.configure("TButton", font=("Arial", 12), padding=5)

    # Frame para contener los botones y centrarlos
    frame = ttk.Frame(root)
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Botón para ejecutar el procedimiento almacenado para ingresar vehículos al inventario
    btn_ingresar = ttk.Button(
        frame,
        text="Ingresar vehículo a inventario",
        command=lambda: mostrar_ingreso_vehiculos(conexion),
        style="TButton",
    )
    btn_ingresar.pack(fill="x", padx=5, pady=5)

    # Botón para mostrar la vista de inventario
    btn_vista_inventario = ttk.Button(
        frame,
        text="Ver Inventario",
        command=lambda: mostrar_vista_inventario(conexion),
        style="TButton",
    )
    btn_vista_inventario.pack(fill="x", padx=5, pady=5)

    btn_vista_ventas = ttk.Button(
        frame,
        text="Ver Ventas",
        command=lambda: mostrar_vista_ventas(conexion),
        style="TButton",
    )
    btn_vista_ventas.pack(fill="x", padx=5, pady=5)

    # Botón para eliminar vehículos
    btn_eliminar_vehiculo = ttk.Button(
        frame,
        text="Eliminar Vehículo",
        command=lambda: mostrar_eliminar_vehiculo(conexion),
        style="TButton",
    )
    btn_eliminar_vehiculo.pack(fill="x", padx=5, pady=5)

    # Botón para volver al login
    btn_volver_login = ttk.Button(
        frame,
        text="Cerrar sesión",
        command=lambda: [root.destroy(), show_login_window()],
        style="TButton",
    )
    btn_volver_login.pack(fill="x", padx=5, pady=5)

    root.mainloop()


def mostrar_eliminar_vehiculo(conexion):
    eliminar_window = tk.Tk()
    eliminar_window.title("Eliminar Vehículo")
    eliminar_window.geometry("600x400")  # Ajusta el tamaño de la ventana

    # Obtener los datos de la tabla Inventario.Vehículos
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT idVehiculo, Marca, Modelo, Estado FROM Inventario.Vehículos"
        )
        vehiculos_data = cursor.fetchall()
        vehiculos_options = [
            f"{vehiculo[0]} - {vehiculo[1]} - {vehiculo[2]} - {vehiculo[3]}"
            for vehiculo in vehiculos_data
        ]
    except pyodbc.Error as e:
        print("Error de pyodbc:", e)
        messagebox.showerror(
            "Error", "No se pudieron obtener los datos de los vehículos."
        )
        eliminar_window.destroy()
        return

    # Crear estilo para el botón
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=5)

    # Frame para centrar los elementos
    frame = ttk.Frame(eliminar_window)
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Etiqueta y dropdown menu para seleccionar el vehículo a eliminar
    ttk.Label(frame, text="Selecciona el Vehículo:").grid(
        row=0, column=0, padx=5, pady=5
    )
    vehiculo_var = tk.StringVar()
    vehiculo_menu = ttk.Combobox(
        frame, textvariable=vehiculo_var, state="readonly", width=30
    )
    vehiculo_menu.grid(row=0, column=1, padx=5, pady=5)
    vehiculo_menu["values"] = vehiculos_options

    # Etiqueta de advertencia
    advertencia_label = ttk.Label(
        frame,
        text="*Atención, solo puede eliminar vehículos que no hayan sido vendidos*",
        foreground="red",
        font=("Arial", 10, "bold"),
    )
    advertencia_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    # Función para eliminar el vehículo
    def eliminar_vehiculo():
        seleccion = (
            vehiculo_menu.get()
        )  # Obtener el valor seleccionado directamente desde el menú desplegable
        if not seleccion:
            messagebox.showerror("Error", "Por favor selecciona un vehículo.")
            return
        id_vehiculo_match = re.search(r"\d+", seleccion)  # Buscar la ID en la cadena
        if id_vehiculo_match:
            id_vehiculo = id_vehiculo_match.group()  # Obtener la ID del match
            try:
                cursor = conexion.cursor()
                cursor.execute(
                    "EXEC Inventario.eliminarVehiculo @idVehiculo = ?", (id_vehiculo,)
                )
                conexion.commit()
                messagebox.showinfo(
                    "Éxito", "El vehículo ha sido eliminado correctamente."
                )
            except pyodbc.Error as e:
                print("Error de pyodbc:", e)
                messagebox.showerror("Error", "No se pudo eliminar el vehículo.")
            except Exception as e:
                print("Error inesperado:", e)
                messagebox.showerror(
                    "Error", "Ocurrió un error inesperado al eliminar el vehículo."
                )
        else:
            messagebox.showerror(
                "Error", "No se pudo obtener la ID del vehículo seleccionado."
            )
        eliminar_window.destroy()

    # Botón para eliminar el vehículo
    btn_eliminar = ttk.Button(
        frame, text="Eliminar", command=eliminar_vehiculo, style="TButton"
    )
    btn_eliminar.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    eliminar_window.mainloop()


def comprar_carro(conexion):
    compra_window = tk.Tk()
    compra_window.title("Comprar Carro")
    compra_window.geometry("600x600")

    # Función para registrar la venta en la base de datos
    def registrar_venta():
        try:
            # Obtener la fecha actual
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Obtener el precio de venta ingresado por el usuario
            precio_venta = float(entry_precio_venta.get())

            # Obtener el método de pago ingresado por el usuario
            metodo_pago = entry_metodo_pago.get()

            # Obtener los índices seleccionados en los menús desplegables
            cliente_index = cliente_menu.current()
            vehiculo_index = vehiculo_menu.current()

            # Validar que se haya seleccionado un cliente y un vehículo
            if cliente_index == -1 or vehiculo_index == -1:
                messagebox.showerror(
                    "Error", "Por favor selecciona un cliente y un vehículo."
                )
                return

            # Obtener los valores de cliente y vehículo seleccionados
            cliente_seleccionado = clientes[cliente_index]
            id_cliente = cliente_seleccionado[0]  # ID del cliente seleccionado
            nombre_apellido = (
                cliente_seleccionado[1] + " " + cliente_seleccionado[2]
            )  # Nombre y apellido del cliente

            vehiculo_seleccionado = vehiculos[vehiculo_index]
            id_vehiculo = vehiculo_seleccionado[0]  # ID del vehículo seleccionado
            marca = vehiculo_seleccionado[1]  # Marca del vehículo
            modelo = vehiculo_seleccionado[2]  # Modelo del vehículo
            estado = vehiculo_seleccionado[3]  # Estado del vehículo

            # Llamar al procedimiento almacenado para registrar la venta
            cursor = conexion.cursor()
            cursor.execute(
                "EXEC sp_RegistrarVenta ?,?,?,?,?",
                (fecha, id_cliente, id_vehiculo, precio_venta, metodo_pago),
            )
            conexion.commit()

            messagebox.showinfo(
                "Éxito",
                "Venta registrada correctamente\n\n"
                f"ID Cliente: {id_cliente}\n"
                f"Nombre y Apellido: {nombre_apellido}\n\n"
                f"ID Vehículo: {id_vehiculo}\n"
                f"Marca: {marca}\n"
                f"Modelo: {modelo}\n"
                f"Estado: {estado}",
            )
            compra_window.destroy()  # Cerrar la ventana después de registrar la venta

        except pyodbc.Error as e:
            print("Error de pyodbc:", e)
            if "El vehiculo ya fue vendido" in str(e):
                messagebox.showerror("Error", "El vehiculo ya fue vendido.")
            else:
                messagebox.showerror("Error", "No se pudo registrar la venta.")
        except ValueError:
            messagebox.showerror(
                "Error", "Por favor ingresa un precio de venta válido."
            )
        except Exception as e:
            print("Error inesperado:", e)
            messagebox.showerror("Error", "Ocurrió un error inesperado.")

    # Crear estilo para los campos de texto
    style = ttk.Style()
    style.configure("TEntry", font=("Arial", 12))

    # Etiquetas y campos de entrada para los detalles de la venta
    tk.Label(compra_window, text="Fecha:").grid(row=0, column=0, padx=5, pady=5)
    entry_fecha = ttk.Entry(compra_window, state="readonly", style="TEntry")
    entry_fecha.grid(row=0, column=1, padx=5, pady=5)
    entry_fecha.insert(tk.END, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    tk.Label(compra_window, text="Cliente:").grid(row=1, column=0, padx=5, pady=5)
    cliente_var = tk.StringVar()
    cliente_menu = ttk.Combobox(
        compra_window, textvariable=cliente_var, state="readonly", width=20
    )
    cliente_menu.grid(row=1, column=1, padx=5, pady=5)
    # Obtener y mostrar los IDs y nombres de los clientes desde la base de datos
    cursor = conexion.cursor()
    cursor.execute("SELECT idCliente, Nombre, Apellido FROM Ventas.Clientes")
    clientes = cursor.fetchall()
    cliente_menu["values"] = [
        f"{cliente[0]} - {cliente[1]} {cliente[2]}" for cliente in clientes
    ]

    tk.Label(compra_window, text="Vehículo:").grid(row=2, column=0, padx=5, pady=5)
    vehiculo_var = tk.StringVar()
    vehiculo_menu = ttk.Combobox(
        compra_window, textvariable=vehiculo_var, state="readonly", width=50, height=10
    )
    vehiculo_menu.grid(row=2, column=1, padx=5, pady=5)
    # Obtener y mostrar los IDs, marcas, modelos y estados de los vehículos desde la base de datos
    cursor.execute("SELECT idVehiculo, Marca, Modelo, Estado FROM Inventario.Vehículos")
    vehiculos = cursor.fetchall()
    vehiculo_menu["values"] = [
        f"{vehiculo[0]} - {vehiculo[1]} - {vehiculo[2]} - {vehiculo[3]}"
        for vehiculo in vehiculos
    ]

    tk.Label(compra_window, text="Precio de Venta:").grid(
        row=3, column=0, padx=5, pady=5
    )
    entry_precio_venta = tk.Entry(compra_window)
    entry_precio_venta.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(compra_window, text="Método de Pago:").grid(
        row=4, column=0, padx=5, pady=5
    )
    entry_metodo_pago = tk.Entry(compra_window)
    entry_metodo_pago.grid(row=4, column=1, padx=5, pady=5)

    # Crear estilo para el botón
    style.configure("TButton", font=("Arial", 12), padding=5)

    # Botón para registrar la venta
    btn_registrar_venta = ttk.Button(
        compra_window, text="Comprar", command=registrar_venta, style="TButton"
    )
    btn_registrar_venta.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    compra_window.mainloop()


def mostrar_menu_opciones(conexion):
    global root
    menu_window = tk.Tk()
    menu_window.title("Menú de Opciones")
    menu_window.geometry("400x300")  # Ampliar tamaño de la ventana

    # Crear estilo para los botones
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=5)

    # Botón para comprar un carro
    btn_comprar_carro = ttk.Button(
        menu_window, text="Comprar un Carro", command=lambda: comprar_carro(conexion)
    )
    btn_comprar_carro.pack(pady=10)

    btn_volver_login = ttk.Button(
        menu_window,
        text="Cerrar sesión",
        command=lambda: [menu_window.destroy(), show_login_window()],
        style="TButton",
    )
    btn_volver_login.pack(fill="x", padx=5, pady=5)

    # Otros botones y opciones pueden agregarse aquí según sea necesario

    menu_window.mainloop()


def show_login_window():
    global login_window_root

    # Crear la ventana de inicio de sesión
    login_window_root = tk.Tk()
    login_window_root.title("Inicio de Sesión")
    login_window_root.geometry("300x200")  # Ampliar tamaño de la ventana

    # Establecer el estilo para los campos de texto
    style = ttk.Style()
    style.configure("TEntry", font=("Arial", 12))

    # Usuario
    tk.Label(login_window_root, text="Usuario:").place(
        relx=0.3, rely=0.3, anchor=tk.CENTER
    )
    entry_username = ttk.Entry(login_window_root, style="TEntry")
    entry_username.place(relx=0.7, rely=0.3, anchor=tk.CENTER)

    # Contraseña
    tk.Label(login_window_root, text="Contraseña:").place(
        relx=0.3, rely=0.5, anchor=tk.CENTER
    )
    entry_password = ttk.Entry(login_window_root, show="*", style="TEntry")
    entry_password.place(relx=0.7, rely=0.5, anchor=tk.CENTER)

    # Botón de inicio de sesión
    btn_login = ttk.Button(
        login_window_root,
        text="Iniciar Sesión",
        command=lambda: iniciar_sesion(entry_username, entry_password),
        style="TButton",
    )
    btn_login.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    login_window_root.mainloop()


def iniciar_sesion(entry_username, entry_password):
    username = entry_username.get()
    password = entry_password.get()
    conexion = conectar_bd(username, password)
    if conexion:
        rol = obtener_rol_usuario(conexion, username)
        if rol == "administrador":
            login_window_root.destroy()
            mostrar_interfaz_principal(conexion)
        elif rol == "usuario":
            login_window_root.destroy()
            mostrar_menu_opciones(conexion)
        else:
            messagebox.showerror("Error", "Usuario no autorizado.")
    else:
        messagebox.showerror("Error", "Conexión fallida. Verifique sus credenciales.")


show_login_window()
