# -*- coding: UTF-8 -*-

from colorama import Fore

import platform
import os
import json
import time
import zipfile
import rarfile

#################################################################################################################################################

plt = platform.system()

with open('config.json', 'r') as file:
	config = json.load(file)
	rarfile.UNRAR_TOOL = config["UNRAR_PATH"]

with open('password.txt', 'r') as file:
	password = file.readlines()[0]
	print("Password Loaded :", password)

#################################################################################################################################################

Banner = Fore.MAGENTA + """
                    _     _            _____                     _               
     /\            | |   (_)          / ____|                   | |              
    /  \   _ __ ___| |__  ___   _____| (___   ___  __ _ _ __ ___| |__   ___ _ __ 
   / /\ \ | '__/ __| '_ \| \ \ / / _ \\___ \ / _ \/ _` | '__/ __| '_ \ / _ \ '__|
  / ____ \| | | (__| | | | |\ V /  __/____) |  __/ (_| | | | (__| | | |  __/ |   
 /_/    \_\_|  \___|_| |_|_| \_/ \___|_____/ \___|\__,_|_|  \___|_| |_|\___|_|   
                                                                                                                                      
                  		  [/ Developer : GameBak \]

"""

menuList = ["Search file in one archive", "Search file in all archives of folder", "List files infos", "Extract all names file in file", "Search and extract files from all archives in folder"]
ModuleChoice = 0

############################################ - Définition Fonction - #################################################################################

def checkExt(ext, file):
	print("\n" + Fore.RESET + file)

	try:
		if "rar" in ext.lower() or "7z" in ext.lower():
			f = rarfile.RarFile(file)
			f.setpassword(pwd=password)
		if "zip" in ext.lower():
			f = zipfile.ZipFile(file, 'r')
	except RuntimeError as e:
		os.replace(file, f"Error/{file}")
		print('Error', str(e))

	if (menuList[ModuleChoice-1] == "Search and extract files from all archives in folder"):
		for i in f.namelist():
			if QuestionFileSort.lower() in i.lower():
				try:
					f.extract(i, "./Results/" + QuestionSortie)
				except zipfile.LargeZipFile as e:
					if "File is encrypted" in str(e):
						f.setpassword(pwd=password)
						f.extract(i, "./Results/" + QuestionSortie)
				except Exception as e:
					print(f"Error Extracting path : {i} {str(e)}")

	if (menuList[ModuleChoice-1] == "Search file in one archive" or menuList[ModuleChoice-1] == "Search file in all archives of folder"):
		retrieved_elements = list(filter(lambda x: QuestionSearch in x, f.namelist()))
		if len(retrieved_elements) != 0: return print(Fore.LIGHTGREEN_EX + "\nFile is Found")
		else: return print(Fore.LIGHTRED_EX + "File is not Found")
	else:
		for f1 in f.namelist():
			if (menuList[ModuleChoice-1] == "List files infos"): print(f"------------\nName : {f1}")
			if (menuList[ModuleChoice-1] == "Extract all names in file"):
				createFolder("./Results/" + QuestionSortie)

				fileOutput = open("./Results/" + QuestionSortie + "/FilesOfArchive.txt", 'a+')
				fileOutput.write(str(f1.encode("utf-8")) + '\n')

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Impossible de crée le dossier : ' + directory)

def ModuleMenu():
    nombre = 0

    for module in menuList:
        nombre += 1
        print(Fore.LIGHTMAGENTA_EX + "[" + str(nombre) + "] " + module)

    print('\n')

def Reset():
    time.sleep(1.1)

    if plt == "Windows": os.system("cls")
    elif plt == "Linux": os.system("clear")
    elif plt == "Darwin": os.system("clear")

    print(Banner)
    ModuleMenu()

def ModuleExec(file, ext):
	if (menuList[ModuleChoice-1] == "Search file in all archives of folder"):
		listRarfiles = os.listdir(Question)
		
		for l in listRarfiles:
			if(os.path.isfile(file + "\\" + l)):
				file_name, file_extension = os.path.splitext(file + "\\" + l)

				try:
					checkExt(file_extension, file + "\\" + l)
				except Exception as e:
					print(f"Error opening archive : {str(e)}")				

	elif (menuList[ModuleChoice-1] == "Search and extract files from all archives in folder"):
		createFolder("./Results/" + QuestionSortie)
		listRarfiles = os.listdir(Question)
		
		for l in listRarfiles:
			if(os.path.isfile(file + "\\" + l)):
				file_name, file_extension = os.path.splitext(file + "\\" + l)
				
				try:
					checkExt(file_extension, file + "\\" + l)
				except Exception as e:
					print(f"Error opening archive : {str(e)}")
	else:
		try:
			checkExt(ext, file)
		except Exception as e:
			print(f"Error opening archive : {str(e)}")

#################################################################################################################################################

createFolder("./Error")
Reset()

while (True):
	QuestionMenu = input(Fore.RESET + "Séléctionner votre Module : ")

	if (QuestionMenu.isnumeric()):
		if (0 < int(QuestionMenu) <= len(menuList)):
			ModuleChoice = int(QuestionMenu)
			break
		else:
			print(Fore.LIGHTRED_EX + "[!] Vous devez entrer un nombre correspondant à un module." + Fore.RESET)
			Reset()
	else:
		print(Fore.LIGHTRED_EX + "[!] Vous devez entrer un nombre correspondant à un module." + Fore.RESET)
		Reset()


if (menuList[ModuleChoice-1] == "Search file in all archives of folder"): Question = input("Enter path of folder : ")
else: Question = input("Enter path of archive : ")

file_name, file_extension = os.path.splitext(Question)

if (menuList[ModuleChoice-1] == "Search file in one archive" or menuList[ModuleChoice-1] == "Search file in all archives of folder"):
	QuestionSearch = input(Fore.RESET + "Entrez le nom du fichier que vous cherchez : ")

if (menuList[ModuleChoice-1] == "Extract all names in file"):
	QuestionSortie = input(Fore.RESET + "Entrez le nom du Dossier de Sortie : ")

if(menuList[ModuleChoice-1] == "Search and extract files from all archives in folder"):
	QuestionFileSort = input(Fore.RESET + "Entrez le mot des fichiers que vous voulez extraire : ")
	QuestionSortie = input(Fore.RESET + "Entrez le nom du Dossier de Sortie : ")

ModuleExec(Question, file_extension)

#################################################################################################################################################

input(Fore.RESET + "\nCheck fini, appuyez sur ENTER pour quitter : ")

#################################################################################################################################################
