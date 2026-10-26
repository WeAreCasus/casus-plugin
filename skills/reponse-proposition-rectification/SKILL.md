---
name: reponse-proposition-rectification
description: Préparer la réponse à une proposition de rectification (procédure de rectification contradictoire, LPF art. L. 57) avec le connecteur Casus - calendrier et délais, contrôle de la régularité de la procédure, analyse de chaque chef de redressement (textes à la date des faits, BOFIP, jurisprudence), pénalités, options (prorogation, recours hiérarchique, interlocuteur, commission, régularisation) et plan de la lettre de réponse. À utiliser dès qu'un utilisateur reçoit ou analyse une proposition de rectification, un redressement ou un rehaussement fiscal, prépare des observations du contribuable ou conteste des rappels d'impôt, même s'il ne cite pas l'article L. 57.
---

# Réponse à une proposition de rectification

La réponse à une proposition de rectification est le moment où le contribuable peut encore faire abandonner des rehaussements sans contentieux, et où il fixe le débat pour la suite (commission, réclamation, juge). Trois choses comptent, dans cet ordre :

1. **ne pas laisser passer un délai** ;
2. **repérer les irrégularités de procédure**, qui peuvent faire tomber tout ou partie de l'imposition ;
3. **contester au fond chaque chef de redressement** avec les textes applicables à la date des faits, la doctrine opposable et la jurisprudence.

Le résultat attendu est un dossier de travail : calendrier, tableau des chefs, points de procédure, options, et le plan de la lettre de réponse. La lettre complète n'est rédigée que si l'utilisateur la demande.

## Socle

1. **Date.** Pour des faits datés, passez `date` (fait générateur, date de l'acte ou de l'acte de procédure) à `get_code_article` et `resolve_references`. Sans date, l'outil répond pour aujourd'hui.
2. **Lire avant d'affirmer.** Un extrait de `search` ne suffit pas pour citer. Une décision citée a été lue elle-même. Toute condition, tout taux, seuil, délai ou numéro affirmé vient d'un texte lu pendant la recherche ; sinon il est présenté comme non vérifié. Aucune dérogation ni exception sans une source lue qui la prévoit.
3. **Citer exactement.** Les passages déterminants sont reproduits mot pour mot dans un bloc `>`, copiés de la sortie de l'outil. Les liens sont ceux que renvoient les outils, jamais construits ni complétés (pas de date ajoutée à un lien Légifrance).
4. **Dire les limites.** « Absent du corpus Casus » ne veut pas dire inexistant. Une version INDÉTERMINÉE ne se décrit pas de mémoire : donnez le lien Légifrance daté. Une date déduite se présente comme une déduction.
5. **Économiser les appels.** Lancez dans le même tour les appels indépendants. Groupez jusqu'à dix articles par `get_code_article` et toutes les références dans un seul `resolve_references`. Ne relisez pas un document déjà lu. En cas de limite de débit, attendez le délai indiqué. Le budget du parcours est un plafond : dès que la conclusion est sourcée, arrêtez de chercher et signalez en une ligne ce qui resterait à approfondir.
6. **Calculer sans erreur.** Jours de la semaine, délais, durées et intérêts se calculent avec `scripts/delais.py` quand l'exécution de code est disponible ; sinon, montrez le calcul pas à pas.
7. **Contrôler avant d'envoyer** (dernière section).

## Parcours et budget

Pour une proposition à deux ou trois chefs, 25 à 45 appels Casus suffisent :

- **premier tour, en parallèle** : `resolve_references` sur la proposition entière (à la date des faits pour les textes de fond), les articles de procédure groupés en un `get_code_article` à la date de l'acte en cause (LPF, art. L. 284) (L. 10, L. 47, L. 48, L. 54 B, L. 57, L. 80 D, L. 169, L. 176…), les articles de fond de chaque chef ;
- **jurisprudence de procédure** : partez des décisions de `references/jurisprudence-procedure.md` (lisez-les avant de les citer, elles se lisent directement par leur numéro) au lieu de recherches larges ;
- **par chef** : une recherche BOFIP, une recherche de jurisprudence rédigée selon `references/carte-des-sources.md`, puis la lecture des deux ou trois meilleurs résultats ;
- **contrôle** : un `resolve_references` sur le brouillon.

Au-delà de 45 appels, arrêtez d'élargir : dites ce qui reste à approfondir dans « Points à confirmer ».

