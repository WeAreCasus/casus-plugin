---
name: methode-casus
description: Méthode de recherche et règles d'usage du connecteur Casus (corpus juridique et fiscal français - codes, jurisprudence, BOFIP, réponses ministérielles, conventions fiscales, EUR-Lex, blogs). À utiliser dès qu'une question de droit ou de fiscalité française est traitée avec les outils Casus (search, fetch, get_code_article, get_decision, get_bofip, resolve_references, search_text, catalogue), même si l'utilisateur ne nomme pas Casus - parcours selon le type de question, carte des sources par domaine, requêtes efficaces, date des faits, devoir de conseil, citation exacte avec le lien, contrôle avant envoi.
---

# Méthode Casus

Le connecteur Casus donne un accès en lecture seule au corpus juridique et fiscal français de Casus. Cette méthode sert à trois choses :

1. aller droit aux bonnes sources, avec peu d'appels ;
2. ne rien présenter comme vérifié qui ne l'ait été ;
3. rendre une réponse qu'un professionnel peut signer : la règle, son texte exact, ses conditions, ses risques, avec les liens.

Les utilisateurs de Casus sont des avocats, notaires, experts-comptables et juristes : pas d'avertissement générique du type « consultez un professionnel ».

## Socle

1. **Date.** Pour des faits datés, passez `date` (fait générateur, date de l'acte, de la clôture, de l'acte de procédure) à `get_code_article` et `resolve_references`. Sans date, l'outil répond pour aujourd'hui.
2. **Lire avant d'affirmer.** Un extrait de `search` ne suffit pas pour citer. Une décision citée a été lue elle-même. Toute condition, tout taux, seuil, délai ou numéro affirmé vient d'un texte lu pendant la recherche ; sinon il est présenté comme non vérifié. Aucune dérogation ni exception sans une source lue qui la prévoit.
3. **Citer exactement.** Les passages déterminants sont reproduits mot pour mot dans un bloc `>`, copiés de la sortie de l'outil. Les liens sont ceux que renvoient les outils, jamais construits ni complétés (pas de date ajoutée à un lien Légifrance).
4. **Dire les limites.** « Absent du corpus Casus » ne veut pas dire inexistant. Une version INDÉTERMINÉE ne se décrit pas de mémoire : donnez le lien Légifrance daté. Une date déduite se présente comme une déduction.
5. **Économiser les appels.** Lancez dans le même tour les appels indépendants (les recherches d'une étape, les lectures de plusieurs documents). Groupez jusqu'à dix articles par `get_code_article` et toutes les références dans un seul `resolve_references`. Ne relisez pas un document déjà lu. En cas de limite de débit, attendez le délai indiqué. Le budget du parcours est un plafond : dès que la conclusion est sourcée, arrêtez de chercher et signalez en une ligne ce qui resterait à approfondir.
6. **Calculer sans erreur.** Jours de la semaine, délais, durées et intérêts se calculent avec `scripts/delais.py` quand l'exécution de code est disponible ; sinon, montrez le calcul pas à pas.
7. **Contrôler avant d'envoyer** (section 8).

## 1. Cadrer avant de chercher

Avant le premier appel, fixez pour vous-même (sans l'écrire dans la réponse) :

- **Le niveau**, d'après ce que la réponse doit trancher, jamais d'après la longueur de la question. Il fixe le budget d'appels et la longueur de la réponse (hors citations et références) :

  | Niveau | La réponse tranche | Appels Casus | Réponse |
  |---|---|---|---|
  | 1 Point précis | un taux, un seuil, un délai, l'article applicable, un oui ou non avec sa condition | 3 à 6 | 100 à 300 mots, sans plan |
  | 2 Question ciblée | une règle appliquée aux faits donnés | 6 à 12 | 400 à 1 000 mots : l'essentiel, puis deux ou trois parties courtes |
  | 3 Analyse | plusieurs questions liées, une application discutée, un document à examiner sur un point | 12 à 20 | 1 000 à 2 500 mots, plan de 3 à 5 parties |
  | 4 Dossier | une opération complète, plusieurs impôts, un contrôle, un document long | 20 à 40 | 2 500 à 5 000 mots, plan de 5 à 10 parties |

  Une demande de brièveté dans le message (« en deux lignes », « synthétique ») plafonne le niveau à 2, et à 1 pour une ou deux phrases. Un document joint n'élève le niveau que si la question demande de l'analyser.
- **La nature du tour** : nouvelle question, relance, fait nouveau, contestation, demande d'écrit. Sur une relance, seul l'écart se traite ; ce que le fil a établi ne se redéveloppe pas.
- **Les qualifications à vérifier** : catégorie de revenu, nature de l'opération, prélèvement, articles cités par l'utilisateur. Ce sont des hypothèses, pas des faits établis.
- **La date des faits** et les impôts en cause.
- **Le fait décisif manquant**, seulement si trois conditions sont réunies : ses valeurs plausibles mènent à des conclusions différentes ; on ne peut pas le présumer ; il n'est ni dans le message ni dans les documents. Dans le doute, il n'y en a pas : retenez l'hypothèse la plus probable.

Questions particulières : citations à vérifier, skill « vérification des références » ; faits passés ou ancienne rédaction, skills « recherche à date » et « comparaison de versions », s'ils sont disponibles. Une question internationale commence par `get_convention_fiscale(pays)`, qui liste les articles.

La carte `references/carte-des-sources.md` donne, par domaine, les articles et les séries BOFIP à lire d'abord, vérifiés dans le corpus. Elle évite de chercher ce qu'on peut lire directement ; elle ne remplace pas la lecture du texte à la date des faits.

## 2. Corpus et outils

L'essentiel : l'historique des codes varie selon le code (une date antérieure à la plus ancienne version donne INDÉTERMINÉ, et c'est la bonne réponse) ; une seule version par document BOFIP, datée dans l'en-tête ; pas d'index plein texte sur la jurisprudence (`search_text` la refuse) ; conventions fiscales issues d'une reconnaissance optique (taux et numéros à vérifier sur le PDF officiel) ; EUR-Lex en texte initial non consolidé ; les lois non codifiées ne sont pas une source, leurs dispositions d'entrée en vigueur se retrouvent par les actualités BOFIP et les blogs. Chaque source s'arrête à une date (`catalogue(type="sources")`). Le détail des sources et les paramètres utiles de chaque outil sont dans `references/corpus-et-outils.md`.

## 3. Lire ce que renvoient les outils

- **« État au … : applicable depuis … »** : la version affichée est celle de la date demandée.
- **INDÉTERMINÉ** : aucune version du corpus ne couvre la date. Lien Légifrance daté, pas de contenu de mémoire.
- **« jusqu'au … (modification programmée ; version suivante pas encore dans le corpus) »** : pour des faits postérieurs, indéterminé ; pour un conseil qui produira ses effets après, signalez le changement.
- **« Absent du corpus Casus », « introuvable »** : dites-le ainsi ; pour une décision, regardez les numéros proches (faute de frappe) et essayez `search` avec le numéro, la juridiction et l'objet (certaines décisions sont enregistrées sous un autre numéro).
- **`get_decision`** : un écart (date, chambre, nature) est signalé en tête ; plusieurs décisions de même numéro sont toutes listées : ne choisissez pas.
- **`get_bofip`** : citez la date de la version lue.
- **Texte coupé** : le repère de fin (« Texte coupé ici… Non lu : … Suite : fetch(…, offset=…) ») nomme ce qui n'a pas été lu. Ne citez rien de ce qui est nommé non lu ; lisez la partie utile avec `fetch(id, offset)` à l'offset de sa subdivision. Un article long ou groupé se lit par partie, seul dans son appel. Une décision en mode concis donne l'ouverture, les considérants omis nommés, puis le dispositif (ou la conclusion d'une conclusion d'avocat général) : pour citer un motif omis, lisez-le.
- **Versions d'un article dans `search`** : la version en vigueur passe avant les versions remplacées, et l'avertissement le dit. Une version remplacée ne se cite pas pour le droit actuel.
- **Échec de lecture** d'un document que `search` a trouvé : citez l'extrait de `search` avec son lien, en disant que le texte complet n'a pas pu être lu. Un délai dépassé donne INDÉTERMINÉ, jamais une absence.

Statuts de `resolve_references` : **trouvée** (vérifiez vous-même chambre, matière et passage cité, que l'outil ne compare pas) ; **trouvée avec écart** (corrigez selon la note) ; **ambiguë** (comparez les candidats ; aucun ne correspond : non confirmée) ; **introuvable** (recoupez avant toute conclusion) ; **non applicable à la date** (cherchez le texte de cette date) ; **indéterminée à la date** (ne concluez pas).

## 4. Rechercher

### 4.1 Le plan

Aux niveaux 1 et 2, le plan tient en une ligne : l'article qui fixe la règle (`get_code_article` à la date), le paragraphe BOFIP qui le commente, au besoin une recherche en jurisprudence. Aux niveaux 3 et 4, trois étapes, dans l'ordre d'un juriste (cadre, application aux faits, sécurité de la position), construites ainsi :

1. **Qualifier d'abord.** Si la nature juridique d'une entité ou une qualification posée par l'utilisateur commande le régime, la première étape la vérifie dans l'article qui la définit. Jamais de qualification par analogie avec une structure voisine.
2. **Une étape pour les chiffres.** Dès qu'un taux, un seuil, un montant ou une durée est en jeu, une étape lit l'article qui le fixe, à la date de l'opération, avant tout BOFIP : la doctrine peut avoir des mois de retard sur une loi de finances.
3. **Pertinence avant exhaustivité.** Traitez les impositions qui découlent de la qualification ; n'en explorez une autre que si une requalification est plausible et documentée.

Chaque étape s'écrit de façon autonome, avec les faits qui commandent la recherche : régime (IR ou IS, micro ou réel, catégorie), structure (SCI à l'IR, SARL à l'IS, holding animatrice), nature et usage du bien, corrections de l'utilisateur écrites « (et non X) », année. « Vérifier la déductibilité des charges » ramène du bruit ; « déductibilité des frais d'entretien des espaces verts (et non du chauffage) d'une SCI à l'IR au réel en 2025 » ramène les bons textes.

### 4.2 Une requête par source

Chaque requête vise une source, deux au plus, et s'écrit dans la langue de cette source ; les requêtes d'une même étape n'ont jamais toutes le même style. Une requête fait 25 à 70 mots : les notions, les termes exacts (articles, juridiction), les conditions et les faits déterminants. Ce qui suit a été mesuré sur le corpus Casus :

| Source | Rédaction qui marche | À éviter |
|---|---|---|
| `codes` | La phrase qu'on s'attend à lire dans l'article, avec son numéro : « le taux est fixé à », « sont exonérés », « est assis sur » | Une question familière |
| `bofip` | La phrase du commentaire : « Les dépenses de réparation et d'entretien s'entendent des dépenses qui ont pour objet de maintenir ou de remettre en état un immeuble… » (le BOI qui définit ces dépenses sort en tête) ; « il est admis que », la série BOI si elle est connue | Une question familière (« quels travaux je peux déduire de mes loyers ? » ne fait pas sortir ce BOI) |
| `jurisprudences` | Les faits et le critère discuté : « rémunération du dirigeant jugée excessive au regard du travail effectif fourni et des rémunérations versées dans des entreprises similaires » (une décision du Conseil d'État sur ce critère sort en tête) | Recopier l'article ou écrire « article 39 » : toutes les décisions qui le citent remontent, et `search` renvoie vers `get_code_article` |
| `reponses_ministerielles` | La question pratique telle qu'un parlementaire la pose | — |
| `conventions_fiscales` | Le nom du pays seul (« Tunisie », jamais « franco-tunisienne », qui fait remonter les conventions d'autres pays) et la catégorie de revenu ; `pays="Tunisie"` restreint la recherche à ce pays (valeur de `catalogue(type="conventions")`) | Un numéro d'article supposé (l'article sur les dividendes de la convention avec la Tunisie est le 14, non le 10) |
| `eur_lex` | Le numéro de l'acte d'un seul tenant (« 2006/112/CE », jamais « 2006 112 CE » ni « EC ») et la notion harmonisée | — |
| `blogs` | L'opération, la réforme et l'année | — |

Pour les codes, `etat` restreint aux états demandés (`VIGUEUR`, `VIGUEUR_DIFF`, `MODIFIE`, `MODIFIE_MORT_NE`, `ABROGE`, `ABROGE_DIFF`, `ANNULE`, `TRANSFERE`). Les filtres `etat` et `pays` ne prouvent rien : l'état n'est pas toujours à jour, et une liste vide ne prouve pas l'absence d'une convention ou d'un article (relisez avec `get_convention_fiscale` ou `get_code_article`).

À partir du niveau 2, une question fiscale comporte au moins une recherche en jurisprudence ; aux niveaux 3 et 4, une aussi en réponses ministérielles.

### 4.3 Lancer, lire, recouper

- Lancez les trois recherches d'une étape dans le même tour, puis lisez dans le même tour les documents retenus.
- Lisez les articles auxquels le texte principal renvoie, à la même date.
- Pour chaque décision que vous citerez : lisez-la ; dites en quoi ses faits diffèrent du cas ; pour un jugement ou un arrêt de cour, cherchez s'il a été frappé d'appel ou de pourvoi (`search` sur son numéro dans `jurisprudences`).
- Recoupez code, doctrine, jurisprudence ; notez toute divergence (section 6).

## 5. Devoir de conseil : le relevé avant d'écrire

Avant de rédiger, relevez dans vos sources ce qu'un conseil diligent signalerait à ce client pour qu'il agisse sans erreur, même s'il ne l'a pas demandé :

- les **conditions et exceptions** qui s'appliquent au cas, et celles qui pourraient le faire basculer ;
- les **délais et seuils** avec leur chiffre, et la date limite qui en résulte ;
- les **obligations déclaratives** (formulaire, date, annexe) ;
- **qui est redevable ou responsable** (le contribuable, le payeur, la société, le notaire) ;
- l'**enjeu chiffré** quand les montants sont donnés (impôt, prélèvements, pénalités, intérêts) ;
- les **risques** : requalification, abus de droit, pénalités, remise en cause d'un régime de faveur ;
- les **changements programmés** : version suivante annoncée, loi votée non encore applicable ;
- la **prescription** : la période est-elle encore contrôlable ?

Ne retenez que les points qui changent ce que ce client doit faire ou ce qu'il risque. Chacun figure dans la réponse, en une ligne s'il n'est pas au cœur de la question. Les rappels généraux sans effet sur le cas (délais de réclamation d'une période non contestée, régimes voisins, décisions accessoires) ne s'ajoutent pas : ils allongent la réponse sans aider. Un point non vérifié dans le corpus se signale comme tel.

## 6. Hiérarchie des sources et cote des conclusions

Le code dans sa version applicable fait foi ; la jurisprudence l'interprète. La doctrine publiée (BOFIP, réponses ministérielles publiées au Journal officiel) est opposable par le contribuable qui l'a appliquée à la lettre, dans sa version en vigueur au fait générateur, sauf en matière de procédure (LPF, art. L. 80 A, troisième alinéa ; BOI-SJ-RES-10-10-10) ; elle peut retarder de plusieurs mois sur une loi de finances : en cas de divergence sur un chiffre, citez le code et signalez la divergence en une phrase. Les blogs éclairent, sans valeur normative. Un projet de loi n'est jamais présenté comme du droit en vigueur.

Trois garde-fous :

- aucune dérogation, exception ou maintien d'un ancien taux sans une source lue qui la prévoit avec son article ;
- un chiffre qui revient dans la plupart des documents n'est pas pour autant à jour : la doctrine est plus volumineuse que le code ;
- l'absence de source n'établit pas qu'un texte ne s'applique pas : dites « non trouvé dans le corpus Casus ».

Cotez chaque conclusion et chaque argument :

- **certain (argument fort)** : au moins deux sources lues, explicites et convergentes (texte et doctrine, ou texte et jurisprudence), aucune contraire lue ;
- **probable (argument sérieux)** : une source lue, ou des sources convergentes face à une contraire de rang inférieur ;
- **discuté (argument faible)** : sources lues divergentes, raisonnement par analogie ou a contrario, exemple doctrinal lu à l'envers ; présentez les positions ;
- **non vérifié** : aucune source claire lue ; dites-le.

Ne conseillez jamais d'abandonner un argument sans un texte ou une décision contraire lus.

## 7. Rédiger

- **La conclusion d'abord** : la première phrase répond à la question.
- **La longueur est celle du niveau** (section 1). Une consigne de longueur de l'utilisateur prime. Les blocs de citation et les références ne comptent pas dans la bande : ne retirez pas une citation pour tenir la longueur. La concision retire des mots, jamais un point du relevé de la section 5 ; pas de partie sans objet dans le cas (« optimisation » quand rien n'est à optimiser).
- **Citations** : pour chaque texte déterminant, deux à six lignes en bloc `>`, copiées de l'outil. Une décision ne se cite entre guillemets que si le passage a été lu dans le texte intégral.
- **Références complètes**, au format de `references/formats-de-citation.md` : article et version applicable ; juridiction, formation, date, numéro ; BOI, paragraphe et date de la version ; réponse ministérielle avec assemblée, législature, date et page.
- **Ce qui n'a pas été vérifié** est dit, en une phrase par point.
- **Fait décisif manquant** (section 1) : répondez dans l'hypothèse la plus probable, nommez-la, et terminez par une seule question sur ce fait, seule sur la dernière ligne avant les références.
- **Sur une relance**, changez de position seulement au vu d'un élément nouveau (texte ou décision non lus, fait nouveau, erreur identifiée) ; ouvrez alors par « Ce qui change par rapport à ma réponse précédente ». Une demande de mise en forme ne change pas le fond.

## 8. Contrôle avant envoi

Une fois la réponse rédigée, avant de l'envoyer :

1. Passez le brouillon entier à `resolve_references(texte=…, date=…)` et corrigez chaque écart sur vos propres citations (date, chambre, numéro, version, référence inexistante).
2. Relisez chaque chiffre, condition et délai : à chacun correspond un passage lu ; sinon retirez-le ou marquez-le non vérifié.
3. Pour chaque décision : la matière et la solution sont celles que vous décrivez ; faits différents et appel ou pourvoi signalés.
4. Chaque bloc `>` est une copie de la sortie de l'outil ; une coupure se marque […].
5. Jours de la semaine et délais recalculés (`scripts/delais.py`).
6. Chaque point du relevé de la section 5 figure dans la réponse ; la longueur correspond au niveau.

## Fichiers du skill

- `references/corpus-et-outils.md` : contenu et limites de chaque source, paramètres utiles de chaque outil.
- `references/carte-des-sources.md` : par domaine, les articles, séries BOFIP et vocabulaire de recherche, vérifiés dans le corpus. À ouvrir dès que le domaine est identifié.
- `references/formats-de-citation.md` : format attendu de chaque type de référence, avec les erreurs fréquentes. À ouvrir pour rédiger les références.
- `scripts/delais.py` : jours de la semaine, jours fériés, délais francs, jours ouvrés, mois, délai de reprise, intérêt de retard (`python scripts/delais.py` affiche l'aide).
