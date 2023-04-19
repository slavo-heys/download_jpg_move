import requests
from bs4 import BeautifulSoup
from PIL import Image
import os

# utwórz pająka który będzie przeszukiwał stronę i podstrony i zapisywał wszystkie linki do listy, na końcu wyświetli listę linków
def get_links(url):
    links = []
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    for link in soup.find_all("a"):
        links.append(link.get("href"))
    # czy chcesz zapisać listę linków do pliku txt?
    odp = input("Czy chcesz zapisać listę linków do pliku txt? (t/n): ")
    if odp == "t":
        with open("links_txt.txt", "w") as f:
            for link in links:
                f.write(link + "\n")
        print("Lista linków została zapisana do pliku txt")
    else:
        pass
    return links

def get_images(links):
    # utwórz folder ZDJECIA
    try:
        os.mkdir("ZDJECIA")
    except:
        pass

    # sprawdz czy na poszczegolnych stronach są zdjęcia
    for link in links:
        try:
            r = requests.get(link)
            soup = BeautifulSoup(r.text, "html.parser")
            for img in soup.find_all("img"):
                # pobierz linki do zdjęć
                img_link = img.get("src")
                # pobierz zdjęcia
                r = requests.get(img_link)
                # zapisz zdjęcia do folderu ZDJECIA
                with open("ZDJECIA/" + img_link.split("/")[-1], "wb") as f:
                    f.write(r.content)
        except:
            print("Nie udało się pobrać zdjęcia" + link)

def get_films(links):
    # utwórz folder FILMY
    try:
        os.mkdir("FILMY")
    except:
        pass

    # sprawdz czy na poszczegolnych stronach są filmy
    for link in links:
        try:
            r = requests.get(link)
            soup = BeautifulSoup(r.text, "html.parser")
            for img in soup.find_all("video"):
                # pobierz linki do zdjęć
                img_link = img.get("src")
                # pobierz zdjęcia
                r = requests.get(img_link)
                # zapisz zdjęcia do folderu ZDJECIA
                with open("FILMY/" + img_link.split("/")[-1], "wb") as f:
                    f.write(r.content)
        except:
            print("Nie udało się pobrać filmu" + link)

# funkcja rekurencyjnie usuwająca pliki z folderu i jego podfolderów
def remove_small_images(path, min_width, min_height):
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.png', '.gif', '.webp')):
                filepath = os.path.join(dirpath, filename)
                try:
                    with Image.open(filepath) as img:
                        width, height = img.size
                        if width < min_width or height < min_height:
                            os.remove(filepath)
                            print(f"Usunięto plik: {filepath}")
                except:
                    print(f"Nie można otworzyć pliku: {filepath}")


# użytkownik podaje adres URL do przeszukania
url = input("Podaj adres URL (https://xxx.xx): ")

# użytkownik podaje co chce ściągnąć (zdjęcia, pliki)
co = input("Co chcesz ściągnąć?\n\n1. zdjęcia,  \n2. filmy: ")

if co == "1":
    # uruchom program
    get_images(get_links(url))
    # ożytkownik decyduje czy chce usunąć małe zdjęcia
    odp = input("Czy chcesz usunąć małe zdjęcia? (t/n): ")
    if odp == "t":
        # użytkownik podaje minimalny rozmiar zdjęcia
        min_width = int(input("Podaj minimalną szerokość zdjęcia: "))
        min_height = int(input("Podaj minimalną wysokość zdjęcia: "))
        # usuń małe zdjęcia
        remove_small_images("ZDJECIA", min_width, min_height)
    else:
        pass
elif co == "2":
    get_films(get_links(url))
else:
    pass

