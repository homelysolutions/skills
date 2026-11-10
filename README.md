# Mes skills Claude

Copie de sauvegarde des skills repérés sur TikTok, pour ne jamais les perdre.
Chaque skill est un dossier avec un fichier `SKILL.md` : Claude le lit quand la tâche s'y prête.

Copiés le 10.11.2026 depuis GitHub. Licences d'origine dans `licences/`.

## Ce qu'il y a dedans

| Skill | À quoi il sert | Source (commit) | Licence |
|---|---|---|---|
| `ponytail` (+ `-review`, `-audit`, `-debt`, `-gain`, `-help`) | Pousse Claude vers la solution la plus simple qui marche, sans code inutile | DietrichGebert/ponytail (96608e0) | MIT |
| `graphify` | Transforme un dossier ou un dépôt en carte de connaissances (graphe) | safishamsi/graphify (5eedffa) | MIT / Apache 2.0 |
| 18 skills d'Emil Kowalski (`emil-design-eng`, `animate`, `apple-design`, `break-ui`, `mobile-native`…) | Finition des interfaces et des animations | emilkowalski/skills (715c180) | MIT |
| `impeccable` | Concevoir, critiquer et peaufiner une interface | pbakaus/impeccable (ec229b4) | Apache 2.0 |
| `taste-skill` | Sites vitrines au rendu professionnel, sans effet « fait par une IA » | Leonxlnx/taste-skill (f6b7657) | MIT |
| 13 skills Instagram (`ig-caption`, `ig-carousel`, `ig-reel`, `ig-plan`, `ig-human`…) | Rédiger et planifier le contenu Instagram | Jakeschincariol/instagram-agent-skill (d03c56b) | MIT |
| Pack `seo-geo` (16 skills : `keyword-research`, `technical-seo-checker`, `rank-tracker`, `geo-content-optimizer`, `offsite-signal-analyzer`, `domain-authority-auditor`…) | Les 5 skills SEO du carrousel Murmur : mots-clés, audit technique, optimisation du contenu, liens entrants, suivi des positions | aaron-he-zhu/aaron-marketing-skills (3017529) | Apache 2.0 |
| Plugin `claude-seo` (26 skills, 19 agents, commande `/seo`) | Audit SEO d'un site : `/seo audit https://exemple.ch` | AgriciDaniel/claude-seo (6be93f4) | MIT |

### Dossier `contenu/` : 5 skills qui attaquent ton contenu avant ton audience

Écrits pour toi d'après le carrousel « 5 Skills Claude » d'automatise_avec_igor (ses fichiers d'origine ne sont pas publics).

| Skill | Quand l'appeler |
|---|---|
| `avocat-du-diable` | Reformule ton idée, puis 5 failles citées et corrigées, verdict PUBLIABLE ou RETRAVAILLER |
| `red-team` | 20 lecteurs hostiles, 3 passes, [SANS PREUVE], note sur 10, journal `attack-log.md` |
| `reality-check` | Vérifie qu'un travail « terminé » marche vraiment ; ne pas livrer en dessous de 6/10 |
| `boucle-infinie` | Gros projet découpé dans `PLAN.md`, une tâche par conversation (méthode Ralph Wiggum) |
| `aigle-superviseur` | Contrôle final en 7 passes ; un seul échec bloque la publication |

Ce sont des skills à appeler (« passe l'aigle sur ce post »), pas des règles qui bloquent tout automatiquement.

### Dossier `perso/` : mes propres skills

Écrits pour moi, sans source externe. Ce sont aussi ceux enregistrés sur mon compte Claude.

| Skill | À quoi il sert |
|---|---|
| `redacteur-marketing` | Rédige ou audite un contenu marketing (blog, article, landing page, lead magnet, ebook, page de vente, webinaire, upsell, e-mails, pub) : questions, choix de la cible, corrections, rapport PDF avant/après |
| `seo-radar` | Tout le SEO en un seul skill : mots-clés, audit des pages, technique et visibilité IA, veille concurrence, plan de croissance. La rédaction passe par `redacteur-marketing` |

Si ces deux skills sont déjà chargés depuis mon compte Claude, inutile de les installer en plus sur l'ordinateur : cela ferait un doublon.

Pas inclus, car ce ne sont pas des skills :
- **OmniRoute** : un logiciel serveur qui fait passer tes outils IA par d'autres fournisseurs. Son skill `ponytail` est inclus ci-dessus.
- **AgentSkills** : le format standard des skills (le dossier + `SKILL.md`), pas un skill à installer.

## Installer

Tous les skills pour tous tes projets, sur ton ordinateur :

```bash
./installer.sh
```

Dans un seul projet : `./installer.sh ~/Projets/viralya`.
Seulement certains skills : `./installer.sh ~/Projets/viralya ponytail impeccable`.

Plugin SEO : dans Claude Code, tape `/plugin marketplace add <chemin>/plugins/claude-seo`,
puis `/plugin install claude-seo@agricidaniel-claude-seo`. Les scripts Python du plugin
s'installent avec `pip install -r plugins/claude-seo/requirements.txt`.

Pack `seo-geo` : `./installer.sh --seo-geo` (copie le pack dans `~/.claude/seo-geo` et
branche ses 16 skills dans `~/.claude/skills`, sans casser ses liens internes).

Graphify a besoin de son programme : `uv tool install graphifyy` (avec deux « y »).

Sur claude.ai : Paramètres, Capacités, Skills, puis importer le dossier d'un skill compressé en .zip.
