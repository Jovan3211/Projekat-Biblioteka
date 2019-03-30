import json
import os, sys
from datetime import datetime
from funkcije import STR_BIBLIOTEKAR, STR_KORISNIK

#Globalne liste
Bibliotekari = [{"id":0,"ime":"Prvi","prezime":"Bibliotekar","korisnickoIme":"admin","lozinka":"admin"},{"id":1,"ime":"Biblio","prezime":"Tekarovic","korisnickoIme":"bite","lozinka":"123"},{"id":3,"ime":"Marko","prezime":"Markovic","korisnickoIme":"mama","lozinka":"123"},{"id":2,"ime":"Petar","prezime":"Petrovic","korisnickoIme":"pepe","lozinka":"123"}]
Korisnici = [{"clanska_karta":1,"ime":"Dusan","prezime":"Dusanovic","obrisan":False,"korisnickoIme":"dudu","lozinka":"123"},{"clanska_karta":3,"ime":"Luka","prezime":"Lukanovic","obrisan":False,"korisnickoIme":"lulu","lozinka":"123"},{"clanska_karta":0,"ime":"Mitro","prezime":"Mitrovic","obrisan":False,"korisnickoIme":"mimi","lozinka":"123"},{"clanska_karta":2,"ime":"Simon","prezime":"Simanovic","obrisan":False,"korisnickoIme":"sisi","lozinka":"123"}]
Knjige = [{"id":5,"autor":"Boris","ime":"Avantureborisa","godinaIzdanja":2019,"brojPrimeraka":30,"brojSlobodnihPrimeraka":28},{"id":3,"autor":"Cetvrtko","ime":"Cetvrta","godinaIzdanja":413,"brojPrimeraka":23,"brojSlobodnihPrimeraka":23},{"id":0,"autor":"Dusandusopisac","ime":"Dusanovaknjiga","godinaIzdanja":2003,"brojPrimeraka":30,"brojSlobodnihPrimeraka":30},{"id":2,"autor":"Milosmilosevic","ime":"KnjigaMilosa","godinaIzdanja":2000,"brojPrimeraka":40,"brojSlobodnihPrimeraka":40},{"id":1,"autor":"Markomarkopisac","ime":"Markovaknjiga","godinaIzdanja":2005,"brojPrimeraka":20,"brojSlobodnihPrimeraka":20},{"id":4,"autor":"Autorsaduzimimenom","ime":"Prilicnodugaknjiga","godinaIzdanja":2014,"brojPrimeraka":25,"brojSlobodnihPrimeraka":24},{"id":6,"autor":"Mala","ime":"Sitna","godinaIzdanja":1987,"brojPrimeraka":7,"brojSlobodnihPrimeraka":4}]
Zaduzenja = [{"idKorisnika":1,"idKnjige":5,"datumZaduzivanja":"2019-03-1315:03","datumRazduzivanja":""},{"idKorisnika":1,"idKnjige":4,"datumZaduzivanja":"2019-03-1315:03","datumRazduzivanja":""},{"idKorisnika":3,"idKnjige":5,"datumZaduzivanja":"2019-03-1315:04","datumRazduzivanja":""}]

#Funkcija za sortiranje liste sa recnicima po odredjenom kljucu
#Koristi binary search za pretragu
def sort_dictionary_array(lista, key):
    for i in range(len(lista) - 1):
        minIndex = i
        for j in range(i+1, len(lista)):
            if lista[j][key] < lista[minIndex][key]:
                minIndex = j
        if minIndex != i:
            lista[i], lista[minIndex] = lista[minIndex], lista[i]

    return lista

#Funkcija koja vraca nadjen element u listi recnika
#Lista se sortira po unesenom kljucu i zavrsi kad se nadje element u recniku
def search_dictionary_list(lista, element, key):
    lista = sort_dictionary_array(lista, key)

    low = 0
    high = len(lista) - 1

    while high >= low:
        mid = (low + high) // 2

        if element < lista[mid][key]:
            high = mid - 1
        elif element == lista[mid][key]:
            return lista[mid]
        else:
            low = mid + 1

    return -1

