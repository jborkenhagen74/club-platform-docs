# Architecture et modèle de sécurité

Le contrôleur du bureau utilise uniquement l’interface commune `Client`. `LocalClient` accède aux services authentifiés du cœur dans le processus ; `RestClient` effectue les mêmes opérations via `/api/v1`. Le choix se fait au démarrage. Le contrôleur UI ne dépend pas des cibles de compilation host, application ou persistence.

> Version cible 0.6.0, préparation G0 : API HTTP `/api/v1` et contrat `Client` commun avec `LocalClient`/`RestClient`. Le schéma 8 et l’ABI 2 restent inchangés. Les anciennes routes `/api/...` répondent 404. Mettre à jour serveur, bureau, portail et proxy ensemble. Les descriptions fonctionnelles ci-dessous proviennent de la base 0.5.0 et restent valables sauf mise à jour par cette note. Core Foundation II, avec ABI V3 et sept langues d’interface, n’est pas encore terminé.


[Accueil](README.md) · [Manuel utilisateur](user-manual.md)

## Périmètre

Cette édition décrit **Club Platform 0.5.0**, commit
`320a4c2709c13dd56455768a2f8819a815ad3997`, schéma de base de données 8 et ABI
d’extension 2. Version du produit, migrations et ABI constituent des contrats
distincts. La traduction de la documentation ne signifie pas que l’interface,
actuellement surtout en allemand, est intégralement traduite.

Le logiciel gère personnes, organisations, adhésions, fonctions, contacts, fichiers
et données sportives. Une personne peut être liée à plusieurs organisations.
Un compte utilisateur sert à se connecter : créer une personne ne crée pas de
compte et ne la rattache pas automatiquement à l’utilisateur courant.
Une organisation peut être une fédération nationale ou régionale, un club,
une école de sport, une entreprise ou une autre structure.

## Modes de fonctionnement

| Mode | Interface | Traitement et stockage |
|---|---|---|
| Monoposte | Qt Quick/QML | Hôte local, SQLite et services applicatifs communs |
| Bureau connecté | Qt Quick/QML | REST via HTTPS ; le serveur possède la connexion à la base |
| Portail web | React/TypeScript, Tailwind 4 | Fichiers statiques et proxy HTTPS vers le serveur C++ |

L’application résout la session et vérifie les droits pour chaque opération.
Le client ne choisit pas l’identité agissante : les objets REST contenant `actor`
ou `actor_id` sont rejetés. Le serveur écoute sur `127.0.0.1` ; un proxy inverse
assure TLS et l’accès public. Les clients ne doivent pas accéder directement à
la base du serveur. SQLite et PostgreSQL sont des alternatives, pas deux bases
synchronisées automatiquement.

Le bureau connecté ne dispose pas de cache d’écriture hors ligne. Le portail
conserve le jeton uniquement en mémoire ; recharger la page exige une nouvelle
connexion. Seul le choix d’apparence est enregistré localement dans le navigateur.

## Modèle des données

Les UUID identifient les enregistrements indépendamment du nom ou du numéro
d’adhérent. Une modification transmet la révision précédemment lue ; un conflit
évite d’écraser une modification concurrente. Les révisions REST sont des chaînes
décimales pour éviter les arrondis de grands entiers en JavaScript.

Le dossier d’une personne rassemble identité, renseignements personnels, contacts,
adresses, relations, adhésions, fonctions, champs personnalisés et fichiers.
Une adhésion relie personne et organisation ; section et groupe tarifaire sont
des affectations complémentaires. Un groupe tarifaire est une donnée de référence,
pas un moteur automatique de facturation, paiement ou prélèvement SEPA.

L’organisation parente forme une hiérarchie : fédération nationale → fédération
régionale → école de sport. Les affiliations supplémentaires sont des relations
séparées. Cette hiérarchie n’accorde aucun droit et ne constitue pas une frontière
de sécurité entre tenants. Les cycles entre parents sont interdits.

Les champs personnalisés possèdent définition, type, droits de groupe et valeurs.
Lecture et écriture sont indépendantes ; un droit d’écriture seul ne révèle pas
la valeur existante. Un changement de type doit convertir toutes les valeurs ;
si une conversion échoue, l’ensemble du changement est annulé.

## Authentification et autorisation

Les mots de passe sont hachés avec Argon2id ; les jetons sont également stockés
sous forme hachée côté serveur. Valeurs par défaut : durée absolue de huit heures,
inactivité maximale de 30 minutes et blocage de 30 secondes après cinq échecs de
connexion. Éviter les boucles de tentatives rapides.

La chaîne est utilisateur → groupes → rôles → permissions. Sans droit explicite,
l’accès est refusé. `records.read/write` concerne les données générales ;
`memberships.read/write`, les adhésions et fonctions. `security.manage` administre
comptes et identité visuelle ; `schema.manage`, définitions, modèles et installation
d’extensions. `audit.read` appartient à l’API applicative : aucune route HTTP
d’audit dédiée n’est exposée en 0.5.0. `*` donne un accès administrateur étendu.
Au moins un administrateur actif doit subsister.

Les droits des champs s’ajoutent aux droits généraux. Les données d’arts martiaux
nécessitent aussi `martial.read` ou `martial.write`. Le produit ne limite pas
automatiquement chaque compte à « sa » personne ou organisation. Le portail est
un outil d’administration contrôlé par droits, pas un espace adhérent autonome achevé.

## Fichiers et limites

Le contenu des fichiers est stocké dans la base et inclus dans sa sauvegarde.
Limite ordinaire : 5 Mio ; photos et identité visuelle : 2 Mio côté service.
Les interfaces redimensionnent les PNG/JPEG et limitent la surface à 16 mégapixels.
Une nouvelle image de profil remplace l’ancienne. Le téléversement de documents
n’installe jamais d’extension native.

Les modifications et leurs traces d’audit sont transactionnelles. SQLite sérialise
les écritures ; PostgreSQL utilise ses mécanismes de transaction et de verrouillage.
Un export CSV paginé n’est toutefois pas un instantané transactionnel.

Ne pas supposer disponibles : installateurs signés universels, installation
automatique des mises à jour, paiements, rendez-vous, synchronisation hors ligne,
isolation multi-tenant, envoi automatique de documents ou menus/routes libres
d’extensions. Voir le [périmètre versionné](versioning.md).
