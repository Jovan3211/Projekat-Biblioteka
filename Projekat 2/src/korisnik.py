from funkcije import print_title, get_selection, get_unos
from knjige import odabir_knjige, nalazenje_knjiga
from bibliotekar import uredjenje_korisnik
import dataHandler

#Meni za zaduzivanje knjiga
def zaduzene_knjige(korisnik):
    if not dataHandler.Knjige:
        print("Greska: Ne postoji nijedna knjiga u bazi.")
        return
    
    nadjeneZaduzeneKnjige = []
    zaduzenja = []
    for zaduzenje in dataHandler.Zaduzenja:
        if korisnik["clanska_karta"] == zaduzenje["idKorisnika"]:
            nadjeneZaduzeneKnjige.append(dataHandler.search_dictionary_list(dataHandler.Knjige, zaduzenje["idKnjige"], "id"))
            zaduzenja.append(zaduzenje)

    if not nadjeneZaduzeneKnjige:
        print("\nGreska: Korisnik nema nijednu zaduzenu knjigu.")
        return

    print("\nPrikaz svih zaduzenih knjiga")
    print ("{:<4}  {:<22}  {:<30}  {:<15}  {:<17}".format("Id", "Autor", "Ime knjige", "Godina izdanja", "Vreme zaduzenja"))
    print("-----------------------------------------------------------------------------------------------")
    if not nadjeneZaduzeneKnjige:
        return

    i = 0
    for knjiga in nadjeneZaduzeneKnjige:
        print("{:<4}  {:<22}  {:<30}  {:<15}  {:<17}".format(knjiga["id"], knjiga["autor"], knjiga["ime"], knjiga["godinaIzdanja"], zaduzenja[i]["datumZaduzivanja"]))
        i += 1

    print()

#Meni za pretrazivanje knjiga
def meni_knjige():
    nadjeno, nadjeneKnjige = nalazenje_knjiga()

    if not nadjeno:
        print("\nNije nadjena knjiga pod navedenim filterom.")
        return

    try:
        odabir_knjige("ime", nadjeneKnjige, noSelection=True)
    except Exception as e:
        print(f"\nGreska: {str(e)}")
        print("Vracanje u prethodni meni.")
        return

#Meni za izmenu podataka korisnika
def izmena_podataka(korisnik):
    while 1:
        print("\nPromena licnih podataka:")
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

#Glavni meni korisnika
def meni_korisnik(korisnik):
    while 1:
        print_title(korisnik)
        print("Korisnik:")
        print("  1) Pregled zaduženih Knjiga")
        print("  2) Pretraživanje knjiga")
        print("  3) Izmena licnih podataka")
        print("  q) Odjavi se\n")

        unos = get_selection(3)

        if unos == 1:
            zaduzene_knjige(korisnik)
        elif unos == 2:
            meni_knjige()
        elif unos == 3:
            izmena_podataka(korisnik)
        else:
            return