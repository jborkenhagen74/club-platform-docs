# Manuel utilisateur

## Connexion et dossiers

Connectez-vous avec votre compte. Les paramètres séparent langue d'interface et paramètres régionaux. Les modules nécessitent une licence, une activation et les droits appropriés. Le gestionnaire affiche aussi les modules découverts mais indisponibles.

Créez personnes et organisations. Les dossiers regroupent contacts, adresses, adhésions, fonctions et fichiers. Les organisations peuvent être hiérarchisées. Un compte utilisateur peut être lié à une personne, ce qui détermine les vues personnelles. Utilisez les champs de recherche, tri et filtre ; ouvrez une ligne pour modifier son dossier ou ses affectations.

## Droits et cycle de vie

Les administrateurs affectent groupes, rôles et permissions à l'aide de listes et d'explications. Un administrateur ne peut pas retirer ses propres droits administratifs effectifs. Testez avec un autre compte.

L'archivage est réversible. La suppression définitive est bloquée par les références ; un module manquant peut empêcher leur vérification. Les écritures financières sont corrigées par contrepassation, jamais effacées.

## Finances, cotisations et achats

Définissez la devise de l'organisation avant les données financières. Elle est ensuite verrouillée, sans conversion automatique. Saisissez des montants décimaux, par exemple `12,50` EUR. L'API utilise toujours les unités monétaires mineures entières.

Créez un compte de personne ou d'organisation. Les créances augmentent le solde dû ; les paiements le réduisent. Le montant payé est positif, son effet sur le solde est affiché séparément. Affectez les paiements aux créances ; paiements partiels et restes non affectés sont possibles. Corrigez par contrepassation et nouvelle écriture.

Les cotisations utilisent des plans et des adhésions ; les achats utilisent produits et lignes. Les comptes personnels apparaissent dans le dossier selon licence et droits. Les responsables voient les organisations autorisées.

## Banque

Choisissez éventuellement une créance ouverte. Les suggestions indiquent une référence ou un montant identique et nécessitent une confirmation. Le paiement partiel laisse le solde ouvert ; le trop-perçu reste disponible comme crédit. Affectez les autres créances dans le compte financier. Utilisez « Charger plus d’opérations » pour les imports volumineux.

Activez Finance et Banking. Dans Finances, ouvrez Banque, rechargez les comptes et créez un compte avec organisation, nom et IBAN. La devise vient de l'organisation.

Choisissez compte, CSV ou CAMT.053 et fichier UTF-8. Modifiez ou chargez la correspondance JSON des colonnes CSV ; le portail permet son export. Vérifiez dates, signes, devises et descriptions, puis confirmez l'import. L'import seul ne crée aucun paiement. Choisissez ensuite le compte financier et confirmez la comptabilisation.

Vérifiez les doublons possibles sans référence unique. Les débits restent à examiner manuellement et ne deviennent pas des encaissements. [Spécification technique et limites](../banking.md).

## Calendrier et événements

Cliquez sur un jour, saisissez le rendez-vous et affectez personne ou organisation. Vérifiez fuseau horaire et récurrence. La visibilité personnelle utilise le lien compte/personne ; les responsables doivent avoir une fonction actuelle et les permissions d'organisation. Les dossiers affichent les rendez-vous associés.

Les événements gèrent inscriptions, délais, places et liste d'attente. Les frais nécessitent Finance ; un événement gratuit ne nécessite pas Calendar. Les rappels sont internes à l'application, sans courriel ni notification push.

## Licences sportives et documents

Dans le dossier sportif, saisissez nom de licence, dates de délivrance et d'expiration, émetteur et préavis en jours. Plusieurs justificatifs sont possibles. Calendar affiche les échéances à partir des données de licence ; modifiez la licence pour les corriger.

Les modèles utilisent des variables enregistrées. Sélectionnez explicitement adresse, fonction ou examen en cas de choix multiples. Aperçu et rendu revérifient les droits. [Liste complète](placeholders.md).
