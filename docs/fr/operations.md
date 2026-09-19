# Exploitation et intégration

## Test local

Exécutez les commandes dans le dépôt privé du logiciel, pas dans ce dépôt documentaire. Prérequis : preset macOS configuré avec Qt, ICU, libxml2 et dépendances natives ; Node.js 22, version 22.12 minimum. `--init admin` ne s'exécute qu'une fois sur une nouvelle base ; le mot de passe est demandé. Gardez le serveur ouvert et lancez le deuxième bloc dans un autre terminal à la racine du projet. Ctrl+C arrête chaque processus. Cette base est distincte des données du bureau.

```bash
cmake --preset user-macos-vscode-debug
cmake --build --preset user-macos-vscode-debug --parallel
mkdir -p build/portal-test
./build/user-macos-vscode-debug/apps/server/clubplatform-server \
  --sqlite build/portal-test/data.sqlite --init admin
./build/user-macos-vscode-debug/apps/server/clubplatform-server \
  --sqlite build/portal-test/data.sqlite \
  --extensions "$PWD/build/user-macos-vscode-debug/runtime-extensions" \
  --port 8080 --portal-origin http://127.0.0.1:5173
```

```bash
cd apps/portal
npm ci
npm run dev -- --port 5173 --strictPort
```

http://127.0.0.1:5173

## Authentification et déploiement

`POST /api/v1/auth/login` reçoit `{"login":"…","password":"…"}` et retourne `token`, `user_id`, `login`, `expires_at`. Envoyez `Authorization: Bearer <token>` et gardez le jeton en mémoire. `GET /api/v1/auth/me` vérifie la session ; `POST /api/v1/auth/logout` la révoque. Valeurs par défaut : huit heures au maximum, 30 minutes d'inactivité, blocage de 30 secondes après cinq échecs. Le serveur vérifie droits et disponibilité des modules.

En production, un proxy HTTPS sert le portail et transmet `/api/v1` au serveur sur loopback. `--portal-origin` doit correspondre exactement à l'origine du navigateur. Préservez Origin et transmettez Host localhost/127.0.0.1. CORS n'authentifie pas cryptographiquement un portail : un client non navigateur peut omettre Origin. mTLS/BFF n'est pas implémenté. Aucun secret dans JavaScript.

## Licences et modules

1. Générez et protégez les clés privées de l'éditeur et de l'autorité hors du dépôt.
2. Déployez le service d'activation derrière HTTPS : [guide opérateur](../../tools/activation/README.md).
3. Définissez modules, limites, validité et politique d'activation. Banking exige `finance` et `banking`.
4. Signez avec la clé de l'éditeur et enregistrez la licence auprès de l'autorité. Ne distribuez que clés publiques et fichiers signés.
5. Configurez `CLUBPLATFORM_PINNED_LICENSE_KEY` pour les paquets de production. Les licences de développement anciennes ne protègent pas contre la copie.
6. Importez et activez la licence, puis installez et activez les modules. Le portail lie l'installation serveur, pas chaque navigateur.
7. Libérez l'ancienne installation avant transfert, puis activez le nouvel hôte. Le mode hors ligne doit être autorisé. La révocation hors ligne attend au plus l'expiration du bail.

Schémas : 18 banque, 17 activation, 16 devises, 15 lien utilisateur/personne, 14 calendrier/événements. Avant mise à jour : arrêter, sauvegarder et vérifier, puis déployer des versions compatibles. Une restauration sur un nouvel hôte nécessite une nouvelle activation.

## API et SDK

L'[index API](../api/overview.md) décrit les contrats. Les montants API sont des chaînes d'entiers en unités mineures. Révisions et identifiants source protègent modifications et répétitions. L'import bancaire requiert aperçu et confirmation : [contrat](../banking.md).

ABI V3 utilise une interface C et des manifestes. Les extensions natives sont du code de confiance dans le processus, sans sandbox. Le serveur possède persistance et autorisation. Voir [V3](../extension-v3.md), [variables](placeholders.md), [état d'acceptation](../status.md).

