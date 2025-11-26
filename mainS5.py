#coding:utf8

import pandas as pd
import math
import scipy
import scipy.stats

#C'est la partie la plus importante dans l'analyse de données. D'une part, elle n'est pas simple à comprendre tant mathématiquement que pratiquement. D'autre, elle constitue une application des probabilités. L'idée consiste à comparer une distribution de probabilité (théorique) avec des observations concrètes. De fait, il faut bien connaître les distributions vues dans la séance précédente afin de bien pratiquer cette comparaison. Les probabilités permettent de définir une probabilité critique à partir de laquelle les résultats ne sont pas conformes à la théorie probabiliste.
#Il n'est pas facile de proposer des analyses de données uniquement dans un cadre univarié. Vous utiliserez la statistique inférentielle principalement dans le cadre d'analyses multivariées. La statistique univariée est une statistique descriptive. Bien que les tests y soient possibles, comprendre leur intérêt et leur puissance d'analyse dans un tel cadre peut être déroutant.
#Peu importe dans quelle théorie vous êtes, l'idée de la statistique inférentielle est de vérifier si ce que vous avez trouvé par une méthode de calcul est intelligent ou stupide. Est-ce que l'on peut valider le résultat obtenu ou est-ce que l'incertitude qu'il présente ne permet pas de conclure ? Peu importe également l'outil, à chaque mesure statistique, on vous proposera un test pour vous aider à prendre une décision sur vos résultats. Il faut juste être capable de le lire.

#Par convention, on place les fonctions locales au début du code après les bibliothèques.
def ouvrirUnFichier(nom):
    with open(nom, "r") as fichier:
        contenu = pd.read_csv(fichier)
    return contenu

#Théorie de l'échantillonnage (intervalles de fluctuation)
#L'échantillonnage se base sur la répétitivité.
print("Résultat sur le calcul d'un intervalle de fluctuation")

donnees = pd.DataFrame(ouvrirUnFichier("./data/Echantillonnage-100-Echantillons.csv"))

# Lecture du fichier d’échantillonnage
print("Résultat sur le calcul d'un intervalle de fluctuation\n")

donnees = pd.DataFrame(ouvrirUnFichier("./data/Echantillonnage-100-Echantillons.csv"))

# Calcul des moyennes par colonne (opinions)
moyennes = []
for col in donnees.columns:
    valeurs = pd.to_numeric(donnees[col], errors="coerce").dropna()
    moyenne = round(valeurs.mean())  # arrondi sans décimale
    moyennes.append(moyenne)

print("Moyennes des 3 opinions (échantillon) :", moyennes)

# Calcul des fréquences de l’échantillon
somme_moyennes = sum(moyennes)
frequences_echantillon = [round(m / somme_moyennes, 2) for m in moyennes]

print("Fréquences de l’échantillon :", frequences_echantillon)

# Fréquences de la population mère
# Population mère : 2185 individus → 852 Pour, 911 Contre, 422 Sans opinion
pop_pour, pop_contre, pop_sans = 852, 911, 422
total_pop = pop_pour + pop_contre + pop_sans

frequences_population = [
    round(pop_pour / total_pop, 2),
    round(pop_contre / total_pop, 2),
    round(pop_sans / total_pop, 2)
]

print("Fréquences de la population mère :", frequences_population)

# Calcul de l’intervalle de fluctuation à 95 %
# Formule : f ± z * sqrt(f * (1 - f) / n)
zC = 1.96  # niveau de confiance 95 %
n = 100    # taille de l’échantillon (100 individus par tirage)

intervalles = []
for f in frequences_echantillon:
    erreur_type = math.sqrt(f * (1 - f) / n)
    borne_inf = round(f - zC * erreur_type, 3)
    borne_sup = round(f + zC * erreur_type, 3)
    intervalles.append((borne_inf, borne_sup))

print("\nIntervalles de fluctuation à 95 % :")
for i, intervalle in enumerate(intervalles):
    print(f"Opinion {donnees.columns[i]} : {intervalle}")

#Théorie de l'estimation (intervalles de confiance)
#L'estimation se base sur l'effectif.
print("Résultat sur le calcul d'un intervalle de confiance")

donnees = pd.DataFrame(ouvrirUnFichier("./data/Echantillonnage-100-Echantillons.csv"))

# Sélection du premier échantillon (première ligne)
# Utilisation de iloc[0] (et non iloc(0), la bonne syntaxe Pandas est iloc[0])
premier_echantillon = donnees.iloc[0]

# Conversion en liste Python (comme demandé)
echantillon_liste = list(premier_echantillon)

print("Premier échantillon :", echantillon_liste)

# Calcul des effectifs totaux et fréquences
total = sum(echantillon_liste)
frequences = [val / total for val in echantillon_liste]

print("Effectif total de l’échantillon :", total)
print("Fréquences (Pour, Contre, Sans opinion) :", [round(f, 2) for f in frequences])

# Calcul des intervalles de confiance à 95 %
zC = 1.96  # coefficient de confiance (pour 95%)

intervalles_confiance = []
for f in frequences:
    erreur_type = math.sqrt(f * (1 - f) / total)
    borne_inf = round(f - zC * erreur_type, 3)
    borne_sup = round(f + zC * erreur_type, 3)
    intervalles_confiance.append((borne_inf, borne_sup))

# Affichage des résultats
print("\nIntervalles de confiance à 95 % pour chaque opinion :")
for i, col in enumerate(donnees.columns):
    print(f"{col} : {intervalles_confiance[i]}")

#Théorie de la décision (tests d'hypothèse)
#La décision se base sur la notion de risques alpha et bêta.
#Comme à la séance précédente, l'ensemble des tests se trouve au lien : https://docs.scipy.org/doc/scipy/reference/stats.html
print("Théorie de la décision")

import scipy.stats as stats

# Lecture des fichiers contenant les données à tester
print("Résultat du test de normalité de Shapiro-Wilk\n")

# Lecture des deux fichiers CSV
test1 = ouvrirUnFichier("./data/Loi-normale-Test-1.csv")
test2 = ouvrirUnFichier("./data/Loi-normale-Test-2.csv")

# Conversion en listes de nombres
# On suppose que les valeurs sont dans la première colonne
serie1 = pd.to_numeric(test1.iloc[:, 0], errors="coerce").dropna().tolist()
serie2 = pd.to_numeric(test2.iloc[:, 0], errors="coerce").dropna().tolist()

# Application du test de Shapiro-Wilk
stat1, pval1 = stats.shapiro(serie1)
stat2, pval2 = stats.shapiro(serie2)

# Affichage des résultats
print("Fichier 1 : Loi-normale-Test-1.csv")
print(f"  Statistique de test = {stat1:.4f}")
print(f"  p-value = {pval1:.4f}")

print("\nFichier 2 : Loi-normale-Test-2.csv")
print(f"  Statistique de test = {stat2:.4f}")
print(f"  p-value = {pval2:.4f}")

# Interprétation automatique
# Règle de décision :
#   H0 : la distribution est normale
#   H1 : la distribution n’est PAS normale
# Si p-value < 0.05 → on rejette H0 → distribution non normale
# Si p-value >= 0.05 → on ne rejette pas H0 → distribution normale

def interpretation(pval):
    if pval < 0.05:
        return "❌ La distribution n'est pas normale (H0 rejetée)."
    else:
        return "✅ La distribution peut être considérée comme normale (H0 conservée)."

print("\nInterprétation :")
print(f"Test 1 → {interpretation(pval1)}")
print(f"Test 2 → {interpretation(pval2)}")