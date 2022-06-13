from browser import document, alert
from visualife.core.HtmlViewport import HtmlViewport
import random


# lista vs krotka?
def stworz_liste_sasiadow(rozmiar_statku, orientacja, wspX, wspY):
    sasiedzi = []
    # poziomy statek
    if orientacja == 0:
        sasiedzi.append([wspX - 1, wspY])
        sasiedzi.append([wspX + rozmiar_statku, wspY])
        for i in range(-1, rozmiar_statku + 1):
            sasiedzi.append([wspX - 1, wspY - 1])
            sasiedzi.append([wspX - 1, wspY + 1])
            wspX += 1
    # pionowy statek
    if orientacja == 1:
        sasiedzi.append([wspX, wspY - 1])
        sasiedzi.append([wspX, wspY + rozmiar_statku])
        for i in range(-1, rozmiar_statku + 1):
            sasiedzi.append([wspX - 1, wspY - 1])
            sasiedzi.append([wspX + 1, wspY - 1])
            wspY += 1
    return sasiedzi


def losuj_statek(rozmiar_statku, plansza, lista_sasiadow):
    statek_pasuje = 0
    # przeprowadzam losowanie tak długo aż wylosuje sensowne wspolrzedne
    while statek_pasuje != rozmiar_statku:
        wspolrzednaX = random.randint(0, len(plansza) - 1)
        wspolrzednaY = random.randint(0, len(plansza) - 1)
        orientacja = random.randint(0, 1)
        pom_wspX = wspolrzednaX
        pom_wspY = wspolrzednaY
        for i in range(0, rozmiar_statku):
            # sprawdzam, czy statek nie wejdzie w inne statki/granice/pola sasiadow - jak tak to losuje jeszcze raz
            if wspolrzednaX < len(plansza) and wspolrzednaY < len(plansza) \
                    and plansza[wspolrzednaX][wspolrzednaY] == 0 and [wspolrzednaX, wspolrzednaY] not in lista_sasiadow:
                statek_pasuje += 1
            else:
                statek_pasuje = 0
                break
            if orientacja == 0:
                wspolrzednaX += 1
            elif orientacja == 1:
                wspolrzednaY += 1
    return [pom_wspX, pom_wspY, orientacja]


# wstawianie konkretnego statku na plansze jezeli jest to mozliwe
def wstaw_statek(rozmiar_statku, plansza, lista_sasiadow):
    parametry_statku = losuj_statek(rozmiar_statku, plansza, lista_sasiadow)
    orientacja = parametry_statku[2]
    wspX = parametry_statku[0]
    wspY = parametry_statku[1]

    # uzupelniam liste sasiadow o nowych i wstawiam statek w wylosowane miejsce
    lista_sasiadow.extend(stworz_liste_sasiadow(rozmiar_statku, orientacja, wspX, wspY))

    # wstawiam tylko statki w prawo i w dół (plusując wspX i wspY, nie minusuję)
    for r in range(0, rozmiar_statku):
        plansza[wspX][wspY] = 1
        if orientacja == 0:
            wspX += 1
        else:
            wspY += 1
    return plansza


# wizualizacja planszy przy uzyciu visualife
def rysowanie(drawing, nazwa, x0, y0):
    for i in range(10):
        for j in range(10):
            key = nazwa + ":%d%d" % (j, i)
            drawing.square(nazwa+":"+str(i) + str(j), i * 20 + 15 + x0, j * 20 + 15 + y0, 18, fill="azure", stroke="black")
            if nazwa == "komputer":
                drawing.define_binding(key, "click", trafiony)
    drawing.close()
    drawing.apply_binding()


def kolorowanie(nazwa, plansza):
    for k in range(0, 10):
        for j in range(0, 10):
            if plansza[k][j] == 1:
                key = nazwa+":%d%d" % (j, k)
                document[key].style.fill = "pink"


def trafiony(event):
    key = event.target.id
    xy = key.split(":")
    x = int(xy[1][0])
    y = int(xy[1][1])
    if key not in lista_klikniec_gracza:
        if plansza_komputer[y][x] == 1:
            document[key].style.fill = "crimson"
            plansza_komputer[y][x] = 2
            if czy_koniec(plansza_komputer):
                alert("Koniec gry, wygrales")
        elif plansza_komputer[y][x] == 0:
            document[key].style.fill = "lightsteelblue"
            ruch_komputera(plansza_gracz, lista_strzalow_komputera)
            if czy_koniec(plansza_gracz):
                alert("Koniec gry, wygral komputer")
    lista_klikniec_gracza.append(key)


