---
name: recherche-a-date
description: Déterminer le régime juridique ou fiscal applicable à la date des faits avec le connecteur Casus - lire les articles de codes dans leur version en vigueur à cette date, puis la doctrine BOFIP et la jurisprudence en tenant compte de leur propre date. À utiliser dès qu'une question porte sur des faits passés ou une période (« en 2019 », « lors de la cession de 2021 », « pour l'exercice clos en 2022 », « au jour du décès », contrôle fiscal sur des années anciennes, rappel d'impôt, contentieux), ou sur une opération à cheval sur une réforme, même si l'utilisateur ne précise pas qu'il faut une version datée.
---

# Recherche à date

Le droit fiscal change à chaque loi de finances. Appliquer à une cession de 2021 l'article tel qu'il est rédigé aujourd'hui est l'erreur la plus fréquente et la plus coûteuse. Cette méthode lit chaque source dans l'état où elle était à la date des faits, et dit clairement ce qui n'a pas pu être lu à cette date.

## Socle

1. **Date.** Pour des faits datés, passez `date` (fait générateur, date de l'acte ou de l'acte de procédure) à `get_code_article` et `resolve_references`. Sans date, l'outil répond pour aujourd'hui.
2. **Lire avant d'affirmer.** Un extrait de `search` ne suffit pas pour citer. Une décision citée a été lue elle-même. Toute condition, tout taux, seuil, délai ou numéro affirmé vient d'un texte lu pendant la recherche ; sinon il est présenté comme non vérifié. Aucune dérogation ni exception sans une source lue qui la prévoit.
3. **Citer exactement.** Les passages déterminants sont reproduits mot pour mot dans un bloc `>`, copiés de la sortie de l'outil. Les liens sont ceux que renvoient les outils, jamais construits ni complétés (pas de date ajoutée à un lien Légifrance).
4. **Dire les limites.** « Absent du corpus Casus » ne veut pas dire inexistant. Une version INDÉTERMINÉE ne se décrit pas de mémoire : donnez le lien Légifrance daté. Une date déduite se présente comme une déduction.
5. **Économiser les appels.** Lancez dans le même tour les appels indépendants. Groupez jusqu'à dix articles par `get_code_article` et toutes les références dans un seul `resolve_references`. Ne relisez pas un document déjà lu. En cas de limite de débit, attendez le délai indiqué. Le budget du parcours est un plafond : dès que la conclusion est sourcée, arrêtez de chercher et signalez en une ligne ce qui resterait à approfondir.
6. **Calculer sans erreur.** Jours de la semaine, délais, durées et intérêts se calculent avec `scripts/delais.py` quand l'exécution de code est disponible ; sinon, montrez le calcul pas à pas.
7. **Contrôler avant d'envoyer** (dernière section).

## Parcours et budget

Une question datée ordinaire se traite en 8 à 15 appels : un `get_code_article` groupé à la date (mode complet), la doctrine (BOFIP du domaine, dont la date est comparée aux faits), la recherche des règles d'application dans le temps, une ou deux recherches en jurisprudence, puis le contrôle avant envoi. Les articles et séries BOFIP de chaque domaine sont dans `references/carte-des-sources.md` ; les lois de finances, leurs dates et la doctrine sur l'application de la loi dans le temps sont dans `references/application-dans-le-temps.md`. Ouvrez-les avant de chercher.

## Étape 1 : fixer la ou les dates utiles

La date à interroger est celle qui déclenche la règle, pas la date de la question. Repérez :

