import plotly.graph_objects as go
import plotly.express as px

# Données
initial_files = 2157
no_individual_competition = 220
not_enough_tireurs = 736
not_poule_exist = 141
not_tableau_exist = 94

withdrawFile=[no_individual_competition,not_enough_tireurs,not_poule_exist,not_tableau_exist]

files_count=[2157]
for i,elem in enumerate(withdrawFile):
    files_count.append(files_count[2*i-1]-elem)
    files_count.append(elem)

# Définir les nœuds (catégories)
labels = [
    f"Nombre initial de compétition : {files_count[0]}", f"Compétitions restantes : {files_count[1]}",
    f"Pas de données de compétition individuelle : {files_count[2]}",f"Compétitions restantes : {files_count[3]}",
    f"Pas assez de tireurs (<10) : {files_count[4]}", f"Compétitions restantes : {files_count[5]}",
    f"Pas de donnée de poule : {files_count[6]}", f"Nombre final de compétitions : {files_count[7]}",
    f"Pas de donnée de tableau : {files_count[8]}"
]

# Sources, cibles, et valeurs
sources = [
    0, 0,       # Total vers No Individual et Remaining
    1, 1,       # Remaining vers Not Enough Tireurs et Remaining 
    3, 3,       # Remaining vers Not Poule Exist et Remaining 
    5, 5 ,       # Remaining vers Not Tableau Exist et Final Files
    7
]

targets = [
    1, 2,       # Total vers No Individual et Remaining
    3, 4,       # Remaining vers Not Enough Tireurs et Remaining After Tireurs
    5, 6,       # Remaining After Tireurs vers Not Poule Exist et Remaining After Poule
    7, 8        # Remaining After Poule vers Not Tableau Exist et Final Files
]

values = [
    initial_files-no_individual_competition, no_individual_competition,      
    initial_files-no_individual_competition-not_enough_tireurs, not_enough_tireurs,  
    initial_files-no_individual_competition-not_enough_tireurs-not_poule_exist, not_poule_exist,  
    initial_files-no_individual_competition-not_enough_tireurs-not_poule_exist - not_tableau_exist,  not_tableau_exist
]

nodesColor =  ["green",*["green","red"]*4]
linksColor = [*["rgba(0,200,0,0.2)","rgba(200,0,0,0.2)"]*4]


fig = go.Figure(go.Sankey(
    arrangement='snap',
    node=dict(
        label=labels,
        align='left',
        color=nodesColor

    ),
    link=dict(
        arrowlen=15,
        source=sources,
        target=targets,
        value=values,
        color=linksColor
    )
))

fig.write_html("sanky_rejection.html")
fig.show()