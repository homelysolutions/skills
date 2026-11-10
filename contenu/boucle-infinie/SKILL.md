---
name: boucle-infinie
description: Mène un gros projet sur des dizaines de tâches sans que Claude perde le fil, avec la méthode « Ralph Wiggum » (Geoffrey Huntley) - un fichier PLAN.md découpé en petites tâches cochables est la seule source de vérité, chaque séance prend la première tâche non faite, l'implémente, la teste, la sauvegarde, coche le plan, puis repart d'un contexte neuf. À utiliser quand l'utilisateur dit « boucle infinie », « plan-driven », « Ralph », « découpe le projet en tâches », « crée un PLAN.md », « continue le plan », ou lance un chantier trop gros pour une seule conversation.
---

# La Boucle Infinie

Une conversation longue dégrade la qualité. La solution : **1 tâche = 1 contexte frais**, et le plan écrit garde la mémoire.

## Créer le plan (première fois)

Crée `PLAN.md` à la racine du projet :

```markdown
# Plan : <objectif en une phrase>

## Règles
- Une tâche à la fois, dans l'ordre.
- Une tâche est finie quand ses tests passent et qu'elle est sauvegardée (commit).

## Tâches
- [ ] 1. <tâche courte, vérifiable> - Test : <comment on sait que c'est fait>
- [ ] 2. ...

## Notes
<décisions prises, pièges découverts, à lire avant chaque tâche>
```

Chaque tâche doit tenir en une séance (environ 30 minutes de travail), avoir un critère de fin vérifiable et ne dépendre que des tâches d'avant. Si une tâche est trop grosse, découpe-la. Montre le plan à l'utilisateur et attends son accord avant de commencer.

## La boucle (chaque séance)

1. **Lis le plan complet**, y compris les Notes.
2. **Prends la première tâche non cochée.** Une seule.
3. **Implémente, puis teste** selon le critère de la tâche.
4. **Sauvegarde** : commit avec un message clair, si le projet utilise Git.
5. **Mets à jour PLAN.md** : coche la tâche, ajoute dans Notes ce que la prochaine séance doit savoir.
6. **Arrête-toi** et dis : « Tâche n terminée. Pour la suivante, ouvre une nouvelle conversation (ou /clear) et dis : continue le plan. »

Si un test échoue et que tu ne trouves pas en deux essais : ne coche pas, écris le blocage dans Notes et arrête-toi.

## Règles

- **Le plan est la seule source de vérité.** Ce qui n'est pas dans PLAN.md n'existe pas pour la séance suivante.
- Ne saute jamais une tâche, n'en fais jamais deux d'un coup.
- Si tu découvres une tâche manquante, ajoute-la au plan au bon endroit au lieu de la faire tout de suite.
- Les règles du projet (CLAUDE.md) priment sur cette méthode.
