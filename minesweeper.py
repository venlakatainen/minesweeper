import random
import haravasto
import time

arvot = {
    "leveys" : 0,
    "korkeus" : 0,
    "Siirrot" :0,
    "miinat" : 0,
    "aika": 0,
    "lopputulos": 0
}

kentat = {
    "mallikentta": [],
    "piirtokentta": []
}


def tee_kentta():
    """
    Kysyy käyttäjältä kentän leveyden ja korkeuden. 
    Tekee niiden perusteella kentän lisäämällä korkeuden verran rivejä ja leveyden verran sarakkeita.
    Kysyy käyttäjältä miinojen lukumäärän ja miinoittaa kentän miinoita-funktiolla. 
    """
    kentat["mallikentta"] = []
    while True:
        try:
            arvot["leveys"] = int(input("Syötä kentän leveys: "))
            if 2 <= arvot["leveys"] <= 30:
                break
            else:
                print("Anna sopiva kokonaisluku.")
        except ValueError:
            print("Vääränlainen syöte.")
   
    while True:
        try:    
            arvot["korkeus"] = int(input("Syötä kentän korkeus: "))
            if 2 <= arvot["korkeus"] <= 18:
                break
            else:
                print("Anna sopiva kokonaisluku")
        except ValueError:
            print("Vääränlainen syöte.")
 
    for rivi in range(arvot["korkeus"]):
        kentat["mallikentta"].append([])
        for sarake in range(arvot["leveys"]):
            kentat["mallikentta"][rivi].append(" ")
    

    while True:
            try:
                arvot["miinat"] = int(input("Syötä miinojen lukumäärä: "))
                if (arvot["miinat"] < (len(kentat["mallikentta"]) * len(kentat["mallikentta"][0]))) and (arvot["miinat"] > 0):
                    miinoita(kentat["mallikentta"], arvot["miinat"])
                    break
                else:
                    print("Väärä määrä miinoja.")
                    continue
            except ValueError:
                print("Vääränlainen syöte.")


def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    for y, i in enumerate(kentat["piirtokentta"]):
        for x, ruutu in enumerate(i):
            haravasto.lisaa_piirrettava_ruutu(ruutu, 40*x, 40*y)
    haravasto.piirra_ruudut()


def kentan_grafiikka():
    """
    Lataa pelin grafiikat, luo peli-ikkunan ja asettaa siihen piirtokäsittelijän,
    hiirikäsittelijän ja toistuvan käsittelijän.
    """
    korkeus = (len(kentat["piirtokentta"])) * 40
    leveys = (len(kentat["piirtokentta"][0])) * 40
    haravasto.lataa_kuvat("spritet")
    haravasto.luo_ikkuna(leveys, korkeus)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aseta_hiiri_kasittelija(hiiri_kasittelija)
    haravasto.aseta_toistuva_kasittelija(paivitys_kasittelija, 1/60)
    haravasto.aloita()


def miinoita(miinakentta, miinojen_lkm):
    """
    Asettaa kentälle käyttäjän syöttämän määrän miinoja satunnaisiin paikkoihin.
    """
    vapaat_ruudut = []
    for j in range(len(miinakentta)):
        for i in range(len(miinakentta[0])):
            vapaat_ruudut.append((i, j))

    for n in range(miinojen_lkm):
        koordinaatit = random.choice(vapaat_ruudut)
        y = koordinaatit[1]
        x = koordinaatit[0]
        miinakentta[y][x] = "x"
        vapaat_ruudut.remove(koordinaatit)


def tulvataytto(tulvakentta, x, y):
    """
    Merkitsee kentällä olevat tyhjät ruudut siten, että
    tulvatäyttö aloitetaan tyhjästä ruudusta, jota klikataan hiiren vasemmalla.
    """

    ruudut = [(x, y)]
    korkeus = len(tulvakentta) - 1
    leveys = len(tulvakentta[0]) - 1

    while ruudut:
        koord = ruudut.pop()
        x_rajat = range(koord[0] - 1, koord[0] + 2)
        y_rajat = range(koord[1] - 1, koord[1] + 2)
        for r in y_rajat:
            for s in x_rajat:
                if ((0 <= r <= korkeus) and (0 <= s <= leveys) and kentat["mallikentta"][r][s] != "x" and kentat["piirtokentta"][r][s] == " "):
                    kentat["piirtokentta"][r][s] = kentat["mallikentta"][r][s]
                    if kentat["piirtokentta"][r][s] == "0":
                        ruudut.append((s, r))

