# Casus

![Casus](assets/logo.png)

Plugin Casus pour Claude : recherche juridique et fiscale française sourcée, par WE ARE CASUS SAS, la legaltech des fiscalistes et des juristes.

## Contenu

- **Connecteur MCP Casus** (`.mcp.json`) : le serveur distant `https://mcp.wearecasus.com/mcp`, en lecture seule, sur le corpus juridique et fiscal de Casus (articles de codes lus dans leur version applicable à une date, plus de 3,4 millions de décisions de justice, doctrine BOFIP, actes de l'Union européenne, réponses ministérielles, conventions fiscales, articles de blogs). Documentation : https://mcp.wearecasus.com/
- **Cinq skills** (`skills/`) qui guident Claude avec les outils du connecteur :
  - `methode-casus` : méthode de recherche, carte des sources, date des faits, citation exacte avec le lien, contrôle avant envoi ;
  - `verification-references` : contrôle de toutes les références d'une note, de conclusions ou d'un courrier avant envoi ;
  - `comparaison-versions` : ce qui a changé dans un article de code entre deux dates ;
  - `recherche-a-date` : le régime applicable à la date des faits ;
  - `reponse-proposition-rectification` : préparation de la réponse à une proposition de rectification (délais, procédure, chefs de redressement, plan de la lettre).

## Prérequis

Un compte Casus (https://app.wearecasus.com) avec un abonnement actif. À la première utilisation, Claude ouvre l'écran de connexion et de consentement Casus (OAuth) ; l'accès accordé est en lecture seule (scope `legal:read`). Les cinq skills sont incluses dans le plugin. Servies par le serveur MCP (ressources `skill://`), `reponse-proposition-rectification` est réservée aux offres Pro, essai et organisation.

## Installation

Depuis l'annuaire de claude.ai (Paramètres > Plugins), ou dans Claude Code :

```
/plugin install casus --marketplace WeAreCasus/casus-plugin
```

## Données

Le plugin n'envoie de données qu'au serveur MCP Casus déclaré dans `.mcp.json` : les requêtes et références que Claude transmet aux outils du connecteur. Aucune autre destination. Les scripts des skills (`scripts/delais.py`, `scripts/comparer_versions.py`) utilisent uniquement la bibliothèque standard Python, sans accès réseau : ils calculent des délais et comparent deux textes fournis. Politique de confidentialité : https://wearecasus.co/privacy-policy

## Support

https://wearecasus.co/contact-us

## Licence

© WE ARE CASUS SAS. Tous droits réservés. Licence propriétaire : voir [LICENSE](LICENSE).
