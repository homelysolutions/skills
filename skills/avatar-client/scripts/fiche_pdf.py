#!/usr/bin/env python3
"""Fiche avatar : synthese JSON -> PDF A4 (une page par fiche) + synthese .md + .html.

Usage :
  python3 fiche_pdf.py synthese.json [--out DOSSIER]
  python3 fiche_pdf.py --exemple exemple.json   # cree un JSON de demonstration

Aucune dependance Python. Le PDF est imprime par Chrome, Chromium, Edge ou Brave
en mode headless. Sans navigateur, seul le .html est produit (le script le dit).
"""
import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata

VIDE = "à définir"

EXEMPLE = {
    "entreprise": {
        "nom": "Exemple Plomberie (fictif)",
        "activite": "Plomberie : dépannage, rénovation de salles de bains, entretien",
        "zone": "Lausanne et environs",
        "situation": "Beaucoup de dépannages chez des particuliers, peu de rénovations",
        "direction": "Développer les rénovations de salles de bains planifiées",
    },
    "meta": {
        "date": "2026-11-12",
        "version": "1",
        "origine": "Exemple de démonstration du skill avatar-client (aucun client réel)",
        "statut": "provisoire",
        "validation": {"personne": "", "date": "", "portee": "", "corrections": ""},
    },
    "fiches": [
        {
            "segment": {
                "id": "S1",
                "intitule": "Propriétaires qui rénovent leur salle de bains",
                "priorite": "prioritaire",
                "situation": "Propriétaires d'un appartement ou d'une maison, salle de bains ancienne",
                "roles": "",
                "exclusions": "Petites réparations isolées, chantiers neufs de promoteurs",
            },
            "besoins": {
                "probleme": "Salle de bains vétuste ou peu pratique, peur d'un chantier qui s'éternise",
                "declencheur": "Fuite récurrente, achat du logement, arrivée d'un enfant",
                "resultat": "Une salle de bains neuve, livrée dans le délai annoncé, sans surprise sur la facture",
            },
            "achat": {
                "criteres": ["Clarté du devis", "Respect du planning", "Propreté du chantier"],
                "objections": ["Peur du dépassement de budget", "Combien de jours sans douche ?"],
                "alternatives": "Entreprise générale, cuisiniste-bainiste",
                "action": "Demander une visite et un devis",
            },
            "offre": {
                "prestation": "Rénovation complète de salle de bains, coordination des corps de métier",
                "benefice": "Un seul interlocuteur du devis à la remise des clés",
                "perimetre": "Démontage, plomberie, carrelage via partenaire, pose sanitaires",
                "conditions": "Visite préalable obligatoire",
                "difference": "[proposé] Planning jour par jour remis avec le devis",
            },
            "prix": {"valeur": "", "devise": "CHF", "statut": "à définir",
                     "a_confirmer": "Fourchette habituelle d'un chantier type"},
            "communication": {
                "vocabulaire": ["« refaire la salle de bains »", "« combien de temps sans douche ? »"],
                "ton": "Rassurant, concret, sans jargon",
                "arguments": ["Un seul interlocuteur", "Devis détaillé poste par poste"],
                "a_eviter": ["Promettre un délai non confirmé", "« Le moins cher de la région »"],
            },
            "fiabilite": {
                "declarations": ["Direction souhaitée et exclusions données par le dirigeant"],
                "hypotheses": ["Déclencheurs proposés par le skill, à confirmer"],
                "inconnues": ["Prix", "Part des clients venant par recommandation"],
            },
        }
    ],
}

