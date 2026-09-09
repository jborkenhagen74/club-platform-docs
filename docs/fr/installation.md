# Installation et mise en service

> Version cible 0.6.0, préparation G0 : API HTTP `/api/v1` et contrat `Client` commun avec `LocalClient`/`RestClient`. Le schéma 8 et l’ABI 2 restent inchangés. Les anciennes routes `/api/...` répondent 404. Mettre à jour serveur, bureau, portail et proxy ensemble. Les descriptions fonctionnelles ci-dessous proviennent de la base 0.5.0 et restent valables sauf mise à jour par cette note. Core Foundation II, avec ABI V3 et sept langues d’interface, n’est pas encore terminé.


[Accueil](README.md) · [Exploitation et restauration](operations.md)

## Préparer l’installation

Sauvegarder une installation existante avant modification. Séparer données,
configuration et programmes. Adapter les chemins d’exemple ; ne jamais utiliser
une base de production pour un test automatisé.

Une archive n’est pas un installateur universel. Les bibliothèques système et,
pour le bureau, une exécution Qt compatible doivent être présentes. La distribution
peut intégrer Qt avec l’option de déploiement du produit. Les commandes de compilation
supposent l’accès au dépôt d’implémentation ; ce dépôt public ne contient pas
l’application propriétaire.

| Système | Référence du projet |
|---|---|
| Windows | Visual Studio 2026 ; MSVC v143/14.44 pour Qt 6.11.2 `msvc2022_64` ; IncrediBuild facultatif |
| macOS | Xcode complet, Apple Clang, VS Code, Ninja, ccache, Qt 6.11.2 `macos` |
| Linux | Compilateur C++23, CMake/Ninja, SQLite, libsodium, cpp-httplib, nlohmann-json ; Qt pour le bureau |
| Portail | Version prise en charge de Node 22, au moins 22.12, et npm |

Ce sont les références du projet, pas l’annonce des dernières versions disponibles.
PostgreSQL nécessite aussi libpq. `QT_ROOT` désigne le SDK de la plateforme.
Ne pas committer la configuration locale `CMakeUserPresets.json`.

Si macOS utilise seulement les Command Line Tools, sélectionner Xcode installé :

```sh
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
sudo xcodebuild -runFirstLaunch
xcodebuild -version
export QT_ROOT="$HOME/Qt/6.11.2/macos"
```

Dans le dépôt d’implémentation :

```sh
./scripts/init-dev-macos.sh
./scripts/verify-dev-macos.sh
cmake --preset user-macos-vscode-debug
cmake --build --preset user-macos-vscode-debug --parallel
ctest --preset user-macos-vscode-debug --output-on-failure
```

Sous Windows, définir `QT_ROOT`, par exemple `C:\Qt\6.11.2\msvc2022_64`, ouvrir un
nouveau terminal et exécuter `scripts\init-dev-windows.ps1` puis
`scripts\verify-dev-windows.ps1`. Le script IncrediBuild accepte
`-Configuration Debug -Desktop`. Ne pas partager les répertoires de compilation
entre systèmes. Quick 3D/Shader Tools concernent les fonctions graphiques associées ;
WebEngine n’est pas nécessaire au portail web indépendant.

## Monoposte et serveur

```sh
clubplatform-desktop --database /chemin/club/data.sqlite \
  --extensions /chemin/club/extensions
```

Une base neuve propose la création du premier administrateur. Choisir un mot de
passe d’au moins douze caractères, se connecter puis activer les extensions dans
`Administration`. La bibliothèque doit déjà exister dans le répertoire configuré.

Pour le serveur, initialiser localement puis démarrer :

```sh
clubplatform-server --sqlite /chemin/club/data.sqlite --init admin
clubplatform-server --sqlite /chemin/club/data.sqlite \
  --extensions /chemin/club/extensions \
  --portal-origin https://gestion.example
```

`--password-stdin` est prévu pour une automatisation maîtrisée. Ne pas exposer les
secrets dans les arguments, Git ou les journaux. Pour PostgreSQL, utiliser
`--postgres` et fournir `CLUBPLATFORM_POSTGRESQL` par une configuration protégée.
Choisir exactement un fournisseur de base.

Le bureau distant utilise `--server https://gestion.example`. Son chemin de base
locale n’est pas une copie hors ligne du serveur. Comptes, droits et modules sont
configurés sur le serveur. L’accès distant passe par HTTPS et un proxy correct ;
HTTP est réservé à la boucle locale.

## Héberger le portail

```sh
cd apps/portal
npm ci
npm run build
```

Copier le contenu de `dist/` dans la racine documentaire HTTPS. Aucun processus
Node n’est nécessaire pour servir ces fichiers. Rediriger `/api/v1/` vers
`127.0.0.1:8080`, fixer le `Host` amont à `127.0.0.1:8080`, conserver `Origin` et
`Authorization`. `--portal-origin` correspond exactement à l’origine du navigateur,
sans barre finale. Le portail fonctionne à `/` ; un sous-chemin arbitraire n’est
pas une fonctionnalité de configuration achevée en 0.5.0.

En développement, Vite utilise normalement `http://127.0.0.1:5173` : autoriser
cette origine exacte. `CLUB_API` modifie la cible du proxy de développement.
`npm run dev` n’est pas un serveur de production.

## Recette

Avec des données de test, vérifier connexion, création/enregistrement/relecture,
organisation, adhésion, photo, téléchargement binaire, graduation, CSV et PDF.
Un compte restreint doit se voir refuser une écriture non autorisée. Restaurer
réellement une sauvegarde dans une nouvelle base et vérifier l’invalidation des
anciennes sessions. Contrôler les dialogues natifs et le lecteur PDF sur chaque OS.
Une compilation réussie ne remplace pas la recette fonctionnelle.

## Exemple de proxy inverse HTTPS

Ajoutez cette configuration Nginx à l’hôte virtuel TLS existant. Adaptez la racine des fichiers et configurez le certificat et l’écoute HTTPS dans l’environnement serveur. La limite accepte le téléversement JSON maximal; l’application contrôle toujours la taille du fichier décodé. Démarrez le service avec exactement la même origine publique.

```nginx
root /srv/club-platform/portal;
client_max_body_size 8m;

location / {
    try_files $uri $uri/ /index.html;
}

location /api/v1/ {
    proxy_pass http://127.0.0.1:8080;
    proxy_set_header Host 127.0.0.1:8080;
    proxy_set_header Origin $http_origin;
    proxy_set_header Authorization $http_authorization;
}
```
