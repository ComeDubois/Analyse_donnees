#coding:utf8

import pandas as pd
import matplotlib.pyplot as plt

# Source des données : https://www.data.gouv.fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/
with open("./data/resultats-elections-presidentielles-2022-1er-tour.csv","r") as fichier:
    tableau = pd.read_csv(fichier)

# Question 5 : Afficher le contenu du fichier dans le terminal
print(tableau)

# Question 6 : Afficher le nombre de lignes et de colonnes du tableau
# Calcul du nombre de lignes
nb_lignes = len(tableau)
# Calcul du nombre de colonnes
nb_colonnes = len(tableau.columns)
# Affichage des résultats
print("Nombre de lignes :", nb_lignes)
print("Nombre de colonnes:", nb_colonnes)

# Question 7 : Faire une liste sur le type statistique de chaque colonne
print(tableau.dtypes)
# Afficher proprement les types statistiques de chaque colonne à l'aide d'une boucle
# Importer les fonctions nécessaires
from pandas.api.types import is_integer_dtype, is_float_dtype, is_bool_dtype, is_object_dtype
# Créer une liste (ou dictionnaire) des types simples
types_colonnes = {}
# Parcourir toutes les colonnes du DataFrame
for colonne in tableau.columns:
    if is_integer_dtype(tableau[colonne]):
        types_colonnes[colonne] = "int"
    elif is_float_dtype(tableau[colonne]):
        types_colonnes[colonne] = "float"
    elif is_bool_dtype(tableau[colonne]):
        types_colonnes[colonne] = "bool"
    elif is_object_dtype(tableau[colonne]):
        types_colonnes[colonne] = "str"
    else:
        types_colonnes[colonne] = "autre"
# Afficher la liste des types détectés
for nom, type_var in types_colonnes.items():
    print(f"La colonne '{nom}' est de type {type_var}.")

    # Question 8 : Afficher le nom des colonnes
    nom_colonnes = tableau.head(0)
print(nom_colonnes)

# Question 9 : Sélectionner le nombre des inscrits
colonne_inscrits = tableau.Inscrits
print(colonne_inscrits)

# Question 10 : Calculer les effectifs de chaque colonne et les placer dans une liste

# Initialiser une liste vide pour stocker les effectifs
liste_effectifs = []
# Parcourir chaque colonne du DataFrame
for colonne in tableau.columns:
    # Créer une condition pour afficher les effectifs uniquement des colonnes numériques
    if is_integer_dtype(tableau[colonne]) or is_float_dtype(tableau[colonne]):
        somme = tableau[colonne].sum()
        liste_effectifs.append(float(somme))
    else:
        liste_effectifs.append(None)

print(liste_effectifs)

# Question 11 : Faire des diagrammes en barres du nombre des inscrits et des votants pour chaque département

import matplotlib.pyplot as plt

# Regrouper les lignes par département et calculer la somme des inscrits et des votants pour chaque département
agg = tableau.groupby("Code du département")[["Inscrits", "Votants"]].sum().reset_index()
# récupérer les listes des départements, inscrits et votants
departements = agg["Code du département"].tolist()
inscrits = agg["Inscrits"].tolist()
votants  = agg["Votants"].tolist()
# Définir les paramètres de tracé
w = 0.35
x = list(range(len(departements)))
fig, ax = plt.subplots(figsize=(10, 5))
# Tracer les barres département par département (boucle demandée)
for i in range(len(departements)):
    ax.bar(x[i] - w/2, inscrits[i], width=w, label="Inscrits" if i == 0 else "")
    ax.bar(x[i] + w/2, votants[i],  width=w, label="Votants"  if i == 0 else "")
 # Mise en forme et affichage
ax.set_xticks(x)
ax.set_xticklabels(departements, rotation=90, ha="center")
ax.set_ylabel("Nombre de personnes")
ax.set_title("Inscrits et votants par département – Présidentielle 2022 (1er tour)")
ax.legend()
plt.tight_layout()
plt.show()
plt.savefig("./Seance-02/diagramme.png", dpi=300, bbox_inches="tight")