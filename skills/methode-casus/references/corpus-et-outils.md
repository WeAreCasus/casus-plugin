# Corpus et outils du connecteur Casus

Détail des sources et des outils, à ouvrir au premier doute sur une source ou un paramètre.

## Ce que contient le corpus

| Source (`sources`) | Contenu | À savoir |
|---|---|---|
| `codes` | articles des codes, base Légifrance | Historique inégal : pour le CGI, le LPF et le CSS, il couvre en général les dates depuis le 1er janvier 2014 ; pour d'autres codes (Code civil, Code de commerce…), il peut se réduire à la version en vigueur. Une date antérieure à la plus ancienne version donne INDÉTERMINÉ, et c'est la bonne réponse. Une version dont la fin précède le début (état MODIFIE_MORT_NE) n'a jamais été appliquée. |
| `bofip` | doctrine (« Contenu ») et actualités | Une seule version par document ; l'en-tête dit depuis quand, et jusqu'où le BOFIP est intégré. |
| `jurisprudences` | décisions françaises et européennes, texte intégral | Pas d'index plein texte : `search_text` la refuse. |
| `reponses_ministerielles` | Assemblée nationale et Sénat | Un même numéro existe dans les deux assemblées et à plusieurs législatures. |
| `conventions_fiscales` | conventions signées par la France | Texte issu d'une reconnaissance optique : vérifiez taux et numéros sur le PDF officiel (lien fourni). |
| `eur_lex` | actes de l'Union européenne | Texte initial publié, non consolidé (`metadata.version`). |
| `blogs` | articles de cabinets et de revues | Éclairage, jamais une source normative. |

Les lois elles-mêmes ne sont pas une source : leurs dispositions non codifiées (entrée en vigueur, mesures transitoires) se retrouvent par les actualités BOFIP et les blogs. Chaque source s'arrête à une date (`catalogue(type="sources")`) ; au-delà, le corpus ne sait rien.

## Quel outil pour quelle question

| Besoin | Outil | Paramètres utiles |
|---|---|---|
| Lire un article connu | `get_code_article` | `code` (CGI, LPF, CSS, C. com.…), `numeros` (dix au plus), `date`, `detail="complet"` pour la frise des versions et les textes qui le citent |
| Retrouver une décision connue | `get_decision` | `numero` ou `ecli` ; `juridiction` et `date` en cas d'homonymie ; `detail="complet"` et `offset` pour tout lire |
| Lire un BOI ou une actualité | `get_bofip` | le mode concis donne le sommaire avec l'offset de chaque section ; `detail="complet"` et `offset` pour une section |
| Lire une convention fiscale | `get_convention_fiscale` | `pays` en français ; sans `article`, la liste des articles |
| Vérifier des citations | `resolve_references` | `texte` (jusqu'à 100 000 caractères) ou `references` (50 au plus), `date` |
| Question ouverte | `search`, puis `fetch` | une ou deux `sources` par appel ; `texte_integral=true` quand vous lirez de toute façon plusieurs des décisions trouvées ; `pays` (conventions) et `etat` (codes) filtrent en amont |
| Formulation exacte, numéro de loi | `search_text` | une seule `source` ; `code` ou `serie` ; une seule expression entre guillemets par requête ; accents obligatoires |
| Nom de code, pays, juridiction ; couverture | `catalogue` | `type` = `codes`, `conventions`, `juridictions`, `sources` |
| Trouver un article sans son numéro | `get_code_plan` | `code`, `article` pour ses voisins, `chemin` pour déplier |
| Actualité d'une juridiction ou du BOFIP | `list_decisions`, `list_bofip` | `date_min`, `date_max` ; `nature="Actualité"`, `depuis` |

`search` ne prouve pas qu'un texte existe ou non : une référence précise se lit par l'outil `get_*`. Les articles renvoyés par `search` et `search_text` sont ceux d'aujourd'hui : relisez-les avec `get_code_article` et `date`.