CSS = """
@page { size: A4; margin: 11mm 12mm; }
* { box-sizing: border-box; }
body { font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; color: #1d2433;
       font-size: 9.2pt; line-height: 1.32; margin: 0; }
.fiche { page-break-after: always; }
.fiche:last-child { page-break-after: auto; }
header { border-bottom: 2.5px solid #1f4e79; padding-bottom: 5px; margin-bottom: 8px; }
h1 { font-size: 15pt; margin: 0 0 3px; color: #1f4e79; letter-spacing: -0.2px; }
.meta { font-size: 8pt; color: #555; display: flex; flex-wrap: wrap; gap: 4px 14px; }
.badge { display: inline-block; padding: 1px 7px; border-radius: 9px; font-weight: 600; font-size: 7.8pt; }
.b-ok { background: #dff3e4; color: #1d6b34; } .b-prov { background: #fff1d6; color: #8a5a00; }
.b-conf { background: #e7eef8; color: #1f4e79; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px 9px; }
.stack { display: flex; flex-direction: column; gap: 6px; } .stack section { flex: 1 1 auto; }
.full { grid-column: 1 / -1; } .g3 { grid-template-columns: 1fr 1fr 1fr; }
section { border: 1px solid #d9dfe8; border-radius: 5px; padding: 6px 8px; break-inside: avoid; }
h2 { font-size: 9.6pt; margin: 0 0 3px; color: #1f4e79; }
h2 .n { display: inline-block; width: 15px; height: 15px; border-radius: 50%; background: #1f4e79;
        color: #fff; font-size: 7.5pt; text-align: center; line-height: 15px; margin-right: 4px; }
dl { margin: 0; } .kv { margin: 0 0 2px; } .kv b { font-weight: 600; color: #3a4456; }
ul { margin: 0; padding-left: 13px; } li { margin: 0; }
.c2 dl { display: grid; grid-template-columns: 1fr 1fr; gap: 0 12px; }
.vide { color: #999; font-style: italic; }
.prix { font-size: 11pt; font-weight: 700; }
section.confirm { background: #fbf8ef; border-color: #eadfbf; }
footer { margin-top: 7px; font-size: 7.6pt; color: #666; border-top: 1px solid #ddd; padding-top: 4px; }
"""


def esc(v):
    return html.escape(str(v))


def val(v):
    if v is None or (isinstance(v, str) and not v.strip()) or (isinstance(v, list) and not v):
        return '<span class="vide">%s</span>' % VIDE
    if isinstance(v, list):
        return "<ul>%s</ul>" % "".join("<li>%s</li>" % esc(x) for x in v)
    return esc(v)


def dl(pairs):
    out = []
    for label, v in pairs:
        if v is None:
            continue
        if isinstance(v, list) and v:
            out.append('<div class="kv"><b>%s :</b>%s</div>' % (esc(label), val(v)))
        else:
            out.append('<div class="kv"><b>%s :</b> %s</div>' % (esc(label), val(v)))
    return "<dl>%s</dl>" % "".join(out)


def section(n, titre, body, cls=""):
    return '<section class="%s"><h2><span class="n">%s</span>%s</h2>%s</section>' % (
        cls, n, esc(titre), body)


def badge(statut):
    s = (statut or "à confirmer").lower()
    cls = "b-ok" if s.startswith("valid") else "b-prov" if s.startswith("provis") else "b-conf"
    return '<span class="badge %s">%s</span>' % (cls, esc(statut or "à confirmer"))


def prix_txt(p):
    valeur = (p.get("valeur") or "").strip()
    statut = (p.get("statut") or "").strip()
    if not valeur:
        return "Sur devis" if statut.lower() == "sur devis" else "Prix à définir"
    dev = (p.get("devise") or "").strip()
    return "%s %s" % (valeur, dev) if dev and dev not in valeur else valeur


