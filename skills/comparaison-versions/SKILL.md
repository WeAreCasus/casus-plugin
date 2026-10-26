---
name: comparaison-versions
description: Dire précisément ce qui a changé dans un article de code (CGI, LPF, Code de commerce, Code civil, CSS…) entre deux dates avec le connecteur Casus - texte de chaque version, ajouts, suppressions, chiffres modifiés, texte modificatif, date d'application et effets pratiques. À utiliser dès que l'utilisateur demande ce qui a changé, ce que la loi de finances a modifié, l'ancienne et la nouvelle rédaction, l'évolution d'un article, ou s'il compare un régime « avant » et « après » une réforme, même sans parler de versions.
---

# Comparaison de versions d'un article

But : montrer au professionnel, ligne par ligne, ce qui a changé dans un article entre deux dates, par quel texte et à partir de quand, puis ce que cela change pour lui. Tout ce qui est affirmé vient du texte des deux versions lues dans le corpus, jamais de la mémoire.

## Socle

1. **Date.** Pour des faits datés, passez `date` (fait générateur, date de l'acte ou de l'acte de procédure) à `get_code_article` et `resolve_references`. Sans date, l'outil répond pour aujourd'hui.
2. **Lire avant d'affirmer.** Un extrait de `search` ne suffit pas pour citer. Une décision citée a été lue elle-même. Toute condition, tout taux, seuil, délai ou numéro affirmé vient d'un texte lu pendant la recherche ; sinon il est présenté comme non vérifié. Aucune dérogation ni exception sans une source lue qui la prévoit.
3. **Citer exactement.** Les passages déterminants sont reproduits mot pour mot dans un bloc `>`, copiés de la sortie de l'outil. Les liens sont ceux que renvoient les outils, jamais construits ni complétés (pas de date ajoutée à un lien Légifrance).
4. **Dire les limites.** « Absent du corpus Casus » ne veut pas dire inexistant. Une version INDÉTERMINÉE ne se décrit pas de mémoire : donnez le lien Légifrance daté. Une date déduite se présente comme une déduction.
5. **Économiser les appels.** Lancez dans le même tour les appels indépendants. Groupez jusqu'à dix articles par `get_code_article` et toutes les références dans un seul `resolve_references`. Ne relisez pas un document déjà lu. En cas de limite de débit, attendez le délai indiqué. Le budget du parcours est un plafond : dès que la conclusion est sourcée, arrêtez de chercher et signalez en une ligne ce qui resterait à approfondir.
6. **Calculer sans erreur.** Montrez chaque calcul de date ou de durée pas à pas, jour de la semaine compris.
7. **Contrôler avant d'envoyer** (dernière section).

## Parcours et budget

Une comparaison se fait en 5 à 12 appels : les versions en mode complet (un appel par date, toutes lancées dans le même tour, plus une par version intermédiaire), la recherche du texte modificatif et de sa date d'application (actualités BOFIP, blogs), le BOFIP qui commente l'article, puis le contrôle. Les lois de finances récentes et leurs dates sont dans `references/application-dans-le-temps.md` : ouvrez-le pour rattacher une date de version à une loi.

## Étape 1 : cadrer la comparaison

- **L'article** : code et numéro. Si l'utilisateur ne donne que le régime (« le crédit d'impôt recherche »), identifiez l'article avec `search(query=…, sources=["codes"])` ou `get_code_plan`, puis confirmez avec `get_code_article`.
- **Les deux dates** :
  - deux dates données : comparez-les ;
  - une seule date : comparez-la à aujourd'hui ;
  - « avant et après la loi X » : la date d'entrée en vigueur de la modification se lit dans la frise des versions (étape 2) ; prenez la veille et le jour même ;
  - « ce qui a changé récemment » : comparez la version en vigueur à la précédente dans la frise.

## Étape 2 : lire les deux versions

Appelez `get_code_article(code=…, numeros=[…], date=…, detail="complet")` pour chaque date. Le mode complet donne le texte entier de la version applicable et la section **Versions dans la base** :

```
### Versions dans la base
- du 21/02/2026 (sans fin) — LEGIARTI000053542636 — état VIGUEUR
- du 16/02/2025 au 21/02/2026 — LEGIARTI000051212954 — état MODIFIE ← version affichée
- du 01/01/2024 au 16/02/2025 — LEGIARTI000048805432 — état MODIFIE
```

(extrait de la frise de l'article 197 du CGI lu au 30/06/2025)

Interprétez :

- **Même identifiant aux deux dates** : aucune modification dans les versions du corpus entre ces dates. Dites-le, en rappelant que l'historique du corpus est partiel.
- **Identifiants différents** : comparez. S'il y a des versions intermédiaires dans la frise, lisez-les aussi (une date à l'intérieur de chaque période) et présentez les changements dans l'ordre.
- **INDÉTERMINÉ à une date** (date antérieure à la plus ancienne version de la base) : la comparaison n'est pas possible à partir du corpus. Donnez le lien Légifrance daté renvoyé par l'outil et proposez de comparer à partir de la plus ancienne version disponible, en le disant.
- **« la version suivante n'est pas encore dans le corpus »** : une modification est programmée mais son texte manque. Signalez-la, sans en décrire le contenu.
- **Version dont la fin précède le début** (état MODIFIE_MORT_NE) : elle n'a jamais été appliquée ; ne la comparez pas.

## Étape 3 : comparer le texte

Comparez par subdivision (I, II, 1°, a., alinéas) et relevez :

- les ajouts, suppressions et reformulations ;
- tout chiffre modifié : taux, seuil, montant, durée, délai, pourcentage ;
- les conditions ajoutées ou supprimées, le champ d'application, les exclusions ;
- les renvois modifiés vers d'autres articles.

Une modification d'un seul chiffre au milieu d'un long article se manque facilement. Si l'exécution de code est disponible, enregistrez les deux textes en les recopiant intégralement depuis la sortie de l'outil (le script ne compare que ce que vous avez enregistré) et lancez `python scripts/comparer_versions.py ancienne.txt nouvelle.txt` (bibliothèque standard seulement) : il liste chaque modification avec son contexte et les chiffres qui apparaissent ou disparaissent. Sinon, comparez subdivision par subdivision en recopiant les deux rédactions côte à côte.

Pour affirmer que le reste de l'article est inchangé, il faut avoir comparé tout le texte (script, ou chaque subdivision) : une longueur égale ne le prouve pas.

Les citations reprennent mot pour mot le texte renvoyé par l'outil.

## Étape 4 : identifier le texte modificatif et sa date d'application

La frise donne les dates, pas la loi. Pour l'identifier :

- regardez la section **Cité par** de l'**ancienne** version (mode complet avec une date à l'intérieur de sa période) : la loi qui l'a modifiée y figure souvent (« LOI n° … du … - art. … »), alors que le « Cité par » de la version en vigueur ne liste en général que des articles de codes. Une loi datée juste avant la nouvelle version oriente vers le texte en cause ; présentez-la comme probable tant qu'aucune autre source ne le confirme ;
- `list_bofip(serie=…, nature="Actualité", depuis=…)` autour de la date de la nouvelle version ;
- `search(query="modification de l'article … du … par la loi de finances … : nouvelles conditions et date d'application", sources=["bofip", "blogs"])` ;
- une fois le numéro connu, `search_text(query="\"…numéro de la loi…\"", source="bofip")` puis `source="blogs"` : un document BOFIP de fond cite souvent la loi et son article (dans une remarque ou un paragraphe mis à jour) même sans actualité dédiée. N'écrivez pas qu'aucune source ne confirme le texte modificatif, ni que le BOFIP ne commente pas la modification, sans avoir lancé ces deux recherches.

