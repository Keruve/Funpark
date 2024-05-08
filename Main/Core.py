import tkinter as tk 
from tkinter import messagebox, ttk
import os
import datetime
import json
import threading
import time
import atexit
import csv
#---------------------------------------------------------------- (⭣) ERRORES CONOCIDOS                                            
"""
-> Condicionales en caso de fallo tanto de almacenamiento como de retirada de vehiculo: ------------------------------------------>(⇛007)/(⇛008)
    - La interfaz actua siempre como si hubiera tanto almacenado como sacado un vehiculo de forma correcta aunque se de fallo.
"""
#---------------------------------------------------------------- (⭣) MEJORAS A FUTURO                                             
"""
-> 
"""
#---------------------------------------------------------------- (⭣) CLASE PARKING SPOT ----------------------------------------->(⇛001)
class ParkingSpot:
    def __init__(self, spot_number, size):
        self.spot_number = spot_number
        self.size = size
        self.occupied = False
#---------------------------------------------------------------- (⭣) CLASE VEHICULO --------------------------------------------->(⇛002)
class Vehicle:
    def __init__(self, plate_number, vehicle_type, size):
        self.plate_number = plate_number
        self.vehicle_type = vehicle_type
        self.size = size
#---------------------------------------------------------------- (⭣) CLASE PARKING ---------------------------------------------->(⇛003)
class Parking:
    #------------------------------------------------------------ (⭣) INNIT ------------------------------------------------------>(⇛004.01)
    def __init__(self):
        self.num_floors = 4
        self.spots_per_floor = 25
        self.spots = [[ParkingSpot(f * self.spots_per_floor + spot_number, size) for spot_number in range(1, self.spots_per_floor + 1)] for f in range(self.num_floors) for size in ["Small", "Regular", "Large", "Van"]]
        self.history_file = "parking_history.json"
        self.load_history()
        self.tariff = {
            "Small": {
                "rate_per_minute": 0.05
            },
            "Regular": {
                "rate_per_minute": 0.06
            },
            "Large": {
                "rate_per_minute": 0.08
            },
            "Van": {
                "rate_per_minute": 0.10
            }
        }
        self.update_tariff_thread = threading.Thread(target=self.update_tariff)
        self.update_tariff_thread.daemon = True
        self.update_tariff_thread.start()

        self.save_thread = threading.Thread(target=self.save_periodically)
        self.save_thread.daemon = True
        self.save_thread.start()
        atexit.register(self.save_history)
    #------------------------------------------------------------ (⭣) ACTUALIZACION DE TARIFA ------------------------------------>(⇛004.02)
    def update_tariff(self):
        while True:
            time.sleep(60)
    #------------------------------------------------------------ (⭣) CARGAR HISTORIAL ------------------------------------------->(⇛004.03)
    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                self.history = json.load(f)
        else:
            self.history = {"entries": []}
    #------------------------------------------------------------ (⭣) GURDAR HISTORIAL ------------------------------------------->(⇛004.04)
    def save_history(self):
        with open(self.history_file, "w") as f:
            json.dump(self.history, f, indent=4)
    #------------------------------------------------------------ (⭣) GUARDADO AUTOMATICO ---------------------------------------->(⇛004.05)
    def save_periodically(self):
        while True:
            self.save_history()
            time.sleep(60)
    #------------------------------------------------------------ (⭣) BUSQUEDA PLAZA DISPONIBLE ---------------------------------->(⇛004.06)
    def find_available_spot(self, vehicle):
        for floor in self.spots:
            for spot in floor:
                if not spot.occupied and (spot.size == vehicle.size):
                    return spot
        return None
    #------------------------------------------------------------ (⭣) APARCAR VEHICULO ------------------------------------------->(⇛004.07)
    def park_vehicle(self, vehicle):
        spot = self.find_available_spot(vehicle)
        if spot:
            spot.occupied = True
            print(f"\nVehicle {vehicle.plate_number} parked in {spot.spot_number}.")
            entry = {"plate_number": vehicle.plate_number, "vehicle_type": vehicle.vehicle_type, "size": vehicle.size, "entry_time": str(datetime.datetime.now()), "total_fee": 0}
            self.history["entries"].append(entry)            
        else:
            print("\nNo places available for this vehicle.")
    #------------------------------------------------------------ (⭣) SACAR VEHICULO --------------------------------------------->(⇛004.08)
    def release_spot(self, plate_number):
        current_time = datetime.datetime.now()
        for entry in self.history["entries"]:
            if entry["plate_number"] == plate_number:
                self.history["entries"].remove(entry)
                check_in_time = datetime.datetime.strptime(entry["entry_time"], "%Y-%m-%d %H:%M:%S.%f")
                duration = current_time - check_in_time
                minutes = duration.total_seconds() / 60
                fee = self.calculate_fee(minutes, entry["size"])
                entry["total_fee"] += fee
                print("\n===== Departure report =====")
                print(f"Plate: {entry['plate_number']}")
                print(f"Type of vehicle: {entry['vehicle_type']}")
                print(f"Size: {entry['size']}")
                print(f"Entry time: {entry['entry_time']}")
                print(f"Departure time: {current_time}")
                print(f"Elapsed time: {int(minutes)} minutes")
                print(f"Total fee: {fee} euros")
                print("===========================")
                return
        print(f"\A vehicle with the license plate {plate_number} was not found in the parking lot.")
    #------------------------------------------------------------ (⭣) CLACULAR TASA ---------------------------------------------->(⇛004.09)
    def calculate_fee(self, minutes, vehicle_size):
        rate_per_minute = self.tariff.get(vehicle_size, {}).get("rate_per_minute", 0)
        return round(rate_per_minute * minutes, 2)
    #------------------------------------------------------------ (⭣) GENERACION DE INFORME GENERAL ------------------------------>(⇛004.10)
    def generate_report(self):
        total_earnings = 0
        current_time = datetime.datetime.now()
        print("\n===== Daily report =====")
        for floor_num, floor in enumerate(self.spots, start=1):
            occupied_spots = sum(1 for spot in floor if spot.occupied)
            available_spots = self.spots_per_floor - occupied_spots
            floor_earnings = 0
            for spot in floor:
                if spot.occupied:
                    entry = next((e for e in self.history["entries"] if e["plate_number"] == spot.occupied), None)
                    if entry:
                        check_in_time = datetime.datetime.strptime(entry["entry_time"], "%Y-%m-%d %H:%M:%S.%f")
                        duration = current_time - check_in_time
                        minutes = duration.total_seconds() / 60
                        fee = self.calculate_fee(minutes, entry["size"])
                        floor_earnings += fee
                        total_earnings += fee
                        print(f"Vehículo {entry['plate_number']} - Tarifa: {fee} euros")
            print(f"Floor {floor_num}:")
            print(f"Número de vehículos estacionados: {occupied_spots}")
            print(f"Number of parked vehicles: {available_spots}")
            print(f"Ganancias de la planta: {floor_earnings} euros")
            print("------------------------------")
        print(f"Floor earnings: {total_earnings} euros")
        print("==========================")
    #------------------------------------------------------------ (⭣) GENERACION DE EXEL ----------------------------------------->(⇛004.11)
    def generate_excel_report(self):
        file_name = "Parked_vehicles.csv"
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Plate", "Type", "Size", "Entry time", "Fee"])
            for entry in self.history["entries"]:
                writer.writerow([entry["plate_number"], entry["vehicle_type"], entry["size"], entry["entry_time"], entry["total_fee"]])
    #------------------------------------------------------------ (⭣) RECOGER TODOS LOS VEHICULOS -------------------------------->(⇛004.12)
    def get_all_vehicles(self):
        return self.history["entries"]