def czy_koniec(plansza):
    licznik_dwojek = 0
    suma_pol_statkow = sum(dostepne_statki)
    for i in range(0, len(plansza)):
        for j in range(0, len(plansza)):
            if plansza[i][j] == 2:
                licznik_dwojek += 1
    if licznik_dwojek == suma_pol_statkow:
        return True
    return False


# funkcja zwracająca wypelnione startowe plansze gracza i komputera
def generator_planszy(drawing, nazwa):
    plansza = []
    n_planszy = 10
    for i in range(0, n_planszy):
        plansza.append([])
        for j in range(0, n_planszy):
            plansza[i].append(0)

    lista_sasiadow = []
    # wstawianie jedynek w miejsce, gdzie mają być statki (losowo)
    for k in range(0, len(dostepne_statki)):
        wstaw_statek(dostepne_statki[k], plansza, lista_sasiadow)

    if nazwa == "komputer":
        rysowanie(drawing, "komputer", 250, 0)
    elif nazwa == "gracz":
        rysowanie(drawing, "gracz", 0, 0)

    print(nazwa, *plansza, sep='\n')
    return plansza


# symulacja ruchu komputera - po trafieniu od razu losowo przeszukuje okolice w tym samym ruchu
def ruch_komputera(plansza, lista_strzalow):
    wspolrzednaX = random.randint(0, len(plansza) - 1)
    wspolrzednaY = random.randint(0, len(plansza) - 1)
    while [wspolrzednaX, wspolrzednaY] in lista_strzalow:
        wspolrzednaX = random.randint(0, len(plansza) - 1)
        wspolrzednaY = random.randint(0, len(plansza) - 1)

    lista_strzalow.append([wspolrzednaX, wspolrzednaY])
    if plansza[wspolrzednaX][wspolrzednaY] == 0:
        key = "gracz" + ":%d%d" % (wspolrzednaY, wspolrzednaX)
        document[key].style.fill = "lightsteelblue"
        # print(wspolrzednaX, wspolrzednaY)

    while plansza[wspolrzednaX][wspolrzednaY] == 1:
        key = "gracz" + ":%d%d" % (wspolrzednaY, wspolrzednaX)
        document[key].style.fill = "crimson"
        plansza[wspolrzednaX][wspolrzednaY] = 2
        # print(wspolrzednaX, wspolrzednaY)
        strona = random.randint(0, 3)  # 0 lewo, 1 prawo, 2 gora, 3 dol

        if strona == 0 and [wspolrzednaX - 1, wspolrzednaY] not in lista_strzalow and wspolrzednaX > 0:
            wspolrzednaX -= 1
        elif strona == 1 and [wspolrzednaX + 1, wspolrzednaY] not in lista_strzalow and wspolrzednaX < len(plansza) - 1:
            wspolrzednaX += 1
        elif strona == 2 and [wspolrzednaX, wspolrzednaY - 1] not in lista_strzalow and wspolrzednaY > 0:
            wspolrzednaY -= 1
        elif strona == 3 and [wspolrzednaX, wspolrzednaY + 1] not in lista_strzalow and wspolrzednaY < len(plansza) - 1:
            wspolrzednaY += 1
        else:
            wspolrzednaX = random.randint(0, len(plansza) - 1)
            wspolrzednaY = random.randint(0, len(plansza) - 1)

        key = "gracz" + ":%d%d" % (wspolrzednaY, wspolrzednaX)
        lista_strzalow.append([wspolrzednaX, wspolrzednaY])
        if plansza[wspolrzednaX][wspolrzednaY] == 0:
            document[key].style.fill = "lightsteelblue"
        else:
            document[key].style.fill = "crimson"


# wywołanie losowania planszy gracza i komputera
drawing = HtmlViewport(document['svg'], 900, 700)
dostepne_statki = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
plansza_komputer = generator_planszy(drawing, "komputer")
plansza_gracz = generator_planszy(drawing, "gracz")
lista_strzalow_komputera = []
lista_klikniec_gracza = []
kolorowanie("gracz", plansza_gracz)