## Étape 0 : réunir les éléments

Lisez la proposition de rectification en entier (fichier joint ou texte collé), et relevez :

- le contribuable, le service, le vérificateur, la nature du contrôle (vérification de comptabilité, examen de comptabilité, ESFP, contrôle sur pièces) et l'imprimé ;
- la **date de réception** : retrait du pli recommandé, ou présentation à domicile si le pli n'a pas été retiré, ou remise en main propre ;
- les impôts, les périodes, et pour chaque chef : le motif, la base légale invoquée, les montants (base, droits, intérêts, majorations) ;
- les pénalités et leur motivation ;
- les mentions obligatoires : faculté de se faire assister d'un conseil (LPF, art. L. 54 B, sous peine de nullité), délai de réponse de trente jours et sa prorogation (R*57-1, L. 57) et, après un ESFP, une vérification ou un examen de comptabilité, le montant des droits, taxes et pénalités (L. 48) ;
- les documents de tiers ou traitements informatiques invoqués.

Si la date de réception manque, demandez-la tout de suite : elle commande tout le calendrier. Les autres manques se signalent dans le dossier, sans bloquer l'analyse.

## Étape 1 : le calendrier

Calculez et présentez en tête du dossier :

| Échéance | Règle | Date |
|---|---|---|
| Réponse à la proposition | 30 jours à compter de la réception | … |
| Demande de prorogation de 30 jours | à faire parvenir avant l'expiration des 30 jours | … |
| Réponse si prorogation obtenue | 60 jours à compter de la réception | … |

Règles de calcul, à confirmer en lisant les sources par les outils (LPF, art. L. 11, L. 57, R*57-1 et L. 286 ; BOI-CF-IOR-10-50-10, § 190 à 270) :

