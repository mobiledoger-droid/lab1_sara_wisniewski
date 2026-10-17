def przykladowy_decorator(func):
    def wrapper(*args, **kwargs):
        print("Przed")
        wynik = func(*args, **kwargs)
        print("Po")
        return wynik

    return wrapper


def suma(a, b):
    print(f">>> Suma a+b = {a + b}")


x = przykladowy_decorator(suma)
x(1, 2)
