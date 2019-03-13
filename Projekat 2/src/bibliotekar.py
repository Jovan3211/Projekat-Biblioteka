from funkcije import *
import dataHandler
import knjige

#Globalna promenljiva ulogovanog korisnika
ULOGOVAN_KORISNIK = {}

#Glavni meni za uredjenje knjiga
def meni_knjige():
    while 1:
        print("\nUnos i izmena podataka o Knjigama")
        print(STR_RAZMAK)
        print("  1) Prikazi knjige")
        print("  2) Nova knjiga")
        print("  q) Nazad\n")

        unos = get_selection(2)

        if unos == 1:
            knjige.uredjenje_knjige()
        elif unos == 2:
            knjige.kreiranje_knjige()
        else:
            return

##Nalozi

#Meni za kreiranje naloga
def kreiranje_naloga():
    try:
        tip = get_tip_naloga()
        ime = get_unos("           Ime: ")
        prezime = get_unos("       Prezime: ")
        korisnickoIme = get_unos("Korisnicko ime: ")
        sifra = get_unos("       Lozinka: ")
    except KeyboardInterrupt:
        print("\nPrekinuto kreiranje naloga, vracanje u prethodni meni.")
        return
        
    try:
        dataHandler.kreiraj_nalog(tip, ime, prezime, korisnickoIme, sifra)
    except Exception as e:
        print(f"\nGreska: {str(e)}")
    else:
        print("\nNalog uspesno kreiran.")

#Funkcija koja prikazuje listu bibliotekara sortiranu po key-u, i ocekuje odabir
def odabir_bibliotekara(sortKey = str):
    if not dataHandler.Bibliotekari:
        raise Exception("Ne postoji nijedan bibliotekar u bazi.")

    bibliotekari = dataHandler.sort_dictionary_array(dataHandler.Bibliotekari, sortKey) #dobijanje sortirane liste knjiga po keyu sortiranja
    
    print("\nUnesite index bibliotekara koga zelite da odaberete.")
    print("{:<5}  {:<4}  {:<15}  {:<15}  {:<15}".format("Index", "Id", "Ime", "Prezime", "Korisnicko ime"))
    print("-------------------------------------------------------------------------------------------------------------------------------------")
    i = 1
    for bibliotekar in bibliotekari:
        print("{:<5}  {:<4}  {:<15}  {:<15}  {:<15}".format(i, bibliotekar["id"], bibliotekar["ime"], bibliotekar["prezime"], bibliotekar["korisnickoIme"]))
        i += 1

    print()
    odabir = get_selection(i-1)
    if odabir == 0:
        raise Exception("Odustano od biranje bibliotekara.")
    else:
        return bibliotekari[int(odabir) - 1]

#Meni za uredjivanje naloga bibliotekara
#Moze se izabrati trenutno ulogovan bibliotekar, i sva funkcionalnost je ista osim brisanja koja je iskljucena
def uredjenje_bibliotekar():
    global ULOGOVAN_KORISNIK

    try:
        bibliotekar = odabir_bibliotekara("ime")
    except Exception as e:
        print(f"\nGreska: {str(e)}")
        print("Vracanje u prethodni meni.")
        return

    while 1:
        print("\nUredjenje bibliotekara {} {}: ".format(bibliotekar["ime"], bibliotekar["prezime"]))
        print("  1) Promena imena")
        print("  2) Promena prezimena")
        print("  3) Promena korisnickog imena")
        print("  4) Promena lozinke")
        print("  5) Brisanje bibliotekara")
        print("  q) Nazad i sacuvaj\n")

        unos = get_selection(5)

        if unos == 1:
            novoIme = get_unos("Novo ime: ")
            bibliotekar.update({"ime":novoIme})
        elif unos == 2:
            novoPrezime = get_unos("Novo prezime: ")
            bibliotekar.update({"prezime":novoPrezime})
        elif unos == 3:
            novoKorisnickoIme = get_unos("Novo korisnicko ime: ")
            if dataHandler.proveri_postoji_korisnicko_ime(novoKorisnickoIme):
                print("Greska: Korisnicko ime je zauzeto.")
            else:
                bibliotekar.update({"korisnickoIme":novoKorisnickoIme})
        elif unos == 4:
            novaSifra = get_unos("Nova sifra: ")
            bibliotekar.update({"lozinka":novaSifra})
        elif unos == 5:
            if bibliotekar["korisnickoIme"] == ULOGOVAN_KORISNIK["korisnickoIme"]:
                print("\nGreska: Ne moze se obrisati ulogovani bibliotekar.")
            else:
                while 1:
                    unos = get_unos_single("Bibliotekar \"{} {}\" ce biti obrisan (d/n): ".format(bibliotekar["ime"], bibliotekar["prezime"]))
                    if unos == "d":
                        dataHandler.delete_bibliotekar(bibliotekar)
                        print("\nBibliotekar je obrisan.")
                        return
                    else:
                        print("\nBrisanje obustavljeno.")
                        break
        else:
            ULOGOVAN_KORISNIK = bibliotekar.copy()
            dataHandler.update_bibliotekar(bibliotekar)
            return

