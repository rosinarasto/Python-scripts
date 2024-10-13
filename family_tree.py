from typing import Dict, List, Set, Tuple


class Person:
    def __init__(self, name: str, birth_year: int):
        self.name = name
        self.birth_year = birth_year
        self.children: List[Person] = []

    def is_valid_rec(self, seen: Set[str]) -> bool:

        for child in self.children:
            if self.birth_year >= child.birth_year or child.name == '' or\
               child.name in seen or not child.is_valid_rec(set()):
                return False

            seen.add(child.name)

        return True

    def is_valid(self) -> bool:
        if self.name == '':
            return False

        return self.is_valid_rec(set())

    def name_birth_year(self, start: str, edge: str) -> None:
        print(start + edge + self.name + ' (' + str(self.birth_year) + ')')

    def draw_rec(self, start: str) -> None:

        for index, child in enumerate(self.children):
            if index == len(self.children) - 1:
                edge, next_line = '└─ ', '   '
            else:
                edge, next_line = '├─ ', '│  '

            child.name_birth_year(start, edge)

            if len(child.children) > 0:
                child.draw_rec(start + next_line)

    def draw(self) -> None:
        self.name_birth_year('', '')
        self.draw_rec('')

    Order = Tuple[Dict['Person', int], int]

    def order_succ_rec(self, result: Dict['Person', int], order: int, alive: Set['Person']) -> Order:
        succ = sorted([(children.birth_year, index, children) for index, children in enumerate(self.children)])

        for _, _, children in succ:

            if children in alive:
                result[children] = order
                order += 1
            result, order = children.order_succ_rec(result, order, alive)

        return result, order

    def order_of_succession(self, alive: Set['Person']) \
            -> Dict['Person', int]:
        result, _ = self.order_succ_rec({}, 1, alive)
        return result

    def remove_rec(self, alive: Set['Person']) -> bool:
        self.children = [child for child in self.children if child.remove_rec(alive) or child in alive]

        return len(self.children) > 0

    def remove_extinct_branches(self, alive: Set['Person']) -> None:
        self.remove_rec(alive)


def main() -> None:
    adam = Person("Adam", 1)
    assert adam.name == "Adam"
    assert adam.birth_year == 1
    assert adam.children == []

    assert adam.is_valid()
    assert adam.order_of_succession({adam}) == {}
    assert adam.order_of_succession(set()) == {}

    qempa = Person("Qempa'", 2256)
    thok_mak = Person("Thok Mak", 2281)
    worf1 = Person("Worf", 2290)
    ag_ax = Person("Ag'ax", 2317)
    k_alaga = Person("K'alaga", 2302)
    samtoq = Person("Samtoq", 2317)
    mogh = Person("Mogh", 2310)
    worf2 = Person("Worf", 2340)
    kurn = Person("Kurn", 2345)
    k_dhan = Person("K'Dhan", 2388)
    alex = Person("Alexander Rozhenko", 2366)
    d_vak = Person("D'Vak", 2390)
    grehka = Person("Grehka", 2359)
    elumen = Person("Elumen", 2357)
    ga_ga = Person("Ga'ga", 2366)

    qempa.children = [thok_mak, worf1]
    thok_mak.children = [ag_ax, k_alaga, samtoq]
    worf1.children = [mogh]
    mogh.children = [worf2, kurn]
    worf2.children = [k_dhan, alex]
    alex.children = [d_vak]
    kurn.children = [grehka, elumen, ga_ga]

    assert qempa.is_valid()
    assert alex.is_valid()

    thok_mak.name = ""
    assert not qempa.is_valid()
    assert alex.is_valid()
    thok_mak.name = "Thok Mak"

    thok_mak.birth_year = 2302
    assert not qempa.is_valid()
    assert alex.is_valid()
    thok_mak.birth_year = 2281

    alive = {qempa, thok_mak, worf1, ag_ax, k_alaga, samtoq, mogh,
             worf2, kurn, k_dhan, alex, d_vak, grehka, elumen, ga_ga}
    succession = {
        ga_ga: 14,
        elumen: 12,
        thok_mak: 1,
        d_vak: 9,
        worf1: 5,
        worf2: 7,
        grehka: 13,
        mogh: 6,
        k_alaga: 2,
        kurn: 11,
        ag_ax: 3,
        samtoq: 4,
        k_dhan: 10,
        alex: 8,
    }

    assert qempa.order_of_succession(alive) == succession
    alive.remove(qempa)
    assert qempa.order_of_succession(alive) == succession

    alive.difference_update({thok_mak, worf1, mogh, kurn})
    assert qempa.order_of_succession(alive) == {
        k_alaga: 1,
        ag_ax: 2,
        samtoq: 3,
        worf2: 4,
        alex: 5,
        d_vak: 6,
        k_dhan: 7,
        elumen: 8,
        grehka: 9,
        ga_ga: 10,
    }

    assert mogh.order_of_succession(alive) == {
        worf2: 1,
        alex: 2,
        d_vak: 3,
        k_dhan: 4,
        elumen: 5,
        grehka: 6,
        ga_ga: 7,
    }

    print("Check the output of draw yourself:\n")
    qempa.draw()

    alive = {ga_ga, elumen, d_vak, worf2, k_dhan, alex}

    print("\nAfter calling remove_extinct_branches:\n")
    qempa.remove_extinct_branches(alive)
    assert len(thok_mak.children) == 0
    assert len(ag_ax.children) == 0
    assert len(samtoq.children) == 0
    assert len(k_alaga.children) == 0
    assert len(kurn.children) == 2
    assert len(grehka.children) == 0
    qempa.draw()


if __name__ == '__main__':
    main()