#---------------------------------------------------------------- (⭣) RECOGIDA DE HORA ------------------------------------------->(⇛004)
def actualizar_reloj():
    hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
    etiqueta_reloj.config(text=hora_actual)
    ventana.after(1000, actualizar_reloj)
#---------------------------------------------------------------- (⭣) CERRAR EL PROGRAMA ----------------------------------------->(⇛005)
def salir():
    result = messagebox.askyesno("Exit", "Are you sure you want to exit?")
    if result:
        parking.save_history()
        ventana.destroy()  
#---------------------------------------------------------------- (⭣) DEFINICION PARKING                                           
parking = Parking()
#---------------------------------------------------------------- (⭣) COMANDO LIMPIEZA DE CONSOLA -------------------------------->(⇛006)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
clear_screen()
#---------------------------------------------------------------- (⭣) VENTANAS
#---------------------------------------------------------------- (⭣) ESTACIONAR VEHICULO ---------------------------------------->(⇛007)
def ventana_estacionar_vehiculo():
    window = tk.Toplevel(ventana)
    window.title("Park new vehicle")
    
    frame = ttk.Frame(window)
    frame.pack(padx=10, pady=10)

    ttk.Label(frame, text="Plate:").grid(row=0, column=0, padx=5, pady=5)
    plate_number_entry = ttk.Entry(frame)
    plate_number_entry.grid(row=0, column=1, padx=5, pady=5)
    #------------------------------------------------------------ (⭣) RECOGER MATRICULA ------------------------------------------>(⇛007.01)
    def get_plate_number():
        global plate_number
        plate_number = plate_number_entry.get()
        print(f"The vehicle plate is: {plate_number}")
        parking.save_history()
    #------------------------------------------------------------ (⭣) ELIMINAR VENTANA ------------------------------------------->(⇛007.02)    
    def destroy_window(window):
        window.destroy()
    #------------------------------------------------------------ (⭣) VEHICULO ALMACENADO ---------------------------------------->(⇛007.03)    
    def vehiculo_almacenado():
        vehicle = Vehicle(plate_number, vehicle_type, size)
        parking.park_vehicle(vehicle)
        window.after(2000, destroy_window, window)
    
    ttk.Label(frame, text="Type of vehicle:").grid(row=1, column=0, padx=5, pady=5)
    vehicle_type_combo = ttk.Combobox(frame, values=["Car", "Motorcycle", "Van"])
    vehicle_type_combo.grid(row=1, column=1, padx=5, pady=5)
    vehicle_type_combo.current(0)

    ttk.Label(frame, text="Size of vehicle:").grid(row=2, column=0, padx=5, pady=5)
    size_options = ["Small", "Regular", "Large"]
    size_combo = ttk.Combobox(frame, values=size_options)
    size_combo.grid(row=2, column=1, padx=5, pady=5)
    #------------------------------------------------------------ (⭣) ACTUALIZADOR ----------------------------------------------->(⇛007.04)
    def actualizar_opciones():
        tipo_seleccionado = vehicle_type_combo.get()
        if tipo_seleccionado == "Motorcycle":
            size_combo.config(values=["Small"])
            size_combo.current(0)
        elif tipo_seleccionado == "Van":
            size_combo.config(values=["Large"])
            size_combo.current(0)
        else:
            size_combo.config(values=size_options)
            size_combo.current(0)

    vehicle_type_combo.bind("<<ComboboxSelected>>", lambda event: actualizar_opciones())

    estacionar_button = ttk.Button(frame, text="Park")
    estacionar_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    #------------------------------------------------------------ (⭣) RECOGER TIPO DE VEHICULO ----------------------------------->(⇛007.05)
    def get_vehicle_type(valor):
        global vehicle_type
        vehicle_type = valor
        print(f"Type of vehicle: {vehicle_type}")
    #------------------------------------------------------------ (⭣) RECOGER TAMAÑO DE VEHICULO --------------------------------->(⇛007.06)
    def get_vehicle_size(valor):
        global size
        size = valor
        print(f"Sice of vehicle: {size}")
    #------------------------------------------------------------ (⭣) ESTACIONAR VEHICULO ---------------------------------------->(⇛007.07)  
    def estacionar_vehiculo():
        global vehicle_type
        global size
        vehicle_type = vehicle_type_combo.get()
        size = size_combo.get()
        get_plate_number()
        get_vehicle_type(vehicle_type)
        get_vehicle_size(size)
        vehiculo_almacenado()
        parking.save_history()
        window.destroy()
    estacionar_button.config(command=estacionar_vehiculo)
