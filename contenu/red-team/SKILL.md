---
name: red-team
description: Fait passer un contenu (post, article, page, script, offre) devant 20 profils de lecteurs hostiles en 3 passes - hypothèses non prouvées, scénario catastrophe, affirmations sans source marquées [SANS PREUVE] - puis le note sur 10 ; en dessous de 7/10, la publication est déconseillée. Chaque revue est consignée dans attack-log.md. À utiliser quand l'utilisateur dit « red team », « sentinel », « attaque mon contenu », « trouve les failles », « qu'est-ce qu'on pourrait me reprocher », ou avant de publier un contenu exposé (réseaux sociaux, presse, page publique).
---

# Le Red Team

Objectif : que l'audience ne trouve rien que tu n'aies pas déjà trouvé.

## Les 20 profils d'attaque

Lis le contenu successivement avec les yeux de chacun :

1. Le concurrent direct
2. L'expert du domaine pointilleux
3. Le journaliste qui cherche une erreur
4. Le client déçu
5. Le sceptique qui demande « source ? »
6. Le juriste (promesse, publicité trompeuse, droit des consommateurs)
7. Le régulateur de la plateforme (règles Meta, TikTok, Google…)
8. Le débutant qui ne connaît aucun jargon
9. Le lecteur pressé qui ne lit que le titre et la première ligne
10. Le comptable qui refait les calculs
11. Le troll qui sort une phrase de son contexte
12. La personne qui se sent visée ou exclue
13. Le lecteur d'un autre pays ou d'une autre culture
14. L'ancien collègue qui connaît la réalité de l'entreprise
15. Le client fidèle qui voit une contradiction avec ce qui a été dit avant
16. Le militant (éthique, écologie, inclusion)
17. Le fact-checker
18. L'investisseur qui cherche l'exagération
19. L'utilisateur en situation de handicap (lisibilité, accessibilité)
20. Le futur toi, dans un an, qui relit ce texte

Ne restitue que les profils qui trouvent quelque chose.

## Les 3 passes

1. **Hypothèses non prouvées** : ce que le texte tient pour acquis sans le démontrer.
2. **Scénario catastrophe** : la pire lecture possible, la capture d'écran qui tourne mal, le commentaire qui fait le buzz contre toi. Probabilité (faible, moyenne, forte) et parade.
3. **Affirmations sans source** : chaque chiffre, superlatif ou fait vérifiable sans source est recopié et marqué **[SANS PREUVE]**.

Pour chaque problème : citation exacte, profil qui l'a trouvé, gravité (CRITIQUE, IMPORTANT, MINEUR), correction proposée.

## Score et décision

- **Score : X/10**. En dessous de 7/10 : **publication déconseillée**, liste des corrections obligatoires.
- À partir de 7/10 : publiable, avec les corrections facultatives.

## Journal

Ajoute une entrée à `attack-log.md` à la racine du projet courant (crée le fichier s'il n'existe pas) :

```
## AAAA-MM-JJ - <titre du contenu>
Score : X/10 - Décision : <publiable | à corriger>
Failles critiques : <liste courte>
```

Avant une nouvelle revue, lis ce journal : si une faille déjà signalée revient, dis-le.
