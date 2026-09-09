# Contrat REST et règles d’intégration

[Accueil](../README.md) · [OpenAPI](../../../openapi/club-platform.yaml)

## Routes disponibles

La version 0.5.0 utilise `/api`, **pas `/api/v1`**. `/health` est hors de ce préfixe.
Une méthode interne ne constitue pas automatiquement une route HTTP. Les rendez-vous,
`/members`, l’affichage d’audit et les callbacks arbitraires de l’ancien projet ne
sont pas des routes implémentées.

| Domaine | Routes |
|---|---|
| Session | `POST /api/auth/login`, `GET /api/auth/me`, `POST /api/auth/logout`, `POST /api/auth/password` |
| Personnes | `GET/POST /api/persons`, `GET/PUT /api/persons/{id}` |
| Gestion | `GET/POST /api/management/{resource}` |
| Fichiers | `GET/POST /api/assets`, `GET /api/assets/{id}`, `GET /api/branding` public |
| Extensions | `GET /api/extensions`, `POST /api/extensions/install` |
| Documents | `POST /api/documents/render`, `GET /api/reports` |
| Sécurité/champs | Routes utilisateurs, groupes, rôles et champs décrites dans OpenAPI |

## Session et représentation

La connexion transmet `{"login":"…","password":"…"}`. La réponse contient
`user_id`, `login`, `expires_at` en secondes Unix et un jeton. Les appels suivants
portent `Authorization: Bearer TOKEN`. À réception de `401`, supprimer la session
locale et demander une nouvelle connexion. Ne jamais conserver mot de passe ou
jeton dans le stockage persistant du navigateur.

Les requêtes JSON exigent `Content-Type: application/json`. Les valeurs génériques
sont des chaînes : `"8"`, `"true"`, `"2026-09-08"`. Les routes de sécurité dédiées
emploient de vrais booléens JSON pour `enabled`, `active`, `read`, `write`.
Les révisions restent des chaînes. Les identifiants sont généralement des UUID ;
les ressources d’association peuvent employer des identifiants composites.

Création d’une personne :

```json
{"given_name":"Erika","family_name":"Mustermann"}
```

Modification par `PUT /api/persons/{id}` :

```json
{"revision":"1","given_name":"Erika","family_name":"Muster"}
```

Une création générique utilise `{"id":"","revision":"0","values":{…}}`.
Une modification reprend identifiant et révision lus. Toutes les ressources ne
sont pas modifiables : `persons` et `organization_children` sont des vues de lecture.
Modifier les personnes par la route dédiée ou `person_identity`. Les associations
possèdent une sémantique d’activation propre.

## Ressources et pagination

Les dossiers utilisent `organizations`, `person_profiles`, `contacts`, `addresses`,
`relationships`, `memberships`, `positions`, `departments`, `fee_groups`,
`organization_affiliations`. Contacts/adresses utilisent `entity_id`, données
personnelles `person_id`, sections organisationnelles `organization_id`.
`owner` filtre selon le dossier et la ressource, sans accorder de droits.

Administration : `users`, `groups`, `roles`, `group_members`, `group_roles`,
`role_permissions`, `field_definitions`, `field_permissions`, `field_values`.
Modèles : `document_templates`. Données natives : `ext:martial.graduation`,
`ext:martial.exam`. La [référence des champs](../../../reference/resources.md)
liste les clés exactes. Ne pas renvoyer `labels` comme valeurs ; envoyer les IDs.
Certaines ressources exigent une liste exacte de champs et refusent les inconnus.

Au plus 100 éléments par page. `after` reprend le dernier curseur ; `q` effectue
une recherche littérale sensible à la casse. Suivre `next_cursor` jusqu’à `null`
lorsqu’il est présent. Pour les fichiers, ce champ n’existe pas : après 100 résultats,
utiliser la dernière ID comme `after`, puis arrêter sur une page courte ou vide.
Les modèles ignorent actuellement les filtres de recherche et d’owner. Tous les
filtres ne sont pas disponibles sur toutes les ressources.

## Fichiers, documents et erreurs

L’envoi de fichier transmet `owner`, `purpose`, `filename`, `media_type` et
`content` Base64 sans préfixe Data URI. `file`/`photo` appartiennent à une personne
ou organisation ; `logo`/`background` utilisent un owner vide et `security.manage`.
Les listes donnent les métadonnées, la lecture individuelle le contenu. L’identité
visuelle est publique avant connexion : aucune information confidentielle dans ces images.

`/api/documents/render` reçoit `template_id`, `person_id`, `date` et renvoie
`title`, `body`, **pas un PDF**. Le client génère le PDF ; la date de transport reste
ISO. `/api/reports` produit du CSV UTF-8 avec BOM pour personnes, organisations,
adhésions, fonctions et données natives, limité à 5 000 lignes. Réduire le filtre
au-delà ; le résultat paginé n’est pas un instantané transactionnel.

| Statut | Action |
|---|---|
| 400 | Vérifier JSON, champs, types et valeurs obligatoires |
| 401 | Abandonner la session et se reconnecter |
| 403 | Vérifier droits et configuration Host/Origin |
| 404 | Vérifier identifiant et ressource existante |
| 409 | Relire, comparer, modifier consciemment la nouvelle révision |
| 500 | Faire examiner l’opération, sans répétition aveugle |

Une écriture ayant expiré côté client peut déjà être validée : relire avant de
réessayer. Pas de clés d’idempotence générales ni de transactions HTTP par lots.
JSON standard : 16 Kio maximum ; fichiers : limite HTTP de 8 Mio et limites du
contenu décodé. Une seule origine exacte est autorisée. Preflight par
`OPTIONS /api/…` ; `Host` amont `localhost` ou `127.0.0.1`, avec port facultatif.
Les clients distants passent par le proxy HTTPS.
