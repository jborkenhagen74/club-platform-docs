# Développer une extension native

> Version cible 0.6.0, préparation G0 : API HTTP `/api/v1` et contrat `Client` commun avec `LocalClient`/`RestClient`. Le schéma 8 et l’ABI 2 restent inchangés. Les anciennes routes `/api/...` répondent 404. Mettre à jour serveur, bureau, portail et proxy ensemble. Les descriptions fonctionnelles ci-dessous proviennent de la base 0.5.0 et restent valables sauf mise à jour par cette note. Core Foundation II, avec ABI V3 et sept langues d’interface, n’est pas encore terminé.


[Accueil](../README.md) · [Interface](ui.md) · [Exemple](../../../examples/extensions/hello-extension/README.md)

L’hôte 0.5.0 attend **ABI 2**. `sdk/extension_api.h` conserve le projet historique
ABI 1 ; ses callbacks de cycle de vie, menus et routes ne sont pas utilisables
sur cet hôte. Employer `sdk/extension_v2.h`. La frontière C évite STL et libérations
entre modules, mais la bibliothèque doit correspondre à l’OS et à l’architecture CPU.

Les modules exécutent du code de confiance avec les privilèges du processus hôte.
Il n’existe pas de bac à sable. Protéger administrativement leur répertoire,
contrôler les bibliothèques avant diffusion et ne jamais charger depuis les
répertoires de téléversement ordinaires. Chargement au démarrage, sans hot reload.

## Point d’entrée et manifeste

Exporter `clubplatform_extension_v2`, qui renvoie une structure durable contenant
numéro ABI, manifeste UTF-8 et validateur. Les chaînes restent propriété du module.
Le validateur reçoit type de donnée et JSON sous forme de chaînes ; il retourne
exactement `1` en cas de succès. Aucune exception ne doit traverser l’ABI et aucun
handle de base de données n’est fourni.

Manifeste : `id`, `name`, `version`, `types`. La version comporte trois nombres.
L’ID de module ne contient pas de point ; les types commencent par `module.`.
Chaque type possède `key`, `label`, `fields` ; chaque champ `key`, `label`, `type`
et éventuellement `required:false`. Types : `text`, `integer`, `decimal`, `boolean`,
`date`. Les clés commencent par une minuscule et utilisent minuscules, chiffres,
soulignements et points pour les espaces de noms. Doublons et espaces étrangers
sont rejetés.

Tous les champs déclarés doivent être transmis, même les facultatifs avec une
chaîne vide. Les inconnus sont rejetés. L’hôte vérifie types et champs obligatoires
avant le validateur métier ; limite actuelle de 512 octets UTF-8 par valeur.
L’exemple enregistre des participations à l’entraînement avec le seul en-tête public :

```sh
cmake -S examples/extensions/hello-extension -B build/hello-extension -DCMAKE_BUILD_TYPE=Release
cmake --build build/hello-extension --config Release
```

Copier la bibliothèque dans un répertoire dédié ; sous Visual Studio, vérifier
le sous-dossier de configuration. Démarrer avec `--extensions /chemin/absolu` ou
`CLUBPLATFORM_EXTENSIONS`. Le bureau distant ne recharge pas les modules du serveur
sur le poste client.

## Activation et persistance

Un administrateur connecté choisit `Erweiterungen aktivieren` ou envoie `{}` à
`POST /api/v1/extensions/install`. Droit requis : `schema.manage`. Enregistrement des
types et manifeste sont transactionnels et audités. `GET /api/v1/extensions` donne
les manifestes chargés et `installed`. Réinstaller un manifeste identique est permis.

Les entrées natives appartiennent actuellement aux personnes. Exemple :
`/api/v1/management/ext:attendance.session`. `values` comprend aussi `person_id`,
retiré avant appel du validateur métier. Affecter `attendance.read/write` aux rôles
en complément de `records.read/write`. L’interface visible ne remplace pas ces contrôles.

Un manifeste déjà installé mais différent est refusé au chargement. Changer son
numéro de version ne migre pas les données. Prévoir migration explicite et sauvegarde
vérifiée avant évolution du schéma. Routes REST libres, tâches de fond et exécution
de QML/JavaScript embarqué ne font pas partie d’ABI 2.
