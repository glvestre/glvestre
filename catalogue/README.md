# Marges catalogue B2B

Calcul du prix de vente, du benefice et de la depense, gamme par gamme.

## Utilisation

```bash
cd catalogue
python3 marges.py catalogue.csv                 # affichage console
python3 marges.py catalogue.csv -o resultats.csv  # + export CSV
```

Aucune dependance. Python 3 seul.

## Remplir catalogue.csv

| Colonne | Sens |
|---|---|
| `gamme` | Regroupement pour l'agregation |
| `reference` | Code produit (ligne ignoree si vide) |
| `produit` | Libelle |
| `cout_achat_ht` | Prix paye au fournisseur, HT |
| `frais_variables_ht` | Port, emballage, marquage, commission — par unite |
| `remise_b2b_pct` | Remise consentie aux pros sur le prix catalogue |
| `marge_cible_pct` | Marge visee sur le prix catalogue (< 100) |
| `quantite_prevue` | Volume prevu, sert aux totaux |
| `tva_pct` | 20 par defaut |
| `pv_ht_impose` | Optionnelle. Prix B2B deja fixe — court-circuite `marge_cible_pct` |

## Formules

```
cout_revient_ht      = cout_achat_ht + frais_variables_ht
pv_catalogue_ht      = cout_revient_ht / (1 - marge_cible_pct/100)
pv_b2b_ht            = pv_catalogue_ht * (1 - remise_b2b_pct/100)
pv_b2b_ttc           = pv_b2b_ht * (1 + tva_pct/100)
benefice_unitaire_ht = pv_b2b_ht - cout_revient_ht
taux_marge_pct       = benefice_unitaire_ht / pv_b2b_ht * 100
coefficient          = pv_b2b_ht / cout_achat_ht
depense_totale_ht    = cout_revient_ht * quantite
benefice_total_ht    = benefice_unitaire_ht * quantite
```

Le taux de marge est un **taux de marque** : benefice rapporte au prix de vente,
la convention du commerce. Un produit achete 6,50 revendu 12,60 marge a 48 %,
pas a 94 %.

## Point de vigilance

`marge_cible_pct` vise le **prix catalogue**. La remise B2B se prend ensuite
sur ce prix, donc la marge reelle encaissee est toujours plus basse que la cible.
Exemple du fichier : cible 45 %, remise 10 % → 38,9 % reels.

Pour toucher 45 % nets apres remise, fixe `marge_cible_pct` a environ 50,5 %,
ou renseigne directement `pv_ht_impose`.

## TVA

Toutes les marges se calculent en HT. La TVA n'est jamais du benefice — elle est
collectee puis reversee. La colonne `pv_b2b_ttc` sert uniquement a l'affichage
client.
