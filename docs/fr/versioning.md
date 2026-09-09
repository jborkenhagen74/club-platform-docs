# Versionnement et périmètre vérifiable

[Accueil](README.md)

Référence : application **0.5.0**, commit `320a4c2709c13dd56455768a2f8819a815ad3997`,
schéma **8**, ABI native **2**, édition documentaire **2026-09-09**.

| Couche | Contrat |
|---|---|
| Produit | Version du paquet 0.5.0 |
| Base | Migrations ordonnées ; définitions inconnues ou modifiées refusées |
| Extension | ABI 2 et version de manifeste à trois nombres |
| HTTP | Routes `/api` et `/health` séparé ; pas de `/api/v1` publié |
| Documentation | Même structure et périmètre dans de/en/fr/es/ko |

R1.9 apporte l’hôte natif, R1.10 les arts martiaux, R1.11 modèles/PDF/CSV et R1.12
les outils de pilote. Le statut pilote ne prouve ni des installateurs signés
universels ni la recette sur tous les postes. Les traductions ne changent pas
la langue de l’interface.

Le projet ABI 1 et `/api/v1` est historique. Ses callbacks menus, vues et REST ne
sont pas garantis en 0.5.0. Rendez-vous, paiements, mode hors ligne, isolation de
tenants, interface libre d’extensions, mises à jour automatiques et localisation
complète restent hors périmètre. Vérifier version du produit, ABI et routes ensemble.

Après évolution, synchroniser les cinq langues, mettre à jour la référence
implémentée et lancer la validation. Ne traduire ni identifiants, clés JSON,
URLs ni options de commandes. Le contrat de sécurité reste identique dans chaque langue.
