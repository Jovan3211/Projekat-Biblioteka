from funkcije import get_selection, get_unos, get_unos_num_positive, get_unos_single
import dataHandler

#Funkcija koja prikazuje listu korisnika sortiranu po key-u, i ocekuje odabir
def odabir_korisnika(sortKey, listaKorisnika):
    if not listaKorisnika:
        raise Exception("Ne postoji nijedan korisnik u bazi.")

    korisnici = dataHandler.sort_dictionary_array(listaKorisnika, sortKey) #dobijanje sortirane liste knjiga po keyu sortiranja
    korisnici = [x for x in korisnici if x["obrisan"] == False]

    print("\nUnesite index korisnika koga zelite da odaberete.")
    print("{:<5}  {:<13}  {:<15}  {:<15}  {:<15}".format("Index", "Clanska karta", "Ime", "Prezime", "Korisnicko ime"))
    print("-------------------------------------------------------------------------------------------------------------------------------------")
    i = 1
    for korisnik in korisnici:
        print("{:<5}  {:<13}  {:<15}  {:<15}  {:<15}".format(i, korisnik["clanska_karta"], korisnik["ime"], korisnik["prezime"], korisnik["korisnickoIme"]))
        i += 1

    print()
    odabir = get_selection(i-1)
    if odabir == 0:
        raise Exception("Odustano od biranje korisnika.")
    else:
        return korisnici[int(odabir) - 1]

#Funkcija koja prikazuje listu knjiga sortiranu po key-u
#Ako je noSelection onda samo ispisuje, bez ocekivanja da korisnik izabere knjigu iz liste
def odabir_knjige(sortKey, listaKnjiga, noSelection = False):
    if not listaKnjiga:
        raise Exception("Ne postoji nijedna knjiga u bazi.")

    knjige = dataHandler.sort_dictionary_array(listaKnjiga, sortKey)
    
    if not noSelection:
        print("\nUnesite index knjige koju zelite da odaberete.")
    print ("{:<5}  {:<4}  {:<22}  {:<30}  {:<15}  {:<21}  {:<24}".format("Index", "Id", "Autor", "Ime knjige", "Godina izdanja", "Ukupan broj primeraka", "Broj slobodnih primeraka"))
    print("-------------------------------------------------------------------------------------------------------------------------------------")
    i = 1
    for knjiga in knjige:
        print("{:<5}  {:<4}  {:<22}  {:<30}  {:<15}  {:<21}  {:<24}".format(i, knjiga["id"], knjiga["autor"], knjiga["ime"], knjiga["godinaIzdanja"], knjiga["brojPrimeraka"], knjiga["brojSlobodnihPrimeraka"]))
        i += 1

    print()
    if noSelection:
        return -1

    odabir = get_selection(i-1)
    if odabir == 0:
        raise Exception("Odustano od biranja knjige.")
    else:
        return knjige[int(odabir) - 1]