- le délai part de la réception (retrait effectif du pli, ou présentation à domicile si le pli n'est pas retiré) ;
- l'administration le traite comme un délai franc : on ne compte ni le jour du départ ni celui de l'échéance ; s'il expire un samedi, un dimanche ou un jour férié, il est reporté au premier jour ouvrable suivant ;
- la recevabilité de la réponse s'apprécie à la date d'envoi (cachet de La Poste ou accusé de réception électronique) ;
- la loi exige que la demande de prorogation soit reçue par l'administration avant l'expiration du délai ; la doctrine admet son expédition avant cette date. Conseillez de l'envoyer tôt et par un moyen daté ;
- la prorogation ne vaut pas pour tous les actes (sanctions motivées séparément, procédure d'office, réponse aux observations) : vérifiez au cas par cas dans le même BOFIP.

Calculez avec `python scripts/delais.py delai-franc JJ/MM/AAAA 30`, puis `… 60` pour la prorogation (bibliothèque standard ; jours fériés calculés ; `--alsace-moselle` ajoute le 26 décembre et le Vendredi saint, ce dernier n'étant férié que dans les communes ayant un temple protestant ou une église mixte, C. trav., art. L. 3134-13 : ne faites pas dépendre la date d'envoi conseillée d'un jour férié local). Recopiez sa sortie : date de réception, premier jour compté, trentième jour, jour d'échéance, report éventuel, avec le jour de la semaine. Sans exécution de code, faites le même calcul pas à pas. En tête du dossier, donnez deux dates distinctes : la **date limite légale** ainsi calculée, et une **date d'envoi conseillée** quelques jours avant, par un moyen qui date l'envoi.

Ajoutez les échéances suivantes pour mémoire :

- réponse de l'administration aux observations, et son délai de 60 jours pour certaines petites entreprises (LPF, art. L. 57 A) ;
- en contrôle fiscal externe, recours hiérarchique dans les 30 jours de la réception de la réponse aux observations, puis interlocution dans les 30 jours de la réception du compte rendu du recours hiérarchique ; saisine directe de l'interlocuteur dans les 30 jours de la réponse aux observations lorsque le supérieur hiérarchique a signé la proposition ou en cas de pénalités exclusives de bonne foi ; délais francs (charte du contribuable vérifié, opposable par l'article L. 10 du LPF ; BOI-CF-PGR-20-10, § 340 et 370 ; ACTU-2023-00126) ;
- en contrôle sur pièces, recours hiérarchique possible dans le délai de réclamation, qu'il suspend (LPF, art. L. 54 C) ;
- saisine de la commission dans les 30 jours de la réponse aux observations (LPF, art. R*59-1) ;
- régularisation (LPF, art. L. 62) : en contrôle sur pièces ou en examen de comptabilité, dans les 30 jours de la réception de la proposition (délai franc) ; en vérification de comptabilité ou en ESFP, elle devait être demandée avant la proposition (BOI-CF-IOR-20-10, § 110 et 120).

## Étape 2 : contrôler la procédure

Lisez la liste de contrôle `references/controle-procedure.md` et passez chaque point en revue au regard des faits. Pour chaque point utile :

- lisez l'article avec `get_code_article(code="LPF", numeros=[…], date=…)` **à la date de l'acte de procédure en cause** (avis de vérification, proposition, etc.) ; groupez jusqu'à dix articles par appel ;
- partez des décisions de principe listées pour ce point dans `references/jurisprudence-procedure.md` ; lisez celles que vous citerez (`get_decision`), puis, si le cas s'en écarte, cherchez une décision sur des faits proches : `search(query=…, sources=["jurisprudences"])` rédigée avec les faits et le critère appliqué par le juge, pas avec le numéro de l'article ;
- qualifiez la conséquence : décharge de l'ensemble (nullité expressément prévue ou atteinte aux droits de la défense), décharge des seules majorations et amendes, à l'exclusion des droits et des intérêts de retard (erreur non substantielle, LPF, art. L. 80 CA), ou simple irrégularité sans effet.

Vérifiez toujours la **prescription**, impôt par impôt et période par période, à la date de présentation de la proposition : le délai de reprise n'est pas le même pour l'IS ou l'IR (LPF, art. L. 169) et pour la TVA, qui court à partir de l'exigibilité (LPF, art. L. 176). `python scripts/delais.py reprise ANNEE` donne la fin du délai de droit commun ; vérifiez dans les articles lus les cas de délai allongé (activité occulte, comptes ou avoirs à l'étranger non déclarés, plainte pour fraude…) et l'interruption par la proposition (LPF, art. L. 189). Une période prescrite est le premier argument de la lettre.

Plusieurs articles de procédure portent dans le corpus la mention « jusqu'au 01/01/2027 (abrogation ou modification programmée) », et d'autres une date plus lointaine : si un acte de la procédure intervient après cette date, la version applicable n'est pas dans le corpus. Signalez-le.

Ne soulevez pas un moyen de procédure sans fondement textuel ou jurisprudentiel lu : un moyen faible affaiblit la lettre.

## Étape 3 : analyser chaque chef de redressement

Pour chaque chef, dans l'ordre de la proposition :

1. **Restituez la position de l'administration** : rehaussement, période, base légale invoquée, montant.
2. **Vérifiez les références** de la proposition en un appel : `resolve_references(texte=…, date=…)` avec le passage de la proposition et la date des faits. Une référence mal citée ou inapplicable à la date est un argument.
3. **Lisez les textes à la date des faits** (pas à la date du contrôle) : `get_code_article` avec `date` = fait générateur de l'impôt redressé, en mode complet si la frise est utile. Un résultat INDÉTERMINÉ se dit tel quel, avec le lien Légifrance daté.
4. **Cherchez la doctrine opposable** : `search(query=…, sources=["bofip"])` puis `get_bofip`. La doctrine non rapportée à la date des opérations est opposable à l'administration (LPF, art. L. 80 A, troisième alinéa), de même qu'une interprétation formellement admise ou une prise de position formelle sur une situation de fait (L. 80 A, premier alinéa, et L. 80 B, 1°), ou une prise de position sur les points contrôlés lors d'un précédent examen ou vérification de comptabilité ou ESFP, y compris tacite par une absence de rectification, dès lors que l'administration a pu se prononcer en toute connaissance de cause (L. 80 A, deuxième alinéa ; ces points figurent sur la proposition ou l'avis d'absence de rectification, L. 49). Comparez la date de la version BOFIP du corpus à la date des faits.
5. **Cherchez la jurisprudence**, favorable et défavorable : deux ou trois recherches ciblées dans `jurisprudences` (critères appliqués par le juge, faits proches), et une dans `reponses_ministerielles` si utile. Lisez les décisions que vous citerez.
6. **Situez la charge de la preuve** : qui doit prouver quoi selon la procédure suivie (procédure contradictoire, taxation d'office, graves irrégularités, avis de la commission ; LPF, art. L. 192).
7. **Mesurez les conséquences sur les autres impôts** : en cas de vérification simultanée de la TVA et de l'IS ou de l'IR, le rappel de TVA d'un exercice est déduit du résultat du même exercice, sauf demande contraire dans le délai de réponse (LPF, art. L. 77) ; une réintégration de charges peut aussi être requalifiée en revenu distribué.
8. **Évaluez** en une phrase motivée, puis listez les pièces à produire : **fort** si au moins deux sources lues, explicites et convergentes le fondent (texte et jurisprudence ou doctrine) sans contraire lue ; **sérieux** si une source lue le fonde, ou si une contraire de rang inférieur existe ; **faible** si des sources lues divergent, ou s'il repose sur une analogie ou un raisonnement a contrario. Ne conseillez jamais d'abandonner un argument sans un texte ou une décision contraire lus. Un raisonnement a contrario tiré d'un exemple BOFIP n'est pas une doctrine opposable : l'article L. 80 A ne joue que si la doctrine vise la situation et que le contribuable s'y est conformé à la lettre.

Suivez la méthode en trois recherches par chef (code, doctrine, jurisprudence) plutôt qu'une recherche large : une requête par source, rédigée dans le vocabulaire de cette source (`references/carte-des-sources.md` donne, par matière, les articles, les séries BOFIP et la forme de requête qui fonctionne).

Lisez une décision en mode concis avant de la lire en entier, utilisez le sommaire d'un BOFIP pour aller à la section utile, et ne relisez pas un document déjà lu.

Chiffrez l'enjeu de chaque chef : droits, intérêt de retard, majorations, et l'effet sur les autres impôts (L. 77, revenus distribués). Un argument fort sur un petit chef passe après un argument sérieux sur le chef principal.

## Étape 4 : les pénalités

- **Intérêt de retard** (CGI, art. 1727) : taux, point de départ, arrêt du décompte ; cas où il n'est pas dû. Pour vérifier le montant réclamé, lisez à l'article 1727 (IV) le point de départ et l'arrêt du décompte ; le taux se détermine par période de décompte, non à la date des faits (0,40 % par mois jusqu'au 31/12/2017, 0,20 % ensuite, BOI-DAE-20-10, § 90 : à relire) : découpez la période et lancez `python scripts/delais.py interet MONTANT DEBUT FIN TAUX` une fois par tranche. Un écart avec la proposition est un point à soulever.
- **Majorations** (CGI, art. 1728, 1729, 1758 A selon le cas) : elles doivent être motivées (LPF, art. L. 80 D) ; la preuve de la mauvaise foi (manquement délibéré) et des manœuvres frauduleuses incombe à l'administration (LPF, art. L. 195 A) ; pour l'abus de droit, l'administration supporte la charge de la preuve lorsque le comité de l'abus de droit fiscal a été saisi, quel que soit son avis (LPF, art. L. 192), et hors saisine il faut vérifier la jurisprudence. Vérifiez que la motivation vise des éléments propres au contribuable, pas une formule générale, et que la décision d'appliquer les majorations de l'article 1729 porte le visa d'un agent ayant au moins le grade d'inspecteur divisionnaire (LPF, art. L. 80 E ; BOI-CF-PGR-30-10, § 140).
- Si les sanctions sont motivées séparément de la proposition, leur délai de réponse de 30 jours court à part (LPF, art. L. 80 D) et ne bénéficie pas de la prorogation.

## Étape 5 : les options

Présentez les options utiles au cas, avec leurs conditions et leurs délais, lues dans les sources :

- accepter certains chefs pour concentrer le débat sur les autres ;
- régularisation (LPF, art. L. 62) pour des erreurs commises de bonne foi dans des déclarations souscrites dans les délais, avec un intérêt de retard dû à 70 % de son montant, sous réserve d'une déclaration complémentaire dans les 30 jours de la demande et du paiement des droits ; possible seulement dans les cas et délais rappelés à l'étape 1 : après une vérification de comptabilité ou un ESFP, la proposition reçue, il est trop tard ;
- entretien avec le vérificateur, recours hiérarchique, puis interlocuteur, dans les délais de l'étape 1 (en contrôle sur pièces, l'interlocuteur ne peut pas être saisi : seul le recours hiérarchique de l'article L. 54 C est ouvert, BOI-CF-PGR-30-10, § 540) ;
- saisine de la commission départementale ou nationale (LPF, art. L. 59 et L. 59 A : vérifiez que le désaccord relève de sa compétence) ou du comité de l'abus de droit (LPF, art. L. 64) ;
- transaction sur les pénalités (LPF, art. L. 247) ;
- après mise en recouvrement : réclamation contentieuse au plus tard le 31 décembre de la deuxième année suivant la mise en recouvrement (LPF, art. R*196-1), ou, après une procédure de rectification, dans un délai égal à celui de reprise de l'administration (LPF, art. R*196-3).

## Étape 6 : le plan de la réponse

Construisez le plan à partir du modèle `references/plan-reponse.md`. Chaque partie du plan indique l'argument, sa source (avec le lien renvoyé par l'outil) et les pièces à joindre. Les faits que vous ne connaissez pas restent entre crochets : `[montant à confirmer]`, `[date de l'entretien]`.

## Le dossier rendu

1. **Synthèse** : date limite légale et date d'envoi conseillée, enjeu total, période prescrite le cas échéant, point de procédure le plus sérieux, chefs contestables.
2. **Calendrier** (étape 1).
3. **Tableau des chefs de redressement** :

   | # | Chef | Période | Montant | Base légale invoquée | Position recommandée | Argument principal | Force | Pièces |
   |---|---|---|---|---|---|---|---|---|

4. **Procédure** : points examinés, irrégularités retenues avec leur conséquence, points sans objet.
5. **Analyse par chef** : textes cités mot pour mot dans des blocs `>`, doctrine, jurisprudence, évaluation.
6. **Pénalités**.
7. **Options et recommandation**.
8. **Plan de la lettre de réponse**.
9. **Points à confirmer** : faits manquants, versions indéterminées, sources non lues.

Chaque élément est développé une seule fois, dans la partie où il sert : le tableau, les options et le plan de la lettre renvoient à l'analyse au lieu de la répéter. Pour une proposition à deux ou trois chefs, visez 3 000 à 4 500 mots, citations comprises ; la lettre complète n'est rédigée que sur demande.

## Règles constantes

- Toute condition, tout taux et tout délai affirmé vient d'un texte lu pendant la recherche ; sinon, il est présenté comme non vérifié. Pour chaque décision citée, dites en quoi ses faits diffèrent du cas et si elle a été frappée d'appel ou de pourvoi.

- Toute référence vient d'un outil Casus ou de la proposition elle-même, et toute référence de la proposition est vérifiée.
- Les textes de fond se lisent à la date des faits ; les règles de procédure, à la date de chaque acte.
- « Absent du corpus Casus » ne veut jamais dire inexistant.
- N'inventez aucun fait. Ce que le dossier ne dit pas reste entre crochets ou devient une question.
- Les liens sont ceux renvoyés par les outils.

## Contrôle avant envoi

1. Passez le dossier entier à `resolve_references(texte=…)` (avec la date des faits pour les textes de fond) : chaque référence revient « trouvée », ou elle est corrigée ou retirée.
2. Les dates du calendrier sortent de `scripts/delais.py` ou d'un calcul montré pas à pas, avec le jour de la semaine ; la date limite légale et la date d'envoi conseillée sont distinctes.
3. Chaque décision citée a été lue, ses faits sont comparés au cas, et sa suite (appel, pourvoi) est dite ou signalée comme non vérifiée.
4. Chaque moyen de procédure repose sur un texte ou une décision lus ; sa conséquence (décharge totale, décharge des seules majorations et amendes avec maintien des droits et de l'intérêt de retard, LPF, art. L. 80 CA, ou sans effet) est dite.
5. La synthèse, le tableau des chefs et le plan de la lettre donnent les mêmes positions et les mêmes montants.
6. Les points du devoir de conseil sont traités : prescription, L. 77, pénalités, options et leurs délais, pièces à réunir.

## Fichiers du skill

- `references/controle-procedure.md` : liste de contrôle de la régularité de la procédure.
- `references/jurisprudence-procedure.md` : décisions de principe sur les irrégularités de procédure, vérifiées dans le corpus, à lire avant de les citer.
- `references/carte-des-sources.md` : par matière, articles, séries BOFIP et requêtes qui fonctionnent.
- `references/plan-reponse.md` : modèle du plan de la lettre de réponse.
- `scripts/delais.py` : délais francs, jours fériés, délai de reprise, intérêt de retard.