#Funkcija koja nadje poslednji id u listi recnika
def get_last_id(lista, key = "id"):
    lista = sort_dictionary_array(lista, key)
    if len(lista) < 1:
        return -1
    
    return lista[len(lista)-1][key]

#Funkcija koja azurira listu sa novim item-om
def update_lista(lista, noviItem, key = "id"):
    index = 0
    for item in lista:
        if item[key] == noviItem[key]:
            lista[index] = noviItem
        index += 1

#Funkcija koja brise item iz liste
def delete_item(lista, inItem, key = "id"):
    index = 0
    for item in lista:
        if item[key] == inItem[key]:
            lista.pop(index)
        index += 1

#Wrapper funkcija za brisanje korisnika
def delete_korisnik(korisnik):
    korisnik.update({"obrisan":True})
    update_lista(Korisnici, korisnik, "clanska_karta")

#Wrapper funkcija za brisanje bibliotekara
def delete_bibliotekar(bibliotekar):
    delete_item(Bibliotekari, bibliotekar)

#Wrapper funkcija za brisanje knjige
def delete_knjiga(knjiga):
    delete_item(Knjige, knjiga)

#Wrapper funkcija za azuriranje korisnika
def update_korisnik(noviKorisnik):
    update_lista(Korisnici, noviKorisnik, "clanska_karta")

#Wrapper funkcija za azuriranje bibliotekara
def update_bibliotekar(noviBibliotekar):
    update_lista(Bibliotekari, noviBibliotekar)

#Wrapper funkcija za azuriranje knjige
def update_knjiga(novaKnjiga):
    update_lista(Knjige, novaKnjiga)

#Funkcija za azuriranje zaduzenja
def update_zaduzenje(novoZaduzenje):
    index = 0
    for item in Zaduzenja:
        if item["idKorisnika"] == novoZaduzenje["idKorisnika"] and item["idKnjige"] == novoZaduzenje["idKnjige"]:
            Zaduzenja[index] = novoZaduzenje
        index += 1

#Wrapper funkcija koja vrati nadjenog korisnika po korisnickom imenu
def get_korisnik(korisnickoIme):
    return search_dictionary_list(Korisnici, korisnickoIme, "korisnickoIme")

#Wrapper funkcija koja vrati nadjenog bibliotekara po korisnickom imenu
def get_bibliotekar(korisnickoIme):
    return search_dictionary_list(Bibliotekari, korisnickoIme, "korisnickoIme")

#Funkcija koja vrati nalog po korisnickom imenu, bez obzira da li je bibliotekar ili korisnik
def get_nalog(korisnickoIme):
    nalog = search_dictionary_list(Korisnici, korisnickoIme, "korisnickoIme")
    if nalog == -1:
        return STR_BIBLIOTEKAR, search_dictionary_list(Bibliotekari, korisnickoIme, "korisnickoIme")
    else:
        if nalog["obrisan"] == True:
            raise Exception("Korisnik je obrisan iz sistema.")
        return STR_KORISNIK, nalog

#Wrapper funkcija koja vrati nadjenu knjigu
def get_knjiga(imeKnjige):
    return search_dictionary_list(Knjige, imeKnjige, "ime")

#Funkcija za dobijanje broja zaduzenja koje knjiga ima na sebi
def get_num_zaduzenja_knjige(knjiga):
    num = 0
    for zaduzenje in Zaduzenja:
        if knjiga["id"] == zaduzenje["idKnjige"]:
            num += 1
    return num

#Funkcija koja proverava da li vec postoji korisnicko ime
def proveri_postoji_korisnicko_ime(korisnickoIme):
    if get_korisnik(korisnickoIme) == -1 and get_bibliotekar(korisnickoIme) == -1:
        return False
    else:
        return True