def fiche_html(data, f):
    e, m = data.get("entreprise", {}), data.get("meta", {})
    s, b, a = f.get("segment", {}), f.get("besoins", {}), f.get("achat", {})
    o, p, c, r = f.get("offre", {}), f.get("prix", {}), f.get("communication", {}), f.get("fiabilite", {})
    statut = f.get("statut") or m.get("statut") or "à confirmer"
    va = m.get("validation", {}) or {}
    if statut.lower().startswith("valid") and va.get("personne"):
        statut = "validée par %s%s%s" % (va["personne"], " le " + va["date"] if va.get("date") else "",
                                          " — " + va["portee"] if va.get("portee") else "")
    titre = "Fiche avatar - %s - %s" % (e.get("nom") or "Entreprise", s.get("intitule") or s.get("id") or "Segment")
    meta = "".join("<span>%s</span>" % x for x in [
        "Date : " + esc(m.get("date") or VIDE), "Version : " + esc(m.get("version") or "1"),
        "Origine : " + esc(m.get("origine") or VIDE), "Statut : " + badge(statut)])
    seg_id = " (%s, %s)" % (s.get("id", ""), s.get("priorite")) if s.get("priorite") else ""
    parts = [
        section(1, "L'entreprise et sa direction", dl([
            ("Activité", e.get("activite")), ("Zone", e.get("zone")),
            ("Aujourd'hui", e.get("situation")), ("Priorité / direction", e.get("direction"))]), "full c2"),
        section(2, "À qui parle-t-on ?" + seg_id, dl([
            ("Segment", s.get("intitule")), ("Situation", s.get("situation")),
            ("Rôles dans l'achat", s.get("roles") if s.get("roles") else None),
            ("Exclusions", s.get("exclusions"))])),
        section(3, "Pourquoi cherche-t-elle une solution ?", dl([
            ("Besoin / problème", b.get("probleme")), ("Déclencheur", b.get("declencheur"))])),
        section(4, "Que veut-elle obtenir ?", dl([("Résultat attendu", b.get("resultat"))])),
        section(5, "Qu'est-ce qui compte dans sa décision ?", dl([
            ("Critères de choix", a.get("criteres")), ("Freins / objections", a.get("objections")),
            ("Alternatives connues", a.get("alternatives") or None)])),
        section(6, "Quelle offre lui adresse-t-on ?", dl([
            ("Prestation", o.get("prestation")), ("Bénéfice", o.get("benefice")),
            ("Périmètre", o.get("perimetre")), ("Conditions / limites", o.get("conditions") or None),
            ("Différence crédible", o.get("difference"))])),
        section(7, "À quel prix ?", '<div class="prix">%s</div>%s' % (esc(prix_txt(p)), dl([
            ("Statut", p.get("statut")), ("À confirmer", p.get("a_confirmer") or None)]))),
        section(8, "Comment lui parler ?", dl([
            ("Ses mots", c.get("vocabulaire")), ("Ton", c.get("ton")),
            ("Arguments étayés", c.get("arguments")), ("À éviter", c.get("a_eviter"))])),
        section(9, "Quelle action lui proposer ?", dl([("Action suivante", a.get("action"))])),
        section(10, "Que reste-t-il à confirmer ?", '<div class="grid g3">%s</div>' % "".join(
            "<div>%s</div>" % dl([(k, v)]) for k, v in [
                ("Déclarations du dirigeant", r.get("declarations")),
                ("Hypothèses", r.get("hypotheses")), ("Inconnues", r.get("inconnues"))]), "full confirm"),
    ]
    def stack(*xs):
        return '<div class="stack">%s</div>' % "".join(xs)
    # 2 colonnes equilibrees : 2 | 3+4, 5 | 7+9, 6 | 8, puis 10 en pleine largeur
    layout = [parts[0], parts[1], stack(parts[2], parts[3]), parts[4], stack(parts[6], parts[8]),
              parts[5], parts[7], parts[9]]
    foot = ("Validation : %s. La validation du dirigeant confirme que la fiche représente sa stratégie "
            "et ses déclarations ; elle ne prouve pas la demande du marché." % esc(
                ", ".join(x for x in [va.get("personne"), va.get("date"), va.get("portee")] if x) or "pas encore validée"))
    if va.get("corrections"):
        foot += " Corrections : %s." % esc(va["corrections"])
    return ('<div class="fiche"><header><h1>%s</h1><div class="meta">%s</div></header>'
            '<div class="grid">%s</div><footer>%s</footer></div>') % (esc(titre), meta, "".join(layout), foot)


def to_html(data):
    body = "".join(fiche_html(data, f) for f in data.get("fiches", []))
    return ('<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Fiche avatar</title>'
            '<style>%s</style></head><body>%s</body></html>') % (CSS, body)


def j(v):
    if isinstance(v, list):
        return " ; ".join(str(x) for x in v) if v else VIDE
    return str(v).strip() if v and str(v).strip() else VIDE


def to_md(data):
    e, m = data.get("entreprise", {}), data.get("meta", {})
    va = m.get("validation", {}) or {}
    lines = ["# Synthèse avatar — %s" % j(e.get("nom")), "",
             "ENTREPRISE : %s | %s | %s | aujourd'hui : %s | direction : %s" % (
                 j(e.get("nom")), j(e.get("activite")), j(e.get("zone")), j(e.get("situation")), j(e.get("direction")))]
    for f in data.get("fiches", []):
        s, b, a = f.get("segment", {}), f.get("besoins", {}), f.get("achat", {})
        o, p, c, r = f.get("offre", {}), f.get("prix", {}), f.get("communication", {}), f.get("fiabilite", {})
        lines += ["", "## %s — %s" % (j(s.get("id")), j(s.get("intitule"))), "",
                  "SEGMENT : %s | %s | priorité : %s | situation : %s | rôles : %s | exclusions : %s" % (
                      j(s.get("id")), j(s.get("intitule")), j(s.get("priorite")), j(s.get("situation")),
                      j(s.get("roles")), j(s.get("exclusions"))),
                  "BESOINS : problème : %s | déclencheur : %s | résultat : %s" % (
                      j(b.get("probleme")), j(b.get("declencheur")), j(b.get("resultat"))),
                  "ACHAT : critères : %s | objections : %s | alternatives : %s | action : %s" % (
                      j(a.get("criteres")), j(a.get("objections")), j(a.get("alternatives")), j(a.get("action"))),
                  "OFFRE : %s | bénéfice : %s | périmètre : %s | conditions : %s | différence : %s" % (
                      j(o.get("prestation")), j(o.get("benefice")), j(o.get("perimetre")),
                      j(o.get("conditions")), j(o.get("difference"))),
                  "PRIX : %s | devise : %s | statut : %s | à confirmer : %s" % (
                      prix_txt(p), j(p.get("devise")), j(p.get("statut")), j(p.get("a_confirmer"))),
                  "COMMUNICATION : mots : %s | ton : %s | arguments : %s | à éviter : %s" % (
                      j(c.get("vocabulaire")), j(c.get("ton")), j(c.get("arguments")), j(c.get("a_eviter"))),
                  "FIABILITÉ : origine : %s | date : %s | déclarations : %s | hypothèses : %s | inconnues : %s" % (
                      j(m.get("origine")), j(m.get("date")), j(r.get("declarations")),
                      j(r.get("hypotheses")), j(r.get("inconnues"))),
                  "STATUT : %s" % j(f.get("statut") or m.get("statut"))]
    lines += ["", "VALIDATION : personne : %s | date : %s | corrections : %s | portée : %s" % (
        j(va.get("personne")), j(va.get("date")), j(va.get("corrections")), j(va.get("portee"))), "",
        "Règle pour les skills suivants : ne pas ajouter de besoin, prix ou promesse sans le signaler comme proposition."]
    lines = ["- " + x if re.match(r"^[A-ZÉ]+ : ", x) else x for x in lines]
    return "\n".join(lines) + "\n"


