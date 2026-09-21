# Référence des formulaires

Cette référence répertorie tous les champs des actions financières et de planification disponibles. Ouvrez le domaine, sélectionnez l’action, puis renseignez les champs. Vérifiez avant d’enregistrer/confirmer, puis rechargez. Créez d’abord les données liées pour alimenter les listes. Les captures montrent les vrais formulaires avec des données de test, pas une validation comptable.

[Retour au manuel](handbook.md) · [Screenshots](../images/pilot/README.md)

## Finances

### Créer un compte

`finance` · `account.create`

| Champ | Saisie | Obligatoire |
|---|---|---|
| Titulaire (personne ou organisation) | Sélection | Obligatoire |
| Organisation | Sélection | Obligatoire |

![Créer un compte (DE)](../images/pilot/desktop/finance-operation-00.png)

### Comptabiliser une créance

`finance` · `receivable.create`

| Champ | Saisie | Obligatoire |
|---|---|---|
| Compte | Sélection | Obligatoire |
| Montant | Montant dans la devise de l’organisation | Obligatoire |
| Date comptable | Date | Obligatoire |
| Échéance | Date | Obligatoire |
| Description / libellé | Texte | Obligatoire |

![Comptabiliser une créance (DE)](../images/pilot/desktop/finance-operation-01.png)

### Enregistrer un paiement

`finance` · `payment.create`

| Champ | Saisie | Obligatoire |
|---|---|---|
| Compte | Sélection | Obligatoire |
| Montant | Montant dans la devise de l’organisation | Obligatoire |
| Date comptable | Date | Obligatoire |
| Description / libellé | Texte | Obligatoire |
| Référence du paiement | Texte | Obligatoire |

![Enregistrer un paiement (DE)](../images/pilot/desktop/finance-operation-02.png)

### Affecter un paiement

`finance` · `allocation.create`

| Champ | Saisie | Obligatoire |
|---|---|---|
| Paiement | Sélection | Obligatoire |
| Créance | Sélection | Obligatoire |
| Montant | Montant dans la devise de l’organisation | Obligatoire |

![Affecter un paiement (DE)](../images/pilot/desktop/finance-operation-03.png)

### Contrepasser une écriture

`finance` · `entry.reverse`

| Champ | Saisie | Obligatoire |
|---|---|---|
| Écriture | Sélection | Obligatoire |
| Date comptable | Date | Obligatoire |
| Description / libellé | Texte | Obligatoire |

![Contrepasser une écriture (DE)](../images/pilot/desktop/finance-operation-04.png)

### Créer un barème de cotisations

`contributions` · `plan.create`

| Champ | Saisie | Obligatoire |
|---|---|---|
| Organisation | Sélection | Obligatoire |
| Nom | Texte | Obligatoire |
| Montant | Montant dans la devise de l’organisation | Obligatoire |
| Intervalle (1, 3, 6 ou 12 mois) | Entier | Obligatoire |
| Valable à partir du | Date | Obligatoire |
| Valable jusqu’au | Date | Obligatoire |
| Jour d’échéance du mois (1–31) | Entier | Obligatoire |

![Créer un barème de cotisations (DE)](../images/pilot/desktop/finance-operation-05.png)

### Attribuer une cotisation

`contributions` · `assignment.create`

| Champ | Saisie | Obligatoire |
|---|---|---|
| Adhésions | Sélection | Obligatoire |
| Barème de cotisations | Sélection | Obligatoire |
| Compte | Sélection | Obligatoire |
| Valable à partir du | Date | Obligatoire |
| Valable jusqu’au | Date | Obligatoire |
| Montant personnalisé | Montant dans la devise de l’organisation | Facultatif |
| Réduction (100 = 1 %, 10000 = 100 %) | Entier | Obligatoire |

![Attribuer une cotisation (DE)](../images/pilot/desktop/finance-operation-06.png)

### Terminer l’attribution

`contributions` · `assignment.end`

| Champ | Saisie | Obligatoire |
|---|---|---|
| Attribution de cotisation | Sélection | Obligatoire |
| Valable jusqu’au | Date | Obligatoire |

![Terminer l’attribution (DE)](../images/pilot/desktop/finance-operation-07.png)

### Facturer les cotisations

`contributions` · `contributions.bill`

| Champ | Saisie | Obligatoire |
|---|---|---|
| Attribution de cotisation | Sélection | Obligatoire |
| Facturer jusqu’au (inclus) | Date | Obligatoire |

![Facturer les cotisations (DE)](../images/pilot/desktop/finance-operation-08.png)

### Enregistrer une relance

`contributions` · `reminder.create`

| Champ | Saisie | Obligatoire |
|---|---|---|
| Créance | Sélection | Obligatoire |
| Date de relance | Date | Obligatoire |
| Délai de paiement | Date | Obligatoire |
| Frais | Montant dans la devise de l’organisation | Obligatoire |
| Description / libellé | Texte | Obligatoire |

![Enregistrer une relance (DE)](../images/pilot/desktop/finance-operation-09.png)

### Créer un produit

`purchases` · `product.create`

| Champ | Saisie | Obligatoire |
|---|---|---|
| Organisation | Sélection | Obligatoire |
| Nom | Texte | Obligatoire |
| Description / libellé | Texte | Obligatoire |
| Prix | Montant dans la devise de l’organisation | Obligatoire |

