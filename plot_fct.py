import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



def plot_diff_score_curve(diff_score):
    """
    Trace la courbe de densité ou histogramme pour diff_score.
    
    Paramètres :
        - diff_score : Liste ou tableau contenant les différences de score.
    """
    plt.figure(figsize=(8, 6))
    
    # Courbe de densité
    sns.kdeplot(diff_score, shade=True, color="blue", label="Densité de diff_score")
    
    # Configurer les axes et titre
    plt.xlabel("Différence de Score")
    plt.ylabel("Densité")
    plt.title("Courbe de Densité : Différence de Score")
    plt.legend()
    
    # Afficher le graphique
    plt.show()

def plot_score_diff_vs_rank_diff_win(ponderedTranche,numMatchTranche):
    # Vérification des entrées
    if not all(isinstance(d, dict) for d in ponderedTranche):
        raise ValueError("Tous les éléments de la liste doivent être des dictionnaires.")

    # Extraire les clés et les valeurs
    keys = sorted({key for d in ponderedTranche for key in d.keys()})  # Toutes les clés uniques, triées
    values = [
        [d.get(key, 0) for key in keys]  # Obtenir les valeurs pour chaque clé, avec 0 par défaut
        for d in ponderedTranche
    ]

    # Normalisation des données (pourcentage par colonne)
    values = np.array(values)
    row_sums = values.sum(axis=1, keepdims=True)
    normalized_values = 100 * values / row_sums

    # Préparer les couleurs (dégradé)
    cmap = plt.cm.Greens
    num_colors = len(keys)
    colors = [cmap((i+4) / (num_colors+4)) for i in range(num_colors)]

    # Création des barres empilées
    fig, (ax1,ax2) = plt.subplots(2, 1,sharex=True)
    indices = np.arange(len(ponderedTranche))  # Position des colonnes
    bottom = np.zeros(len(ponderedTranche))

    for i, key in enumerate(keys):
        ax1.bar(
            indices,
            normalized_values[:, i],
            bottom=bottom,
            label=key,
            color=colors[i]
        )

        #for j, value in enumerate(normalized_values[:, i]):
        #    if value > 0.17:  # Seulement si le pourcentage dépasse 15%
        #        ax1.text(indices[j], bottom[j] + value / 2, f"{int(value * 100)}", ha="center", va="center", rotation=90, fontsize=8,rotation_mode='default')


        bottom += normalized_values[:, i]

    ax2.bar(indices, numMatchTranche, color="gray", alpha=0.7)
    ax2.set_title("Nombre de matchs analysés par tranche")
    ax2.set_ylabel("Nombre de matchs")

    # Configurer les labels et la légende
    ax1.set_xticks(indices)
    labels=["" for _ in range (len(ponderedTranche))]
    labels[0]="Adversaire\nmieux classé"
    labels[-1]="Adversaire\nmoins bien classé"
    labels[int(len(ponderedTranche)/2)]="Classement\néquivalant"
    ax1.tick_params(axis="x", labelbottom=True)
    ax2.tick_params(axis="x", labelbottom=False)
    ax1.set_xticklabels(labels)
    ax1.set_ylabel("Pourcentage des matchs")

    ax1.set_ylabel("Pourcentage des matchs")
    ax1.set_title("Différence de score selon la différence de rang pour une victoire")
    ax1.legend(title="Différence de touche", bbox_to_anchor=(1.05, 1), loc='upper left')

    #fig.text(0.5, -0.3, "Différence de score : Score du gagnant - Score du perdant. 1 ≤ diff ≤ 5\n\nDifférence de rang : En début de compétition, chaque tireur se voit attribuer un numéro allant de 1 au nombre de participants.\nPour trouver la différence de rang, on fait (rang tireur 1 - rang tireur 2)/nombre tireur.\nCela nous donne un score de -1 (le tireur 2 est beaucoup mieux classé) à 1 (le tireur 1 est beaucoup mieux classé). 0 correspond donc à un rang équivalant. ", ha="left", fontsize=10)
    #fig.subplots_adjust(bottom=0.5)

    plt.tight_layout()
    plt.show()