#---------------------------------------------------------------- (⭣) SACAR VEHIUCLO --------------------------------------------->(⇛008)
def ventana_sacar_vehiculo():
    
    window = tk.Toplevel(ventana)
    window.title("Check-out")

    frame = ttk.Frame(window)
    frame.pack(padx=10, pady=10)
    
    ttk.Label(frame, text="Plate:").grid(row=0, column=0, padx=5, pady=5)
    plate_number_entry = ttk.Entry(frame)
    plate_number_entry.grid(row=0, column=1, padx=5, pady=5) 
    #------------------------------------------------------------ (⭣) RECOGER MATRIUCLA ------------------------------------------>(⇛008.01)
    def get_plate_number():
        global plate_number
        plate_number = plate_number_entry.get()
        print(f"Actual plate: {plate_number}")
        release_spot()
    
    estacionar_button = ttk.Button(frame, text="Departure")
    estacionar_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5) 
    #------------------------------------------------------------ (⭣) GENERAR REPORTE -------------------------------------------->(⇛008.02)
    def create_report():
        vehicles = parking.get_all_vehicles()#(⇛004.13)
    
        window = tk.Toplevel(ventana)
        window.title("Departure report")
        window.configure(bg="#FF5733") 
        
        tree = ttk.Treeview(window)
        tree["columns"] = ("Plate", "Type", "Size", "Entry time", "Departure time", "Fee")
        tree.heading("#0", text="ID")
        tree.heading("Plate", text="Plate")
        tree.heading("Type", text="Type")
        tree.heading("Size", text="Size")
        tree.heading("Entry time", text="Entry time")
        tree.heading("Departure time", text="Departure time")
        tree.heading("Fee", text="Fee")
        
        for i, vehicle in enumerate(vehicles):
            plate_number_in = vehicle["plate_number"]
            if plate_number == plate_number_in:
                continue
        
        plate_number_in = vehicle["plate_number"]
        vehicle_type = vehicle["vehicle_type"]
        size = vehicle["size"]
        entry_time = vehicle["entry_time"]
        current_time = datetime.datetime.now()
        check_in_time = datetime.datetime.strptime(vehicle["entry_time"], "%Y-%m-%d %H:%M:%S.%f")
        duration = current_time - check_in_time
        minutes = duration.total_seconds() / 60
        fee = parking.calculate_fee(minutes, size)#(⇛004.09)
        tree.insert("", i, text=str(i), values=(plate_number, vehicle_type, size, entry_time, fee))
            
        tree.pack(expand=True, fill="both")
    #------------------------------------------------------------ (⭣) LIBERAR ESPACIO PARKING ------------------------------------>(⇛008.03)      
    def release_spot():
        global plate_number
        parking.release_spot(plate_number)
        create_report()
        parking.save_history()
    estacionar_button.config(command=get_plate_number)
