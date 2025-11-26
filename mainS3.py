#coding:utf8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Source des données : https://www.data.gouv.fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/

# Sources des données : production de M. Forriez, 2016-2023

# Ouverture du fichier csv
import pandas as pd

with open('./data/resultats-elections-presidentielles-2022-1er-tour.csv', 'r', encoding='utf-8') as fichier:
    donnees = pd.read_csv(fichier)
print(donnees.head())
df = pd.read_csv("./data/resultats-elections-presidentielles-2022-1er-tour.csv")

# Sélection des colonnes contenant des données quantitatives
colonnes_quantitatives = df.select_dtypes(include=["number"])
print(colonnes_quantitatives)

# Calcul des moyennes de chaque colonne
moyennes = colonnes_quantitatives.mean()
print(moyennes)

# Calcul des médianes de chaque colonne
mediane = colonnes_quantitatives.median()
print(mediane)

# Calcul des modes de chaque colonne
modes = colonnes_quantitatives.mode()
if not modes.empty:
    modes = modes.iloc[0]
else:
    modes = pd.Series([None] * len(colonnes_quantitatives.columns), index=colonnes_quantitatives.columns)
print(modes)
    
# Calcul de l'écart-type de chaque colonne
ecarts_type = colonnes_quantitatives.std()
print(ecarts_type)

# Calcul de l'écart absolu à la moyenne de chaque colonne
ecart_absolu_moyenne = (colonnes_quantitatives - moyennes).abs().mean()
print(ecart_absolu_moyenne)

# Calcul de l'étendue de chaque colonne
etendue = colonnes_quantitatives.max() - colonnes_quantitatives.min()
print(etendue)

# Affichage des paramètres dans un dataframe
stats = pd.DataFrame({
    'Moyenne': moyennes.round(2),
    'Médiane': mediane.round(2),
    'Mode': modes.round(2),
    'Écart-type': ecarts_type.round(2),
    'Écart absolu à la moyenne': ecart_absolu_moyenne.round(2),
    'Étendue': etendue.round(2)})
for colonne in stats.index:
    print(f"\n📊 Statistiques pour la colonne : {colonne}")
    for stat_name, value in stats.loc[colonne].items():
        print(f"  - {stat_name} : {value}")

# Calcul des distances interquartiles et interdéciles
q1 = colonnes_quantitatives.quantile(0.25)
q3 = colonnes_quantitatives.quantile(0.75)
iqr = (q3 - q1).round(2)

# Calcul des déciles
d1 = colonnes_quantitatives.quantile(0.10)
d9 = colonnes_quantitatives.quantile(0.90)
distance_interdecile = (d9 - d1).round(2)

# Afficher les résultats
print("Distance interquartile (IQR) par colonne :")
print(iqr)

print("\nDistance interdécile par colonne :")
print(distance_interdecile)

# Faire des boîtes à moustaches
import os
import matplotlib.pyplot as plt
os.makedirs("img", exist_ok=True)

for col in colonnes_quantitatives.columns:
    plt.figure(figsize=(6, 4))               # Taille de la figure
    plt.boxplot(colonnes_quantitatives[col].dropna())     # Crée le boxplot (sans valeurs NaN)
    plt.title(f"Boîte à moustache - {col}") # Titre du graphique
    plt.ylabel(col)                          # Label axe Y (optionnel)
    plt.grid(True, linestyle='--', alpha=0.7) # Grille en arrière-plan

    # Chemin complet du fichier image à sauvegarder
    filename = f"img/boxplot_elections_{col}.png"
    plt.savefig(filename)  # Sauvegarde dans dossier img
    plt.close()            # Ferme la figure pour libérer la mémoire

print("Boxplots sauvegardés dans le dossier 'img'")

# Fichier Island-index
# Étape 1 : lire le fichier CSV
df = pd.read_csv("./data/island-index.csv", low_memory=False)
print("Colonnes disponibles :")
print(df.columns.tolist())

# Étape 2 : sélectionner la colonne "Surface (km2)"
surfaces = df["Surface (km²)"]

# Étape 3 : définir les bornes des classes (intervalle croissant)
# On utilise les bornes exactes correspondant aux intervalles :
# [0-10], ]10-25], ]25-50], ]50-100], ]100-2500], ]2500-5000], ]5000-10000], ]10000+[
bins = [0, 10, 25, 50, 100, 2500, 5000, 10000, float('inf')]

# Étape 4 : définir les étiquettes associées à chaque tranche
labels = [
    "0–10 km²",
    "10–25 km²",
    "25–50 km²",
    "50–100 km²",
    "100–2 500 km²",
    "2 500–5 000 km²",
    "5 000–10 000 km²",
    "≥ 10 000 km²"
]

# Étape 5 : découper les surfaces en tranches
categories = pd.cut(surfaces, bins=bins, labels=labels, right=True, include_lowest=True)

# Étape 6 : compter le nombre d’îles dans chaque tranche
resultats = categories.value_counts(sort=False)

# Affichage
print("Nombre d’îles par tranche de surface :")
print(resultats)

# Organigramme présentant la démarche

# BONUS : Export au format CSV

resultats = resultats.to_frame(name="Nombre d'îles")

resultats.to_csv("repartition_surface.csv", index=True, encoding='utf-8')

# BONUS : Export au format Excel

resultats.to_excel("nombre_iles_par_tranche.xlsx", sheet_name="Données", index=True)