def avaamattomat():
    """
    Käy käyttäjälle näkyvän piirtokentan läpi ja 
    laskee avaamattomien ja liputettujen ruutujen määrän.
    """
    avaamattomat_ruudut = 0
    for n in range(len(kentat["piirtokentta"])):
        for m in range(len(kentat["piirtokentta"][0])):
            if (kentat["piirtokentta"][n][m] == " " or kentat["piirtokentta"][n][m] == "f"):
                avaamattomat_ruudut += 1
    return avaamattomat_ruudut

def voitto():
    """
    Vertaa miinojen lukumäärää ja avaamattomat-funktion
    palauttamaa lukumäärää avaamattomista ja liputetuista ruuduista. Jos lukumäärä on sama, peli on voitettu,
    koska silloin kaikissa avaamattomissa/liputetuissa ruuduissa on miina. Päivittää tilastoja.
    """
    if avaamattomat() == arvot["miinat"]:
        arvot["lopputulos"] = "VOITTO"
        tilastot()
        print("VOITIT PELIN!!")
        haravasto.lopeta()
        arvot["aika"] = 0
        arvot["Siirrot"] = 0
    


def paivitys_kasittelija(kulunut_aika):
    """
    Tarkistaa voiton kulunut_aika välein ja laskee peliin kulunutta aikaa.
    """
    voitto()
    arvot["aika"] += kulunut_aika


def havio():
    """
    Jos miinoitettu ruutu avataan, kutsutaan havio-funktiota,
    joka lopettaa pelin, merkitsee lopputulokseksi häviön,
    kutsuu tilastot-funktiota ja ilmoittaa käyttäjälle häviöstä.
    """

    arvot["lopputulos"] = "HÄVIÖ"
    tilastot()
    print("HÄVISIT PELIN!!")
    haravasto.lopeta()
    arvot["aika"] = 0
    arvot["Siirrot"] = 0


            

def hiiri_kasittelija(x, y, nappi, muokkausnapit):
    """
    Käsittelee hiiren klikkauksia. Jos klikataan vasemmalla tarkistetaan ettei
    käyttäjä ole merkannut ruutua lipuksi, jos on ruutua ei avata. Jos ei, tarkistetaan
    onko ruudussa miina, jos on peli hävitään. Jos avattu ruutu on tyhjä, aloitetaan
    tulvatäyttö. Jos ruudussa ei ole lippua tai miinaa eikä se ole tyhjä, ruudussa on numero
    ja numero merkitään käyttäjälle näkyvään piirtokenttaan.

    Jos klikataan hiiren oikealla, merkitään ruutu lipuksi jos se ei ole lippu,
    jos ruutu on lippu, poistetaan lippu.

    Ohitetaan hiiren keskinäppäimellä tehdyt klikkaukset.

    Kaikista klikkauksista, lukuunottamatta keskinäppäimellä, tehdyista klikkauksista
    päivitetään sanakirjan siirrot arvoa, joka laskee montako siirtoa eli klikkausta peliin
    kului.
    """
    x = int(x/40)
    y = int(y/40)
    if nappi == haravasto.HIIRI_VASEN and kentat["piirtokentta"][y][x] != "f":
        arvot["Siirrot"] += 1
        if kentat["mallikentta"][y][x] == "x":
            kentat["piirtokentta"][y][x] = "x"
            havio()
        elif kentat["mallikentta"][y][x] == "0":
            tulvataytto(kentat["piirtokentta"], x, y)
        else: 
            kentat["piirtokentta"][y][x] = "{}".format(kentat["mallikentta"][y][x])
    elif nappi == haravasto.HIIRI_OIKEA:
        arvot["Siirrot"] += 1
        if kentat["piirtokentta"][y][x] == "f":
            kentat["piirtokentta"][y][x] = " "
        else:
            kentat["piirtokentta"][y][x] = "f"
    elif nappi == haravasto.HIIRI_KESKI:
        pass


