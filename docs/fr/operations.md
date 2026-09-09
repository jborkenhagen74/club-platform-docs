# Exploitation, sauvegardes et mises à jour

> Version cible 0.6.0, préparation G0 : API HTTP `/api/v1` et contrat `Client` commun avec `LocalClient`/`RestClient`. Le schéma 8 et l’ABI 2 restent inchangés. Les anciennes routes `/api/...` répondent 404. Mettre à jour serveur, bureau, portail et proxy ensemble. Les descriptions fonctionnelles ci-dessous proviennent de la base 0.5.0 et restent valables sauf mise à jour par cette note. Core Foundation II, avec ABI V3 et sept langues d’interface, n’est pas encore terminé.


[Accueil](README.md) · [Installation](installation.md)

Séparer comptes de service, programmes, modules et données. Les utilisateurs du
portail ne doivent pas écrire dans le répertoire des modules. Les sauvegardes
contiennent données personnelles, fichiers et mots de passe hachés : restreindre
l’accès et protéger la destination. Les outils `scripts/pilot-*.py` appartiennent
au paquet d’implémentation, pas à ce dépôt public ; Python 3.11 ou ultérieur est requis.

> La compilation Windows et la restauration PostgreSQL nécessitent également le correctif `6ebb363ec28ab8631fb82a88051351f87659b523`. Il corrige le symbole du SDK Windows `LOAD_LIBRARY_SEARCH_DEFAULT_DIRS` et ajoute `--file=-` lors de l’export SQL par `pg_restore`. Le schéma et l’API restent inchangés. Le chemin de recherche configuré est également rétabli avant la révocation des sessions, car le dump le vide. Un test de régression vérifie qu’un échec de révocation annule aussi la restauration des tables.

## SQLite

```sh
python3 scripts/pilot-data.py backup data.sqlite sauvegarde-2026-09-09
python3 scripts/pilot-data.py diagnose sauvegarde-2026-09-09/database.sqlite
python3 scripts/pilot-data.py restore sauvegarde-2026-09-09 restauree.sqlite
```

La sauvegarde en ligne inclut les écritures WAL validées. Le répertoire cible ne
doit pas exister. Intégrité, clés étrangères, suite de migrations et SHA-256 sont
contrôlés. Un échec peut laisser un répertoire incomplet : sans manifeste valide,
ne pas le considérer comme sauvegarde exploitable.

La restauration crée une **nouvelle** base, vérifie son contenu et révoque les
sessions existantes. Arrêter ensuite l’hôte avant de modifier son chemin de base.
Conserver l’ancienne base jusqu’à validation fonctionnelle. Les documents sont
inclus ; programmes, modules, certificats et configuration doivent également pouvoir
être rétablis, par une sauvegarde distincte adaptée.

## PostgreSQL

Utiliser des versions de `pg_dump`, `pg_restore`, `psql` compatibles avec le serveur.
Configurer l’accès via `pg_service.conf`, `.pgpass` ou paramètres libpq protégés.
Créer une base cible neuve et vide avec son propre service ; ne pas démarrer d’hôte
sur cette base pendant la restauration.

```sh
python3 scripts/pilot-postgres.py backup --service club-production --directory pg-backup
python3 scripts/pilot-postgres.py restore --service club-restore --directory pg-backup
```

Archive au format custom et manifeste de somme de contrôle. La présence de tables
utilisateur bloque la restauration. Import et révocation des sessions partagent
une transaction. Propriétaires et ACL de l’ancien système ne sont pas réimportés ;
préparer séparément les rôles d’exploitation. Ne jamais restaurer sur des tables
actives de production.

## Procédure de mise à jour

1. Informer les utilisateurs, terminer les travaux et sauvegarder.
2. Placer nouveaux exécutables et modules compatibles dans un répertoire de version séparé.
3. Restaurer en base de test neuve ; démarrer le nouvel hôte pour vérifier/appliquer les migrations.
4. Tester connexion, modifications, adhésions, graduations, fichier, CSV et PDF, avec un compte restreint.
5. Arrêter la production ; après recette, basculer programmes/configuration et portail statique correspondant.
6. Recharger les navigateurs, se reconnecter et effectuer des contrôles métier.
7. Pour revenir en arrière, employer ancienne application **et sauvegarde antérieure aux migrations correspondante**.

Ne pas ouvrir une base migrée avec d’anciens exécutables. Les modifications
postérieures à la sauvegarde peuvent être perdues ; les traiter avant retour arrière.
La recherche de mises à jour n’installe rien. Signature, notarisation et diffusion
générale restent des étapes de livraison distinctes.

## Diagnostic et incidents

`clubplatform-server --sqlite BASE_TEST --diagnose` indique connexion et migrations
sans données de personnes. Attention : ouvrir l’hôte vérifie **et applique** les
migrations. `pilot-data.py diagnose` inspecte SQLite sans migration. Pour le support,
noter version, mode, heure et message, sans mots de passe ni jetons.

Si Git manque de suivi de branche, sélectionner la branche voulue puis définir
une fois `git branch --set-upstream-to=origin/feature/core-foundation
feature/core-foundation`, avant `git pull --ff-only`. Ne pas écraser les changements
locaux par reset forcé. Un `403` nécessite droits et configuration proxy/origin.
Pour une extension absente, vérifier chemin, CPU, ABI, manifeste installé et activation.
Ne pas modifier manuellement tables de migrations ou manifestes pour contourner le contrôle.