La date à laquelle la nouvelle rédaction s'applique aux opérations (« transmissions réalisées à compter du … ») peut différer de la date de début de version dans la frise : cherchez-la dans les mêmes sources. Ne donnez jamais un numéro de loi, un article de loi ou une date d'application qui ne sort pas d'une source lue ; s'ils restent inconnus, dites-le. Une actualité BOFIP trouvée par `search` peut ne pas se lire par `get_bofip` ou `fetch` : citez alors l'extrait de `search` avec son lien, en le disant.

Quand la date d'application reste inconnue et que la situation du client chevauche le changement, ne choisissez pas une version : présentez les deux hypothèses, ou une conduite qui respecte les deux rédactions à la fois.

## Étape 5 : mesurer les effets

- **Doctrine** : la date de la version BOFIP qui commente l'article (en-tête de `get_bofip`) est-elle antérieure à la modification ? Alors le BOFIP décrit peut-être l'ancienne rédaction : signalez-le.
- **Jurisprudence** : une décision rendue sur l'ancienne rédaction ne vaut plus pour la partie modifiée.
- **Situations en cours** : engagements, délais, opérations commencées avant le changement. Dites quelle version leur est applicable si une source le précise ; sinon, posez la question comme un point à vérifier.
- **Articles liés** : un article qui renvoie à celui-ci, ou auquel il renvoie (section « Cite » et « Cité par » du mode complet), a-t-il changé à la même date ? Une modification arrive souvent en bloc.
- **Conduite à tenir** : pour un client concerné, dites ce qu'il doit faire différemment (déclaration, délai, condition nouvelle), avec la date à partir de laquelle cela compte.

## Étape 6 : rendre le résultat

1. **Synthèse** (deux ou trois lignes) : ce qui a changé, à quelle date, par quel texte.
2. **Tableau des changements** :

   | Point | Rédaction au JJ/MM/AAAA | Rédaction au JJ/MM/AAAA | Portée |
   |---|---|---|---|
   | [subdivision] : [objet] | « [ancienne rédaction] » | « [nouvelle rédaction] » | [ce que cela change pour le client] |

3. **Extraits exacts** : pour chaque changement important, l'ancienne et la nouvelle rédaction dans deux blocs `>`.
4. **Versions intermédiaires**, s'il y en a.
5. **Texte modificatif et date d'application**, avec leur source.
6. **Effets pratiques** : doctrine, jurisprudence, situations en cours.
7. **Limites** : historique partiel, version suivante absente, date d'application non trouvée.

Chaque version est citée avec sa période de validité et son lien Légifrance, tel que renvoyé par l'outil.

## Contrôle avant envoi

1. Passez le brouillon entier à `resolve_references(texte=…)` : chaque article cité existe, et sa version est celle que vous datez.
2. Chaque « rien d'autre n'a changé » repose sur une comparaison complète (script ou subdivision par subdivision), jamais sur une longueur égale.
3. Chaque rédaction citée en bloc `>` est une copie de la sortie de l'outil, pour la bonne version.
4. Le texte modificatif et sa date d'application sortent d'une source lue, ou sont présentés comme probables ou inconnus.
5. Le tableau des changements et la synthèse disent la même chose.

## Fichiers du skill

- `scripts/comparer_versions.py` : comparaison mot à mot de deux textes, avec les chiffres qui apparaissent ou disparaissent.
- `references/application-dans-le-temps.md` : lois de finances récentes et leurs dates, où lire la date d'application d'une modification.
