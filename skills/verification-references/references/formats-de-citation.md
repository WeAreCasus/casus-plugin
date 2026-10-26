# Formats de citation

Établi le 25/10/2026. Chaque exemple vient d'un résultat d'outil du corpus Casus (serveur casus-mcp) : get_decision, resolve_references, list_decisions, get_code_article, get_bofip, list_bofip, search_text, get_convention_fiscale, fetch. Les libellés renvoyés sont reproduits entre guillemets ; la forme proposée est celle attendue dans une consultation.

Règle générale : n'écrire un élément (formation, mention au Recueil, page, paragraphe) que s'il apparaît dans un résultat d'outil. resolve_references vérifie l'existence, le numéro et la date, pas la formation ni la mention au Recueil.

## Conseil d'État

Forme : CE, formation, date de lecture, n° numéro.

- Exemple : CE, 8e et 3e ch. réunies, 15 nov. 2021, n° 454105.
  get_decision : titre « France, Conseil d'État, 8ème - 3ème chambres réunies, 15 novembre 2021, 454105 » ; ECLI « ECLI:FR:CE:2021:454105.20211115 ». Le texte porte « Délibéré à l'issue de la séance du 22 octobre 2021 » et « Rendu le 15 novembre 2021 » : la date à citer est celle de la lecture.
