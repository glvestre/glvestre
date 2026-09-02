#!/usr/bin/env python3
"""Calcul des marges B2B gamme par gamme.

Lit catalogue.csv, calcule prix de vente B2B, benefice unitaire,
depense totale et benefice total, puis agrege par gamme.

Colonnes attendues :
  gamme, reference, produit, cout_achat_ht, frais_variables_ht,
  remise_b2b_pct, marge_cible_pct, quantite_prevue, tva_pct
Colonnes optionnelles :
  poids_g       -> active les prix de revient et de vente au gramme
  pv_ht_impose  -> si renseignee, remplace le calcul par marge cible
"""

import argparse
import csv
import sys
from collections import OrderedDict

CHAMPS_SORTIE = [
    "gamme", "reference", "produit", "poids_g",
    "cout_revient_ht", "cout_revient_par_g", "pv_catalogue_ht",
    "pv_b2b_ht", "pv_b2b_par_g", "pv_b2b_ttc",
    "benefice_unitaire_ht", "taux_marge_pct", "coefficient",
    "quantite", "depense_totale_ht", "ca_total_ht", "benefice_total_ht",
]

PALIERS_GRILLE = (30, 40, 50, 60)


def nombre(valeur, defaut=0.0):
    valeur = (valeur or "").strip().replace(",", ".").replace(" ", "")
    if not valeur:
        return defaut
    return float(valeur)


def calcule_ligne(ligne):
    cout_achat = nombre(ligne.get("cout_achat_ht"))
    frais = nombre(ligne.get("frais_variables_ht"))
    remise = nombre(ligne.get("remise_b2b_pct"))
    marge_cible = nombre(ligne.get("marge_cible_pct"))
    quantite = nombre(ligne.get("quantite_prevue"))
    tva = nombre(ligne.get("tva_pct"), 20.0)
    pv_impose = nombre(ligne.get("pv_ht_impose"))
    poids = nombre(ligne.get("poids_g"))

    cout_revient = cout_achat + frais

    if pv_impose:
        pv_b2b = pv_impose
        pv_catalogue = pv_b2b / (1 - remise / 100) if remise < 100 else pv_b2b
    else:
        if marge_cible >= 100:
            raise ValueError(
                "%s : marge_cible_pct doit rester sous 100" % ligne.get("reference")
            )
        pv_catalogue = cout_revient / (1 - marge_cible / 100)
        pv_b2b = pv_catalogue * (1 - remise / 100)

    benefice_unitaire = pv_b2b - cout_revient
    taux_marge = (benefice_unitaire / pv_b2b * 100) if pv_b2b else 0.0
    coefficient = (pv_b2b / cout_achat) if cout_achat else 0.0

    return OrderedDict([
        ("gamme", ligne.get("gamme", "")),
        ("reference", ligne.get("reference", "")),
        ("produit", ligne.get("produit", "")),
        ("poids_g", poids),
        ("cout_revient_ht", cout_revient),
        ("cout_revient_par_g", cout_revient / poids if poids else 0.0),
        ("pv_catalogue_ht", pv_catalogue),
        ("pv_b2b_ht", pv_b2b),
        ("pv_b2b_par_g", pv_b2b / poids if poids else 0.0),
        ("pv_b2b_ttc", pv_b2b * (1 + tva / 100)),
        ("benefice_unitaire_ht", benefice_unitaire),
        ("taux_marge_pct", taux_marge),
        ("coefficient", coefficient),
        ("quantite", quantite),
        ("depense_totale_ht", cout_revient * quantite),
        ("ca_total_ht", pv_b2b * quantite),
        ("benefice_total_ht", benefice_unitaire * quantite),
    ])


def agrege(lignes):
    gammes = OrderedDict()
    for ligne in lignes:
        cumul = gammes.setdefault(ligne["gamme"], {
            "references": 0, "depense_totale_ht": 0.0,
            "ca_total_ht": 0.0, "benefice_total_ht": 0.0,
        })
        cumul["references"] += 1
        for cle in ("depense_totale_ht", "ca_total_ht", "benefice_total_ht"):
            cumul[cle] += ligne[cle]
    for cumul in gammes.values():
        cumul["taux_marge_pct"] = (
            cumul["benefice_total_ht"] / cumul["ca_total_ht"] * 100
            if cumul["ca_total_ht"] else 0.0
        )
    return gammes


