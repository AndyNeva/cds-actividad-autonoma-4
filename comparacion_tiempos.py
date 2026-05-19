"""
comparacion_tiempos.py
Compara el rendimiento entre el código original y el optimizado:
- Mide tiempos con time.
- Genera reporte de profiling con cProfile.
- Produce gráficas comparativas con Matplotlib.
"""

# Librerías

import cProfile
import io
import os
import pstats
import time
import matplotlib.pyplot as plt


# Constantes globales
LIMITE = 100_000
CARPETA_GRAFICAS = "graficas"


# Funciones de búsqueda de primos
from codigo_original import encontrar_primos
from codigo_optimizado import encontrar_primos_comprehension, encontrar_primos_numpy



# Medición de tiempos

def medir_tiempos(limite: int) -> dict:
    """Ejecuta los tres métodos y devuelve sus tiempos.

    Args:
        limite: Límite superior del rango a evaluar.

    Returns:
        Diccionario con los tiempos de cada método.
    """
    tiempos = {}

    print(f"Midiendo tiempos para rango 1 al {limite}\n")

    # Original
    print("Búsqueda original")
    inicio = time.time()
    encontrar_primos(limite)
    fin = time.time()
    tiempos["original"] = fin - inicio
    print(f"Tiempo: {tiempos['original']:.4f} segundos\n")

    # List comprehension
    print("List comprehension")
    inicio = time.time()
    encontrar_primos_comprehension(limite)
    fin = time.time()
    tiempos["comprehension"] = fin - inicio
    print(f"Tiempo: {tiempos['comprehension']:.4f} segundos \n")

    # NumPy
    print("NumPy (Criba de Eratóstenes)")
    inicio = time.time()
    encontrar_primos_numpy(limite)
    fin = time.time()
    tiempos["numpy"] = fin - inicio
    print(f"Tiempo: {tiempos['numpy']:.4f} segundos \n")

    return tiempos


# cProfile

def generar_profiling(limite: int) -> None:
    """Ejecuta cProfile sobre el código optimizado y guarda el reporte.

    Args:
        limite: Límite superior del rango a evaluar.
    """
    print("Generando reporte de cProfile")

    # Captura la salida de cProfile en un string
    perfil = cProfile.Profile()
    perfil.enable()
    encontrar_primos_comprehension(limite)
    encontrar_primos_numpy(limite)
    perfil.disable()

    buffer = io.StringIO()
    estadisticas = pstats.Stats(perfil, stream=buffer)
    estadisticas.sort_stats("cumulative")
    estadisticas.print_stats()

    archivo_salida = "profiling_optimizado"
    with open(archivo_salida, "w", encoding="utf-8") as archivo:
        archivo.write(buffer.getvalue())

    print(f"Reporte guardado en: {archivo_salida}")


# Gráficas

def crear_graficas(tiempos: dict) -> None:
    """Genera y guarda las dos gráficas comparativas.

    Args:
        tiempos: Diccionario con los tiempos medidos.
    """
    
    etiquetas = ["Original", "List Comprehension", "NumPy"]
    valores = [tiempos["original"], tiempos["comprehension"], tiempos["numpy"]]
    colores = ["#e74c3c", "#f39c12", "#2ecc71"]

    # Gráfica 1: Barras comparativas
    fig, ax = plt.subplots(figsize=(9, 5))

    barras = ax.bar(etiquetas, valores, color=colores, width=0.5, edgecolor="white")

    # Etiqueta encima de cada barra
    for barra, valor in zip(barras, valores):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height() * 1.05,
            f"{valor:.4f}s",
            ha="center", va="bottom",
            fontsize=10, fontweight="bold",
        )

    ax.set_yscale("log")  # escala logarítmica para ver todas las barras
    ax.set_title("Comparativa de tiempos de ejecución", fontsize=13, fontweight="bold", pad=15)
    ax.set_ylabel("Tiempo (segundos) - escala log", fontsize=11)
    ax.set_xlabel("Método", fontsize=11)
    ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    ruta_barras = os.path.join("graficas", "comparativa_tiempos.png")
    plt.savefig(ruta_barras, dpi=150)
    plt.close()
    print(f"Gráfica guardada: {ruta_barras}")

    # Gráfica 2: Distribución de tiempos (pastel)
    fig, ax = plt.subplots(figsize=(7,7))
    wedges, texts, autotexts = ax.pie(
        valores,
        colors=colores,
        autopct="%1.1f%%",
        startangle=140,
        wedgeprops={"edgecolor": "white", "linewidth": 2},
        pctdistance=0.6,
        labeldistance=1.3,
    )

    for text in texts:
        text.set_visible(False)  # sin etiquetas directas

    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_fontweight("bold")

    ax.set_title("Distribución del tiempo de ejecución por método", fontsize=13, fontweight="bold")
    ax.legend(wedges, etiquetas, loc="lower right", fontsize=10)
    plt.tight_layout()
    ruta_pastel = os.path.join("graficas", "distribucion_tiempos.png")
    plt.savefig(ruta_pastel, dpi=150)
    plt.close()
    print(f"Gráfica guardada: {ruta_pastel}")

# Ejecución principal
def main ():
    print("Comparación de tiempos y profiling \n")

    # 1. Medir tiempos
    tiempos = medir_tiempos(LIMITE)

    # 2. Generar profiling
    generar_profiling(LIMITE)

    # 3. Crear gráficas
    crear_graficas(tiempos)

    # 4. Resumen final
   # 4. Resumen final
    print("\n")
    print("Resumen \n")
    print(f"Original: {tiempos['original']:.4f}s")
    print(f"Comprehension: {tiempos['comprehension']:.4f}s")
    print(f"NumPy: {tiempos['numpy']:.4f}s")
    print("\nArchivos generados:")
    print("- profiling_optimizado.txt")
    print("- graficas/comparativa_tiempos.png")
    print("- graficas/distribucion_tiempos.png")

if __name__ == "__main__":
    main()