![Créer un produit (DE)](../images/pilot/desktop/finance-operation-10.png)

### Modifier un produit

`purchases` · `product.update`

| Champ | Saisie | Obligatoire |
|---|---|---|
| Produit | Sélection | Obligatoire |
| Révision du produit | Entier | Obligatoire |
| Nom | Texte | Obligatoire |
| Description / libellé | Texte | Obligatoire |
| Prix | Montant dans la devise de l’organisation | Obligatoire |
| Actif | Oui/Non | Obligatoire |

![Modifier un produit (DE)](../images/pilot/desktop/finance-operation-11.png)

### Comptabiliser un achat

`purchases` · `purchase.post`

| Champ | Saisie | Obligatoire |
|---|---|---|
| Compte | Sélection | Obligatoire |
| Date comptable | Date | Obligatoire |
| Échéance | Date | Obligatoire |
| Description / libellé | Texte | Obligatoire |

Lignes d’achat: Produit · Quantité · Ajouter une ligne / Retirer la ligne.

![Comptabiliser un achat (DE)](../images/pilot/desktop/finance-operation-12.png)

### Comptabiliser un retour

`purchases` · `purchase.return`

| Champ | Saisie | Obligatoire |
|---|---|---|
| Ligne d’achat | Sélection | Obligatoire |
| Quantité | Entier | Obligatoire |
| Date comptable | Date | Obligatoire |
| Description / libellé | Texte | Obligatoire |

![Comptabiliser un retour (DE)](../images/pilot/desktop/finance-operation-13.png)

## Calendrier et événements

### Créer une entrée

`calendar` · `create`

| Champ | Saisie | Obligatoire |
|---|---|---|
| Titre | Texte | Obligatoire |
| Description / libellé | Texte | Obligatoire |
| Lieu | Texte | Obligatoire |
| Personne ou organisation associée | Sélection | Obligatoire |
| Début | Date et heure | Obligatoire |
| Fin | Date et heure | Obligatoire |
| Fuseau horaire | Texte | Obligatoire |
| Toute la journée | Oui/Non | Obligatoire |
| Heure répétée au changement d’heure | earlier, later | Obligatoire |
| Répétition | none, DAILY, WEEKLY, MONTHLY | Obligatoire |
| Intervalle de répétition | Entier | Obligatoire |
| Nombre d’occurrences (366 maximum) | Entier | Obligatoire |

### Annuler une occurrence

`calendar` · `cancel`

| Champ | Saisie | Obligatoire |
|---|---|---|
| Occurrence | Sélection | Obligatoire |

### Définir un rappel

`calendar` · `remind`

| Champ | Saisie | Obligatoire |
|---|---|---|
| Occurrence | Sélection | Obligatoire |
| Rappel : minutes avant | Entier | Obligatoire |

### Marquer le rappel comme terminé

`calendar` · `acknowledge`

| Champ | Saisie | Obligatoire |
|---|---|---|
| Rappel | Sélection | Obligatoire |

### Créer un événement

`events` · `create`

| Champ | Saisie | Obligatoire |
|---|---|---|
| Titre | Texte | Obligatoire |
| Description / libellé | Texte | Obligatoire |
| Catégorie | Texte | Obligatoire |
| Lieu | Texte | Obligatoire |
| Organisation | Sélection | Obligatoire |
| Responsable | Sélection | Obligatoire |
| Début | Date et heure | Obligatoire |
| Fin | Date et heure | Obligatoire |
| Fuseau horaire | Texte | Obligatoire |
| Toute la journée | Oui/Non | Obligatoire |
| Heure répétée au changement d’heure | earlier, later | Obligatoire |
| Répétition | none, DAILY, WEEKLY, MONTHLY | Obligatoire |
| Intervalle de répétition | Entier | Obligatoire |
| Nombre d’occurrences (366 maximum) | Entier | Obligatoire |
| Ouverture des inscriptions | Date et heure | Obligatoire |
| Clôture des inscriptions | Date et heure | Obligatoire |
| Places par occurrence | Entier | Obligatoire |
| Frais de participation | Montant dans la devise de l’organisation | Obligatoire |
| Devise | Texte | Obligatoire |

### Inscrire / inviter un participant

`events` · `register`

| Champ | Saisie | Obligatoire |
|---|---|---|
| Occurrence | Sélection | Obligatoire |
| Personne | Sélection | Obligatoire |
| Compte | Sélection | Facultatif |
| État | registered, invited | Obligatoire |

### Modifier le statut du participant

`events` · `participant`

| Champ | Saisie | Obligatoire |
|---|---|---|
| Participant | Sélection | Obligatoire |
| Version de l’entrée | Entier | Obligatoire |
| État | registered, confirmed, cancelled, attended, no_show | Obligatoire |

### Modifier la capacité

`events` · `capacity`

| Champ | Saisie | Obligatoire |
|---|---|---|
| Occurrence | Sélection | Obligatoire |
| Capacité précédente | Entier | Obligatoire |
| Places par occurrence | Entier | Obligatoire |

### Annuler une date d’événement

`events` · `cancel`

| Champ | Saisie | Obligatoire |
|---|---|---|
| Occurrence | Sélection | Obligatoire |
