#!/usr/bin/env python3
"""Compare deux versions d'un texte juridique, mot par mot.

Usage :
    python comparer_versions.py ancienne.txt nouvelle.txt [--contexte 12]

Sortie (Markdown, sur la sortie standard) :
    - le nombre de modifications ;
    - chaque modification avec son contexte, l'ancien texte entre [- -] et le
      nouveau entre {+ +} ;
    - les nombres, pourcentages et durées qui apparaissent ou disparaissent.

Bibliothèque standard uniquement. Le texte est comparé après normalisation des
espaces : un simple retour à la ligne n'est pas une modification.
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from collections import Counter
from pathlib import Path

# Un mot (lettres, chiffres, apostrophes et traits d'union internes) ou un signe.
_TOKEN = re.compile(r"\w+(?:[’'\-]\w+)*|[^\w\s]", re.UNICODE)

# Nombres, pourcentages, montants et durées : en chiffres (au moins deux chiffres,
# ou un chiffre suivi d'une unité) ou en lettres suivis d'une unité.
_UNITE = r"(?:%|€|euros?|ans?|années?|mois|jours?|pour\s+cent)"
_LETTRES = (
    r"(?:deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|quinze|vingt|"
    r"trente|quarante|cinquante|soixante|cent)"
)
_FIGURE = re.compile(
    rf"\d[\d\s.,]*\d(?:\s?{_UNITE})?|\d\s?{_UNITE}|\b{_LETTRES}(?:[\s-]{_LETTRES})*\s+{_UNITE}",
    re.IGNORECASE,
)


def tokens(text: str) -> list[str]:
    return _TOKEN.findall(" ".join(text.split()))


def join(words: list[str]) -> str:
    out = ""
    for word in words:
        if out and not re.fullmatch(r"[,.;:)\]’'»]", word) and not out.endswith(("(", "[", "’", "'", "«")):
            out += " "
        out += word
    return out


def figures(text: str) -> Counter[str]:
    return Counter(m.group(0).strip(" .,") for m in _FIGURE.finditer(" ".join(text.split())))


def compare(old: str, new: str, context: int) -> str:
    a, b = tokens(old), tokens(new)
    matcher = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    changes = [op for op in matcher.get_opcodes() if op[0] != "equal"]

    lines = [f"# Comparaison : {len(changes)} modification(s)", ""]
    if not changes:
        lines.append("Les deux textes sont identiques après normalisation des espaces.")
        return "\n".join(lines)

    for n, (tag, i1, i2, j1, j2) in enumerate(changes, start=1):
        before = join(a[max(0, i1 - context) : i1])
        after = join(a[i2 : i2 + context])
        removed, added = join(a[i1:i2]), join(b[j1:j2])
        kind = {"replace": "remplacé", "delete": "supprimé", "insert": "ajouté"}[tag]
        diff = (f"[-{removed}-]" if removed else "") + (f" {{+{added}+}}" if added else "")
        lines.append(f"{n}. ({kind}) … {before} {diff.strip()} {after} …")

    old_fig, new_fig = figures(old), figures(new)
    gone = old_fig - new_fig
    came = new_fig - old_fig
    lines += ["", "## Chiffres et durées"]
    if not gone and not came:
        lines.append("Aucun nombre, pourcentage ou durée n'apparaît ni ne disparaît.")
    else:
        if gone:
            lines.append("Disparaissent : " + " ; ".join(f"{k} (×{v})" for k, v in sorted(gone.items())))
        if came:
            lines.append("Apparaissent : " + " ; ".join(f"{k} (×{v})" for k, v in sorted(came.items())))
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("ancienne", type=Path)
    parser.add_argument("nouvelle", type=Path)
    parser.add_argument("--contexte", type=int, default=12, help="mots de contexte de chaque côté")
    args = parser.parse_args()
    old = args.ancienne.read_text(encoding="utf-8")
    new = args.nouvelle.read_text(encoding="utf-8")
    sys.stdout.write(compare(old, new, args.contexte) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
