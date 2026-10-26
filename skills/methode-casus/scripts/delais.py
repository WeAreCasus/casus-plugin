#!/usr/bin/env python3
"""Calculs de dates et de délais en procédure fiscale française.

Bibliothèque standard uniquement. Chaque commande affiche le calcul pas à pas,
pour qu'il puisse être recopié dans la réponse.

Commandes :
  jour DATE                         jour de la semaine (ex. « mercredi 1er avril 2026 »)
  feries ANNEE                      jours fériés légaux de l'année
  delai-franc DATE JOURS            délai franc à compter de DATE (réception) :
                                    ni le jour de départ ni le jour d'échéance ne
                                    comptent ; report au premier jour ouvrable si
                                    l'échéance tombe un samedi, un dimanche ou un
                                    jour férié
  jours-ouvres DATE1 DATE2          jours ouvrés strictement entre DATE1 et DATE2
                                    (ni l'un ni l'autre compté ; samedis, dimanches
                                    et jours fériés exclus)
  mois DATE N                       date de même quantième N mois plus tard (fin de
                                    mois si le quantième n'existe pas) et veille
  reprise ANNEE [N]                 fin du délai de reprise : 31 décembre de la
                                    N-ième année suivant ANNEE (N = 3 par défaut)
  interet MONTANT DEBUT FIN [TAUX]  intérêt de retard : nombre de mois de DEBUT
                                    (premier jour du mois de départ) à FIN (dernier
                                    mois inclus), au TAUX mensuel en % ; le taux
                                    dépend de la période de décompte (0,40 % jusqu'au
                                    31/12/2017, 0,20 % ensuite, BOI-DAE-20-10 § 90) :
                                    une commande par tranche

Options : --alsace-moselle ajoute le 26 décembre et le vendredi saint ; ce dernier
n'est férié que dans les communes ayant un temple protestant ou une église mixte
(C. trav., art. L. 3134-13).
Les dates s'écrivent JJ/MM/AAAA ou AAAA-MM-JJ.

Ces calculs appliquent des règles qu'il faut confirmer dans les sources (par
exemple BOI-CF-IOR-10-50-10, § 192, pour le délai franc de réponse à une
proposition de rectification). Le script calcule ; il ne dit pas le droit.
"""

from __future__ import annotations

import sys
from datetime import date, timedelta

JOURS = ("lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche")
MOIS = (
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
)


def lire(texte: str) -> date:
    texte = texte.strip()
    if "/" in texte:
        j, m, a = (int(x) for x in texte.split("/"))
        return date(a, m, j)
    a, m, j = (int(x) for x in texte.split("-"))
    return date(a, m, j)


def ecrire(d: date) -> str:
    jour = "1er" if d.day == 1 else str(d.day)
    return f"{JOURS[d.weekday()]} {jour} {MOIS[d.month - 1]} {d.year}"


def paques(annee: int) -> date:
    """Dimanche de Pâques (calendrier grégorien, algorithme de Meeus)."""
    a, b, c = annee % 19, annee // 100, annee % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mois = (h + l - 7 * m + 114) // 31
    jour = (h + l - 7 * m + 114) % 31 + 1
    return date(annee, mois, jour)


def feries(annee: int, alsace_moselle: bool = False) -> dict[date, str]:
    p = paques(annee)
    jours = {
        date(annee, 1, 1): "jour de l'an",
        p + timedelta(days=1): "lundi de Pâques",
        date(annee, 5, 1): "fête du travail",
        date(annee, 5, 8): "victoire 1945",
        p + timedelta(days=39): "Ascension",
        p + timedelta(days=50): "lundi de Pentecôte",
        date(annee, 7, 14): "fête nationale",
        date(annee, 8, 15): "Assomption",
        date(annee, 11, 1): "Toussaint",
        date(annee, 11, 11): "armistice 1918",
        date(annee, 12, 25): "Noël",
    }
    if alsace_moselle:
        jours[p - timedelta(days=2)] = "vendredi saint (Alsace-Moselle)"
        jours[date(annee, 12, 26)] = "saint Étienne (Alsace-Moselle)"
    return dict(sorted(jours.items()))


def ouvrable(d: date, am: bool) -> bool:
    return d.weekday() < 5 and d not in feries(d.year, am)


def raison_non_ouvrable(d: date, am: bool) -> str:
    if d.weekday() >= 5:
        return JOURS[d.weekday()]
    return feries(d.year, am).get(d, "")