def plot_result_by_rank(tranches):
    # Préparer les données
    labels=["" for _ in range (len(tranches))]
    labels[0]="Adversaire\nmieux classé"
    labels[-1]="Adversaire\nmoins bien classé"
    labels[int(len(tranches)/2)]="Classement\néquivalant"
    V_values = [item["V"] for item in tranches]
    D_values = [item["D"] for item in tranches]

    # Calculer les pourcentages
    totals = [v + d for v, d in zip(V_values, D_values)]
    V_percentages = [v / t * 100 if t > 0 else 0 for v, t in zip(V_values, totals)]
    D_percentages = [d / t * 100 if t > 0 else 0 for d, t in zip(D_values, totals)]

    # Configuration du graphique
    x = np.arange(len(tranches))
    width = 0.8  # Largeur des barres

    # Création du graphique
    fig, ax = plt.subplots(figsize=(10, 6))

    # Barres pour V (au-dessus)
    ax.bar(x, V_percentages, width, color="green", label="Victoire", align="center")

    # Barres pour D (en-dessous)
    ax.bar(x, [-d for d in D_percentages], width, color="red", label="Défaite", align="center")

    # Ajouter des lignes horizontales discrètes pour V (au-dessus de l'axe des x)
    for mark in [25, 50, 75]:
        ax.hlines(mark, xmin=-0.5, xmax=len(tranches) - 0.5, colors="gray", linestyles="dashed", alpha=0.3)

    # Ajouter des lignes horizontales discrètes pour D (en-dessous de l'axe des x)
    for mark in [-25, -50, -75]:
        ax.hlines(mark, xmin=-0.5, xmax=len(tranches) - 0.5, colors="gray", linestyles="dashed", alpha=0.3)

    # Ajouter des labels et des lignes pour l'axe x
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.axhline(0, color="black", linewidth=0.8)  # Ligne de l'axe des x
    ax.set_ylabel("Pourcentage des matchs")
    ax.set_title("Pourcentage de victoire et défaite par différence de rang")
    ax.legend()

    plt.tight_layout()
    plt.show()

