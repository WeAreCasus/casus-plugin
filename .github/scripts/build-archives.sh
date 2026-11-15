#!/usr/bin/env bash
# Construit les archives des skills dans le dossier donné (dist par défaut) :
# une archive <nom>.zip par dossier de skills/ (le dossier de la skill à la racine),
# casus-skills.zip (toutes les skills) et casus-skills-starter.zip (sans la skill
# réservée aux offres Pro, essai et organisation).
set -euo pipefail

PRO_ONLY="reponse-proposition-rectification"
root="$(cd "$(dirname "$0")/../.." && pwd)"
out="$(mkdir -p "${1:-dist}" && cd "${1:-dist}" && pwd)"
rm -f "$out"/*.zip

cd "$root/skills"
for skill in */; do
  skill="${skill%/}"
  test -f "$skill/SKILL.md" || { echo "skills/$skill n'a pas de SKILL.md" >&2; exit 1; }
  zip -qrX "$out/$skill.zip" "$skill"
done
test -d "$PRO_ONLY" || { echo "skills/$PRO_ONLY est introuvable" >&2; exit 1; }
zip -qrX "$out/casus-skills.zip" .
zip -qrX "$out/casus-skills-starter.zip" . -x "$PRO_ONLY/*"

# Contrôle : chaque archive contient au moins un SKILL.md, l'archive Starter ne contient pas la skill Pro.
for archive in "$out"/*.zip; do
  unzip -Z1 "$archive" '*/SKILL.md' > /dev/null || { echo "$archive ne contient aucun SKILL.md" >&2; exit 1; }
done
if unzip -Z1 "$out/casus-skills-starter.zip" "$PRO_ONLY/*" > /dev/null 2>&1; then
  echo "casus-skills-starter.zip contient $PRO_ONLY" >&2; exit 1
fi
ls -1 "$out"