#Meni za uredjivanje knjige
def uredjenje_knjige():
    try:
        knjiga = odabir_knjige("ime", dataHandler.Knjige)
    except Exception as e:
        print(f"\nGreska: {str(e)}")
        print("Vracanje u prethodni meni.")
        return

    while 1:
        print("\nUredjenje knjige '{}': ".format(knjiga["ime"]))
        print("  1) Promena imena knjige")
        print("  2) Promena autora")
        print("  3) Promena godine")
        print("  4) Dodavanje ukupnog broja primeraka")
        print("  5) Menjanje broja slobodnih primeraka")
        print("  6) Brisanje knjige")
        print("  q) Nazad i sacuvaj\n")

        unos = get_selection(6)

        if unos == 1:
            novoIme = get_unos("Novo ime knjige: ")
            knjiga.update({"ime":novoIme})
        elif unos == 2:
            noviAutor = get_unos("Novi autor: ")
            knjiga.update({"autor":noviAutor})
        elif unos == 3:
            novaGodina = get_unos_num_positive("Nova godina: ")
            knjiga.update({"godinaIzdanja":novaGodina})
        elif unos == 4:
            brPrimeraka, brSlobodnihPrimeraka = knjiga["brojPrimeraka"], knjiga["brojSlobodnihPrimeraka"]
            print(f"Trenutan ukupan broj primeraka: {str(brPrimeraka)}.")
            while 1:
                unos = get_unos_num_positive("Novi ukupan broj primeraka: ")
                if unos < brPrimeraka:
                    print("\nGreska: Novi ukupan broj primeraka knjiga ne sme biti manji od trenutnog.")
                else:
                    brSlobodnihPrimeraka += (unos - brPrimeraka)
                    brPrimeraka = unos
                    print(f"Novi broj primeraka: {brPrimeraka}. Novi broj slobodnih primeraka: {brSlobodnihPrimeraka}.")
                    knjiga.update({"brojPrimeraka":brPrimeraka})
                    knjiga.update({"brojSlobodnihPrimeraka":brSlobodnihPrimeraka})
                    break
        elif unos == 5:
            brPrimeraka, brSlobodnihPrimeraka = knjiga["brojPrimeraka"], knjiga["brojSlobodnihPrimeraka"]
            trenutnoZaduzeni = dataHandler.get_num_zaduzenja_knjige(knjiga)
            print(f"Trenutni broj primeraka: {brPrimeraka}. Trenutni broj slobodnih primeraka: {brSlobodnihPrimeraka}.")

            while 1:
                unos = get_unos_num_positive("Novi broj slobodnih primeraka: ")
                if unos > brPrimeraka:
                    print("\nGreska: Novi ukupan broj slobodnih primeraka ne sme biti veci od trenutnog ukupnog broja primeraka.")
                else:
                    if (unos + trenutnoZaduzeni) > brPrimeraka:
                        print(f"\nGreska: Mora se ostaviti mesta za razduzenje trenutno zaduzenih korisnika ({trenutnoZaduzeni}).")
                    else:
                        brSlobodnihPrimeraka = unos
                        print(f"Novi broj slobodnih primeraka: {brSlobodnihPrimeraka}.")
                        knjiga.update({"brojSlobodnihPrimeraka":brSlobodnihPrimeraka})
                        break
        elif unos == 6:
            for zaduzenje in dataHandler.Zaduzenja:
                if knjiga["id"] == zaduzenje["idKnjige"]:
                    print("\nSva zaduzenja za ovu knjigu moraju biti razduzena da bi se obrisala.")
                    return

            while 1:
                unos = get_unos_single("Knjiga '{}' ce biti obrisana (d/n): ".format(knjiga["ime"]))
                if unos == "d":
                    dataHandler.delete_knjiga(knjiga)
                    print("\nKnjiga je obrisana.")
                    return
                else:
                    print("\nBrisanje obustavljeno.")
                    break
        else:
            dataHandler.update_knjiga(knjiga)
            return

#Meni polja za kreiranje knjige
def kreiranje_knjige():
    try:
        brojSlobodnih = -1

        autor = get_unos("         Autor: ")
        imeKnjige = get_unos("    Ime knjige: ")
        godina = get_unos_num_positive("Godina izdanja: ")
        brojPrimeraka = get_unos_num_positive("Broj primeraka: ")
        while 1:
            brojSlobodnih = get_unos_num_positive("Broj slobodnih primeraka: ")
            if brojSlobodnih > brojPrimeraka:
                print("\nGreska: Broj slobodnih primeraka ne sme biti veci od ukupnog broja primeraka.")
            else:
                break
    except KeyboardInterrupt:
        print("\nPrekinuto kreiranje knjige, vracanje u prethodni meni.")
        return

    try:
        dataHandler.kreiraj_knjigu(autor.title(), imeKnjige, godina, brojPrimeraka, brojSlobodnih)
    except Exception as e:
        print(f"\nGreska: {str(e)}")
    else:
        print(f"\nKnjiga '{imeKnjige}' je uspesno kreirana i dodata.\n")