def plot_streak_by_rank(data_list):
    """
    Compare les pourcentages V-D avec VV-VD et DV-DD pour chaque élément de data_list.

    Parameters:
        data_list (list): Liste de dictionnaires avec "V", "D", "VV", "VD", "DV", "DD" comme clés.
    """
    # Allocation des couleurs
    colors = {
        "V": "green",
        "D": "red",
        "VV": "#87E68E",  # Vert 
        "VD": "#FF867D",  # Rouge 
        "DV": "#87E68E",  # Vert 
        "DD": "#FF867D"   # Rouge 
    }

    # Préparer les données
    labels = [str(i) for i in range(len(data_list))]  # Un label par élément de la liste
    V_values = [item["V"] for item in data_list]
    D_values = [item["D"] for item in data_list]
    VV_values = [item["VV"] for item in data_list]
    VD_values = [item["VD"] for item in data_list]
    DV_values = [item["DV"] for item in data_list]
    DD_values = [item["DD"] for item in data_list]

    # Calculer les pourcentages pour chaque colonne
    V_D_totals = [v + d for v, d in zip(V_values, D_values)]
    VV_VD_totals = [vv + vd for vv, vd in zip(VV_values, VD_values)]
    DV_DD_totals = [dv + dd for dv, dd in zip(DV_values, DD_values)]

    V_percentages = [v / t * 100 if t > 0 else 0 for v, t in zip(V_values, V_D_totals)]
    D_percentages = [d / t * 100 if t > 0 else 0 for d, t in zip(D_values, V_D_totals)]

    VV_percentages = [vv / t * 100 if t > 0 else 0 for vv, t in zip(VV_values, VV_VD_totals)]
    VD_percentages = [vd / t * 100 if t > 0 else 0 for vd, t in zip(VD_values, VV_VD_totals)]

    DV_percentages = [dv / t * 100 if t > 0 else 0 for dv, t in zip(DV_values, DV_DD_totals)]
    DD_percentages = [dd / t * 100 if t > 0 else 0 for dd, t in zip(DD_values, DV_DD_totals)]

    x = np.arange(len(data_list))
    width = 0.3  # Largeur des barres

    # Graphique 1 : V-D et VV-VD
    fig, (ax1,ax2) = plt.subplots(2,1,figsize=(10, 6))

    # Barres pour V et D
    ax1.bar(x - width, V_percentages, width, color=colors["V"], label="Victoire", align="center")
    ax1.bar(x - width, [-d for d in D_percentages], width, color=colors["D"], label="Défaite", align="center")

    # Barres pour VV et VD
    ax1.bar(x, VV_percentages, width, color=colors["VV"], label="Victoire après victoire", align="center")
    ax1.bar(x, [-vd for vd in VD_percentages], width, color=colors["VD"], label="Défaite après victoire", align="center")

    for mark in [25, 50, 75]:
        ax1.hlines(mark, xmin=-0.5, xmax=len(data_list) - 0.5, colors="gray", linestyles="dashed", alpha=0.3)

    # Ajouter des lignes horizontales discrètes pour D (en-dessous de l'axe des x)
    for mark in [-25, -50, -75]:
        ax1.hlines(mark, xmin=-0.5, xmax=len(data_list) - 0.5, colors="gray", linestyles="dashed", alpha=0.3)

    # Ajouter des labels et une légende
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.axhline(0, color="black", linewidth=0.8)
    ax1.set_ylabel("Pourcentage")
    ax1.set_title("Comparaison après une victoire")
    ax1.legend()

    # Graphique 2 : V-D et DV-DD

    # Barres pour V et D
    ax2.bar(x - width, V_percentages, width, color=colors["V"], label="Victoire", align="center")
    ax2.bar(x - width, [-d for d in D_percentages], width, color=colors["D"], label="Défaite", align="center")

    # Barres pour DV et DD
    ax2.bar(x, DV_percentages, width, color=colors["DV"], label="Victoire après défaite", align="center")
    ax2.bar(x, [-dd for dd in DD_percentages], width, color=colors["DD"], label="Défaite après défaite", align="center")

        # Ajouter des lignes horizontales discrètes pour V (au-dessus de l'axe des x)
    for mark in [25, 50, 75]:
        ax2.hlines(mark, xmin=-0.5, xmax=len(data_list) - 0.5, colors="gray", linestyles="dashed", alpha=0.3)

    # Ajouter des lignes horizontales discrètes pour D (en-dessous de l'axe des x)
    for mark in [-25, -50, -75]:
        ax2.hlines(mark, xmin=-0.5, xmax=len(data_list) - 0.5, colors="gray", linestyles="dashed", alpha=0.3)


    # Ajouter des labels et une légende
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels)
    ax2.axhline(0, color="black", linewidth=0.8)
    ax2.set_ylabel("Pourcentage")
    ax2.set_title("Comparaison après une défaite")
    ax2.legend()

    plt.tight_layout()
    plt.show()


def plot_streaks(values_dict, num_matches,labelColor):
    

    # Pondération des valeurs
    weighted_values = {key: value * num_matches for key, value in values_dict.items()}

    # Préparer les données pour le camembert
    labels = [labelColor[key]["name"] for key in weighted_values.keys()]
    sizes = list(weighted_values.values())
    colors = [labelColor[key]["color"] for key in weighted_values.keys()]

    # Création du diagramme camembert
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)
    plt.title("Issue d'un match selon le résultat précédant")
    plt.show()