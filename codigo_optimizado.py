"""
codigo_optimizado.py
Búsqueda de números primos en un rango usando técnicas de optimización:
- Raíz cuadrada para reducir iteraciones en la verificación.
- List comprehensions para construir listas de forma eficiente.
- Numpy (Criba de Eratóstenes) para operaciones vectorizadas.
"""

# Librerías 

import time
import numpy as np
from math import isqrt


# Constantes globales

LIMITE = 100_000


# Funciones

def num_primo_optimizado(n: int) -> bool:
    """Verifica si un número es primo iterando solo hasta su raíz cuadrada.

    Args:
        n: Número entero a evaluar.

    Returns:
        True si n es primo, False en caso contrario.
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Itera solo hasta √n en lugar de hasta n
    limite_raiz = isqrt(n)
    return all(n % i != 0 for i in range(3, limite_raiz+1, 2))


def encontrar_primos_comprehension(limite: int) -> list[int]:
    """Encuentra primos usando list comprehension y raíz cuadrada.

    Args:
        limite: Límite superior del rango (inclusivo).

    Returns:
        Lista de números primos entre 2 y limite.
    """
    return [n for n in range(2, limite + 1) if num_primo_optimizado(n)]


def encontrar_primos_numpy(limite: int) -> np.ndarray:
    """Encuentra primos mediante el Criba de Eratóstenes con Numpy.

    Crea un array booleano donde cada posición representa un número. Todos inician 
    en True (primo) y se marcan False si son múltiplos de algún primo anterior. Numpy 
    aplica esto en una sola operación sin bucles Python, lo que lo hace 
    significativamente más rápido.

    Args:
        limite: Límite superior del rango (inclusivo).

    Returns:
        Array Numpy con los números primos encontrados.
    """
    # Crea array booleano donde True = posiblemente primo
    num_primo = np.ones(limite + 1, dtype=bool)
    num_primo[0] = False
    num_primo[1] = False

    # Marca múltiplos como no primos (Criba de Eratóstenes)
    for i in range(2, isqrt(limite) + 1):
        if num_primo[i]:
            num_primo[i * i :: i] = False  

    return np.where(num_primo)[0]

# Ejecución principal
def main():
    print(f"Buscando números primos del 1 al {LIMITE}. \n")

    # Método 1: list comprehension + raíz cuadrada
    inicio = time.time()
    primos_comprehension = encontrar_primos_comprehension(LIMITE)
    fin = time.time()
    tiempo_comprehension = fin - inicio

    print(f"Mediante list comprehension")
    print(f"Primos encontrados: {len(primos_comprehension)}")
    print(f"Tiempo: {tiempo_comprehension:.4f} segundos\n")

    # Método 2: operaciones vectorizadas de Numpy
    inicio = time.time()
    primos_numpy = encontrar_primos_numpy(LIMITE)
    fin = time.time()
    tiempo_numpy = fin - inicio

    print(f"Mediante operaciones vectorizadas de Numpy (Criba de Eratóstenes)")
    print(f"Primos encontrados: {len(primos_numpy)}")
    print(f"Tiempo: {tiempo_numpy:.4f} segundos")



if __name__ == "__main__":
    main()