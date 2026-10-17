import requests

def download_file(url: str, filename: str = "latest.txt") -> None:
    """Pobiera plik spod adresu url i zapisuje go na dysku jako filename."""
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, "wb") as file:
        file.write(response.content)