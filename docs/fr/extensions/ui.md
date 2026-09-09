# Contributions déclaratives à l’interface

> Version cible 0.6.0, préparation G0 : API HTTP `/api/v1` et contrat `Client` commun avec `LocalClient`/`RestClient`. Le schéma 8 et l’ABI 2 restent inchangés. Les anciennes routes `/api/...` répondent 404. Mettre à jour serveur, bureau, portail et proxy ensemble. Les descriptions fonctionnelles ci-dessous proviennent de la base 0.5.0 et restent valables sauf mise à jour par cette note. Core Foundation II, avec ABI V3 et sept langues d’interface, n’est pas encore terminé.


[Accueil](../README.md) · [Développement](getting-started.md)

ABI 2 décrit types et champs. Bureau et portail génèrent des onglets et formulaires
dans les **dossiers des personnes**. Un manifeste ne définit pas librement menus,
widgets ou scripts ; ces types ne sont pas automatiquement ajoutés aux dossiers
d’organisations.

Le `label` du type devient le nom de l’onglet ; celui du champ devient son libellé.
`integer` désigne un entier et `date` voyage en ISO. L’affichage utilise les paramètres
régionaux du système ou navigateur. Signaler les champs facultatifs et transmettre
une chaîne vide en l’absence de valeur. Les clés techniques ne se traduisent pas ;
les labels de 0.5.0 sont des chaînes simples, pas des dictionnaires multilingues.

Les droits sont contrôlés de nouveau à la lecture et à l’enregistrement. Un refus
peut donc survenir après ouverture du dossier. Conserver les révisions et traiter
`409` par comparaison, jamais par écrasement forcé. Un onglet visible ne prouve
pas l’autorisation d’écrire.

Pour la recette, charger/activer comme administrateur, ouvrir une personne,
renseigner les champs obligatoires, enregistrer et rouvrir. Tester date invalide
et valeur métier refusée. Vérifier ensuite qu’un lecteur peut consulter mais pas
modifier. Contrôler les deux interfaces et une fenêtre étroite. Le module d’arts
martiaux illustre désignations libres et niveaux 1–30, sans imposer une échelle
universelle aux fédérations.