- Chambre seule : le titre porte « 4ème chambre » (par exemple) ; on écrit « CE, 4e ch., date, n° … ».
- Avis contentieux : CE, avis, 5 avril 1996, n° 176611 (resolve_references : trouvée ; le BOFIP l'écrit « n° 176 611 »).
- Rec. / Tables : aucun résultat d'outil n'a affiché cette mention. resolve_references a renvoyé « trouvée » pour « CE, 15 novembre 2021, n° 454105, Rec. » sans contrôler la mention : ne pas l'ajouter sans source.
- Forme utilisée par le BOFIP : « CE, décision du 15 novembre 2021, n° 454105 » (titre de ACTU-2024-00216).

## Cour administrative d'appel

Forme : CAA ville, chambre, date, n° numéro.

- Exemple : CAA Lyon, 2e ch., 19 mars 2019, n° 17LY04048.
  get_decision : titre « France, Cour administrative d'appel de LYON, 2ème chambre - formation à 3, 19 mars 2019, 17LY04048 ». Pas d'ECLI dans le résultat.
- Le jugement attaqué y est cité « jugement n° 1501449 du 17 octobre 2017 » du tribunal administratif de Clermont-Ferrand. Il n'est pas dans le corpus (tribunaux administratifs couverts depuis le 22/06/2022) : le citer d'après l'arrêt, sans lien.

## Tribunal administratif

Forme : TA ville, nature si ce n'est pas un jugement, date, n° numéro.

- Exemple : TA Cergy-Pontoise, ord. réf., 9 oct. 2026, n° 2621928.
  get_decision : « Tribunal Administratif de Cergy-Pontoise — n° 2621928 — 09/10/2026 », sans titre, formation ni ECLI. La nature se lit dans le texte (« La juge des référés », « O R D O N N E ») ; lien opendata.justice-administrative.fr.

## Cour de cassation

Forme : Cass. chambre, date, n° de pourvoi avec point.

- Exemple : Cass. com., 7 juin 2011, n° 10-18.860.
  get_decision : « Cour de cassation, chambre commerciale — n° 10-18.860 — 07/06/2011 » ; titre « France, Cour de cassation, Chambre commerciale, 07 juin 2011, 10-18860 » ; ECLI « ECLI:FR:CCASS:2011:10.18860 » ; « Autres numéros connus : 41100587 ». Le texte se clôt sur « chambre commerciale, financière et économique ».
- Autre : Cass. com., 15 sept. 2009, n° 08-18.013 (resolve_references : trouvée ; le BOFIP écrit « pourvoi n° 08-18013 »).

## Conseil constitutionnel

Forme : Cons. const., date, n° numéro DC ou QPC.

- DC : Cons. const., 27 déc. 2019, n° 2019-796 DC ; ECLI « ECLI:FR:CC:2019:2019.796.DC » ; saisi « de la loi de finances pour 2020 » le 20 décembre 2019.
- QPC : Cons. const., 5 déc. 2025, n° 2025-1175 QPC ; ECLI « ECLI:FR:CC:2025:2025.1175.QPC ».
- Le numéro 2019-796 désigne aussi une QPC du 05/07/2019 : sans suffixe, resolve_references répond « ambiguë ».

## Cour de justice de l'Union européenne

Forme : CJUE, chambre, date, aff. C-numéro, nom, ECLI.

- Exemple : CJUE, 4e ch., 8 juill. 2021, aff. C-71/20, VAS Shipping, ECLI:EU:C:2021:550.
  get_decision : titre « CJUE, Arrêt de la Cour, Procédure pénale contre VAS Shipping ApS., 08/07/2021, C-71/20 » ; texte « ARRÊT DE LA COUR (quatrième chambre) ».
- Les conclusions de l'avocat général (10/06/2021) portent le même numéro : resolve_references répond « ambiguë » sans date.

## Cour européenne des droits de l'homme

Forme : CEDH, date, nom de l'affaire, n° de requête.

- Exemple : CEDH, 15 déc. 2025, Danileţ c. Roumanie, n° 16915/21.
  list_decisions : « n° 16915/21 — 15/12/2025 », libellé « CEDH, AFFAIRE DANILEŢ c. ROUMANIE, 2025, 001-247796 ». Le numéro 001-247796 n'est pas le numéro de requête. Formation non affichée par la liste. Corpus CEDH arrêté au 15/12/2025.

## Article de code, avec sa version

Forme : CGI, art. numéro, dans sa rédaction applicable à la date des faits (ou « en vigueur depuis le … »).

- Version actuelle : CGI, art. 197, dans sa rédaction applicable depuis le 21 février 2026 (get_code_article : « applicable depuis le 21/02/2026 », LEGIARTI000053542636).
- Version passée : CGI, art. 200 A, dans sa version applicable du 31 décembre 2020 au 21 février 2026 (get_code_article avec date 30/06/2024 : LEGIARTI000042909847).
- Autres libellés vus : « Article L284 — Livre des procédures fiscales — applicable depuis le 31/03/2000 » ; « Article 1 — Code civil — applicable depuis le 01/06/2004 ».

## Document BOFIP

Forme : BOI-série-…-AAAAMMJJ, § numéro.

- Exemple : BOI-CTX-DG-20-10-20-20130329, § 250.
  get_bofip : « Version du corpus Casus : en vigueur depuis le 29/03/2013 » ; lien « …identifiant=BOI-CTX-DG-20-10-20-20130329 ». Les paragraphes sont numérotés 1, 10, 20… avec des intercalaires (135, 295).
- resolve_references vérifie l'identifiant et la date de version, pas le paragraphe : lire le § avec get_bofip.

## Actualité BOFIP

Forme : BOFiP-Impôts, ACTU-AAAA-NNNNN du JJ/MM/AAAA, intitulé.

- Exemple : ACTU-2026-00081 du 22/07/2026, « BIC - IS - Sécurisation du régime des plus-values à long terme (loi n° 2026-103 du 19 février 2026 de finances pour 2026, art. 15) ».
- L'année de l'identifiant n'est pas l'année de publication : ACTU-2024-00216 est datée du 10/06/2026, ACTU-2020-00236 du 18/12/2024, ACTU-2025-00206 du 07/04/2026. Citer la date affichée par list_bofip.

## Réponse ministérielle

Forme : Rép. min. n° numéro (type, législature) : JOAN ou JO Sénat date de publication de la réponse, p. page.

- Assemblée nationale : Rép. min. n° 89485 (QE, 14e lég.) : JOAN 4 avr. 2017, p. 357 — libellé de resolve_references : « Rép. min. n° 89485 (QE, 14e lég.) : JOAN 04/04/2017, p. 357 (page non vérifiée) — Budget ».
- Sénat : Rép. min. n° 05059 (15e lég.) : JO Sénat 27 déc. 2018, p. 6762 (resolve_references : trouvée).
- Question orale : « Question orale sans débat n° 1586 (15e lég.) : JOAN 08/12/2021, p. 1573 (page non vérifiée) ».
- Le BOFIP cite avec le nom du parlementaire : « RM Serre n° 35810, JO AN du 15 février 2022, p. 993 » (ACTU-2022-00091). Sous cette forme : introuvable. Sous la forme « Rép. min. n° 35810, JOAN 15 février 2022, p. 993 » : trouvée avec écart, page 180 dans le corpus (non vérifiée). Page non tranchée.

## Convention fiscale

Forme : Convention fiscale entre la France et pays signée à lieu le date, art. numéro, § numéro.

- L'en-tête de get_convention_fiscale donne le pays, l'impôt et l'article, sans date de signature : la date et le lieu se lisent dans le texte, en général au dernier article (« Fait en deux exemplaires, à …, le … ») ou dans l'échange de lettres.
- Paragraphe : citer « art. N, § M » d'après le texte lu ; un protocole renvoie souvent à « l'article N, paragraphe M ».
- Texte OCR : l'outil demande de vérifier taux, seuils et numéros sur le PDF officiel (lien impots.gouv.fr).

## Acte de l'Union européenne

Forme : directive numéro du Conseil du date, art. numéro, § numéro, sous point.

- Exemple : directive 2006/112/CE du Conseil du 28 novembre 2006 relative au système commun de taxe sur la valeur ajoutée, art. 135, § 1, sous b).
  fetch eur_lex:32006L0112:art_135 : « 1. Les États membres exonèrent les opérations suivantes: […] b) l'octroi et la négociation de crédits […] ».