- **le fait générateur** de l'impôt en cause. La doctrine sur l'application de la loi fiscale dans le temps (BOI-CTX-DG-20-10-20) donne les règles générales : lisez-la quand la date applicable est discutée. Repères courants, à confirmer sur le texte :
  - impôt sur le revenu : revenus réalisés ou dont le contribuable a disposé au cours de l'année N (CGI, art. 12) ; législation applicable : celle en vigueur à la fin de l'année N, sauf disposition contraire (BOI-CTX-DG-20-10-20, § 230) ; situation et charges de famille au 1er janvier de N, ou au 31 décembre de N l'année d'un événement mentionné aux 4 à 6 de l'article 6 du CGI ou d'une augmentation des charges de famille (CGI, art. 196 bis) ;
  - barème de l'impôt sur le revenu : celui appliqué aux revenus de N est fixé par la loi de finances pour N+1 (BOI-CTX-DG-20-10-20, § 250). Lu à la date du 31/12/N, l'article 197 du CGI donne donc le barème de l'année précédente : lisez-le à une date postérieure à l'entrée en vigueur de la loi de finances pour N+1, et vérifiez à quels revenus elle s'applique ;
  - impôt sur les sociétés : législation en vigueur au jour de la clôture de l'exercice (BOI-CTX-DG-20-10-20, § 240) ;
  - plus-value immobilière : date de la cession, soit la date portée dans l'acte authentique, à défaut la date à laquelle le contrat est régulièrement formé ; une promesse synallagmatique vaut cession à sa signature ; sous condition suspensive, date de réalisation de la condition (BOI-RFPI-PVI-30-10, § 10 à 50). Autres plus-values : lisez la règle propre au régime ;
  - droits de mutation à titre gratuit : date du décès ou de l'acte de donation ; pour un don manuel, tarif et abattements en vigueur au jour de sa déclaration, de son enregistrement ou de sa révélation (CGI, art. 757) ;
  - droits d'enregistrement : date de l'acte ou de la mutation pour les actes soumis obligatoirement à l'enregistrement et les mutations à déclarer dans un délai ; pour les autres actes, date de leur présentation à la formalité (BOI-CTX-DG-20-10-20, § 90) ;
  - IFI : situation au 1er janvier de l'année d'imposition ;
  - TVA : fait générateur et exigibilité (livraison, encaissement, débit selon l'opération) ;
  - pénalités : loi en vigueur à la date du manquement ; une loi nouvelle plus douce s'applique toutefois aux manquements antérieurs qui n'ont pas fait l'objet d'une sanction définitive, et une sanction créée ou aggravée ne vaut que pour les manquements postérieurs (BOI-CTX-DG-20-10-20, § 120 et 130) ;
- **la date des actes de procédure** quand la question porte sur un contrôle ou un contentieux (avis de vérification, proposition de rectification, mise en recouvrement, réclamation) : les règles de procédure se lisent à la date de chaque acte ;
- **les périodes** quand les faits s'étalent (durée de détention, engagement de conservation, plusieurs exercices) : lisez le texte au début, à la fin et à chaque changement repéré.

Si une date manque et change la réponse, posez la question ; sinon retenez l'hypothèse la plus probable et dites-la.

## Étape 2 : lire les textes à la date

Lisez chaque article utile avec `get_code_article(code=…, numeros=[…], date="JJ/MM/AAAA", detail="complet")`. Le mode complet donne la frise des versions présentes dans la base : elle montre si le texte a changé autour de la date des faits. Groupez jusqu'à dix articles du même code par appel, et lisez à la même date les articles auxquels le texte renvoie.

Lisez la ligne d'état de chaque article :

| Ce que dit l'outil | Ce que cela veut dire | Ce que vous écrivez |
|---|---|---|
| « État au … : applicable depuis le X » (sans fin, ou fin postérieure aux faits) | La version lue est celle des faits. | Citez-la avec sa période de validité. |
| « … jusqu'au Y (abrogation ou modification programmée ; la version suivante n'est pas encore dans le corpus) » | Le texte change à la date Y. | Si les faits sont après Y : indéterminé. Si les effets se prolongent après Y : signalez le changement. |
| INDÉTERMINÉ, « aucune version antérieure dans le corpus Casus » | La base ne contient pas la version de cette date. | Ne décrivez pas le contenu de mémoire. Donnez le lien Légifrance daté que l'outil fournit et dites que la version applicable n'a pas pu être lue. Une version postérieure peut être citée seulement comme telle : rattachez chaque chiffre à sa version là où vous le donnez (« X % selon la version en vigueur du JJ/MM/AAAA au JJ/MM/AAAA »), et ne titrez pas une partie « conditions à la date des faits » si elle repose sur une version postérieure. |
| « non applicable à la date », article abrogé | L'article n'existait plus ou pas encore. | Cherchez le texte qui le remplaçait à cette date (`get_code_plan`, `search` avec `sources=["codes"]`). |

`search` et `search_text` renvoient les versions actuelles : un article trouvé par eux se relit toujours avec `get_code_article` et `date`.

## Étape 3 : entrée en vigueur et dispositions transitoires

Une loi nouvelle dit elle-même à quelles opérations elle s'applique (« aux cessions réalisées à compter du … », « aux exercices clos à compter du … »). Ces règles d'application ne figurent souvent pas dans le code. Pour les retrouver :

- `list_bofip(serie=…, nature="Actualité", depuis=…)` sur la période qui entoure le changement ;
- `search(query="entrée en vigueur et date d'application de la modification de l'article … par la loi …", sources=["bofip", "blogs"])` ;
- `search_text(query="\"entrée en vigueur\" …numéro de l'article…", source="bofip", serie=…)` pour une formulation précise (une seule expression entre guillemets par requête).

Quand l'article a changé juste avant ou après la date des faits, la date d'application de la loi modificative est décisive : ne concluez pas sans elle, et dites si elle n'a pas pu être trouvée. Une actualité BOFIP trouvée par `search` peut ne pas se lire par `get_bofip` ou `fetch` : citez alors l'extrait de `search` avec son lien, en disant que le texte complet n'a pas pu être lu. Quand la règle d'application reste inconnue et que le conseil en dépend, proposez une conduite qui respecte les deux rédactions, ou présentez les deux hypothèses.

