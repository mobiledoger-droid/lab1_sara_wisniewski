import os
import requests

class DownloadError(Exception):
    """Baza dla wszystkich błędów pobierania plików."""

class NotFoundError(DownloadError):
    """Serwer zwrócił kod 404."""

class AccessDeniedError(DownloadError):
    """Serwer zwrócił kod 403."""

DANE_DIR = "dane"

def download_file(url: str, filename: str = "latest.txt") -> None:
    """Pobiera plik spod adresu url i zapisuje go w folderze dane jako filename."""
    os.makedirs(DANE_DIR, exist_ok=True)
    sciezka = os.path.join(DANE_DIR, filename)
    response = requests.get(url)
    if response.status_code == 404:
        raise NotFoundError(f"Nie znaleziono zasobu: {url}")
    if response.status_code == 403:
        raise AccessDeniedError(f"Odmowa dostępu: {url}")
    response.raise_for_status()
    with open(sciezka, "wb") as file:
        file.write(response.content)
    print(f"Zapisano: {sciezka}")

if __name__ == "__main__":
    # Test 1: poprawne pobieranie
    download_file("https://oleksandr-fedoruk.com/sggw/podyplomowe/file", "plik.csv")

    # Test 2: łapanie konkretnego typu
    try:
        download_file("http://oleksandr-fedoruk.com/sggw/podyplomowe/404", "brak.csv")
    except NotFoundError as e:
        print(f"Złapano NotFoundError: {e}")

    # Test 3: łapanie całej rodziny jednym exceptem
    try:
        download_file("http://oleksandr-fedoruk.com/sggw/podyplomowe/403", "odmowa.csv")
    except DownloadError as e:
        print(f"Złapano DownloadError: {e}")