- metadata.version : « texte initial publié au JO (non consolidé) ». Le préciser si la rédaction en cause a pu être modifiée.

## Erreurs fréquentes à vérifier

Constatées pendant ce travail :

1. Formation du Conseil d'État : absente du libellé de resolve_references ; seul le titre de get_decision la donne (« 8ème - 3ème chambres réunies », « 4ème chambre »). Ne pas l'inventer.
2. Mention Rec. ou Tables : jamais affichée par les outils, et acceptée sans contrôle par resolve_references.
3. Date de lecture et autres dates : CE n° 454105 délibéré le 22/10/2021, rendu le 15/11/2021 ; conclusions CJUE C-71/20 du 10/06/2021, arrêt du 08/07/2021 ; 2019-796 DC saisi le 20/12/2019, décidée le 27/12/2019 ; LF 2024 datée du 29/12/2023, publiée au JO du 30/12/2023.
4. Pourvoi et numéro d'arrêt : Cass. com. 7 juin 2011 a pour pourvoi 10-18.860 et pour autre numéro 41100587 ; « n° 41100587 » n'est pas reconnu par resolve_references.
5. Suffixe DC ou QPC : « 2025-1175 DC » renvoie « trouvée avec écart » (c'est une QPC) ; 2019-796 existe en DC et en QPC.
6. Arrêt ou conclusions (CJUE) : même numéro d'affaire ; préciser la date.
7. Suffixe de date des BOI : « BOI-CTX-DG-20-10-20-20120912 » renvoie « version citée du 12/09/2012 ; version du corpus en vigueur depuis le 29/03/2013 ». Le lien servi pour BOI-RSA-ES-20-20-20 porte -20170724 alors que son texte cite une loi du 30/12/2025.
8. Année d'une actualité BOFIP : ACTU-2024-00216 est du 10/06/2026.
9. Date d'une loi dans un titre BOFIP : LF 2020 écrite « 29 décembre 2019 » (ACTU-2022-00041, au lieu du 28) ; LF 2023 « 29 décembre 2022 » (ACTU-2023-00059, au lieu du 30) ; LFR 2020 « 24 avril 2020 » dans le corps de ACTU-2020-00090 (au lieu du 25). Contrôler par le texte des codes (search_text, source codes).
10. Réponse ministérielle : législature (14e pour 2017, 15e pour 2018 à 2022) ; page de l'Assemblée nationale « non vérifiée » ; écart 993 / 180 sur le n° 35810 ; l'id Sénat du n° 05059 contient « p-2429 » alors que la page affichée est 6762 : ne jamais tirer une page d'un identifiant.
11. Numérotation des conventions : elle diffère d'une convention à l'autre (article des biens immobiliers, articles « bis ») ; ne jamais transposer la numérotation du modèle OCDE ou d'une autre convention : lister les articles avec get_convention_fiscale.
12. CEDH : citer le numéro de requête (16915/21), pas l'identifiant 001-247796.
13. ECLI : recopier celui que renvoie get_decision (ex. « ECLI:FR:CE:2021:454105.20211115 ») plutôt que de le reconstruire.
