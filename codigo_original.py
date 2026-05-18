import time


def num_primo(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def encontrar_primos(limite):
    primos = []
    for numero in range(1, limite + 1):
        if num_primo(numero):
            primos.append(numero)
    return primos

def main():
    limite = 100000
    print(f"Buscando números primos del 1 al {limite}")
    inicio = time.time()
    primos = encontrar_primos(limite)
    fin = time.time()
    tiempo_total = fin-inicio
    print(f"Se encontraron {len(primos)} números primos.")
    print(f"Tiempo de ejecución: {tiempo_total:.4f} segundos")


if __name__ == "__main__":
    main()