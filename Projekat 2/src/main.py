#  Projekat iz Osnova Programiranja Python
#  Bibliotecko poslovanje
#  Jovan Zlatanovic, 271634/2018 SIIT

import dataHandler
from funkcije import STR_BIBLIOTEKAR, STR_KORISNIK, STR_RAZMAK, get_tip_naloga, get_selection, get_unos
from bibliotekar import meni_bibliotekar
from korisnik import meni_korisnik

#Logovanje korisnika i bibliotekara
def login():
    brojPokusaja = 3
 
    while 1:
        korisnickoIme = get_unos("\nKorisnicko ime: ")
        sifra = get_unos("       Lozinka: ")

        try:
            tip, korisnik = dataHandler.get_nalog(korisnickoIme)
        except Exception as e:
            print(f"\nGreska: {str(e)}")
            return -1, -1

        if korisnik == -1:
            print(f"\nGreska: Korisnicko ime nije registrovano.")
            print(f"Vracanje u glavni meni")
            return -1, -1
        else:
            if korisnik["lozinka"] == sifra:
                return tip, korisnik
            else:
                brojPokusaja -= 1
                print(f"Greska: Lozinka pogresna ({brojPokusaja}).")

                if brojPokusaja < 1:
                    print(f"Vracanje u glavni meni.")
                    return -1, -1

        print()

#Metoda koja pokrece meni korisnika ili bibliotekara
def run_biblioteka(tipNaloga, korisnik):
    print("\nDobrodosli.")

    if tipNaloga == STR_BIBLIOTEKAR:
        meni_bibliotekar(korisnik)
    elif tipNaloga == STR_KORISNIK:
        meni_korisnik(korisnik)
    else:
        print("  Neocekivana greska: Tip nije bibliotekar ili korisnik, Aplikacija.py -> runBiblioteka()")

#Glavna funkcija programa
def main():
    dataHandler.initialize()
    while 1:
        print(STR_RAZMAK)
        print("Aplikacija Biblioteka\n")
        print("Glavni meni:")
        print("  1) Login")
        print("  q) Izlaz\n")

        unos = get_selection(1)
                
        if unos == 1:
            tipNaloga, korisnik = login()
            if korisnik is not -1:
                run_biblioteka(tipNaloga, korisnik)
        else:
            print("\nHvala sto ste koristli Biblioteku!")
            break

        print()

#Pozivanje glavne funkcije
main()