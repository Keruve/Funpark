import os

def guiongen():
    print("-------------------------------------------------------------------------")
def clear_console():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')
def main_menu():
    print("------------------------------ PARKING-001 ------------------------------")
    print("1. Gestion de plazas disponibles")
    print("2. Gestion de plazas ocupadas")
    print("3. Gestion de plazas por tipo de vehiculo")
    print("4. Gestion de plazas por planta")
    print("5. Generacion ticket estacionamiento.")
    print("6. Registro de clientes.")
    print("7. Facturacion y registro de pagos.")
    print("1. ")
    print("1. ")
    print("1. ")
    print("1. ")
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