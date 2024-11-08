import random

def generar_carton_loteria():
    carton = [[None for _ in range(9)] for _ in range(3)]
    decenas = [list(range(1 + i * 10, 11 + i * 10)) for i in range(9)]
    numeros_seleccionados = []
    
    for numeros_decena in decenas:
        numeros_elegidos = random.sample(numeros_decena, k=random.choice([1, 2]))
        numeros_seleccionados.extend(numeros_elegidos)
    
    while len(numeros_seleccionados) != 15:
        if len(numeros_seleccionados) > 15:
            numeros_seleccionados.pop(random.randint(0, len(numeros_seleccionados) - 1))
        else:
            for numeros_decena in decenas:
                if len([n for n in numeros_seleccionados if n in numeros_decena]) < 2:
                    faltante = [n for n in numeros_decena if n not in numeros_seleccionados]
                    if faltante:
                        numeros_seleccionados.append(random.choice(faltante))
                    if len(numeros_seleccionados) == 15:
                        break
    
    columnas = {i: [] for i in range(9)}
    for numero in numeros_seleccionados:
        col = (numero - 1) // 10
        columnas[col].append(numero)
    
    for col, numeros in columnas.items():
        random.shuffle(numeros)
        fila_indices = random.sample(range(3), k=len(numeros))
        
        for i, fila in enumerate(fila_indices):
            carton[fila][col] = numeros[i]
    
    # Extraemos los números del cartón como un conjunto para facilitar la comparación en el sorteo
    numeros_carton = set([n for fila in carton for n in fila if n is not None])
    return carton, numeros_carton

# Generar múltiples cartones distintos
def generar_varios_cartones(cantidad):
    cartones = []
    numeros_cartones = []
    
    while len(cartones) < cantidad:
        carton, numeros_carton = generar_carton_loteria()
        
        # Agregar solo si es único
        if numeros_carton not in numeros_cartones:
            cartones.append(carton)
            numeros_cartones.append(numeros_carton)
    
    return cartones, numeros_cartones

# Realizar el sorteo y encontrar el cartón ganador
def sorteo(numeros_cartones):
    numeros_sorteados = set()
    numeros_posibles = list(range(1, 91))
    ganador = None

    while ganador is None:
        numero = random.choice(numeros_posibles)
        numeros_posibles.remove(numero)  # Eliminamos el número para no repetirlo
        numeros_sorteados.add(numero)
        
        # Revisar si algún cartón ha ganado
        for i, numeros_carton in enumerate(numeros_cartones):
            if numeros_carton.issubset(numeros_sorteados):
                ganador = i + 1  # Sumamos 1 para indicar el número del cartón
                break

    return ganador, numeros_sorteados

# Mostrar los cartones generados en formato de tabla
def mostrar_carton(carton):
    for fila in carton:
        print(" | ".join(str(n).rjust(2) if n is not None else '  ' for n in fila))
    print("\n")

# Generar y mostrar 100 cartones distintos
cartones_distintos, numeros_cartones_distintos = generar_varios_cartones(300)
for i, carton in enumerate(cartones_distintos, 1):
    print(f"Cartón {i}:")
    mostrar_carton(carton)

# Realizar el sorteo y encontrar el cartón ganador
ganador, numeros_sorteados = sorteo(numeros_cartones_distintos)

print(f"El cartón ganador es el número {ganador}!")
print(f"Números sorteados: {sorted(numeros_sorteados)}")
print("\nCartón ganador:")
mostrar_carton(cartones_distintos[ganador - 1])

print(len(numeros_sorteados))
