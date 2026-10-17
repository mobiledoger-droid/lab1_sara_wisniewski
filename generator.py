"""Prosty proces ETL na pliku CSV: extract -> transform -> load."""

import csv
import os
import time

DANE_DIR = "dane"

# Jedyne zrodlo prawdy o tym, co oznacza brak wartosci w pliku wejsciowym.
BRAK_OZNACZENIA = ("-", "")


class EtlCsv:
    """Symuluje proces ETL na pliku CSV z liczbami i brakami oznaczonymi myslnikiem."""

    def __init__(self, sciezka_wejscia: str, separator: str = ",", pomin_naglowek: bool = False) -> None:
        self.sciezka_wejscia = sciezka_wejscia
        self.separator = separator
        self.pomin_naglowek = pomin_naglowek

    def extract(self):
        """Generator: wczytuje plik linijka po linijce, zwraca liste pol kazdego wiersza."""
        with open(self.sciezka_wejscia, "r", encoding="utf-8", newline="") as plik:
            reader = csv.reader(plik, delimiter=self.separator)
            if self.pomin_naglowek:
                next(reader, None)
            for wiersz in reader:
                yield wiersz

    def transform(self):
        """Generator: dla kazdego wiersza liczy sume, srednia i indeksy brakow."""
        for wiersz in self.extract():
            if not wiersz:
                continue
            numer = wiersz[0].strip()
            braki = [i for i, pole in enumerate(wiersz[1:], start=1)
                     if pole.strip() in BRAK_OZNACZENIA]
            wartosci = [float(pole) for pole in wiersz[1:]
                        if pole.strip() not in BRAK_OZNACZENIA]
            suma = sum(wartosci)
            srednia = suma / len(wartosci) if wartosci else ""
            yield numer, suma, srednia, braki

    def zmierz_czas(func):
        """Dekorator wypisujacy czas przed i po wywolaniu funkcji."""

        def wrapper(*args, **kwargs):
            print(f"[CZAS] Przed: {time.strftime('%H:%M:%S')}")
            wynik = func(*args, **kwargs)
            print(f"[CZAS] Po:    {time.strftime('%H:%M:%S')}")
            return wynik

        return wrapper

    @zmierz_czas

    def load(self, nazwa_values: str = "values.csv",
             nazwa_missing: str = "missing_values.csv") -> None:
        """Zapisuje dwa pliki CSV, konsumujac generator transform() dokladnie raz."""
        os.makedirs(DANE_DIR, exist_ok=True)
        sciezka_values = os.path.join(DANE_DIR, nazwa_values)
        sciezka_missing = os.path.join(DANE_DIR, nazwa_missing)
        with open(sciezka_values, "w", encoding="utf-8", newline="") as plik_values, \
             open(sciezka_missing, "w", encoding="utf-8", newline="") as plik_missing:
            writer_values = csv.writer(plik_values)
            writer_missing = csv.writer(plik_missing)
            writer_values.writerow(["numer porzadkowy", "suma", "srednia"])
            writer_missing.writerow(["numer porzadkowy", "indeksy_brakow"])
            for numer, suma, srednia, braki in self.transform():
                writer_values.writerow([numer, suma, srednia])
                writer_missing.writerow([numer, *braki])
        print(f"Zapisano: {sciezka_values}")
        print(f"Zapisano: {sciezka_missing}")



if __name__ == "__main__":
    etl = EtlCsv(os.path.join(DANE_DIR, "plik.csv"))
    etl.load()