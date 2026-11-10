---
name: reality-check
description: Vérifie qu'un travail annoncé comme « terminé » fonctionne vraiment et pas seulement en démo - cas normal exécuté pour de vrai, gestion d'erreurs réelle, connexions branchées, cas limites couverts - avec une gravité par problème (CRITIQUE à FAIBLE) et un score de crédibilité sur 10 ; en dessous de 6/10, on ne livre pas. À utiliser quand l'utilisateur dit « reality check », « karen », « est-ce que c'est vraiment fini », « vérifie avant de livrer », ou avant d'annoncer qu'une fonction, une page ou une automatisation est terminée.
---

# Le Reality Check

« Terminé » veut dire : ça marche pour un vrai utilisateur, avec de vraies données, quand quelque chose se passe mal.

Règle de base : **on vérifie en exécutant**, pas en relisant. Lance les tests, l'application, la commande, la requête. Si tu ne peux pas exécuter quelque chose, dis-le explicitement : un point non vérifié n'est jamais compté comme réussi.

## Les 5 contrôles

1. **Le cas normal fonctionne en vrai ?** Parcours complet avec des données réalistes, du début à la fin. Pas de donnée codée en dur, pas de faux client (mock) qui masque le vrai appel, pas de « TODO ».
2. **La gestion d'erreurs est réelle ?** Que se passe-t-il si le réseau coupe, si l'API répond une erreur, si le champ est vide, si l'utilisateur n'a pas les droits ? Un message clair est-il affiché ? Rien n'est avalé en silence ?
3. **Les connexions sont branchées ?** Base de données, API, e-mails, webhooks, variables d'environnement : chaque connexion est réellement appelée (pas un bouton qui ne fait rien, pas une route jamais reliée à l'interface).
4. **Les cas limites sont couverts ?** Liste vide, texte très long, caractères spéciaux et accents, double clic, deux utilisateurs en même temps, fuseau horaire, montants à zéro ou négatifs, téléphone mobile.
5. **Score de crédibilité : X/10.** Probabilité qu'un vrai utilisateur ne rencontre aucun problème cette semaine.

## Rapport

Pour chaque problème :

- 🔴 **CRITIQUE** : ça casse ou ça perd des données.
- 🟠 **IMPORTANT** : ça marche mal ou trompe l'utilisateur.
- 🟡 **FAIBLE** : finition.

Avec : où (fichier, écran, étape), comment le reproduire, correction proposée.

## Décision

- Score **en dessous de 6/10** : **ne pas livrer**. Liste ce qui doit être corrigé avant.
- À partir de 6/10 : livrable, avec la liste des réserves à annoncer honnêtement.

Ne dis jamais « tout fonctionne » si un contrôle n'a pas pu être exécuté.