def laske_miinat(x, y, lista):

    """
    Laskee klikatun ruudun ympärillä olevat miinat ja palauttaa
    niiden lukumäärän. 
    """

    lukumaara = 0
    x_rajat = range(x - 1, x + 2)
    y_rajat = range(y - 1, y + 2)
    for rivin_numero in y_rajat:
        for sarakkeen_numero in x_rajat:
            if (rivin_numero >= 0 and rivin_numero <= (len(lista) - 1)) and (sarakkeen_numero >= 0 and sarakkeen_numero <= (len(lista[0]) - 1)):
                if kentat["mallikentta"][rivin_numero][sarakkeen_numero] == "x":
                    lukumaara += 1
    return lukumaara

def numeroi_kentan():
    """
    Käy kentän läpi ja miinoitettujen ruutujen kohdalla kutsuu 
    laske_miinat-funktiota ja merkitsee miinoitetun ruudun ympärille numerot
    kuinka monen miinan kanssa ruutu on kosketuksissa. 
    """
    for y, rivi in enumerate(kentat["mallikentta"]):
        for x, ruutu in enumerate(kentat["mallikentta"][y]):
            if ruutu != "x":
                kentat["mallikentta"][y][x] = str(laske_miinat(x, y, kentat["mallikentta"]))
                 

def tee_avaamaton_kentta():
    """
    Tekee käyttäjälle näkyvän kentän käyttäjän syöttämien
    leveyden ja korkeuden mukaan.
    """
    kentat["piirtokentta"] = []
    for rivi in range(arvot["korkeus"]):
        kentat["piirtokentta"].append([])
        for sarake in range(arvot["leveys"]):
            kentat["piirtokentta"][rivi].append(" ")

def tilastot():
    """
    Kirjoittaa ja tallentaa tilastot-tiedostoon pelin ajankohdan,
    pelin keston, siirtojen lukumäärän, päättyikö peli voittoon vai häviöön sekä
    kentän koon ja miinojen lukumäärän.
    """
    try:
        with open("tilastot.txt", "a+") as tilasto:
            tilasto.write("Pelin ajankohta: {pvm}\nPelin kesto: {aika} min\nSiirtojen määrä: {siirrot}\nLopputulos: {tulos}\nKentän koko: {leveys}x{korkeus}\nMiinojen lukumäärä: {miinat}\n\n".format(
                pvm=(time.strftime("%a %d.%m.%Y %H:%M", time.localtime())),
                aika=round((arvot["aika"] / 60), 2),
                siirrot=arvot["Siirrot"],
                tulos=arvot["lopputulos"],
                leveys=arvot["leveys"],
                korkeus=arvot["korkeus"],
                miinat=arvot["miinat"]
            ))
    except IOError:
        print("Kohdetiedostoa ei voitu avata. Tallennus epäonnistui.")

def avaa_tilastot():
    """
    avaa tilastot-tiedoston ja näyttää sisällön käyttäjälle.
    """
    try:
        with open("tilastot.txt", "r") as tilastot:
            sisalto = tilastot.read()
            print(sisalto)
    except FileNotFoundError:
        print("Tiedostoa ei löydy.")


def uusi_peli():
    """
    Aloittaa uuden pelin tekemällä mallikentan, käyttäjälle näkyvän
    piirtokentan, numeroi mallikentan ja piirtämällä käyttäjälle näkyvän
    piirtokentan grafiikan.
    """
    tee_kentta()
    tee_avaamaton_kentta()
    numeroi_kentan()
    kentan_grafiikka()


def aloitusvalikko():
    """
    Tekee aloitusvalikon. Käyttäjän mahdolliset valinnat ovat
    t, u ja l. Jos valitaan t, näytetään tilastot avaa_tilastot-funktion avulla,
    jos valinta u, aloitetaan uusi peli ja jos valinta l, lopetaan ohjelma. 
    """
    while True:
        toiminto = input("Anna haluamasi toiminto: (t)ilastot, (u)usi peli tai (l)opeta > ")
        if toiminto == "t":
            avaa_tilastot()
        elif toiminto == "u":
            uusi_peli()
        elif toiminto == "l":
            break
        else:
            print("Vääränlainen syöte.") 

if __name__ == "__main__":
    try:
        aloitusvalikko()
    except KeyboardInterrupt:
        print("Nähdään seuraavalla kerralla!")
