from abc import ABC, abstractmethod
from datetime import datetime

class Jarat(ABC):
    def __init__(self, jaratszam, celallomas, jegyar):
        self._jaratszam = jaratszam
        self._celallomas = celallomas
        self._jegyar = jegyar
        self._elerheto = True

    def get_jaratszam(self):
        return self._jaratszam

    def get_celallomas(self):
        return self._celallomas

    def get_jegyar(self):
        return self._jegyar

    def is_elerheto(self):
        return self._elerheto

    def set_elerheto(self, value):
        self._elerheto = value

    @abstractmethod
    def tipus(self):
        pass


class BelfoldiJarat(Jarat):
    def tipus(self):
        return "Belföldi"


class NemzetkoziJarat(Jarat):
    def tipus(self):
        return "Nemzetközi"

class JegyFoglalas:
    def __init__(self, foglalas_id, jarat, datum):
        if not isinstance(datum, datetime):
            raise ValueError("Érvénytelen dátum!")

        if datum < datetime.now():
            raise ValueError("Nem lehet múltbeli dátumra foglalni!")

        if not jarat.is_elerheto():
            raise Exception("A járat nem elérhető!")

        self._foglalas_id = foglalas_id
        self._jarat = jarat
        self._datum = datum

    def get_id(self):
        return self._foglalas_id

    def __str__(self):
        return (f"Foglalás ID: {self._foglalas_id}, "
                f"Járat: {self._jarat.get_jaratszam()}, "
                f"Cél: {self._jarat.get_celallomas()}, "
                f"Dátum: {self._datum.strftime('%Y-%m-%d')}, "
                f"Ár: {self._jarat.get_jegyar()} Ft")

class LegiTarsasag:
    def __init__(self, nev):
        self._nev = nev
        self._jaratok = []
        self._foglalasok = []

    def add_jarat(self, jarat):
        self._jaratok.append(jarat)

    def list_jaratok(self):
        for j in self._jaratok:
            print(f"{j.get_jaratszam()} - {j.get_celallomas()} ({j.tipus()}) - {j.get_jegyar()} Ft")

    def foglalas(self, jaratszam, datum):
        jarat = next((j for j in self._jaratok if j.get_jaratszam() == jaratszam), None)

        if not jarat:
            raise Exception("Nincs ilyen járat!")

        foglalas_id = len(self._foglalasok) + 1
        uj_foglalas = JegyFoglalas(foglalas_id, jarat, datum)
        self._foglalasok.append(uj_foglalas)

        return jarat.get_jegyar()

    def lemondas(self, foglalas_id):
        foglalas = next((f for f in self._foglalasok if f.get_id() == foglalas_id), None)

        if not foglalas:
            raise Exception("Nem létező foglalás!")

        self._foglalasok.remove(foglalas)

    def list_foglalasok(self):
        if not self._foglalasok:
            print("Nincsenek foglalások.")
        for f in self._foglalasok:
            print(f)



def inicializalas():
    lt = LegiTarsasag("DemoAir")

    j1 = BelfoldiJarat("B101", "Debrecen", 15000)
    j2 = NemzetkoziJarat("N202", "London", 55000)
    j3 = NemzetkoziJarat("N303", "Párizs", 50000)

    lt.add_jarat(j1)
    lt.add_jarat(j2)
    lt.add_jarat(j3)

    # 6 előre foglalás (jövőbeli dátumokkal)
    for i in range(6):
        lt.foglalas(j1.get_jaratszam(), datetime.now().replace(day=datetime.now().day + 1))

    return lt


def menu():
    lt = inicializalas()

    while True:
        print("\n--- Repülőjegy rendszer ---")
        print("1 - Jegy foglalása")
        print("2 - Foglalás lemondása")
        print("3 - Foglalások listázása")
        print("4 - Kilépés")

        valasz = input("Választás: ")

        try:
            if valasz == "1":
                lt.list_jaratok()
                jaratszam = input("Járatszám: ")
                datum_str = input("Dátum (YYYY-MM-DD): ")
                datum = datetime.strptime(datum_str, "%Y-%m-%d")

                ar = lt.foglalas(jaratszam, datum)
                print(f"Sikeres foglalás! Ár: {ar} Ft")

            elif valasz == "2":
                foglalas_id = int(input("Foglalás ID: "))
                lt.lemondas(foglalas_id)
                print("Foglalás törölve.")

            elif valasz == "3":
                lt.list_foglalasok()

            elif valasz == "4":
                print("Kilépés...")
                break

            else:
                print("Érvénytelen opció!")

        except Exception as e:
            print(f"Hiba: {e}")


if __name__ == "__main__":
    menu()
