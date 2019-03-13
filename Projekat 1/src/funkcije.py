#Globalne konstante
STR_BIBLIOTEKAR = "bibliotekar"
STR_KORISNIK = "korisnik"
STR_RAZMAK = "---------------------"

#Privatna funkcija za proveru da li je broj
def _isDigit(n):
    try:
        int(n)
        return True
    except ValueError:
        return  False

#Funkcija za stampanje header-a menija
def print_title(korisnik):
    ime, prezime = korisnik["ime"], korisnik["prezime"]
    print(STR_RAZMAK)
    print(f"{ime} {prezime}\n")

#Funkcija za unos teksta sa jednim stringom
def get_unos_single(text):
    while 1:
        unos = input(text)
        if unos.isalpha():
            return unos
        else:
            print("\nGreska: Unos mora imati jednu rec, bez brojeva i znakova.")

#Funkcija za unos teksta sa vise stringova
def get_unos(text):
    while 1:
        unos = input(text)
        if unos:
            return unos
        else:
            print("\nGreska: Unos ne sme biti prazan.")

#Funkcija za unos pozitivnog broja
def get_unos_num_positive(text):
    while 1:
        unos = input(text)
        if unos.isdecimal() and int(unos) > -1:
            return int(unos)
        else:
            print(f"\nGreska: Uneti odabir pozitivnim brojem.")

#Funkcija za unos broja
def get_unos_num(text):
    while 1:
        unos = input(text)
        if _isDigit(unos):
            return int(unos)
        else:
            print(f"\nGreska: Uneti odabir brojem.")

#Funkcija za unos od 1 do maksimuma selekcije, vraca 0 ako se unese "q"
def get_selection(max):
    while 1:
        unos = input(" >")
        if unos.lower() == "q":
            return 0
        if unos.isdecimal() and int(unos) >= 1 and int(unos) <= max:
            return int(unos)
        else:
            print(f"\nGreska: Uneti odabir brojem (1-{max}) ili 'q' za izlaz.")

#Funkcija za biranje tipa naloga korisnika
def get_tip_naloga():
    tip = None
    while 1:
        tip = input("\nTip naloga (`Bibliotekar` ili `Korisnik`): ")
        tip = tip.lower()
        if tip == STR_BIBLIOTEKAR or tip == STR_KORISNIK:
            return tip
        else:
            print("\nGreska: Unesite tip naloga. Tipovi su `Bibliotekar` ili `Korisnik`.")
