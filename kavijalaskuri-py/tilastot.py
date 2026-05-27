
import json	# JSON-tallennuksen käyttöönotto
import os	# tuo käyttöön tiedostoihin ja kansioihin liittyviä toimintoja(esim. tarkistaa onko tietty kansio jo olemassa).
from collections import Counter, defaultdict	#määrien lasku automaattisesti

TIEDOSTO = "data.json"

def lataa_data():
    if os.path.exists(TIEDOSTO):					# tarkistaa löytyykö tiedosto
        with open(TIEDOSTO, "r", encoding="utf-8") as tiedosto: 	# "r" lukee tiedoston ja encoding= auttaa ääkkösten kanssa
            return json.load(tiedosto)					
    return []

def hae_kuukausi(paiva):
    return paiva[:7]     # esim. 2026-05-22 -> 2026-05

def hae_kvartaali(paiva):
    vuosi = paiva[:4]
    kuukausi = int(paiva[5:7])
    if kuukausi <= 3:
        return f"{vuosi} Q1"
    elif kuukausi <= 6:
        return f"{vuosi} Q2"
    elif kuukausi <= 9:
        return f"{vuosi} Q3"
    else:
        return f"{vuosi} Q4"

def laske_kuukausitilastot():
    data = lataa_data()
    tilastot = defaultdict(lambda: {
        "yhteensa": 0,
        "vanha": 0,
        "uusi": 0,
        "sukupuolet": Counter(),
        "iat": Counter()
    })
    for merkinta in data:
        kuukausi = hae_kuukausi(merkinta["paiva"])
        tilastot[kuukausi]["yhteensa"] += 1
        tilastot[kuukausi][merkinta["kayttaja_tyyppi"]] += 1
        tilastot[kuukausi]["sukupuolet"][merkinta["sukupuoli"]] += 1
        tilastot[kuukausi]["iat"][merkinta["ika"]] += 1
    return tilastot

def laske_kvartaalitilastot():
    data = lataa_data()
    tilastot = defaultdict(lambda: {
        "yhteensa": 0,
        "vanha": 0,
        "uusi": 0,
        "sukupuolet": Counter(),
        "iat": Counter()
    })
    for merkinta in data:
        kvartaali = hae_kvartaali(merkinta["paiva"])
        tilastot[kvartaali]["yhteensa"] += 1
        tilastot[kvartaali][merkinta["kayttaja_tyyppi"]] += 1
        tilastot[kvartaali]["sukupuolet"][merkinta["sukupuoli"]] += 1
        tilastot[kvartaali]["iat"][merkinta["ika"]] += 1
    return tilastot


def tulosta_tilastot(tilastot):
    for jakso, arvot in sorted(tilastot.items()):
        print()
        print(jakso)
        print("-" * 30)
        print("Yhteensä:", arvot["yhteensa"])
        print("Vanhat konkarit:", arvot["vanha"])
        print("Uudet tuttavuudet:", arvot["uusi"])
        print("\nSukupuolet:")
        for sukupuoli, maara in arvot["sukupuolet"].items():
            print(f" - {sukupuoli}: {maara}")
        print("\nIkäryhmät:")
        for ika, maara in arvot["iat"].items():
            print(f" - {ika} - {maara}")
def tallenna_raportti(
    tiedostonimi,
    tilastot
):
    os.makedirs(		#luodaan kansio raportit, ei haittaa vaikka olisi jo olemassa
        "raportit",
        exist_ok=True
    )
    polku = f"raportit/{tiedostonimi}"
    with open(		#avataan kirjoittamista varten
        polku,
        "w",
        encoding="utf-8"
    ) as tiedosto:
        for jakso, arvot in sorted(tilastot.items()):
            tiedosto.write(f"\n{jakso}\n")
            tiedosto.write("-" * 30 + "\n")
            tiedosto.write(
                f"Yhteensä: {arvot['yhteensa']}\n"
            )
            tiedosto.write(
                f"Vanhat konkarit: {arvot['vanha']}\n"
            )
            tiedosto.write(
                f"Uudet tuttavuudet: {arvot['uusi']}\n"
            )
            #sukupulet siistiksi
            tiedosto.write("Sukupuolet:\n")
            for sukupuoli, maara in arvot["sukupuolet"].items():
                tiedosto.write(
                    f" - {sukupuoli}: {maara}\n"
            )
            # ikäryhmät siistiksi myös
            tiedosto.write("Ikäryhmät:\n")
            for ika, maara in arvot["iat"].items():
                tiedosto.write(
                    f" - {ika}: {maara}\n"
            )
    print(f"Raportti tallennettu: {polku}")

if __name__ == "__main__":
    kuukausi = laske_kuukausitilastot()
    kvartaali = laske_kvartaalitilastot()
    print("KUUKAUSITILASTOT")
    tulosta_tilastot(kuukausi)
    print()
    print("KVARTAALITILASTOT")
    tulosta_tilastot(kvartaali)

    # Tallennus tiedostoihin
    tallenna_raportti(
        "kuukausiraportti.txt",
        kuukausi
    )
    tallenna_raportti(
        "kvartaaliraportti.txt",
        kvartaali
    )