#Meni za uredjivanje korisnika
#Sadrzi opciju za brisanje odabranog korisnika
def uredjenje_korisnik():
    try:
        korisnik = knjige.odabir_korisnika("ime", dataHandler.Korisnici)
    except Exception as e:
        print(f"\nGreska: {str(e)}")
        print("Vracanje u prethodni meni.")
        return

    while 1:
        print("\nUredjenje korisnika {} {}: ".format(korisnik["ime"], korisnik["prezime"]))
        print("  1) Promena imena")
        print("  2) Promena prezimena")
        print("  3) Promena korisnickog imena")
        print("  4) Promena lozinke")
        print("  q) Nazad i sacuvaj\n")

        unos = get_selection(4)

        if unos == 1:
            novoIme = get_unos("Novo ime: ")
            korisnik.update({"ime":novoIme})
        elif unos == 2:
            novoPrezime = get_unos("Novo prezime: ")
            korisnik.update({"prezime":novoPrezime})
        elif unos == 3:
            novoKorisnickoIme = get_unos("Novo korisnicko ime: ")
            if dataHandler.proveri_postoji_korisnicko_ime(novoKorisnickoIme):
                print("Greska: Korisnicko ime je zauzeto.")
            else:
                korisnik.update({"korisnickoIme":novoKorisnickoIme})
        elif unos == 4:
            novaSifra = get_unos("Nova sifra: ")
            korisnik.update({"lozinka":novaSifra})
        else:
            dataHandler.update_korisnik(korisnik)
            return

#Glavni meni za uredjivanje naloga
def meni_nalozi():
    while 1:
        print("\nUredjivanje bibliotekara i korisnika:")
        print("  1) Uredjenje bibliotekara")
        print("  2) Uredjenje korisnika")
        print("  3) Kreiranje novog naloga")
        print("  q) Nazad\n")

        unos = get_selection(3)

        if unos == 1:
            uredjenje_bibliotekar()
        elif unos == 2:
            uredjenje_korisnik()
        elif unos == 3:
            kreiranje_naloga()
        else:
            return

#Glavni meni za zaduzivanje i razduzivanje
def meni_zaduzivanje_razduzivanje():
    while 1:
        print("\nIzaberite opciju:")
        print("  1) Zaduzivanje")
        print("  2) Razduzivanje")
        print("  q) Nazad\n")

        unos = get_selection(2)

        if unos == 1:
            knjige.meni_zaduzivanje()
        elif unos == 2:
            knjige.meni_razduzivanje()
        else:
            return

#Meni za uredjenje trenutno prijavljenog bibliotekara
def meni_trenutno_prijavljeni():
    global ULOGOVAN_KORISNIK
    bibliotekar = ULOGOVAN_KORISNIK

    while 1:
        print("\nUredjenje bibliotekara {} {}: ".format(bibliotekar["ime"], bibliotekar["prezime"]))
        print("  1) Promena imena")
        print("  2) Promena prezimena")
        print("  3) Promena korisnickog imena")
        print("  4) Promena lozinke")
        print("  q) Nazad i sacuvaj\n")

        unos = get_selection(5)

        if unos == 1:
            novoIme = get_unos("Novo ime: ")
            bibliotekar.update({"ime":novoIme})
        elif unos == 2:
            novoPrezime = get_unos("Novo prezime: ")
            bibliotekar.update({"prezime":novoPrezime})
        elif unos == 3:
            novoKorisnickoIme = get_unos("Novo korisnicko ime: ")
            if dataHandler.proveri_postoji_korisnicko_ime(novoKorisnickoIme):
                print("Greska: Korisnicko ime je zauzeto.")
            else:
                bibliotekar.update({"korisnickoIme":novoKorisnickoIme})
        elif unos == 4:
            novaSifra = get_unos("Nova sifra: ")
            bibliotekar.update({"lozinka":novaSifra})
        else:
            ULOGOVAN_KORISNIK = bibliotekar.copy()
            dataHandler.update_bibliotekar(bibliotekar)
            return

