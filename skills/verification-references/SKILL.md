---
name: verification-references
description: Contrôler toutes les références d'une note, d'une consultation, de conclusions, d'un mémoire, d'un courrier ou d'un acte avant envoi, avec le connecteur Casus - articles de codes, décisions, ECLI, BOFIP, réponses ministérielles, conventions fiscales, actes de l'UE. Rend un tableau citation, statut, écart et correction, puis les points de fond. À utiliser dès que l'utilisateur demande de vérifier, relire, sourcer, fiabiliser ou « checker » les références ou citations d'un texte juridique ou fiscal, ou soupçonne une référence inventée, même s'il ne parle pas de Casus.
---

# Vérification des références

Objectif : qu'aucune référence fausse, périmée ou mal attribuée ne parte chez le client ou devant le juge. Le contrôle porte sur trois niveaux, du plus mécanique au plus juridique :

1. **existence** : la référence existe-t-elle dans le corpus Casus ?
2. **exactitude** : chaque élément cité (numéro, date, juridiction, chambre, version, paragraphe, page) est-il juste ?
3. **portée** : la source dit-elle ce que le texte lui fait dire, et s'appliquait-elle à la date des faits ?

L'outil `resolve_references` fait l'essentiel du niveau 1 et une partie du niveau 2. Le reste demande de lire les sources.

## Socle

1. **Date.** Pour des faits datés, passez `date` (fait générateur, date de l'acte ou de l'acte de procédure) à `get_code_article` et `resolve_references`. Sans date, l'outil répond pour aujourd'hui.
2. **Lire avant d'affirmer.** Un extrait de `search` ne suffit pas pour citer. Une décision citée a été lue elle-même. Toute condition, tout taux, seuil, délai ou numéro affirmé vient d'un texte lu pendant la recherche ; sinon il est présenté comme non vérifié. Aucune dérogation ni exception sans une source lue qui la prévoit.
3. **Citer exactement.** Les passages déterminants sont reproduits mot pour mot dans un bloc `>`, copiés de la sortie de l'outil. Les liens sont ceux que renvoient les outils, jamais construits ni complétés (pas de date ajoutée à un lien Légifrance).
4. **Dire les limites.** « Absent du corpus Casus » ne veut pas dire inexistant. Une version INDÉTERMINÉE ne se décrit pas de mémoire : donnez le lien Légifrance daté. Une date déduite se présente comme une déduction.
5. **Économiser les appels.** Lancez dans le même tour les appels indépendants. Groupez jusqu'à dix articles par `get_code_article` et toutes les références dans un seul `resolve_references`. Ne relisez pas un document déjà lu. En cas de limite de débit, attendez le délai indiqué. Le budget du parcours est un plafond : dès que la conclusion est sourcée, arrêtez de chercher et signalez en une ligne ce qui resterait à approfondir.
6. **Calculer sans erreur.** Montrez chaque calcul de date ou de durée pas à pas, jour de la semaine compris.
7. **Contrôler avant d'envoyer** (dernière section).

## Parcours et budget

- Un seul `resolve_references` pour tout le texte (ou un par date retenue), puis un seul appel de rattrapage avec `references=[…]` pour ce que l'extraction a manqué.
- Les lectures de portée se lancent ensemble, dans le même tour : décisions, articles groupés par code et par date, paragraphes BOFIP.
- Ordre de grandeur : 5 à 10 appels pour une note de 10 références, 15 à 25 pour un mémoire de 30 références. Au-delà, contrôlez la portée des citations qui fondent les conclusions et dites lesquelles restent au niveau de l'existence.
- Les corrections suivent les formes de `references/formats-de-citation.md` : ouvrez-le avant de rédiger la colonne « Correction proposée ».

## Étape 1 : préparer le contrôle

- Lisez le document en entier (texte collé ou fichier joint).
- Fixez la **date de référence** :
  - un document qui analyse des faits datés (opération de 2021, exercice 2023, contrôle portant sur 2022) se vérifie à la date de ces faits, pour savoir si les articles cités s'appliquaient alors ;
  - un document qui conseille pour l'avenir ou décrit le droit actuel se vérifie à la date du jour ;
  - si les citations portent sur des dates différentes, groupez-les par date (un appel par date).
  Dites en une ligne quelle date vous avez retenue et pourquoi.
- Dressez votre propre inventaire des citations, dans l'ordre du texte, en relevant pour chacune : la citation telle qu'écrite, la proposition qu'elle soutient, et si elle est entre guillemets (citation textuelle).

## Étape 2 : contrôle automatique

Appelez `resolve_references(texte=…, date=…)` avec le passage contenant les citations (100 000 caractères au plus par appel ; au-delà, découpez par parties).

