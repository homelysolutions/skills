# Synthèse stable (JSON)

C'est la source de la fiche PDF et la base transmise aux autres skills. Même structure dans les trois modes.

Règles de remplissage :
- Une valeur absente = `""` ou `[]`. Le PDF affichera « à définir ». N'invente rien pour remplir.
- Dans les listes, préfixe si utile par `[proposé]` ce qui vient de toi et non du dirigeant. Les déclarations, hypothèses et inconnues vont aussi dans `fiabilite`.
- `statut` : `"à confirmer"`, `"provisoire"` ou `"validée"`. Si `"validée"`, remplis `validation.personne`, `validation.date` et `validation.portee` (sur quoi porte la validation).
- Une fiche par couple cible-offre. Chaque fiche a son propre prix et ses arguments.

```json
{
  "entreprise": {
    "nom": "",
    "activite": "",
    "zone": "",
    "situation": "",
    "direction": ""
  },
  "meta": {
    "date": "AAAA-MM-JJ",
    "version": "1",
    "origine": "entretien guidé avec le dirigeant | formulaire du JJ.MM | notes d'agence",
    "statut": "à confirmer",
    "validation": { "personne": "", "date": "", "portee": "", "corrections": "" }
  },
  "fiches": [
    {
      "segment": {
        "id": "S1",
        "intitule": "",
        "priorite": "prioritaire | secondaire",
        "situation": "",
        "roles": "qui utilise, recommande, décide, paie (B2B) ; vide en B2C simple",
        "exclusions": ""
      },
      "besoins": {
        "probleme": "",
        "declencheur": "",
        "resultat": ""
      },
      "achat": {
        "criteres": [],
        "objections": [],
        "alternatives": "",
        "action": "appel | devis | rendez-vous | achat | autre"
      },
      "offre": {
        "prestation": "",
        "benefice": "",
        "perimetre": "",
        "conditions": "",
        "difference": ""
      },
      "prix": {
        "valeur": "montant, fourchette ou règle de devis réelle ; vide si inconnu",
        "devise": "CHF | EUR | …",
        "statut": "confirmé | fourchette | sur devis | à définir",
        "a_confirmer": ""
      },
      "communication": {
        "vocabulaire": [],
        "ton": "",
        "arguments": [],
        "a_eviter": []
      },
      "fiabilite": {
        "declarations": [],
        "hypotheses": [],
        "inconnues": []
      },
      "statut": "facultatif : remplace meta.statut pour cette fiche"
    }
  ]
}
```

## Correspondance avec la fiche PDF

| Question de la fiche | Champs |
|---|---|
| 1. Qui est l'entreprise et où va-t-elle ? | `entreprise.*` |
| 2. À qui parle-t-on ? | `segment.*` |
| 3. Pourquoi cherche-t-elle une solution ? | `besoins.probleme`, `besoins.declencheur` |
| 4. Que veut-elle obtenir ? | `besoins.resultat` |
| 5. Qu'est-ce qui compte dans sa décision ? | `achat.criteres`, `achat.objections`, `achat.alternatives` |
| 6. Quelle offre ? | `offre.*` |
| 7. À quel prix ? | `prix.*` |
| 8. Comment lui parler ? | `communication.*` |
| 9. Quelle action proposer ? | `achat.action` |
| 10. Que reste-t-il à confirmer ? | `fiabilite.*`, `prix.a_confirmer` |

## Version texte pour les autres skills

Le script écrit aussi une synthèse `.md` dans ce format :

```
ENTREPRISE : nom, activité, zone, situation actuelle, direction souhaitée
SEGMENT : identifiant, intitulé, situation, rôles, exclusions
BESOINS : problème, déclencheur, résultat attendu
ACHAT : critères, objections, alternatives connues, action suivante
OFFRE : prestation, bénéfice, périmètre, conditions, différence crédible
PRIX : valeur ou règle, devise si connue, statut, points à confirmer
COMMUNICATION : vocabulaire client, ton souhaité, arguments et limites
FIABILITÉ : origine, date, déclarations, hypothèses, inconnues
VALIDATION : personne, date, corrections et portée de la validation
```