#Meni za rashodovanje knjiga
def meni_rashodovanje():
    print("\nRashodovanje knjiga:")
    try:
        knjiga = knjige.odabir_knjige("ime", dataHandler.Knjige)
    except Exception as e:
        print(f"\nGreska: {str(e)}")
        print("Vracanje u prethodni meni.")
        return

    brPrimeraka, brSlobodnihPrimeraka = knjiga["brojPrimeraka"], knjiga["brojSlobodnihPrimeraka"]
    trenutnoZaduzeni = dataHandler.get_num_zaduzenja_knjige(knjiga)
    print(f"Trenutni broj primeraka: {brPrimeraka}. Trenutni broj slobodnih primeraka: {brSlobodnihPrimeraka}.")

    while 1:
        unos = get_unos_num_positive("Broj knjiga koje zelite da rashodujete: ")
        noviBrojPrimeraka = brPrimeraka - unos
        print(f"Novi broj primeraka: {noviBrojPrimeraka}")
        if noviBrojPrimeraka < trenutnoZaduzeni:
            print(f"\nGreska: Ne ostati manji broj knjiga od trenutno zaduzenih ({trenutnoZaduzeni}).")
        else:
            if noviBrojPrimeraka < brSlobodnihPrimeraka:
                knjiga.update({"brojSlobodnihPrimeraka":noviBrojPrimeraka})
            knjiga.update({"brojPrimeraka":noviBrojPrimeraka})
            dataHandler.update_knjiga(knjiga)
            break

#Meni za brisanje korisnika
def meni_brisanje_korisnika():
    print("\nBrisanje korisnika:")

    try:
        korisnik = knjige.odabir_korisnika("ime", dataHandler.Korisnici)
    except Exception as e:
        print(f"\nGreska: {str(e)}")
        print("Vracanje u prethodni meni.")
        return

    for zaduzenje in dataHandler.Zaduzenja:
        if korisnik["clanska_karta"] == zaduzenje["idKorisnika"]:
            print("\nGreska: Korisnik prvo mora da razduzi sve knjige da bi bio obrisan.")
            return

    while 1:
        unos = get_unos_single("Korisnik '{} {}' ce biti obrisan (d/n): ".format(korisnik["ime"], korisnik["prezime"]))
        if unos == "d":
            dataHandler.delete_korisnik(korisnik)
            print("\nKorisnik je obrisan.")
            return
        else:
            print("\nBrisanje obustavljeno.")
            break


##Glavni meni bibliotekara
def meni_bibliotekar(korisnik):
    global ULOGOVAN_KORISNIK
    ULOGOVAN_KORISNIK = korisnik

    while 1:
        print_title(ULOGOVAN_KORISNIK)
        print("Bibliotekar:")
        print("  1) Unos i izmena podataka o Knjigama")
        print("  2) Unos podataka za Bibliotekara i Korisnika")
        print("  3) Izmena podataka trenutno prijavljenog Bibliotekara")
        print("  4) Zaduživanje i razduživanje Korisnika")
        print("  5) Rashodovanje knjiga")
        print("  6) Brisanje Korisnika")
        print("  q) Odjavi se\n")

        unos = get_selection(6)

        if unos == 1:
            meni_knjige()
        elif unos == 2:
            meni_nalozi()
        elif unos == 3:
            meni_trenutno_prijavljeni()
        elif unos == 4:
            meni_zaduzivanje_razduzivanje()
        elif unos == 5:
            meni_rashodovanje()
        elif unos == 6:
            meni_brisanje_korisnika()
        else:
            return