## Étape 4 : la doctrine BOFIP à la date

Le corpus ne contient qu'une version de chaque document BOFIP. Lisez son en-tête (« Version du corpus Casus : en vigueur depuis le … ») et la date à la fin de l'identifiant (`BOI-…-20240612`).

- Version antérieure aux faits et texte inchangé entre-temps : elle décrit la doctrine applicable aux faits, sous réserve d'une version intermédiaire.
- Version postérieure aux faits : la doctrine en vigueur à la date des faits peut être différente. Dites-le et renvoyez au lien BOFIP, dont la page donne l'historique des versions.
- La doctrine opposable à l'administration est celle qui n'était pas rapportée à la date des opérations en cause (LPF, art. L. 80 A) : c'est la date des faits qui compte, pas celle du contrôle.
- Une actualité BOFIP ou un rescrit antérieurs aux faits peuvent décrire la doctrine de l'époque : `list_bofip(serie=…, nature="Actualité", depuis=…)` sur la période, puis `get_bofip`.
- Pour la règle au cœur de la question (durée, taux, seuil, condition), cherchez d'abord une source en vigueur à la date des faits : un document BOFIP voisin non mis à jour depuis (souvent un sous-document de la même division, `list_bofip(serie=…, division=…)`), une actualité antérieure. Ne fondez la règle sur des sources postérieures aux faits que si aucune source antérieure n'est trouvée, et dites-le.
- Dans la réponse, chaque document BOFIP cité porte la date de sa version et la mention « antérieure aux faits » ou « postérieure aux faits ».

## Étape 5 : la jurisprudence et les réponses ministérielles à la date

- Une décision applique le texte dans la version des années en litige. Repérez ces années dans la décision (`get_decision`, `fetch`) et comparez avec la version applicable à vos faits : si la rédaction utile a changé, la solution ne se transpose pas d'elle-même. Dites-le.
- Formulez les recherches avec la période : `search(query="… au titre des années 2019 et 2020 …", sources=["jurisprudences"])`.
- Une réponse ministérielle vaut pour le texte en vigueur à sa date : vérifiez que le texte n'a pas changé depuis.

## Étape 6 : les délais qui courent encore

Des faits passés posent toujours deux questions de délai, à traiter en quelques lignes avec les articles lus à la date utile :

- l'administration peut-elle encore rectifier cette période (délai de reprise, LPF, art. L. 169 et suivants selon l'impôt ; `python scripts/delais.py reprise ANNEE`) ?
- le contribuable peut-il encore réclamer (LPF, art. R*196-1, R*196-2 pour les impôts directs locaux, et R*196-3, dans leur version en vigueur à la date de la mise en recouvrement) ?

## Étape 7 : rendre le résultat

1. **Conclusion** : le régime applicable à la date retenue, en une ou deux phrases.
2. **Date retenue** et pourquoi (fait générateur, acte).
3. **Textes applicables** :

   | Texte | Version applicable aux faits | Période de validité | Ce qu'il prévoit pour le cas | Lien |
   |---|---|---|---|---|

   Puis, pour chaque texte déterminant, un bloc `>` avec les lignes exactes de la version applicable.
4. **Doctrine et jurisprudence** : ce qu'elles ajoutent, avec la date de chaque source et toute réserve de version.
5. **Délais** : reprise et réclamation (étape 6).
6. **Ce qui a changé depuis** (si la question peut servir pour l'avenir ou si le client compare) : en quelques lignes.
7. **Points non vérifiés** : versions indéterminées, date d'application non trouvée, BOFIP postérieur aux faits.

## Contrôle avant envoi

1. Passez le brouillon entier à `resolve_references(texte=…, date=date des faits)` : un article « non applicable à la date » ou « indéterminé à la date » que la réponse présente comme applicable est une erreur à corriger.
2. Chaque chiffre et chaque condition est rattaché à une version lue, avec sa période de validité ; ce qui vient d'une version postérieure le dit à l'endroit même.
3. Chaque document BOFIP cité porte sa date et sa position par rapport aux faits.
4. Chaque décision citée a été lue ; les années en litige et la version du texte qu'elle applique sont comparées à celles des faits.
5. Les dates et jours de la semaine sont recalculés (`scripts/delais.py`).

## Fichiers du skill

- `references/application-dans-le-temps.md` : lois de finances et leurs dates, doctrine sur l'application de la loi fiscale dans le temps (BOI-CTX-DG-20-10-20) par paragraphe, où lire la date d'application d'une modification.
- `references/carte-des-sources.md` : articles et séries BOFIP par domaine, vérifiés dans le corpus.
- `scripts/delais.py` : jours de la semaine, délais, fin du délai de reprise.
