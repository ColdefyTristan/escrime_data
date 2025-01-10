from playwright.sync_api import sync_playwright
import requests

def download_files():
    with sync_playwright() as p:
        # Lancement du navigateur headless
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Accéder à la page
        page.goto("https://www.escrime-info.com/gregxml/Greg/BD/ChercheEpreuve.html")

        # Cliquer sur le lien "Rechercher"
        try:
            page.click("a[ng-click='recherche()']")  # Sélecteur du lien
            page.wait_for_timeout(5000)  # Attendre que les résultats se chargent
        except Exception as e:
            print("Erreur lors du clic sur le lien :", e)
            browser.close()
            return

        # Extraire les liens contenant "services/service"
        try:
            links = page.eval_on_selector_all(
                "a[href*='services/service']",
                "elements => elements.map(e => e.href)"  # Récupérer l'attribut href de chaque lien
            )
            print(f"Liens trouvés : {links}")
        except Exception as e:  
            print("Erreur lors de l'extraction des liens :", e)
            browser.close()
            return

        # Télécharger les fichiers à partir des liens
        for link in links:
            try:
                file_name = "data/"+link.split('=')[-1] + ".xml"  # Nom de fichier basé sur l'ID
                response = requests.get(link)
                with open(file_name, 'wb') as file:
                    file.write(response.content)
                print(f"Téléchargé : {file_name}")
            except Exception as e:
                print(f"Erreur lors du téléchargement du fichier {link} :", e)

        # Fermer le navigateur
        browser.close()

if __name__ == "__main__":
    download_files()
