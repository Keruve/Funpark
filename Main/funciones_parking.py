import os

class ParkingSpot:
    def __init__(self, spot_number, spot_type, size) -> None:
        self.spot_number = spot_number
        self.spot_type = spot_type
        self.sice = size
        self.vehicle = None
        self.is_empty = True
class Vehicle:
    def __init__(self, license_plate, vehicle_type, size) -> None:
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
        self.sice = size
class Parking:
    def __init__(self) -> None:
        self.spots = self.initialize_spots()
        self.vehicles = []
    def initialize_spots(self):
        spots = []
        spot_number = 1
        for floor in range(1, 5):
            for place in range(5):
                spots.append(ParkingSpot(spot_number, "large", "Camion"))
                spot_number += 1
            for place in range(15):
                spots.append(ParkingSpot(spot_number, "medium", "Coche"))
                spot_number += 1
            for place in range(5):
                spots.append(ParkingSpot(spot_number, "Small", "Motocicleta"))
                spot_number += 1
        return spots
    def park_vehicle(self, vehicle):
        spot = self.find_available_spot(vehicle)
        if spot:
            spot.is_empty = False
            spot.vehicle = None
            self.vehicle = vehicle
            self.vehicles.append(vehicle)
            print(f"Vehiculo con matricula ({vehicle.license_plate}) agredado con exito a la plaza {spot.spot_number}")
        else:
            print(f"La plaza {spot.spot_number} no existe.")
    def release_spot(self, spot_number):
        for spot in self.spots:
            if spot.spot_number == spot_number:
                spot.is_empty = True
                spot.vehicle = None
                print(f"Plaza numero {spot_number} liberada.")
                return
        print(f"Plaza numero {spot_number} no encontrada")
    def find_available_spot(self, vehicle):
        for spot in self.spots:
            if spot.is_empty and spot.size == vehicle.size and spot.vehicle_type == vehicle.vehicle_type:
                return spot
        return None
    def available_spots_floor(self):
        available_spots = {
            "Coche": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "Motocicleta": [0, 0, 0, 0, 0],
            "Camion": [0, 0, 0, 0, 0]
        }
        for spot in self.spots:
            floor = (spot.spot_number -1) // 25
            if spot.is_empty:
                if spot.spot_type == "camion":
                    available_spots["camion"][floor] += 1
                elif spot.spot_type == "coche":
                    available_spots["coche"][floor] += 1
                elif spot.spot_type == "motocicleta":
                    available_spots["motocicleta"][floor] += 1
        return available_spots
    def print_available_spots(self):
        available_spots = self.available_spots_floor()

        print("Plazas disponibles por piso:")
        for floor in range(4):
            trucks = available_spots["Camion"][floor]
            cars = available_spots["Coche"][floor]
            motorcycles = available_spots["Motocicleta"][floor]
            print(f"Piso {floor + 1}:\nPlaza camiones:        {trucks}\nPlaza coches:          {cars}\nPlaza motocicletas:    {motorcycles}\n")
            
parking = Parking()


def guiongen():
    print("-------------------------------------------------------------------------")
def clear_console():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')
def main_menu():
    print("------------------------------ PARKING-001 ------------------------------")
    print("1. Gestion de plazas general")
    print("2. Gestion de plazas ocupadas")
    print("3. Gestion de plazas por tipo de vehiculo")
    print("4. Gestion de plazas por planta")
    print("5. Generacion ticket estacionamiento.")
    print("6. Registro de clientes.")
    print("7. Facturacion y registro de pagos.")
    guiongen()
    print("E. Cerrar el programa.")
    guiongen()
def selector_main_menu():
    optiongen = str(input(">"))
    option = optiongen.lower()
    while True:
        if option == "1":
            clear_console()
            print("---------------------- GESTION PLAZAS DISPONIBLES -----------------------")
            parking.print_available_spots()
            input(">")
        if option == "2":
            clear_console()
            print("---------------------- GESTION DE PLAZAS OCUPADAS -----------------------")
            input(">")
        if option == "3":
            clear_console()
            print("---------------- GESTION DE PLAZAS POR TIPO DE VEHICULO -----------------")
            gestion_plazas_tipo_vehiculo()
        if option == "4":
            clear_console()
            print("--------------------- GESTION DE PLAZAS POR PLANTA ----------------------")
            gestion_plazas_planta()
        if option == "5":
            clear_console()
            print("---------------- GENERACION DE TICKET DE ESTACIONAMIENTO ----------------")
            input(">")
        if option == "6":
            clear_console()
            print("------------------------- REGISTRO DE CLIENTES --------------------------")
            input(">")
        if option == "7":
            clear_console()
            print("-------------------- FACTURACION Y REGISTRO DE PAGOS --------------------")
            input(">")
        if option == "e":
            clear_console()
            print("Gracias por utilizar Funpark :)")
            breakpoint()
        else:
            clear_console()
            print("------------------------------ ERROR ------------------------------------")
            input("Porfavor ingrese una opcion valida, Presiona enter para continuar...")
            continue
def gestion_plazas_planta():
    print("0. Planta 0")
    print("1. Planta 1")
    print("2. Planta 2")
    print("3. Planta 3")
    print("4. Planta VIP")
    guiongen()
    print("E. Para retroceder en el menu.")
    guiongen()
    optiongen = str(input(">"))
    option = optiongen.lower()
    while True:
        if option == "0":
            clear_console()
            print("------------------------------- PLANTA 0 --------------------------------")
        if option == "1":
            clear_console()
            print("------------------------------- PLANTA 1 --------------------------------")
        if option == "2":
            clear_console()
            print("------------------------------- PLANTA 2 --------------------------------")
        if option == "3":
            clear_console()
            print("------------------------------- PLANTA 3 --------------------------------")
        if option == "4":
            clear_console()
            print("------------------------------ PLANTA VIP -------------------------------")
        if option == "e":
            clear_console()
            main_menu()
            selector_main_menu()
        else:
            clear_console()
            print("------------------------------ ERROR ------------------------------------")
            input("Porfavor ingrese una opcion valida, Presiona enter para continuar...")
            continue
def gestion_plazas_tipo_vehiculo():
    print("1. Coche")
    print("2. Motocicletas")
    print("3. Camion")
    print("4. Bicicleta")
    print("5. Vehiculo VIP")
    guiongen()
    print("E. Para retroceder en el menu.")
    guiongen()
    optiongen = str(input(">"))
    option = optiongen.lower()
    while True:
        if option == "1":
            clear_console()
            print("-------------------------------- COCHES ---------------------------------")
        if option == "2":
            clear_console()
            print("----------------------------- MOTOCICLETAS ------------------------------")
        if option == "3":
            clear_console()
            print("------------------------------- CAMIONES --------------------------------")
        if option == "4":
            clear_console()
            print("------------------------------ BICICLETAS -------------------------------")
        if option == "5":
            clear_console()
            print("----------------------------- VEHICULO VIP ------------------------------")
        if option == "e":
            clear_console()
            main_menu()
            selector_main_menu()
        else:
            clear_console()
            print("------------------------------ ERROR ------------------------------------")
            input("Porfavor ingrese una opcion valida, Presiona enter para continuar...")
            continue