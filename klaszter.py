import os
import subprocess
import random
import string
from datetime import datetime

class Klaszter:
    def __init__(self, gykonyvtar):  # klaszter: gyokerkonyvtar, klaszter adatok, szamitogepek
        self.gykonyvtar = gykonyvtar  # A klaszter gyökérkönyvtára
        self.kl_adatok = self.bekladat()  # Klaszter adatok betöltése
        self.szamitogepek = self.beszamitogepek()  # Számítógépek adatainak betöltése

    def bekladat(self):
        kl_cim = os.path.join(self.gykonyvtar, ".klaszter")  # A klaszter konfigurációs fájl elérési útja
        if not os.path.exists(kl_cim):  # Ha a fájl nem létezik, üres dictionary-t ad vissza
            return {}
        with open(kl_cim, "r", encoding="utf8") as f:  # Fájl megnyitása olvasásra
            sorok = f.readlines()  # Fájl sorainak beolvasása
        kl_adat = []  # Klaszter adatai
        for i in range(0, len(sorok), 4):
            program = sorok[i].strip()  # Program neve
            szam = int(sorok[i + 1].strip())  # Program példányainak száma
            cpu = int(sorok[i + 2].strip())  # Szükséges CPU erőforrás
            memoria = int(sorok[i + 3].strip())  # Szükséges memória
            kl_adat.append({"nev": program, "szam": szam, "processzorok": cpu, "memoria": memoria})  # Program adatainak hozzáadása
        return kl_adat

    def beszamitogepek(self):
        szamitogepek = []  # Számítógépek listája
        for nev in os.listdir(self.gykonyvtar):
            gep_utvonal = os.path.join(self.gykonyvtar, nev)  # Számítógép könyvtárának elérési útja
            if not os.path.isdir(gep_utvonal):  # Ha nem könyvtár, akkor kihagyja
                continue
            konfig = os.path.join(gep_utvonal, ".szamitogep_config")  # Számítógép konfigurációs fájlja
            if not os.path.exists(konfig):  # Ha a konfigurációs fájl nem létezik, kihagyja
                continue
            with open(konfig, "r", encoding="utf8") as f:
                sorok = f.readlines()
                if len(sorok) < 2:  # Ha nincs elég adat, kihagyja
                    continue
                cpu = int(sorok[0].strip())  # CPU erőforrások száma
                memoria = int(sorok[1].strip())  # Memória mérete
            alkalmazasok = []  # Alkalmazások listája
            for file in os.listdir(gep_utvonal):
                if file.startswith("."):  # Rejtett fájlokat kihagyja
                    continue
                with open(gep_utvonal + "//" + file, "r", encoding="utf8") as app:  # Alkalmazás fájl megnyitása
                    sorok = app.readlines()
                    datum = sorok[0].strip()  # Alkalmazás indításának dátuma
                    statusz = sorok[1].strip()  # Alkalmazás állapota (AKTÍV/INAKTÍV)
                    pcpu = int(sorok[2].strip())  # Alkalmazás által használt CPU
                    pmemoria = int(sorok[3].strip())  # Alkalmazás által használt memória
                    alkalmazasok.append({
                        "program": file,
                        "datum": datum,
                        "statusz": statusz,
                        "processzorok": pcpu,
                        "memoria": pmemoria
                    })  # Alkalmazás adatainak hozzáadása
            szamitogepek.append({
                "nev": nev,
                "processzorok": cpu,
                "memoria": memoria,
                "alkalmazasok": alkalmazasok,
            })  # Számítógép adatainak hozzáadása
        return szamitogepek

    def kl_mentes(self):
        kl_cim = os.path.join(self.gykonyvtar, ".klaszter")
        subprocess.check_call(["attrib", "-H", kl_cim])  # Fájl rejtett attribútumának eltávolítása
        with open(kl_cim, "w", encoding="utf8") as f:
            for data in self.kl_adatok:  # Klaszter adatok kiírása a .klaszter fájlban
                f.write(f"{data['nev']}\n{data['szam']}\n{data['processzorok']}\n{data['memoria']}\n")
            for gep in self.szamitogepek:  # Számítógépek adatainak kiírása
                gep_utvonal = os.path.join(self.gykonyvtar, gep["nev"])
                konfig = os.path.join(gep_utvonal, ".szamitogep_config")
                subprocess.check_call(["attrib", "-H", konfig])  # Konfigurációs fájl rejtett attribútumának eltávolítása
                with open(konfig, "w", encoding="utf8") as f:
                    f.write(f"{gep['processzorok']}\n{gep['memoria']}\n")
                    for app in gep["alkalmazasok"]:  # Alkalmazások adatainak kiírása
                        app_file = os.path.join(gep_utvonal, app["program"])
                        with open(app_file, "w", encoding="utf8") as f:
                            f.write(f"{app['datum']}\n{app['statusz']}\n{app['processzorok']}\n{app['memoria']}\n")
                subprocess.check_call(["attrib", "+H", konfig])  # Konfigurációs fájl rejtett attribútumának visszaállítása
        subprocess.check_call(["attrib", "+H", kl_cim])  # Klaszter konfigurációs fájl rejtett attribútumának visszaállítása
    def kl_ellenorzes(self):
        hibalista = []  # Hibalista, amelybe a klaszter hibái kerülnek
        for program in self.kl_adatok:
            program_nev = program["nev"]  # Program neve
            elvart_prog = program["szam"]  # Elvárt programpéldányok száma
            akt_prog = 0  # Aktív programpéldányok száma
            inakt_prog = 0  # Inaktív programpéldányok száma
            ossz_prog = 0  # Összes programpéldány száma

            for szgep in self.szamitogepek:
                ossz_cpu = 0  # Összes CPU-használat
                ossz_mem = 0  # Összes memóriahasználat
                for alk in szgep["alkalmazasok"]:
                    if alk["program"].startswith(program_nev):
                        ossz_prog += 1  # Összes programpéldány számának növelése
                        if alk["statusz"] == "AKTÍV":  # Ha az alkalmazás aktív
                            akt_prog += 1
                        else:  # Ha inaktív
                            inakt_prog += 1
                        ossz_cpu += alk["processzorok"]  # CPU-használat összegzése
                        ossz_mem += alk["memoria"]  # Memóriahasználat összegzése
                max_cpu = szgep["processzorok"]  # Számítógép maximális CPU kapacitása
                max_mem = szgep["memoria"]  # Számítógép maximális memóriája
                if ossz_cpu > max_cpu or ossz_mem > max_mem:  # Ha túllépte az erőforrásokat
                    uzi = f"{szgep['nev']}: Erőforrás-túllépés!"  # Hibaüzenet
                    if ossz_cpu > max_cpu:
                        uzi += f" - CPU: {ossz_cpu} > {max_cpu}"  # CPU túllépés hozzáadása
                    if ossz_mem > max_mem:
                        uzi += f" - Memória: {ossz_mem} > {max_mem}"  # Memória túllépés hozzáadása
                    hibalista.append(uzi)

            if akt_prog < elvart_prog:  # Ha kevesebb az aktív példány, mint az elvárt
                uzi = f"{program_nev}: Túl kevés AKTÍV példány! (Elvárt: {elvart_prog}, Aktuális: AKTÍV: {akt_prog}, INAKTÍV: {inakt_prog})"
                hibalista.append(uzi)

            if ossz_prog > elvart_prog:  # Ha több példány fut, mint az elvárt
                uzi = f"{program_nev}: Túl sok példány fut! (Elvárt: {elvart_prog}, Aktuális: {ossz_prog}, AKTÍV: {akt_prog}, INAKTÍV: {inakt_prog})"
                hibalista.append(uzi)

        if not hibalista:  # Ha nincs hiba
            hibalista.append("Klaszter állapota megfelelő.")
        return hibalista

    def monitoring(self, v, program_nev=None):
        valasz = []  # Válaszlista, amelybe az eredmények kerülnek
        if v == 1:  # CPU és memória használat lekérdezése
            for szg in self.szamitogepek:
                haszp = 0  # CPU-használat
                haszm = 0  # Memóriahasználat
                for app in szg["alkalmazasok"]:
                    haszp += app["processzorok"]  # CPU-használat összegzése
                    haszm += app["memoria"]  # Memóriahasználat összegzése
                valasz.append(haszp)  # CPU-használat hozzáadása
                valasz.append(haszm)  # Memóriahasználat hozzáadása
            return valasz

        if v == 2:  # Alkalmazások listázása
            for szg in self.szamitogepek:
                for app in szg["alkalmazasok"]:
                    valasz.append({
                        "nev": app["program"].split("-")[0],  # Alkalmazás neve
                        "azonosito": app["program"],  # Alkalmazás azonosítója
                        "statusz": app["statusz"]  # Alkalmazás állapota
                    })
            # Rendezés név szerint
            for i in range(len(valasz)):
                for j in range(i, len(valasz)):
                    if valasz[i]["nev"] > valasz[j]["nev"]:
                        aux = valasz[i]
                        valasz[i] = valasz[j]
                        valasz[j] = aux
            return valasz

        if v == 3:  # Aktív és inaktív alkalmazások száma
            akt = 0  # Aktív alkalmazások száma
            inakt = 0  # Inaktív alkalmazások száma
            for szg in self.szamitogepek:
                for alk in szg["alkalmazasok"]:
                    if alk["statusz"] == "AKTÍV":
                        akt += 1  # Aktív alkalmazások számának növelése
                    elif alk["statusz"] == "INAKTÍV":
                        inakt += 1  # Inaktív alkalmazások számának növelése
            valasz.append(akt)  # Aktív alkalmazások hozzáadása
            valasz.append(inakt)  # Inaktív alkalmazások hozzáadása
            return valasz

        if v == 4:  # Klaszter állapotának ellenőrzése
            valasz = self.kl_ellenorzes()  # Hibalista lekérése
            return valasz

        if v == 5 and program_nev:  # Egy adott program részletes adatai
            for szg in self.szamitogepek:
                for app in szg["alkalmazasok"]:
                    if app["program"].startswith(program_nev):
                        valasz.append({
                            "szamitogep": szg["nev"],  # Számítógép neve
                            "azonosito": app["program"],  # Alkalmazás azonosítója
                            "processzorok": app["processzorok"],  # CPU-használat
                            "memoria": app["memoria"]  # Memóriahasználat
                        })
            return valasz

    def szamitogep_torles(self, szamitogep):
        gep_utvonal = os.path.join(self.gykonyvtar, szamitogep)
        konfig = os.path.join(gep_utvonal, ".szamitogep_config")
        if os.path.exists(konfig):  # Ha a konfigurációs fájl létezik
            os.remove(konfig)  # Konfigurációs fájl törlése
        if not os.listdir(gep_utvonal):  # Ha a könyvtár üres
            os.rmdir(gep_utvonal)  # Könyvtár törlése
        for szg in self.szamitogepek:
            if szg["nev"] == szamitogep:
                self.szamitogepek.remove(szg)  # Számítógép eltávolítása a listából

    def szamitogep_hozzaad(self, szamitogep, cpu, memoria):
        gep_utvonal = os.path.join(self.gykonyvtar, szamitogep)
        konfig = os.path.join(gep_utvonal, ".szamitogep_config")
        os.makedirs(gep_utvonal)  # Könyvtár létrehozása
        with open(konfig, "w", encoding="utf8") as f:
            f.write(f"{cpu}\n{memoria}\n")
        uj_gep = {
            "nev": szamitogep,
            "processzorok": cpu,
            "memoria": memoria,
            "alkalmazasok": [],
        }
        self.szamitogepek.append(uj_gep)  # Új számítógép hozzáadása a listához

    def program_leallit(self, program):
        for alk in self.kl_adatok:
            if alk["nev"] == program:
                self.kl_adatok.remove(alk)
        for szg in self.szamitogepek:
            torlendo = []  # Törlendő alkalmazások listája
            for app in szg["alkalmazasok"]:
                if program == app["program"].split("-")[0]:
                    app_utvonal = os.path.join(self.gykonyvtar, szg["nev"], app["program"])
                    if os.path.exists(app_utvonal):
                        os.remove(app_utvonal)  # Fájl törlése
                    torlendo.append(app)  # Alkalmazás hozzáadása a törlendő listához
            for app in torlendo:  # Törlendő alkalmazások törlése
                szg["alkalmazasok"].remove(app)
        self.kl_mentes()  # Klaszter adatok mentése

    def program_modosit(self, prognev, szam, cpu, memoria):
        for program in self.kl_adatok:
            if program["nev"] == prognev:
                program["szam"] = szam  # Program példányainak számának módosítása
                program["processzorok"] = cpu  # CPU erőforrások módosítása
                program["memoria"] = memoria  # Memória méretének módosítása
        self.kl_mentes()  # Klaszter adatok mentése

    def hozzaad_ell(self, nev, gep):
        haszp = 0  # Összes CPU-használat
        haszm = 0  # Összes memóriahasználat
        for szg in self.szamitogepek:
            if szg["nev"] == gep:
                agep = szg  # Keresett számítógép
                for app in szg["alkalmazasok"]:
                    haszp += app["processzorok"]  # CPU-használat összegzése
                    haszm += app["memoria"]  # Memóriahasználat összegzése
        for program in self.kl_adatok:
            if program["nev"] == nev:
                haszp += program["processzorok"]  # CPU-használat hozzáadása
                haszm += program["memoria"]  # Memóriahasználat hozzáadása
        if haszp > agep["processzorok"] or haszm > agep["memoria"]:  # Ha túllépte az erőforrásokat
            return False  # Nem lehet hozzáadni
        return True  # Hozzáadható

    def programpeldany_hozzaad(self, nev, gep):
        # Ellenőrzi, hogy a programpéldány hozzáadható-e a számítógéphez (erőforrások alapján)
        if self.hozzaad_ell(nev, gep):
            for program in self.kl_adatok:
                if program["nev"] == nev:
                    program_adat = program  # Program adatainak elmentése

            for szg in self.szamitogepek:
                if szg["nev"] == gep:
                    while True:
                        # Egyedi azonosító generálása a programpéldányhoz
                        egyedi_azonosito = nev + "-" + "".join(
                            random.choices(string.ascii_lowercase + string.digits, k=6))
                        # Az új fájl elérési útja
                        ujfile = os.path.join(self.gykonyvtar, szg["nev"], egyedi_azonosito)
                        if not os.path.exists(ujfile):  # Ha az azonosító egyedi, kilép a ciklusból
                            break

                    # Az aktuális dátum és idő lekérése
                    datum = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # Új programpéldány hozzáadása a számítógép alkalmazásaihoz
                    szg["alkalmazasok"].append({
                        "program": egyedi_azonosito,  # Program azonosítója
                        "datum": datum,  # Létrehozás dátuma
                        "statusz": "AKTÍV",  # Alapértelmezett állapot
                        "processzorok": program_adat["processzorok"],  # CPU igény
                        "memoria": program_adat["memoria"]  # Memória igény
                    })

            # Klaszter adatok mentése
            self.kl_mentes()

    def programpeldany_torles(self, nev):
        for program in self.kl_adatok:
            if program["nev"] == nev:
                if program["szam"]-1 <= 0:  # Ha nincs több példány, eltávolítja a programot
                    self.kl_adatok.remove(program)
        for szg in self.szamitogepek:
            for alk in szg["alkalmazasok"]:
                if alk["program"] == nev:
                    szg["alkalmazasok"].remove(alk)  # Példány eltávolítása a listából
                    app_utvonal = os.path.join(self.gykonyvtar, szg["nev"], alk["program"])
                    if os.path.exists(app_utvonal):
                        os.remove(app_utvonal)  # Fájl törlése
        # Klaszter adatok mentése
        self.kl_mentes()