Comparez la liste rendue avec votre inventaire. L'extraction automatique peut manquer ou déformer certaines citations, notamment :

- l'article d'un acte de l'UE cité après l'acte (« directive 2006/112/CE, art. 135 ») : seul l'acte est contrôlé ; lisez l'article avec `fetch(id="eur_lex:{CELEX}:art_{N}")` à partir de l'id renvoyé (par exemple `eur_lex:32006L0112:art_135`) ;
- les articles introduits par « du même code », « dudit code » quand le code n'est pas repérable ;
- les articles de conventions fiscales : lisez-les avec `get_convention_fiscale(pays=…, article=…)` ;
- les lois, décrets et arrêtés non codifiés, la doctrine privée : ils ne sont pas dans le corpus ; classez-les « hors corpus », sans conclure.

Relancez ce qui manque avec `references=[…]` (une référence par élément, 50 au plus par appel), en écrivant chaque référence en entier (« art. L. 57 LPF », « CE, 8e et 3e ch. réunies, 15 nov. 2021, n° 454105 »).

## Étape 3 : traiter chaque statut

| Statut rendu | Ce que vous faites | Statut dans votre tableau |
|---|---|---|
| trouvée | Comparez vous-même chaque élément cité au libellé renvoyé : juridiction, **chambre ou formation**, date, numéro. L'outil ne compare pas tous les éléments (la chambre, par exemple). Pour une citation qui porte un raisonnement, passez à l'étape 4. | Exacte, À corriger si un élément diffère, ou Portée contestable après l'étape 4 |
| trouvée avec écart | Lisez la note : elle dit quel élément diffère. Corrigez avec le libellé renvoyé. | À corriger |
| ambiguë | Comparez les candidats aux éléments cités (assemblée, législature, date, page ; juridiction et date). Un seul correspond : corrigez. Aucun ne correspond : la citation n'est pas confirmée ; listez les candidats. | À corriger, ou Non confirmée |
| introuvable | Recoupez : `get_code_article` pour un article (catalogue si le nom du code est douteux), `get_decision` avec `juridiction` et `date` pour une décision (regardez les numéros proches signalés : faute de frappe possible). Une décision peut aussi être enregistrée sous un autre numéro (numéro d'arrêt au lieu du numéro de pourvoi) : essayez `search(query="… numéro, juridiction, date et objet …", sources=["jurisprudences"])` puis `fetch` sur l'id trouvé. | Exacte ou À corriger si le recoupement la retrouve ; sinon Absente du corpus Casus |
| non applicable à la date | L'article était abrogé à la date retenue. Trouvez le texte applicable à cette date (`get_code_article` avec `detail="complet"`, `get_code_plan`, `search`). | À corriger |
| indéterminée à la date | Aucune version du corpus ne couvre la date. Donnez le lien Légifrance daté. | Indéterminée à la date |

« Absente du corpus Casus » ne veut jamais dire que la référence n'existe pas : écrivez-le ainsi et indiquez où la vérifier (Légifrance, BOFIP, site de la juridiction).

## Étape 4 : contrôler la portée

Pour chaque citation qui porte un argument (pas seulement un « voir aussi »), lisez la source :

- **Décision** : `get_decision` (mode concis : en-tête et début du texte ; `detail="complet"` si nécessaire). Vérifiez la matière (une décision de droit du travail citée pour une question fiscale est une erreur d'attribution), la solution retenue et que le passage cité figure bien dans la décision.
- **Article de code** : `get_code_article` à la date retenue. Vérifiez que l'alinéa invoqué dit ce que le texte affirme ; toute citation entre guillemets se compare mot pour mot avec la version applicable.
- **BOFIP** : `get_bofip`, sommaire puis section utile. Vérifiez le paragraphe (§) cité et la date de la version : si l'article commenté a changé depuis, le BOFIP peut décrire l'ancien droit.
- **Réponse ministérielle** : vérifiez l'assemblée, la législature, la date et la page ; une page de l'Assemblée nationale signalée « non vérifiée » vient des métadonnées.
- **Décision de première instance ou d'appel** : regardez si elle a été frappée de pourvoi ou d'appel (`search(query="… parties, numéro, juridiction : pourvoi ou appel contre cette décision", sources=["jurisprudences"])`, ou la mention d'une décision ultérieure dans le corpus). Une décision annulée ou cassée ne se cite plus comme solution ; une décision isolée de tribunal se signale comme telle quand le texte la présente comme une jurisprudence établie.
- **Faits de la décision** : une décision citée pour un principe peut avoir été rendue sur des faits très différents du dossier (autre impôt, autre procédure, autre période). Signalez l'écart quand il affaiblit l'argument.

Sur un document long, contrôlez la portée en priorité pour les citations qui fondent les conclusions et celles placées entre guillemets ; dites lesquelles n'ont été contrôlées qu'au niveau de l'existence.

## Étape 5 : rendre le résultat

Commencez par une synthèse de deux ou trois lignes : nombre de références contrôlées (le même que le nombre de lignes du tableau), combien sont exactes, à corriger, de portée contestable, non confirmées, et la correction la plus importante.

Puis le tableau, une ligne par citation, dans l'ordre du texte :

| # | Citation telle qu'écrite | Statut | Écart constaté | Correction proposée | Source |
|---|---|---|---|---|---|
| 1 | CE, [chambre citée], [date], n° [numéro] | Portée contestable | Chambre : la décision est d'une autre chambre que celle citée. Matière : elle tranche un litige de droit du travail, sans rapport avec la proposition qu'elle est censée soutenir. | Supprimer la citation, ou la remplacer par une décision pertinente lue dans le corpus | [lien renvoyé par l'outil] |
| 2 | art. [numéro] CGI | Exacte | — | — | [lien renvoyé par l'outil] |

Valeurs de la colonne Statut :

- **Exacte** : la référence existe, chaque élément cité est juste et la source dit ce que le texte lui fait dire ;
- **À corriger** : un élément cité est faux (numéro, date, chambre, paragraphe, version) ;
- **Portée contestable** : la référence est exacte, mais elle ne soutient pas la proposition (autre matière, solution contraire, texte hors champ, version ou doctrine périmée à la date des faits) ;
- **Non confirmée** : candidats ambigus dont aucun ne correspond aux éléments cités ;
- **Absente du corpus Casus** ;
- **Indéterminée à la date** ;
- **Hors corpus** : loi non codifiée, doctrine privée, texte étranger.

Une référence que vous conseillez de supprimer ou de remplacer n'est jamais notée « Exacte ».

Règles du tableau :

- « Écart constaté » dit précisément ce qui diffère, élément par élément.
- « Correction proposée » donne la citation corrigée, prête à recopier, avec les éléments renvoyés par les outils ; jamais d'élément deviné.
- Quand une citation doit être supprimée et qu'elle soutenait un argument, cherchez une source de remplacement (une recherche ciblée, puis la lecture des une ou deux meilleures décisions ou du paragraphe BOFIP). Une décision proposée en remplacement doit avoir été lue elle-même (`get_decision` ou `fetch`) : une décision seulement mentionnée dans le texte d'une autre ne suffit pas. À défaut, recommandez la suppression sans remplacement et dites-le.
- « Source » contient le lien renvoyé par l'outil, et rien d'autre.

Après le tableau, une section **Points de fond** liste, s'il y en a :

- les citations exactes mais mal employées (portée, matière, version périmée à la date des faits, BOFIP antérieur à la modification du texte) ;
- les citations textuelles qui ne correspondent pas mot pour mot au texte ;
- les références qui n'ont pu être contrôlées qu'au niveau de l'existence.

Si l'utilisateur le demande, renvoyez ensuite les seuls passages corrigés du document, dans leur nouvelle rédaction.

## Règles constantes

- N'ajoutez au document aucune condition, aucun taux ni délai qui ne vienne d'un texte lu pendant le contrôle ; sinon, présentez-le comme non vérifié.

- Passez `date` à `resolve_references` et à `get_code_article` dès que le document porte sur des faits datés.
- Ne corrigez jamais avec un élément (numéro, date, chambre, paragraphe) qui ne sort pas d'un outil.
- Ne choisissez jamais entre plusieurs décisions de même numéro sans un élément cité qui les départage.
- Groupez les appels : une seule liste de `references` pour toutes les citations d'une même date.

## Contrôle avant envoi

1. Passez à `resolve_references(texte=…, date=…)` les corrections que vous proposez et les sources de remplacement : chacune doit revenir « trouvée ».
2. Le nombre de lignes du tableau est celui annoncé dans la synthèse, et les compteurs par statut s'additionnent.
3. Chaque « Exacte » a été comparée élément par élément (juridiction, chambre, date, numéro, paragraphe, version).
4. Aucune correction ne contient un élément qui ne sort pas d'un outil.
5. Chaque citation entre guillemets du document a été comparée mot pour mot, ou figure dans « Points de fond » comme non comparée.
6. Une décision que vous nommez sans l'avoir lue (renvoi après cassation, décision mentionnée dans le texte d'une autre, résultat de recherche) porte la mention « non lue » ; n'écrivez « toutes les sources citées ont été lues » que si c'est vrai.

## Fichiers du skill

- `references/formats-de-citation.md` : formes de citation des articles, décisions, BOFIP, réponses ministérielles, conventions et actes de l'UE, avec les erreurs fréquentes.
