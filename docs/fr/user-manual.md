# Manuel utilisateur

> Version cible 0.6.0, préparation G0 : API HTTP `/api/v1` et contrat `Client` commun avec `LocalClient`/`RestClient`. Le schéma 8 et l’ABI 2 restent inchangés. Les anciennes routes `/api/...` répondent 404. Mettre à jour serveur, bureau, portail et proxy ensemble. Les descriptions fonctionnelles ci-dessous proviennent de la base 0.5.0 et restent valables sauf mise à jour par cette note. Core Foundation II, avec ABI V3 et sept langues d’interface, n’est pas encore terminé.


[Accueil](README.md) · [Installation](installation.md) · [Exploitation](operations.md)

**Édition :** 0.5.0 / 2026-09-09. Pour les équipes administratives, enseignants et
administrateurs. Les exemples sont fictifs. Les libellés allemands cités sont ceux
de l’application ; la visibilité dépend des droits et de la taille de l’écran.

## Sommaire

1. [Notions de base](#notions-de-base)
2. [Se connecter](#se-connecter)
3. [Organisations et hiérarchie](#organisations-et-hiérarchie)
4. [Dossier d’une personne](#dossier-dune-personne)
5. [Adhésions et fonctions](#adhésions-et-fonctions)
6. [Photos et pièces jointes](#photos-et-pièces-jointes)
7. [Arts martiaux](#arts-martiaux)
8. [Champs personnalisés](#champs-personnalisés)
9. [Modèles et exports](#modèles-et-exports)
10. [Apparence et aide](#apparence-et-aide)
11. [Administration](#administration)
12. [Incidents et contrôle quotidien](#incidents-et-contrôle-quotidien)

## Notions de base

Une **personne** représente un adhérent, enseignant, contact ou soutien. Un
**utilisateur** est un compte de connexion. Une personne peut être gérée sans compte
et aucun lien automatique avec l’utilisateur courant n’est créé.

Une **organisation** peut être école, club, fédération ou entreprise. Une
**adhésion** relie personne et organisation avec numéro, état et dates. Une
**fonction** décrit un poste ; une **relation** décrit une autre qualité de contact
ou de soutien. Ne pas dupliquer une personne pour représenter plusieurs adhésions.
Les droits viennent du compte, pas de la place d’une organisation dans la hiérarchie.

## Se connecter

1. Ouvrir l’application de bureau ou l’adresse HTTPS fournie par l’administrateur.
2. Vérifier le mode monoposte/serveur. Deux bases portant des noms identiques ne sont pas synchronisées automatiquement.
3. Saisir identifiant et mot de passe, puis choisir `Anmelden`.
4. Vérifier que les dossiers attendus sont accessibles.

`Administrator einrichten` est la création initiale de l’administrateur dans une
base monoposte neuve, pas la procédure normale pour ajouter un collègue.
Les comptes serveur sont créés par l’administration. Mot de passe : au moins
douze caractères. Après plusieurs échecs, patienter brièvement et vérifier les données.

Recharger le portail impose une nouvelle connexion. Par défaut, la session expire
après huit heures au maximum ou 30 minutes d’inactivité. Enregistrer avant une
pause et se déconnecter ; une page ouverte ne verrouille pas le poste. Le changement
de mot de passe se fait au bureau dans `Administration → Passwort ändern` ;
il n’existe pas encore de formulaire dédié dans le portail.

## Organisations et hiérarchie

Dans `Organisationen`, rechercher d’abord l’organisation pour éviter les doublons.
Choisir `Neu anlegen`, saisir le nom complet et le type : `Dachverband`
(fédération faîtière), `Landesverband` (fédération régionale), `Verein` (club),
`Sportschule` (école de sport), `Unternehmen` (entreprise), `Sonstige` (autre).
Compléter les informations connues : nom court, registre, date de création,
coordonnées, adresse et identifiants fédéraux. Choisir `Speichern`, rouvrir et contrôler.
Ne pas inventer de numéros pour remplir un champ facultatif.

Créer d’abord la fédération nationale, puis la régionale en sélectionnant la
nationale comme parente, enfin le club ou l’école en sélectionnant la régionale.
Utiliser une véritable référence à un enregistrement ; un nom saisi seul ne crée
pas une liaison. `Struktur` au bureau affiche les sous-organisations.
`Verbandszugehörigkeit` conserve les affiliations supplémentaires avec rôle et dates.
Une organisation ne peut pas devenir son propre ancêtre : corriger la chaîne plutôt
que créer un doublon. Aucune de ces liaisons ne donne de droits de connexion.

`Abteilungen` contient sections et disciplines. `Beiträge` contient groupes
tarifaires, monnaie et périodicité. Les montants sont en **centimes** : 25,00 EUR
se saisit `2500`. Ces données ne déclenchent aucun paiement. Membres, fonctions,
relations, contacts, adresses et fichiers sont accessibles dans le dossier ;
les vues exactes varient entre bureau et portail.

## Dossier d’une personne

1. Ouvrir `Personen` et rechercher prénom/nom.
2. Créer la personne, renseigner prénom et nom, enregistrer.
3. Ouvrir l’enregistrement ou `Akte öffnen`.
4. Compléter et enregistrer chaque section utile.

La recherche est littérale et sensible à la casse. Réduire le texte et vérifier
les pages suivantes si nécessaire : 100 résultats maximum par page ne représentent
pas forcément tout le fichier.

| Libellé | Usage |
|---|---|
| Übersicht | Identité, prénom et nom |
| Persönlich | Naissance, civilité, genre, responsable légal et contact d’urgence |
| Kontakt | Téléphone, courriel et autres moyens de contact nommés |
| Anschriften | Adresses avec une désignation claire |
| Mitgliedschaften | Organisation, numéro, état et dates d’adhésion |
| Funktionen | Fonctions et périodes de validité |
| Beziehungen | Autres relations avec des organisations |
| Dateien | Pièces jointes ; photo dans l’en-tête |
| Eigene Felder | Champs Core personnalisés autorisés, au bureau |
| Graduierungen / Prüfungshistorie | Graduations et examens après activation du module |
| Dokumente / Dokumentvorlagen | Production de documents pour la personne |

La saisie de date suit les paramètres système/navigateur ; l’API et les exports
techniques peuvent afficher `2026-09-08`. Respecter le format proposé par le champ.
Sur petit écran, `Aktenbereich` sélectionne la section. Au bureau,
`Entwurf behalten und schließen` conserve un brouillon marqué d’un point :
ce n’est **pas un enregistrement en base**. Dans le portail, enregistrer ou abandonner
volontairement le formulaire avant de changer de section. Un brouillon n’est pas sauvegardé.

## Adhésions et fonctions

Dans le dossier personnel, choisir `Mitgliedschaften → Neu anlegen`.
La personne est déjà fixée ; sélectionner explicitement l’organisation. Saisir
numéro d’adhérent, état, début, puis type, section, groupe tarifaire et sortie selon
le besoin. Depuis un dossier d’organisation, c’est l’organisation qui est fixée et
la personne qu’il faut sélectionner.

La fin ne peut pas précéder le début. `Aktiv`, `Ruhend`, `Beendet` signifient actif,
en pause et terminé ; ne pas les confondre avec l’activation d’un compte utilisateur.
Lors d’un départ, modifier l’adhésion existante avec date et motif, sans recréer
la personne. Facturation, relances, prélèvements et calcul juridique des préavis
ne sont pas automatisés dans cette version.

Dans `Funktionen`, saisir le poste et ses dates, par exemple enseignant ou direction.
Une fonction métier ne donne pas de droit logiciel : elle ne remplace pas
`martial.write`. Une personne peut cumuler plusieurs adhésions et fonctions.

## Photos et pièces jointes

La photo personnelle ou le logo organisationnel se place dans l’en-tête fixe.
Utiliser `Foto auswählen`, `Logo auswählen` ou `Foto / Logo hochladen`.
Formats prévus : PNG/JPEG. Les images sont redimensionnées ; une image démesurée
ou corrompue peut être refusée. La nouvelle image remplace l’ancienne du même dossier.

Pour contrats, attestations et autres pièces, ouvrir `Dateien` ou
`Unterlagen und Dateien`, puis `Datei hochladen`. Choisir le fichier, attendre la
confirmation et vérifier nom et dossier. Maximum 5 Mio, soit 5 × 1 024 × 1 024 octets.
Employer un nom significatif ; ne pas utiliser cet espace pour des identifiants
d’accès ni pour installer des bibliothèques exécutables.

Sélectionner le fichier ou `Herunterladen` et une destination. L’ouvrir ensuite
volontairement avec un logiciel adapté. Conserver l’original jusqu’à vérification
d’un téléchargement de contrôle. Il n’existe pas d’interface générale de suppression
en 0.5.0 ; contacter l’administration pour une pièce mal classée. Toutes les listes
de fichiers ne permettent pas la recherche par nom.

## Arts martiaux

L’administration doit placer la bibliothèque sur l’hôte et l’activer.
`Graduierungen` et `Prüfungshistorie` apparaissent alors dans les dossiers personnels.
Si les onglets manquent, vérifier connexion/activation ; en cas de refus d’accès,
faire vérifier également les permissions du module.

Une graduation comprend discipline/style, niveau 1–30, désignation libre,
date d’attribution et examinateur facultatif. Exemple : `Taekwon-Do`, niveau `8`,
`8. Kup`. Ces nombres neutres ne constituent pas une hiérarchie universelle entre
fédérations ; appliquer le règlement métier de la structure.

Un examen comprend discipline, niveau visé, date, résultat, examinateur et remarques
facultatives. Utiliser exactement `passed` (réussi) ou `failed` (échoué).
Enregistrer un examen ne crée pas automatiquement une graduation ou un certificat :
effectuer ces opérations séparément. Aucun contrôle automatique d’admissibilité
ni calcul de frais d’examen n’est fourni.

## Champs personnalisés

Au bureau, l’administration définit des champs supplémentaires par type de donnée :
texte, entier, décimal, booléen, date. Elle attribue ensuite les droits du champ aux
groupes. Les valeurs s’éditent dans `Eigene Felder` du dossier.

Avec un droit d’écriture seul, la valeur existante reste cachée. Un champ visuellement
vide ne signifie donc pas forcément absence de valeur. Vérifier et sauvegarder
les données avant changement de type : une seule valeur non convertible annule
la conversion complète. Le portail ne gère pas encore ces définitions et droits Core.

## Modèles et exports

Un administrateur crée titre et texte simple dans `Dokumentvorlagen`.
Seuls ces paramètres sont acceptés, sans traduction des clés :

```text
Attestation de participation

Nous attestons la participation de {{given_name}} {{family_name}}.
Date de délivrance : {{date}}
```

Ne pas inventer `{{member_number}}` ou un autre paramètre. Les inconnus sont refusés ;
le modèle n’exécute pas de code. Ouvrir le dossier de la personne concernée pour
choisir le destinataire des valeurs.

Au bureau : ouvrir un modèle enregistré dans `Dokumente`, choisir
`Gespeicherte Vorlage als PDF öffnen`, indiquer le fichier cible et contrôler dans
le lecteur PDF système. Au portail : `PDF-Vorschau`. Si le navigateur mobile
n’affiche pas le PDF intégré, utiliser `PDF öffnen` ou `Herunterladen`.
Contrôler nom, date, mise en page et texte avant diffusion. Aucun courriel n’est
expédié automatiquement. La date du modèle est actuellement insérée au format ISO.

Pour une liste, choisir d’abord ressource et filtre, puis `CSV exportieren` ou
`Gefilterte Liste exportieren`. Jusqu’à 5 000 éléments de toutes les pages sont
possibles ; éviter les modifications concurrentes durant l’export. Dans le tableur,
choisir UTF-8 et virgule. L’apostrophe initiale d’une valeur ressemblant à une formule
est une protection : ne pas la retirer sans examen. En cas de résultat vide,
vérifier filtres et droits.

## Apparence et aide

Au bureau : `Einstellungen → Ansicht → Darstellung und Farben`. Le mode système
suit clair/sombre ; cinq thèmes proposent notamment un contraste élevé. Le bureau
permet aussi les couleurs personnalisées. Au portail : `Einstellungen → Ansicht`,
mode système ou clair, sombre, forêt, prune, contraste élevé. Les couleurs libres
ne sont pas encore une fonction distincte du portail.

L’administrateur choisit logo et fond sous `Einstellungen → Startbildschirm` ou
les réglages correspondants du portail. Ils sont visibles **avant connexion** :
ne pas y placer d’informations confidentielles. Ce ne sont pas des photos personnelles.

Au bureau, `Hilfe → Nach Updates suchen` interroge les versions stables. Un dépôt
privé peut exiger des accès adaptés ; un échec ne prouve pas que la version est
à jour. Rien n’est installé automatiquement. Prévoir la mise à niveau avec
l’administration et la procédure d’exploitation.

## Administration

Créer un utilisateur, l’ajouter à un groupe, affecter un rôle au groupe, puis
accorder les permissions au rôle. Vérifier la chaîne entière. Lecture générale :
`records.read` ; adhésions : aussi `memberships.read` ; arts martiaux : aussi
`martial.read`. Ajouter les écritures uniquement si nécessaires. Ne pas distribuer
`*` pour masquer des erreurs non comprises.

Le dernier administrateur actif ne peut être désactivé ou privé de sa dernière
affectation administrateur. Pour un mot de passe perdu, utiliser la récupération
locale documentée ; aucun API public de remise à zéro administrateur n’existe.
Les fonctions métier ne sont pas des rôles de sécurité. Les champs exigent aussi
leurs permissions de groupe propres.

## Incidents et contrôle quotidien

| Observation | Action suivante |
|---|---|
| Blocage après saisie du nom | Vérifier action de création/enregistrement, message visible, taille de fenêtre et build |
| Modification invisible | Vérifier dossier/mode, actualiser et retirer le filtre |
| Accès refusé | Faire contrôler rôle, droits de champ et de module |
| Donnée modifiée ailleurs | Préserver les intentions, relire et comparer avant réécriture |
| Erreur réseau après sauvegarde | Vérifier si l’opération a déjà réussi avant de recommencer |
| Module absent | Faire contrôler chemin, activation et version |
| PDF non ouvert | Vérifier fichier, lecteur système ou “PDF öffnen” |
| Fichier trop volumineux | Préparer une copie réduite en conservant l’original |

En fin de journée, traiter les brouillons, relire les modifications importantes
et se déconnecter. Suivi des sauvegardes et exercices de restauration relèvent de
l’administration. Un ticket de support doit indiquer version, mode, heure, action
et erreur, sans mot de passe, jeton ou données personnelles inutiles.