def affiche(lignes, gammes):
    entete = "%-12s %-11s %-24s %8s %9s %9s %8s %7s" % (
        "GAMME", "REF", "PRODUIT", "REVIENT", "PV B2B HT", "PV TTC", "BENEF/U", "MARGE%")
    print(entete)
    print("-" * len(entete))
    for l in lignes:
        print("%-12s %-11s %-24s %8.2f %9.2f %9.2f %8.2f %6.1f%%" % (
            l["gamme"][:12], l["reference"][:11], l["produit"][:24],
            l["cout_revient_ht"], l["pv_b2b_ht"], l["pv_b2b_ttc"],
            l["benefice_unitaire_ht"], l["taux_marge_pct"]))

    print()
    entete = "%-12s %5s %13s %13s %13s %7s" % (
        "GAMME", "REFS", "A DEPENSER", "CA HT", "BENEFICE", "MARGE%")
    print(entete)
    print("-" * len(entete))
    total = {"references": 0, "depense_totale_ht": 0.0,
             "ca_total_ht": 0.0, "benefice_total_ht": 0.0}
    for nom, c in gammes.items():
        print("%-12s %5d %13.2f %13.2f %13.2f %6.1f%%" % (
            nom[:12], c["references"], c["depense_totale_ht"],
            c["ca_total_ht"], c["benefice_total_ht"], c["taux_marge_pct"]))
        for cle in total:
            total[cle] += c[cle]
    taux_global = (total["benefice_total_ht"] / total["ca_total_ht"] * 100
                   if total["ca_total_ht"] else 0.0)
    print("-" * len(entete))
    print("%-12s %5d %13.2f %13.2f %13.2f %6.1f%%" % (
        "TOTAL", total["references"], total["depense_totale_ht"],
        total["ca_total_ht"], total["benefice_total_ht"], taux_global))


def affiche_grille(lignes):
    """Pour chaque produit, le prix de vente et le benefice a plusieurs marges."""
    entete = "%-11s %-22s %9s" % ("REF", "PRODUIT", "REVIENT")
    for palier in PALIERS_GRILLE:
        entete += " %17s" % ("marge %d%%" % palier)
    print(entete)
    print("-" * len(entete))
    for l in lignes:
        au_gramme = bool(l["poids_g"])
        base = l["cout_revient_par_g"] if au_gramme else l["cout_revient_ht"]
        ligne = "%-11s %-22s %8.2f%s" % (
            l["reference"][:11], l["produit"][:22], base, "/g" if au_gramme else "  ")
        for palier in PALIERS_GRILLE:
            pv = base / (1 - palier / 100)
            ligne += " %8.2f (+%.2f)" % (pv, pv - base)
        print(ligne)
    print("\nPV et benefice %s, HT. Marge = benefice / prix de vente."
          % ("au gramme" if any(l["poids_g"] for l in lignes) else "a l'unite"))


def main():
    parseur = argparse.ArgumentParser(description=__doc__)
    parseur.add_argument("catalogue", nargs="?", default="catalogue.csv")
    parseur.add_argument("-o", "--sortie", help="chemin du CSV de resultats")
    parseur.add_argument("-g", "--grille", action="store_true",
                         help="grille des prix de vente par palier de marge")
    args = parseur.parse_args()

    try:
        with open(args.catalogue, newline="", encoding="utf-8") as f:
            lignes = [calcule_ligne(l) for l in csv.DictReader(f)
                      if (l.get("reference") or "").strip()]
    except FileNotFoundError:
        sys.exit("Catalogue introuvable : %s" % args.catalogue)
    except ValueError as erreur:
        sys.exit("Donnee invalide : %s" % erreur)

    if not lignes:
        sys.exit("Catalogue vide.")

    if args.grille:
        affiche_grille(lignes)
        print()
    affiche(lignes, agrege(lignes))

    if args.sortie:
        with open(args.sortie, "w", newline="", encoding="utf-8") as f:
            redacteur = csv.DictWriter(f, fieldnames=CHAMPS_SORTIE)
            redacteur.writeheader()
            for l in lignes:
                redacteur.writerow({
                    k: (round(v, 2) if isinstance(v, float) else v)
                    for k, v in l.items()
                })
        print("\nResultats ecrits : %s" % args.sortie)


if __name__ == "__main__":
    main()
