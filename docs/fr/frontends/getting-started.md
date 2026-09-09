# Frontends et intégration web

[Accueil](../README.md) · [REST](../api/overview.md) · [Installation](../installation.md)

Le portail utilise React/TypeScript et Tailwind 4. `npm ci` suit le fichier de
verrouillage ; `npm run build` produit `dist/`. Code PDF et polices proviennent du
build, chargés au besoin, sans CDN obligatoire. `examples/frontends/web-basic`
démontre seulement connexion et liste des personnes.

Servir navigateur et API derrière la même origine HTTPS. Le proxy transmet `/api/`
à la boucle locale, avec `Host: 127.0.0.1:8080`, en conservant `Authorization` et
`Origin`. Configurer exactement cette origine dans `--portal-origin`. Sans cela,
les requêtes portant Origin sont refusées. Ne pas remplacer une configuration
correcte par une autorisation universelle.

Pour une supervision publique, configurer `/health` séparément : le proxy `/api/`
ne l’inclut pas. Ne pas journaliser corps de requêtes, mots de passe ou jetons.
DNS, certificats et comptes de service relèvent de l’exploitation ; l’application
ne gère pas automatiquement les certificats.

## Comportement du client

Garder le jeton en mémoire, jamais dans les URL ou stockages persistants. Sur `401`,
effacer session, listes personnelles et brouillons, puis redemander la connexion.
Expliquer `403`. Après une erreur réseau d’écriture, relire avant répétition ;
après `409`, comparer la révision actuelle.

Paginer les listes. Afficher des noms de référence lisibles avec `labels` ou les
données liées, tout en envoyant les IDs. Rendre le texte comme texte, pas comme
HTML. Ne télécharger un fichier qu’à la suite d’une action explicite. Aucun fichier
téléversé n’est exécuté comme extension.

## Apparence et périmètre

Les thèmes clair, sombre, forêt, prune et contraste élevé complètent le mode
système. Les dates affichées suivent les paramètres régionaux ; l’API conserve ISO.
Sur petit écran, `Aktenbereich` sélectionne la section du dossier. Les définitions
et droits des champs personnalisés Core restent administrés au bureau. Le compte
n’est pas automatiquement associé à son propre dossier d’adhérent.

Utiliser ensemble [OpenAPI](../../../openapi/club-platform.yaml) et la
[référence des champs](../../../reference/resources.md). Ne pas reprendre les
routes inexistantes de l’ancien projet, telles que `/api/v1/appointments`.
Vérifier la compatibilité avant une mise à jour du produit.
