import pandas as pd

# Charger le fichier CSV
df = pd.read_csv("competitions_data.csv")

# Compter les occurrences dans la colonne "Licence"
counts = df['Licence'].value_counts()

# Calculer les statistiques demandées
nb_licences_differentes = len(counts)
moyenne_apparition = counts.mean()
max_apparition = counts.max()
mediane_apparition = counts.median()

# Afficher les résultats
print(f"Nombre de licences différentes : {nb_licences_differentes}")
print(f"Moyenne d'apparition : {moyenne_apparition:.2f}")
print(f"Maximum d'apparition : {max_apparition}")
print(f"Médiane d'apparition : {mediane_apparition:.2f}")