#Funkcija koja po unosu trazi korisnike i vrati rezultat
def nalazenje_korisnika():
    pretraga = input("\nUnesite filter pretrage korisnika: ")
    
    nadjeniKorisnici = []

    if pretraga == "":
        nadjeniKorisnici = dataHandler.Korisnici
    else:
        for korisnik in dataHandler.Korisnici:
            if (pretraga == str(korisnik["clanska_karta"]) or \
                pretraga.lower() in korisnik["ime"].lower() or \
                pretraga.lower() in korisnik["prezime"].lower() or \
                pretraga.lower() == korisnik["korisnickoIme"].lower()):

                nadjeniKorisnici.append(korisnik)

    return True, nadjeniKorisnici

#Funkcija koja po unosu trazi knjige i vrati rezultat
def nalazenje_knjiga():
    pretraga = input("\nUnesite filter pretrage knjige: ")
    
    nadjeneKnjige = []

    if pretraga == "":
        nadjeneKnjige = dataHandler.Knjige
    else:
        for knjiga in dataHandler.Knjige:
            if (pretraga == str(knjiga["id"]) or \
                pretraga.lower() in knjiga["ime"].lower() or \
                pretraga.lower() in knjiga["autor"].lower() or \
                pretraga == str(knjiga["godinaIzdanja"])):

                nadjeneKnjige.append(knjiga)

    return True, nadjeneKnjige

#Meni za zaduzivanje knjige
#Ispisu se knjige po potrazi od kojih se odabere jedna, i odabere se korisnik koji da se zaduzi
def meni_zaduzivanje():
    print("\nZaduzivanje knjiga")

    nadjeno, nadjeneKnjige = nalazenje_knjiga()
    if not nadjeno:
        print("\nNije nadjena knjiga pod navedenim filterom.")
        return

    try:
        knjiga = odabir_knjige("ime", nadjeneKnjige)
    except Exception as e:
        print(f"\nGreska: {str(e)}")
        print("Vracanje u prethodni meni.")
        return

    nadjeno, nadjeniKorisnici = nalazenje_korisnika()
    if not nadjeno:
        print("\nNije nadjen korisnik pod navedenim filterom.")
        return

    try:
        korisnik = odabir_korisnika("ime", nadjeniKorisnici)
    except Exception as e:
        print(f"\nGreska: {str(e)}")
        print("Vracanje u prethodni meni.")
        return

    try:
        dataHandler.kreiraj_zaduzenje(korisnik, knjiga)
    except Exception as e:
        print(f"\nGreska: {str(e)}")
    else:
        print("\nKreirano zaduzenje korisnika '{} {}' za knjigu '{}'.".format(korisnik["ime"], korisnik["prezime"], knjiga["ime"]))

#Meni za razduzivanje knjige
#Ispisu se knjige po potrazi od kojih se odabere jedna, ispisu se svi korisnici zaduzenu za knjigu, i onda se izabere koji da se razduzi
def meni_razduzivanje():
    print("\nRazduzivanje knjiga")
    
    nadjeno, nadjeniKorisnici = nalazenje_korisnika()
    if not nadjeno:
        print("\nNije nadjen korisnik pod navedenim filterom.")
        return

    try:
        korisnik = odabir_korisnika("ime", nadjeniKorisnici)
    except Exception as e:
        print(f"\nGreska: {str(e)}")
        print("Vracanje u prethodni meni.")
        return

    nadjeneZaduzeneKnjige = []
    for zaduzenje in dataHandler.Zaduzenja:
        if korisnik["clanska_karta"] == zaduzenje["idKorisnika"]:
            nadjeneZaduzeneKnjige.append(dataHandler.search_dictionary_list(dataHandler.Knjige, zaduzenje["idKnjige"], "id"))

    if not nadjeneZaduzeneKnjige:
        print("\nGreska: Korisnik nema nijednu zaduzenu knjigu.")
        return

    try:
        knjiga = odabir_knjige("ime", nadjeneZaduzeneKnjige)
    except Exception as e:
        print(f"\nGreska: {str(e)}")
        print("Vracanje u prethodni meni.")
        return

    try:
        dataHandler.skloni_zaduzenje(korisnik, knjiga)
    except Exception as e:
        print(f"\nGreska: {str(e)}")
    else:
        print("\nKorisnik '{} {}' je razduzio knjigu '{}'.".format(korisnik["ime"], korisnik["prezime"], knjiga["ime"]))