def delai_franc(depart: date, jours: int, am: bool = False) -> list[str]:
    echeance = depart + timedelta(days=jours + 1)
    lignes = [
        f"Point de départ (non compté) : {ecrire(depart)}",
        f"Premier jour compté : {ecrire(depart + timedelta(days=1))}",
        f"{jours}e jour : {ecrire(depart + timedelta(days=jours))}",
        f"Jour d'échéance (délai franc, non compté) : {ecrire(echeance)}",
    ]
    d = echeance
    while not ouvrable(d, am):
        lignes.append(f"  {ecrire(d)} n'est pas ouvrable ({raison_non_ouvrable(d, am)}) : report au lendemain")
        d += timedelta(days=1)
    lignes.append(f"Dernier jour pour agir : {ecrire(d)}")
    return lignes


def jours_ouvres(d1: date, d2: date, am: bool = False) -> list[str]:
    if d2 < d1:
        d1, d2 = d2, d1
    lignes = [f"Entre {ecrire(d1)} et {ecrire(d2)} (bornes exclues) :"]
    n = 0
    d = d1 + timedelta(days=1)
    while d < d2:
        if ouvrable(d, am):
            n += 1
            lignes.append(f"  {ecrire(d)} : ouvré")
        else:
            lignes.append(f"  {ecrire(d)} : non ouvré ({raison_non_ouvrable(d, am)})")
        d += timedelta(days=1)
    lignes.append(f"Jours ouvrés : {n}")
    return lignes


def ajouter_mois(d: date, n: int) -> date:
    m = d.month - 1 + n
    a, m = d.year + m // 12, m % 12 + 1
    for jour in range(d.day, 27, -1):
        try:
            return date(a, m, jour)
        except ValueError:
            continue
    return date(a, m, min(d.day, 28))


def mois(d: date, n: int) -> list[str]:
    cible = ajouter_mois(d, n)
    return [
        f"Départ : {ecrire(d)}",
        f"Même quantième {n} mois plus tard : {ecrire(cible)}",
        f"Veille (dernier jour d'une période de {n} mois commencée le jour du départ) : {ecrire(cible - timedelta(days=1))}",
    ]


def reprise(annee: int, n: int = 3) -> list[str]:
    return [f"Impôt dû au titre de {annee} : délai de reprise jusqu'au {ecrire(date(annee + n, 12, 31))} (fin de la {n}e année suivante)"]


def euros(v: float) -> str:
    return f"{v:,.2f}".replace(",", " ").replace(".", ",")


def interet(montant: float, debut: date, fin: date, taux: float) -> list[str]:
    nb = (fin.year - debut.year) * 12 + fin.month - debut.month + 1
    total = round(montant * taux / 100 * nb, 2)
    return [
        f"Premier mois compté : {MOIS[debut.month - 1]} {debut.year}",
        f"Dernier mois compté : {MOIS[fin.month - 1]} {fin.year}",
        f"Nombre de mois : {nb}",
        f"Taux mensuel : {str(taux).replace('.', ',')} % (taux de la période de décompte, à confirmer : BOI-DAE-20-10 § 90)",
        f"Intérêt de retard : {euros(montant)} € × {str(taux).replace('.', ',')} % × {nb} = {euros(total)} €",
    ]


def main(argv: list[str]) -> int:
    am = "--alsace-moselle" in argv
    args = [a for a in argv if a != "--alsace-moselle"]
    if not args:
        print(__doc__)
        return 1
    cmd, rest = args[0], args[1:]
    if cmd == "jour":
        out = [ecrire(lire(rest[0]))]
    elif cmd == "feries":
        out = [f"{ecrire(d)} : {nom}" for d, nom in feries(int(rest[0]), am).items()]
    elif cmd == "delai-franc":
        out = delai_franc(lire(rest[0]), int(rest[1]), am)
    elif cmd == "jours-ouvres":
        out = jours_ouvres(lire(rest[0]), lire(rest[1]), am)
    elif cmd == "mois":
        out = mois(lire(rest[0]), int(rest[1]))
    elif cmd == "reprise":
        out = reprise(int(rest[0]), int(rest[1]) if len(rest) > 1 else 3)
    elif cmd == "interet":
        taux = float(rest[3].replace(",", ".")) if len(rest) > 3 else 0.20
        out = interet(float(rest[0].replace(",", ".")), lire(rest[1]), lire(rest[2]), taux)
    else:
        print(__doc__)
        return 1
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