def slug(t):
    t = unicodedata.normalize("NFKD", str(t)).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "-", t).strip("-")[:50] or "x"


def find_browser():
    mac = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
           "/Applications/Chromium.app/Contents/MacOS/Chromium",
           "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
           "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
           r"C:\Program Files\Google\Chrome\Application\chrome.exe",
           r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"]
    for p in mac:
        if os.path.exists(p):
            return p
    for n in ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
              "microsoft-edge", "brave-browser", "chrome", "msedge"]:
        w = shutil.which(n)
        if w:
            return w
    return None


def print_pdf(browser, html_path, pdf_path):
    with tempfile.TemporaryDirectory() as prof:
        cmd = [browser, "--headless=new", "--disable-gpu", "--no-first-run", "--user-data-dir=" + prof,
               "--no-pdf-header-footer", "--print-to-pdf-no-header", "--print-to-pdf=" + pdf_path,
               "file://" + os.path.abspath(html_path)]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
    return os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("json", help="synthèse JSON (ou chemin à créer avec --exemple)")
    ap.add_argument("--out", default=None, help="dossier de sortie (défaut : celui du JSON)")
    ap.add_argument("--exemple", action="store_true", help="écrire un JSON de démonstration et s'arrêter")
    args = ap.parse_args()

    if args.exemple:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(EXEMPLE, fh, ensure_ascii=False, indent=2)
        print("Exemple écrit : %s" % args.json)
        return 0

    with open(args.json, encoding="utf-8") as fh:
        data = json.load(fh)
    fiches = data.get("fiches") or []
    if not fiches:
        print("Erreur : aucune fiche dans 'fiches'.", file=sys.stderr)
        return 1

    out = args.out or os.path.dirname(os.path.abspath(args.json))
    os.makedirs(out, exist_ok=True)
    seg = slug(fiches[0].get("segment", {}).get("intitule") or "segment") if len(fiches) == 1 else "multi-segments"
    base = os.path.join(out, "Fiche-avatar-%s-%s" % (slug(data.get("entreprise", {}).get("nom") or "entreprise"), seg))

    with open(base + ".html", "w", encoding="utf-8") as fh:
        fh.write(to_html(data))
    with open(base + ".md", "w", encoding="utf-8") as fh:
        fh.write(to_md(data))
    print("Synthèse : %s.md" % base)

    browser = find_browser()
    if not browser:
        print("Aucun navigateur Chrome/Chromium/Edge/Brave trouvé : PDF NON créé.")
        print("HTML imprimable : %s.html (ouvrir puis Imprimer > Enregistrer en PDF)." % base)
        return 2
    if not print_pdf(browser, base + ".html", base + ".pdf"):
        print("Échec de l'impression PDF : PDF NON créé. HTML : %s.html" % base)
        return 3
    with open(base + ".pdf", "rb") as fh:
        pages = len(re.findall(rb"/Type\s*/Page[^s]", fh.read()))
    print("PDF : %s.pdf (%d page(s) pour %d fiche(s))" % (base, pages, len(fiches)))
    if pages > 2 * len(fiches):
        print("Attention : plus de deux pages par fiche, raccourcir les formulations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