#Funkcija koja proverava da li vec postoji knjiga
def proveri_postojanje_knjige(imeKnjige):
    if get_knjiga(imeKnjige) == -1:
        return False
    else:
        return True

#Funkcija koja zaduzuje korisnika za knjigu
def kreiraj_zaduzenje(korisnik, knjiga):
    brSlobodnih = knjiga["brojSlobodnihPrimeraka"]

    if brSlobodnih > 0:
        brSlobodnih -= 1

        knjiga.update({"brojSlobodnihPrimeraka":brSlobodnih})
        zaduzenje = {"idKorisnika":korisnik["clanska_karta"], "idKnjige":knjiga["id"], "datumZaduzivanja":datetime.now().strftime("%Y-%m-%d %H:%M"), "datumRazduzivanja":""}

        update_knjiga(knjiga)

        Zaduzenja.append(zaduzenje) 
        return
    else:
        raise Exception("Nema vise slobodnih primeraka knjige.")

#Funkcija koja razduzuje korisnika od knjige
def skloni_zaduzenje(korisnik, knjiga):
    brSlobodnih = knjiga["brojSlobodnihPrimeraka"]

    for zaduzenje in Zaduzenja:
        if korisnik["clanska_karta"] == zaduzenje["idKorisnika"] and knjiga["id"] == zaduzenje["idKnjige"]:
            brSlobodnih += 1

            knjiga.update({"brojSlobodnihPrimeraka":brSlobodnih})
            zaduzenje.update({"datumRazduzivanja":datetime.now().strftime("%Y-%m-%d %H:%M")})
       
            update_knjiga(knjiga)
            update_zaduzenje(zaduzenje)
            return

    raise Exception("Neuspesno razduzavanje, nije nadjen id korisnika i knjige u listi zaduzenja.")

#Funkcija koja kreira knjigu po parametrima
def kreiraj_knjigu(autor = str, ime = str, godinaIzdanja = int, brojPrimeraka = 0, brojSlobodnih = -1):
    knjiga = {}
    noviID = None

    autor = autor.lower()
    autor = autor.capitalize()

    if proveri_postojanje_knjige(ime):
        raise Exception("Knjiga sa tim imenom vec postoji, mozete dodati broj primeraka u podesavanjima.")

    if brojSlobodnih == -1:
        brojSlobodnih = brojPrimeraka

    noviID = get_last_id(Knjige) + 1
    knjiga.update({"id":noviID, "autor":autor, "ime":ime, "godinaIzdanja":godinaIzdanja, "brojPrimeraka":brojPrimeraka, "brojSlobodnihPrimeraka":brojSlobodnih})
    Knjige.append(knjiga)

    return

#Funkcija koja kreira nalog po parametrima
def kreiraj_nalog(tipNaloga, ime, prezime, korisnickoIme, sifra):
    nalog = {}
    noviID = None

    ime = ime.lower()
    ime = ime.capitalize()
    prezime = prezime.lower()
    prezime = prezime.capitalize()

    if proveri_postoji_korisnicko_ime(korisnickoIme):
        raise Exception("Korisnicko ime je zauzeto.")

    if tipNaloga == STR_BIBLIOTEKAR:
        noviID = get_last_id(Bibliotekari) + 1
        nalog.update({"id":noviID, "ime":ime, "prezime":prezime, "korisnickoIme":korisnickoIme, "lozinka":sifra})
        Bibliotekari.append(nalog)
    elif tipNaloga == STR_KORISNIK:
        noviID = get_last_id(Korisnici, "clanska_karta") + 1
        nalog.update({"clanska_karta":noviID, "ime":ime, "prezime":prezime, "obrisan":False, "korisnickoIme":korisnickoIme, "lozinka":sifra})
        Korisnici.append(nalog)
    else:
        raise Exception("Neocekivano: Tip nije bibliotekar ili korisnik kod kreiranja novog naloga.")

    return