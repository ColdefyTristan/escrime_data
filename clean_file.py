import os
import pandas as pd
import xml.etree.ElementTree as ET
import shutil
import json
import datetime



def check_file(file):
	"""
	input : filepath to analyse
	output : tupple (isFileGood,reason)

	"""
	if not file.endswith(".xml"):
		return (False,"notXml")
	else:
		tree = ET.parse(file)
		root = tree.getroot()
		if root.tag!="CompetitionIndividuelle":
			return (False,"noIndividualCompetition")
		infoCompet = root.attrib
		if infoCompet == None:
			return (False,"noIndividualCompetition")

		if root.find("Tireurs")==None:
			return (False,"noTireurs")
		if len(root.find("Tireurs").findall("Tireur"))<10:
			return (False,"notEnoughTireurs")	

		havePoule = {"exist":False,"haveMatch":False,"haveTireur":False}	
		haveTableau = {"exist":False,"haveTableau":False,"haveMatch":False,"haveTireur":False}		
			
		for phase in root.findall("Phases"):

			tourDePoule=phase.find("TourDePoules")
			if tourDePoule:
				havePoule["exist"]=True

				if tourDePoule.findall("Tireur"):
					havePoule["haveTireur"]=True
				if len(tourDePoule.findall("Poule"))>=1:
					havePoule["haveMatch"]=True

				
			phaseDeTableaux=phase.find("PhaseDeTableaux")
			if phaseDeTableaux:
				haveTableau["exist"]=True
				if phaseDeTableaux.findall("Tireur"):
					haveTableau["haveTireur"]=True
				if phaseDeTableaux.find("SuiteDeTableaux").findall("Tableau"):
					haveTableau["haveTableau"]=True
					for tableau in phaseDeTableaux.find("SuiteDeTableaux").findall("Tableau"):
						if tableau.findall("Match"):
							haveTableau["haveMatch"]=True
							break

		if all(havePoule.values()):
			if all(haveTableau.values()):
				return(True,"allGood")
			else:
				reason = "notTableau"+next(key for key, value in haveTableau.items() if not value)
				return(False,reason)
		else:
			reason = "notPoule"+next(key for key, value in havePoule.items() if not value)
			return(False,reason)


def is_hidden(filepath):
    return bool(os.stat(filepath).st_file_attributes & 2)  # 2 = FILE_ATTRIBUTE_HIDDEN


def check_all_compet(path,rejectionPath):
	results_dict = {}
	for file in os.listdir(path):
		file_path=os.path.join(path, file)
		if not file.startswith(".") and not is_hidden(file_path):
			print("reading file "+file)
			
			result,reason=check_file(file_path)

			results_dict[file]={"result":result,"reason":reason}
			if result==False:
				shutil.move(file_path, os.path.join(rejectionPath,file))
				print(f"File {file} rejected and moved to {rejectionPath}")
			
	date=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
	with open(f"rejection_results_{date}.json", "w") as file:
		json.dump(results_dict, file, indent=4)



if __name__ == "__main__":
	#print(check_file("data/20840.xml"))
	#print(json.dumps(data, indent=4))

	file_path = 'data'
	rejection_path = 'rejected_data'
	check_all_compet(file_path,rejection_path)
