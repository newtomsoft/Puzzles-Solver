import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))


LINKEDIN_PROFILE_URL = "https://www.linkedin.com/in/{user}/details/featured/"
CREDENTIALS_FILE = Path(__file__).parent.parent / "linkedin_credentials.json"


def check_dependencies():
    print("Vérification des dépendances...")
    try:
        from rebrowser_playwright.async_api import async_playwright
        print("Dépendances OK.")
        return True
    except ImportError:
        print("Erreur : playwright n'est pas installé.")
        print("Veuillez installer : pip install playwright")
        return False


async def load_credentials():
    import json
    if not CREDENTIALS_FILE.exists():
        return None
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return None


async def save_credentials(email, password):
    import json
    data = {"email": email, "password": password}
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(data, f)
    print(f"Identifiants sauvegardés dans {CREDENTIALS_FILE}")


async def linkedin_login(page):
    print("Connexion à LinkedIn...")

    # Charger les identifiants sauvegardés ou demander
    creds = await load_credentials()
    if not creds:
        email = input("Email LinkedIn : ")
        password = input("Mot de passe LinkedIn : ")
        await save_credentials(email, password)
        creds = {"email": email, "password": password}

    email = creds["email"]
    password = creds["password"]

    await page.goto("https://www.linkedin.com/login")

    # Remplir le formulaire de connexion
    await page.fill('input[name="session_key"]', email)
    await page.fill('input[name="session_password"]', password)
    await page.click('button[type="submit"]')

    # Attendre la navigation ou la vérification 2FA
    await page.wait_for_load_state("networkidle")

    # Vérifier si connexion réussie
    if "login" in page.url:
        print("Échec de la connexion. Veuillez vérifier vos identifiants.")
        return False

    print("Connexion réussie.")
    return True


async def add_featured_link(page, youtube_url):
    print(f"Ajout du lien YouTube à la section Featured : {youtube_url}")

    # Aller sur la page des détails/featured
    await page.goto("https://www.linkedin.com/me/profile-details/featured/")

    # Attendre que la page charge
    await page.wait_for_load_state("networkidle")

    # Cliquer sur le bouton "Ajouter" - sélecteur peut varier
    try:
        # Essayer de trouver le bouton "Ajouter un lien" ou similaire
        add_button = await page.wait_for_selector(
            'button[aria-label*="Ajouter"]', timeout=5000
        )
        await add_button.click()
        await asyncio.sleep(1)

        # Sélectionner "Lien" parmi les options
        link_option = await page.wait_for_selector(
            'text=Lien', timeout=5000
        )
        await link_option.click()
        await asyncio.sleep(1)
    except Exception:
        # Essayer une approche alternative - cliquer direct sur "Lien externe"
        try:
            link_btn = await page.wait_for_selector(
                'button[aria-label*="Lien externe"], button:has-text("Lien externe")',
                timeout=5000
            )
            await link_btn.click()
            await asyncio.sleep(1)
        except Exception:
            print("Impossible de trouver le bouton d'ajout de lien.")
            return False

    # Remplir l'URL
    try:
        url_input = await page.wait_for_selector(
            'input[name="url"], input[placeholder*="lien"], input[placeholder*="URL"]',
            timeout=5000
        )
        await url_input.fill(youtube_url)

        # Soumettre
        submit_btn = await page.wait_for_selector(
            'button[type="submit"], button:has-text("Ajouter")',
            timeout=5000
        )
        await submit_btn.click()

        print("Lien ajouté avec succès !")
        return True
    except Exception as e:
        print(f"Erreur lors de l'ajout du lien : {e}")
        return False


async def upload_featured_link(youtube_url):
    if not check_dependencies():
        return False

    from rebrowser_playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            if not await linkedin_login(page):
                return False

            success = await add_featured_link(page, youtube_url)

            if success:
                print("\n=== Lien ajouté avec succès à LinkedIn ===")
            return success

        finally:
            await browser.close()


async def main():
    print("=== LinkedIn Featured Link Adder ===")
    print("Ce script ajoute un lien YouTube à votre section Featured LinkedIn.\n")

    # Demander l'URL YouTube
    youtube_url = input("Entrez l'URL YouTube à ajouter : ").strip()

    if not youtube_url:
        print("URL vide. Fin du programme.")
        return

    # Vérifier que c'est une URL YouTube valide
    if "youtube.com" not in youtube_url and "youtu.be" not in youtube_url:
        print("Attention : L'URL ne semble pas être une URL YouTube valide.")

    await upload_featured_link(youtube_url)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterruption par l'utilisateur.")
        sys.exit(0)
    except Exception as e:
        print(f"\nErreur inattendue : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)