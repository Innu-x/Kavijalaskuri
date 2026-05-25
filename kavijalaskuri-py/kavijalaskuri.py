
import tkinter as tk	#ikkunakirjasto
from datetime import date	#päivämäärä
import json	#JSON-tiedostot
import os	#kasioiden ja tiedostojen toiminnot

# DATA
TIEDOSTO = "data.json"
def lataa_data():
    if os.path.exists(TIEDOSTO):	#sijainti
        with open(TIEDOSTO, "r", encoding="utf-8") as f:	#avataan, luetaan ja ääkköset
            return json.load(f)
    return []

def tallenna_data(merkinta):
    data = lataa_data()
    data.append(merkinta)
    with open(TIEDOSTO, "w", encoding="utf-8") as f:	#kirjoitetaan 
        json.dump(data, f, ensure_ascii=False, indent=2) 	#kirjoitetaan JSON-tiedostoon, näytetäään ääkköset oikein, siistitään tallennusta

# TALLENNUS
def lisaa_kavija(kayttaja_tyyppi, sukupuoli, ika): 	#tämä suoritetaan kun painetaan nappia
    merkinta = {
        "paiva": str(date.today()),
        "kayttaja_tyyppi": kayttaja_tyyppi,
        "sukupuoli": sukupuoli,
        "ika": ika
    }
    tallenna_data(merkinta)
    status_label.config(
    text=f"Tallennettu: {kayttaja_tyyppi} / {sukupuoli} / {ika}"
)
    ikkuna.after(
    2000,                                #ilmoituksen häviämisen viive
    lambda: status_label.config(text="")
)
    print("Tallennettu:", merkinta) 	#näyttää tehdyn muutoksen ja että tallennus onnistui

# ASETUKSET
IKARYHMAT = [		#eka näytetään napissa ja toinen tallennetaan tiedostoon
    ("<18", "<18"),
    ("18–29", "18-29"),
    ("30–49", "30-49"),
    ("50–64", "50-64"),
    ("65+", "65+")
]
VARIT = {
    "mies": "#00aafb",
    "nainen": "#f58e1e",
    "muu": "#69c33b"
}

# SUKUPUOLI OSIO
def luo_sukupuoli_osio(
    juuri,		#paikka mihin tehdään osio
    otsikko,
    kayttaja_tyyppi,
    sukupuoli,
    vari
):
    frame = tk.Frame(	
        juuri,
        bg="white"
    )
    frame.pack(pady=5)

    # Sukupuoliotsikko
    tk.Label(
        frame,
        text=otsikko,
        font=("Arial", 14, "bold"),
        fg=vari,		#otsikko tekstistä ja napinpohjasta saman väriset
        bg="white"
    ).pack(pady=(5, 2))		#lisää tyhjää tilaa ylä- ja alapuolelle

    # Nappirivi
    nappirivi = tk.Frame(
        frame,
        bg="white"
    )
    nappirivi.pack()		#näytetään nappirivi

    # Ikänapit
    for ika_nimi, ika_arvo in IKARYHMAT:
        nappi = tk.Label(
            nappirivi,
            text=ika_nimi,
            bg=vari,
            fg="white",
            font=("Arial", 12, "bold"),
            width=8,
            height=2,
            cursor="hand2",
            relief="solid",
            bd=1
    )
        nappi.bind(
            "<Button-1>",
            lambda event,
            kt=kayttaja_tyyppi,
            s=sukupuoli,
            i=ika_arvo:
            lisaa_kavija(kt, s, i)
    )
        nappi.pack(
            side="left",
            padx=3,
            pady=3
    )

# OTSIKKO
def otsikko(teksti, vari):
    tk.Label(
        ikkuna,
        text=teksti,
        font=("Arial", 22, "bold"),
        fg=vari,
        bg="white"
    ).pack(
        fill="x",
        pady=(10, 5)
    )

# PÄÄIKKUNA
ikkuna = tk.Tk()
ikkuna.title("Kävijälaskuri")
ikkuna.configure(bg="white")
ikkuna.geometry("700x650")

# VANHA KONKARI 
otsikko(
    "Vanha konkari",
    "black"
)
for s_nimi, s_arvo in [
    ("Mies", "mies"),
    ("Nainen", "nainen"),
    ("Muu", "muu")
]:
    luo_sukupuoli_osio(
        ikkuna,
        s_nimi,
        "vanha",
        s_arvo,
        VARIT[s_arvo]
    )

# UUSI TUTTAVUUS
otsikko(
    "Uusi tuttavuus",
    "black"
)
for s_nimi, s_arvo in [
    ("Mies", "mies"),
    ("Nainen", "nainen"),
    ("Muu", "muu")
]:
    luo_sukupuoli_osio(
        ikkuna,
        s_nimi,
        "uusi",
        s_arvo,
        VARIT[s_arvo]
    )

# STATUS (näyttää alareunassa tekstikentän, jossa näytetään tallennus)
status_label = tk.Label(
    ikkuna,
    text="",
    bg="white",
    fg="green",
    font=("Arial", 12, "bold")
)
status_label.pack(pady=10)

# LOOP (pidetään ikkuna auki ja odotetaan napin painallusta)
ikkuna.mainloop()
