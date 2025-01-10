import csv
import ast
from collections import Counter
import plot_fct




def digit_or_None(x):
    if x!=None and x.isdigit():
        return int(x)
    else:
        return None

def extract_poules_data(poules,tireurs):
    try:
        poules_data = ast.literal_eval(poules)
        tireurs_data = ast.literal_eval(tireurs)
    except Exception as e:
        print(f"Erreur lors de la lecture de 'Poules': {e}")
        return


    match_results={}
    participant_rank={}

    for participant_id,participant_info in tireurs_data.items():
        match_results[participant_id]=[]
        rangInitialPoule =participant_info.get("RangInitialPoule")
        participant_rank[participant_id]= digit_or_None(rangInitialPoule)
       
    rankMax=participant_rank[(max(participant_rank,key= lambda x: (participant_rank[x] or 0)  ))]-1
    if rankMax<10:
        rankMax=None

    for poule_id, poule_info in poules_data.items():


        for match_id, match_details in poule_info.get("Matchs").items():
            opponent, details = zip(*match_details.items())
            if rankMax==None:
                scoreDiff=None
                scoreDiffCentred= None
            else:
                scoreDiff=None if (participant_rank[opponent[0]] == None or participant_rank[opponent[1]]==None) else (participant_rank[opponent[0]]-participant_rank[opponent[1]])/rankMax
                scoreDiffCentred= None if scoreDiff==None else (participant_rank[opponent[0]]-participant_rank[opponent[1]])/((rankMax+1)/2)

            score0=digit_or_None(details[0].get("Score"))
            score1=digit_or_None(details[1].get("Score"))

            diffTouche=None if (score0==None or score1==None) else abs(score0-score1)
            match_results[opponent[0]].append({"Score":details[0].get("Score"), "Statut":details[0].get("Statut"), "ScoreDiff":None if scoreDiff==None else -scoreDiff,"scoreDiffCentred":None if scoreDiffCentred==None else -scoreDiffCentred, "DiffTouche":diffTouche})
            match_results[opponent[1]].append({"Score":details[1].get("Score"), "Statut":details[1].get("Statut"), "ScoreDiff":scoreDiff,"scoreDiffCentred":scoreDiffCentred, "DiffTouche":diffTouche})


    return (match_results)


def score_diff_vs_rank_diff(reader,nbr_tranche=20):
    columns_to_extract = ["Tireurs", "Poules"]
    allTranche=[[] for _ in range(nbr_tranche+1)]

    for i,row in enumerate(reader):
        print(f'row {i}')

        extracted_data = {column: row[column] for column in columns_to_extract if column in row}
        match_results=extract_poules_data(extracted_data["Poules"],extracted_data["Tireurs"])

        for participant,matchs in match_results.items():
            try :
                for i,match in enumerate(matchs):
                    result=match.get("Statut")
                    if result==("V"):
                        scoreDiff=match.get("ScoreDiff")
                        diffTouche=match.get("DiffTouche")

                        if scoreDiff!=None and diffTouche!=None and diffTouche>0 and diffTouche<6:
                            iTranche=int(((scoreDiff+1)/2)*nbr_tranche) 
                            allTranche[iTranche].append(diffTouche)

            except Exception as e:
                print(f"error with match {matchs},\n Exeption : {e}")





    allPonderedTranche=[]
    allNumMatchTranche=[]
    for tranche in allTranche:
        nbrMatchTranche=len(tranche)
        allNumMatchTranche.append(nbrMatchTranche)
        ponderedTranche=dict(Counter(tranche))
        finalPonderedTranche={}
        for key,val in ponderedTranche.items():
            finalPonderedTranche[key]=int(ponderedTranche[key])/nbrMatchTranche
        allPonderedTranche.append(finalPonderedTranche)

    plot_fct.plot_score_diff_vs_rank_diff_win(allPonderedTranche,allNumMatchTranche)


def streaks(reader):
    columns_to_extract = ["Tireurs", "Poules"]

    results_count = {
            "VV": 0,
            "VD": 0,
            "DV": 0,
            "DD": 0,
        }
    nbrMatch=0

    for i,row in enumerate(reader):
        print(f'row {i}')

        extracted_data = {column: row[column] for column in columns_to_extract if column in row}
        match_results=extract_poules_data(extracted_data["Poules"],extracted_data["Tireurs"])

        for participant,matchs in match_results.items():
            try :
                for i,match in enumerate(matchs):

                    result=match.get("Statut")

                    
                    if i!=0:
                        if prev in ("D","V") and result in ("D","V"):
                            results_count[prev+result]+=1
                            nbrMatch+=1

                    prev=result


            except Exception as e:
                print(f"error with match {matchs},\n Exeption : {e}")

    labelColor={  "VV":{"name":"Victoire après victoire","color":"#29CF3A"},
                "VD":{"name":"Victoire après défaite","color":"#87E68E"},
                "DD":{"name":"Défaite après défaite","color":"#CC372D"},
                "DV":{"name":"Défaite après victoire","color":"#CC776C"}}


    plot_fct.plot_streaks(results_count,nbrMatch,labelColor)


def result_by_rank_diff(reader,nbr_tranche=20):

    columns_to_extract = ["Tireurs", "Poules"]
    allTranche=[{"V":0,"D":0} for _ in range(nbr_tranche+1)]

    for i,row in enumerate(reader):
        print(f'row {i}')

        extracted_data = {column: row[column] for column in columns_to_extract if column in row}
        match_results=extract_poules_data(extracted_data["Poules"],extracted_data["Tireurs"])

        for participant,matchs in match_results.items():
            #try :
            for i,match in enumerate(matchs):
                result=match.get("Statut")
                scoreDiff=match.get("ScoreDiff")

                if result in ("D","V") and scoreDiff!=None:
                    iTranche=int(((scoreDiff+1)/2)*nbr_tranche) 
                    allTranche[iTranche][result]+=1

            #except Exception as e:
            #    print(f"error with match {matchs},\n Exeption : {e}")
    plot_fct.plot_result_by_rank(allTranche)


def streak_by_rank_diff(reader,nbr_tranche=20):

    columns_to_extract = ["Tireurs", "Poules"]
    allTranche=[{"V":0,"D":0,"VV":0,"VD":0,"DV":0,"DD":0} for _ in range(nbr_tranche+1)]

    for i,row in enumerate(reader):
        print(f'row {i}')

        extracted_data = {column: row[column] for column in columns_to_extract if column in row}
        match_results=extract_poules_data(extracted_data["Poules"],extracted_data["Tireurs"])

        for participant,matchs in match_results.items():
            for i,match in enumerate(matchs):
                result=match.get("Statut")
                scoreDiff=match.get("ScoreDiff")
                if result in ("D","V") and scoreDiff!=None:
                    iTranche=int(((scoreDiff+1)/2)*nbr_tranche) 
                    allTranche[iTranche][result]+=1
                    if i!=0:
                        if prev in ("D","V"): 
                            allTranche[iTranche][prev+result]+=1
                prev=result


    plot_fct.plot_streak_by_rank(allTranche)




if __name__=="__main__":

    csv_file = "competitions_data.csv"

    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        #result_by_rank_diff(reader)
        #streaks(reader)
        #score_diff_vs_rank_diff(reader)
        streak_by_rank_diff(reader)