#---------------------------------------------------------------- (⭣) LISTAR VEHICULOS ------------------------------------------->(⇛009)
def ventana_listar_vehiculo():
    #------------------------------------------------------------ (⭣) FORMATO VENTANA LISTAR VEHICULO
    vehicles = parking.get_all_vehicles()#(⇛004.12)
    
    window = tk.Toplevel(ventana)
    window.title("List parked vehicles")
    window.configure(bg="#FF5733") 
    
    tree = ttk.Treeview(window)
    tree["columns"] = ("Plate", "Type", "Size", "Entry time", "Fee")
    tree.heading("#0", text="ID")
    tree.heading("Plate", text="Plate")
    tree.heading("Type", text="Type")
    tree.heading("Size", text="Size")
    tree.heading("Entry time", text="Entry time")
    tree.heading("Fee", text="Fee")
    
    for i, vehicle in enumerate(vehicles):
        plate_number = vehicle["plate_number"]
        vehicle_type = vehicle["vehicle_type"]
        size = vehicle["size"]
        entry_time = vehicle["entry_time"]
        current_time = datetime.datetime.now()
        check_in_time = datetime.datetime.strptime(vehicle["entry_time"], "%Y-%m-%d %H:%M:%S.%f")
        duration = current_time - check_in_time
        minutes = duration.total_seconds() / 60
        fee = parking.calculate_fee(minutes, size)#(⇛004.09)
        tree.insert("", i, text=str(i), values=(plate_number, vehicle_type, size, entry_time, fee))
    
    tree.pack(expand=True, fill="both")
