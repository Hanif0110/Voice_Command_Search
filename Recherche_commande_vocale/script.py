import speech_recognition as sr
import pyttsx3
import locale
import os
import time
from datetime import datetime

# Initialisation du moteur de synthèse vocale
engine = pyttsx3.init()

# Fonction pour parler
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Détecter la langue du système
def get_system_language():
    system_lang, _ = locale.getlocale()  # Utilisation de getlocale() au lieu de getdefaultlocale() pour éviter le warning
    return system_lang

# Fonction pour écouter la commande vocale en fonction de la langue détectée
def get_audio(system_lang, retries=3):
    recognizer = sr.Recognizer()
    attempt = 0
    while attempt < retries:
        with sr.Microphone() as source:
            print("Je vous écoute...")
            audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_google(audio, language=system_lang)
                print(f"Vous avez dit: {command}")
                return command.lower()
            except sr.UnknownValueError:
                speak("Je n'ai pas compris, pouvez-vous répéter ?")
            except sr.RequestError:
                speak("Erreur de reconnaissance vocale. Assurez-vous d'avoir une connexion internet.")
                return ""
        attempt += 1
    speak("Trop de tentatives. Arrêt de la reconnaissance vocale.")
    return ""

# Confirmation avant d'effectuer une action
def confirm_action(text):
    speak(text)
    response = get_audio(get_system_language())
    return "oui" in response

# Fonction pour rechercher un fichier ou dossier en fonction du mot clé
def find_file_or_folder(name, root_path="C:\\"):
    found_items = []
    unique_types = set()
    print(f"Recherche en cours pour '{name}' ...")

    start_time = time.time()

    # Recherche dans le système de fichiers
    for dirpath, dirnames, filenames in os.walk(root_path):
        current_time = time.time()
        elapsed_time = int(current_time - start_time)
        print(f"Recherche en cours: {elapsed_time} secondes...", end="\r")
        
        for dirname in dirnames:
            if name.lower() in dirname.lower():
                found_items.append({
                    'type': 'dossier',
                    'path': os.path.join(dirpath, dirname),
                    'mod_time': os.path.getmtime(os.path.join(dirpath, dirname))
                })
                unique_types.add('dossier')
        
        for filename in filenames:
            if name.lower() in filename.lower():
                file_path = os.path.join(dirpath, filename)
                file_type = filename.split(".")[-1] if "." in filename else "autre"
                found_items.append({
                    'type': file_type,
                    'path': file_path,
                    'mod_time': os.path.getmtime(file_path)
                })
                unique_types.add(file_type)

    if found_items:
        speak(f"J'ai trouvé {len(found_items)} éléments contenant {name}.")
        print(f"Types trouvés: {', '.join(unique_types)}")
        speak(f"Quel type souhaitez-vous explorer ?")
        desired_type = get_audio(get_system_language())

        if confirm_action(f"Vous avez choisi le type {desired_type}, est-ce correct ?"):
            filtered_items = [item for item in found_items if item['type'] == desired_type]
        else:
            speak("Veuillez entrer le type souhaité.")
            desired_type = input("Entrez le type: ")
            filtered_items = [item for item in found_items if item['type'] == desired_type]

        # Ajout de la demande claire pour "TOUT" ou "DEPUIS UNE DATE"
        speak("Voulez-vous voir tous les fichiers (dites 'TOUT') ou bien filtrer par date (dites 'DEPUIS UNE DATE') ?")
        filter_choice = get_audio(get_system_language())

        if "tout" in filter_choice:  # On vérifie si "TOUT" est dit
            speak("Affichage de tous les fichiers.")
        elif "depuis une date" in filter_choice:
            speak("Indiquez la date de dernière modification au format 'jour mois année', par exemple, '1er janvier 2022'.")
            mod_date = get_audio(get_system_language())
            try:
                # Conversion en format date - Gestion des jours et mois avec des espaces et minuscules
                mod_date_timestamp = datetime.strptime(mod_date, "%d %B %Y").timestamp()
                filtered_items = [item for item in filtered_items if item['mod_time'] >= mod_date_timestamp]
            except ValueError:
                try:
                    # Essayer un autre format de date si l'utilisateur entre un autre format
                    mod_date_timestamp = datetime.strptime(mod_date, "%d %m %Y").timestamp()
                    filtered_items = [item for item in filtered_items if item['mod_time'] >= mod_date_timestamp]
                except ValueError:
                    speak("Date invalide, aucun filtre appliqué.")

        speak(f"J'ai trouvé {len(filtered_items)} fichiers correspondant à votre requête.")
        for item in filtered_items:
            print(f"Chemin : {item['path']}")
            print()

        return filtered_items
    else:
        speak(f"Aucun fichier ou dossier contenant {name} n'a été trouvé.")
        return []

# Assistant vocal pour explorer les fichiers
def assistant():
    # Timer de début
    start_time = time.time()

    system_lang = get_system_language()
    speak(f"Langue du système détectée : {system_lang}")

    speak("Bienvenue. Voulez-vous rechercher un fichier ou un dossier ? Dites 'RECHERCHER' pour commencer.")
    command = get_audio(system_lang)

    if "rechercher" in command:
        if confirm_action("Vous voulez rechercher un fichier ou un dossier, est-ce correct ?"):
            speak("Quel est le mot clé du fichier ou dossier que vous cherchez ?")
            search_name = get_audio(system_lang)

            if confirm_action(f"Vous avez dit '{search_name}', est-ce bien cela ?"):
                find_file_or_folder(search_name)
            else:
                speak("Veuillez entrer le mot clé.")
                search_name = input("Entrez le mot clé: ")
                find_file_or_folder(search_name)
        else:
            speak("Commande annulée.")
    
    elif "arrêter" in command or "quitter" in command:
        speak("Arrêt de l'assistant.")

    # Timer de fin et affichage de la durée totale
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Le script a pris {total_time:.2f} secondes pour s'exécuter.")

# Lancer l'assistant
assistant()
