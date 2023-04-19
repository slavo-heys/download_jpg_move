import requests
from bs4 import BeautifulSoup
import os

# przeszukiwanie strony pod kątem linków do listy
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

    # sprawdzanie czy na poszczegolnych stronach są zdjęcia
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

    # sprawdzanie czy na poszczegolnych stronach są filmy
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


# użytkownik podaje adres URL do przeszukania
url = input("Podaj adres URL (https://xxx.xx): ")

# użytkownik podaje co chce ściągnąć (zdjęcia, pliki)
co = input("Co chcesz ściągnąć?\n\n1. zdjęcia,  \n2. filmy: ")


# uruchom program
if co == "1":    
    get_images(get_links(url))
elif co == "2":
    get_films(get_links(url))
else:
    pass

