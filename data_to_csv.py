import os
import pandas as pd
import xml.etree.ElementTree as ET
import json


def get_files_shape(file_path):
	data = []
	for file in os.listdir(file_path):
		print(file)
		if file.endswith(".xml"):
			tree = ET.parse(os.path.join(file_path, file))
			root = tree.getroot()
			fileData={root:{}}


def file_to_dico_item(file):
	if file.endswith(".xml"):
		tree = ET.parse(file)
		root = tree.getroot()
		if root.tag!="CompetitionIndividuelle":
			raise Exception("No individual competition in "+file)
		infoCompet = root.attrib
		if infoCompet == None:
			raise ValueError("No individual competition in "+file)

		dataCompet={
			"ID":infoCompet.get("ID"),
			"FileName":file,
			"Date":infoCompet.get("Date"),
			"Lieu":infoCompet.get("Lieu"),
			"Arme":infoCompet.get("Arme"),
			"Categorie":infoCompet.get("Categorie"),
			"Niveau":infoCompet.get("Niveau"),
			"Poules":{},
			"Tableaux":{},
			"Tireurs":{}
		}


		for tireur in root.find("Tireurs"):
			dataCompet["Tireurs"][tireur.get("ID")]={"LicenceNat":tireur.get("LicenceNat"),
													"Licence":tireur.get("Licence"),
													"Nom":tireur.get("Nom"),
													"Prenom":tireur.get("Prenom"),
													"Sexe":tireur.get("Sexe"),
													"Lateralite":tireur.get("Lateralite"),
													"DateNaissance":tireur.get("DateNaissance"),
													"RangInitialPoule":None,
													"RangFinalPoule":None,
													"RangFinalTableau":None
													}
				
			

		for phase in root.findall("Phases"):

			if len(phase.findall("TourDePoules"))>1:
				print(f"WARNING : {file} contains more than 1 poule")

			tourDePoule=phase.find("TourDePoules")
			for tireur in tourDePoule.findall("Tireur"):
				try :
					dataCompet["Tireurs"][tireur.get("REF")]["RangInitialPoule"]=tireur.get("RangInitial")
					dataCompet["Tireurs"][tireur.get("REF")]["RangFinalPoule"]=tireur.get("RangFinal")

				except KeyError:
					print(f"error: {file} -> tourDePoule -> tireuf ref: {tireur.get('REF')} not found in tireur dict")

			for iPoule,poule in enumerate(tourDePoule.findall("Poule")):
				matchsPoule={}
				resultsPoule={}
				for tireur in poule.findall("Tireur"):
					refTir=tireur.get("REF")
					rangTir=tireur.get("RangPoule")
					resultsPoule[refTir]=rangTir

				dataCompet["Poules"][str(iPoule)]={"Results":resultsPoule}
				for iMatch,match in  enumerate(poule.findall("Match")):
					matchsPoule[str(iMatch)]={}
					for tireur in match.findall("Tireur"):
						matchsPoule[str(iMatch)][tireur.get("REF")]={"Score":tireur.get("Score"),"Statut":tireur.get("Statut")}

				dataCompet["Poules"][str(iPoule)]["Results"]=resultsPoule
				dataCompet["Poules"][str(iPoule)]["Matchs"]=matchsPoule
				
			phaseDeTableaux=phase.find("PhaseDeTableaux")
			if phaseDeTableaux:
				for tireur in phaseDeTableaux.findall("Tireur"):
					try :
						dataCompet["Tireurs"][tireur.get("REF")]["RangFinalTableau"]=tireur.get("RangFinal")
					except KeyError:
						print(f"error: {file} -> phaseDeTableaux -> tireuf ref: {tireur.get('REF')} not found in tireur dict")

				matchsTableau={}
				for iMatch,match in enumerate(phaseDeTableaux.find("SuiteDeTableaux").findall("Match")):
					matchsTableau[str(iMatch)]={}
					for tireur in match.findall("Tireur"):
						matchsTableau[str(iMatch)][tireur.get("REF")]={"Score":tireur.get("Score"),"Statut":tireur.get("Statut")}
				dataCompet["Tableaux"][str(iMatch)]={"Matchs":matchsTableau}



	return(dataCompet)

def is_hidden(filepath):
    return bool(os.stat(filepath).st_file_attributes & 2)  # 2 = FILE_ATTRIBUTE_HIDDEN

def get_all_compet_data(path):
	data = []
	for file in os.listdir(path):
		file_path=os.path.join(path, file)
		if not file.startswith(".") and not is_hidden(file_path):
			print("reading file "+file)
			try :
				data.append(file_to_dico_item(file_path))



			except Exception as e:
				print(f"Erreur : {e} in file {file}")
					



	df = pd.DataFrame(data)
	df.to_csv("competitions_data.csv", index=False)

def get_tireurs_data(file_path):
	
	data = []
	for file in os.listdir(file_path):
		print("reading file "+file)
		if file.endswith(".xml"):
			tree = ET.parse(os.path.join(file_path, file))
			root = tree.getroot()
			
			for child in root:
				if child.tag=="Tireurs":
					for tireur in child :
						data.append({
							"Licence": tireur.get("Licence"),
							"DateNaissance": tireur.get("DateNaissance"),
							"Sexe": tireur.get("Sexe"),
							"Nation": tireur.get("Nation"),
							"Club": tireur.get("Club"),
							"Classement": tireur.get("Classement"),
							"Ranking": tireur.get("Ranking")
						})
						print(data[-1])



	df = pd.DataFrame(data)
	df.to_csv("tireurs_data.csv", index=False)


if __name__ == "__main__":
	#data=file_to_dico_item("data/20840.xml")
	#print(json.dumps(data, indent=4))

	file_path = 'data'
	get_all_compet_data(file_path)