#---------------------------------------------------------------- (⭣) GENERAR INFORME -------------------------------------------->(⇛010)
def ventana_generar_informe():
    #------------------------------------------------------------ (⭣) FORMATO VENTANA GENERAR INFORME GENERAL
    result = messagebox.showinfo("Excel file",  "Excel file generated successfully.")
    if result:
        print("Excel file generated successfully.")
#---------------------------------------------------------------- (⭣) FIN VENTANAS
ventana = tk.Tk()
ventana.title("FunPark v.001")
#---------------------------------------------------------------- (⭣) FORMATO VENTANA MAIN
ventana.geometry("282x284")
ventana.config(bg="white")
heigthbutton = 1
widthbutton = 30
colorbutton = "lightgray"
colortextbutton = "black"

colorbuttonsalir = "#FF5733"
colortextbuttonsalir = "white"

fontbutton = "Helvetica"
reliefbutton = "flat"
#---------------------------------------------------------------- (⭣) ETIQUETA TITULO
etiquetaFunPark = tk.Label(ventana, text="FunPark", font=(fontbutton, 12), bg="white", relief=reliefbutton)
etiquetaFunPark.pack()
etiquetaFunPark.place(x=113, y=1)
#---------------------------------------------------------------- (⭣) BOTON ESTACIONAR
botonEstacionar = tk.Button(ventana, text="Park vehicle", command=ventana_estacionar_vehiculo)#(⇛007)
botonEstacionar.pack()
botonEstacionar.place(x=1, y=51)
botonEstacionar.config(width=widthbutton, height=heigthbutton, bg=colorbutton, fg=colortextbutton, font=(fontbutton, 12), relief=reliefbutton)
#---------------------------------------------------------------- (⭣) BOTON SACAR
botonSacar = tk.Button(ventana, text="Vehicle departure", command=ventana_sacar_vehiculo)#(⇛008)
botonSacar.pack()
botonSacar.place(x=1, y=101)
botonSacar.config(width=widthbutton, height=heigthbutton, bg=colorbutton, fg=colortextbutton, font=(fontbutton, 12), relief=reliefbutton)
#---------------------------------------------------------------- (⭣) BOTON LISTA
botonListar = tk.Button(ventana, text="List parked vehicles", command=ventana_listar_vehiculo)#(⇛009)
botonListar.pack()
botonListar.place(x=1, y=151)
botonListar.config(width=widthbutton, height=heigthbutton, bg=colorbutton, fg=colortextbutton, font=(fontbutton, 12), relief=reliefbutton)
#---------------------------------------------------------------- (⭣) BOTON INFORME
#botonInforme = tk.Button(ventana, text="WIP", command=ventana_generar_informe)#(⇛010)
#botonInforme.pack()
#botonInforme.place(x=1, y=201)
#botonInforme.config(width=widthbutton, height=heigthbutton, bg=colorbutton, fg=colortextbutton, font=(fontbutton, 12), relief=reliefbutton)
#---------------------------------------------------------------- (⭣) BOTON SALIR
botonSalir = tk.Button(ventana, text="Exit", command=salir)#(⇛005)
botonSalir.pack()
botonSalir.place(x=1, y=251)
botonSalir.config(width=widthbutton, height=heigthbutton, bg=colorbuttonsalir, fg=colortextbuttonsalir, font=(fontbutton, 12), relief=reliefbutton)
#---------------------------------------------------------------- (⭣) Etiqueta reloj
etiqueta_reloj = tk.Label(ventana, text="", bg="white", font=(fontbutton, 10), relief=reliefbutton)
etiqueta_reloj.pack()
etiqueta_reloj.place(x=225, y=1)

ventana.mainloop()