import re
import shutil
import sys
import inspect
import asyncio
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

try:
    import google.oauth2.credentials
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.http import MediaFileUpload
    HAS_GOOGLE_LIBS = True
except ImportError:
    HAS_GOOGLE_LIBS = False

from Run.GameRegistry import GameRegistry

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
CLIENT_SECRETS_FILE = PROJECT_ROOT / 'client_secrets.json'
CREDENTIALS_FILE = PROJECT_ROOT / 'youtube_credentials.json'
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube'
]
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
PLAYLIST_ID = "PLy2aC65W0E6uwwybB9RWW5fEoeZo9aZk4"
BACKUP_DIR = Path("H:/Proton Drive/My files/Puzzle")


def check_dependencies():
    print("Vérification des dépendances...")
    if not HAS_GOOGLE_LIBS:
        print("Erreur : Les bibliothèques Google API sont manquantes.")
        print("Veuillez installer les dépendances suivantes :")
        print("pip install google-api-python-client google-auth-oauthlib google-auth-httplib2")
        return False
    print("Dépendances OK.")
    return True


def get_video_files(video_dir="../videos"):
    print(f"Recherche des vidéos dans le dossier : {video_dir}")
    path = Path(video_dir)
    if not path.exists():
        print(f"Le dossier '{video_dir}' n'existe pas.")
        return []
    # On prend webm, mp4, mkv
    videos = [f for f in path.iterdir() if f.suffix.lower() in ('.webm', '.mp4', '.mkv')]
    # Trier par date de modification décroissante
    sorted_videos = sorted(videos, key=lambda x: x.stat().st_mtime, reverse=True)
    print(f"{len(sorted_videos)} vidéo(s) trouvée(s).")
    return sorted_videos


def select_video(videos):
    if not videos:
        print("Aucune vidéo trouvée dans le dossier 'videos/'.")
        return None

    print("\nVidéos disponibles (de la plus récente à la plus ancienne) :")
    for i, video in enumerate(videos):
        print(f"  {i + 1}. {video.name}")

    while True:
        try:
            choice = input("\nSélectionnez le numéro de la vidéo (ou 'q' pour quitter) : ")
            if choice.lower() == 'q':
                print("Opération annulée par l'utilisateur.")
                return None
            idx = int(choice) - 1
            if 0 <= idx < len(videos):
                print(f"Vidéo sélectionnée : {videos[idx].name}")
                return videos[idx]
        except ValueError:
            pass
        print("Choix invalide. Veuillez entrer un numéro valide.")


def import_configs():
    print("Chargement des configurations de jeux...")
    games_dir = Path("Run/Games")
    if not games_dir.exists():
        print("Le dossier Run/Games n'existe pas.")
        return

    count = 0
    for config_file in games_dir.glob("*Config.py"):
        module_name = f"Run.Games.{config_file.stem}"
        try:
            import importlib
            module = importlib.import_module(module_name)
            if hasattr(module, 'register'):
                module.register()
                count += 1
        except Exception as e:
            # On ignore silencieusement les erreurs d'import pour ne pas polluer l'affichage
            pass
    print(f"{count} configuration(s) chargée(s).")


async def get_puzzle_metadata(video_name):
    print(f"Extraction des métadonnées pour la vidéo : {video_name}")
    # On suppose que le nom est {puzzle}_{reste}.extension ou {puzzle} {reste}.extension
    puzzle_name_raw = re.split(r'[_ ]', video_name)[0].lower()

    # Charger toutes les configs pour remplir le registre
    import_configs()

    patterns = GameRegistry.get_all_patterns()
    print(f"Recherche du puzzle '{puzzle_name_raw}' dans {len(patterns)} pattern(s)...")

    best_match_provider = None
    best_match_solver = None
    best_match_url = None

    for pattern, (solver_class, provider_class, player_class) in patterns.items():
        if puzzle_name_raw in pattern.lower() or puzzle_name_raw in solver_class.__name__.lower():
            best_match_provider = provider_class
            best_match_solver = solver_class
            # On essaie d'extraire une URL de base du pattern
            best_match_url = pattern.replace("r\"", "").replace("https://.*", "https://www.").split("/")[0] + "/" + puzzle_name_raw
            print(f"Correspondance trouvée avec le pattern : {pattern}")
            break

    title = f"{puzzle_name_raw.capitalize()} Solver #ortools #playwright"
    description = ""

    # Tentative 1: README.md du solver
    if best_match_solver:
        solver_file = Path(inspect.getfile(best_match_solver))
        readme_path = solver_file.parent / "README.md"
        if readme_path.exists():
            print(f"Recherche de la description dans le README : {readme_path}")
            description = readme_path.read_text(encoding='utf-8')

    # Tentative 2: Docstring du provider
    if not description and best_match_provider:
        print(f"Recherche de la description dans le provider : {best_match_provider.__name__}")
        doc = inspect.getdoc(best_match_provider)
        if doc and "ABC" not in doc:  # éviter la docstring par défaut d'ABC
            description = doc

    # Tentative 3: Docstring du solver
    if not description and best_match_solver:
        print(f"Recherche de la description dans le solver : {best_match_solver.__name__}")
        doc = inspect.getdoc(best_match_solver)
        if doc and "ABC" not in doc:
            description = doc

    # Tentative 4: Scraping minimal si on a une URL gridpuzzle
    if not description and "gridpuzzle.com" in (best_match_url or ""):
        print("Tentative de récupération de la description depuis gridpuzzle.com...")
        try:
            description = await fetch_gridpuzzle_description(puzzle_name_raw)
        except Exception as e:
            print(f"Erreur lors du scraping : {e}")

    if not description:
        description = f"Résolution automatique du puzzle {puzzle_name_raw.capitalize()} utilisant OR-Tools et Playwright."
        print("Utilisation de la description par défaut.")

    print(f"Titre généré : {title}")
    print(f"Description générée : {description[:80]}...")
    return title, description


async def fetch_gridpuzzle_description(puzzle_name):
    from playwright.async_api import async_playwright
    print(f"Ouverture de https://www.gridpuzzle.com/{puzzle_name}")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(f"https://www.gridpuzzle.com/{puzzle_name}")
        # Sur gridpuzzle.com, la description est souvent dans un div .col-lg-12
        desc_element = await page.query_selector('.col-lg-12 p')
        if desc_element:
            text = await desc_element.inner_text()
            await browser.close()
            return text.strip()
        await browser.close()
    return None


def save_credentials(credentials):
    import json
    data = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(data, f)
    print(f"Identifiants sauvegardés dans {CREDENTIALS_FILE}")


def load_credentials():
    import json
    if not CREDENTIALS_FILE.exists():
        return None
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            data = json.load(f)
        creds = google.oauth2.credentials.Credentials(
            token=data['token'],
            refresh_token=data['refresh_token'],
            token_uri=data['token_uri'],
            client_id=data['client_id'],
            client_secret=data['client_secret'],
            scopes=data['scopes']
        )
        # Vérifier si le token est encore valide
        if creds.valid:
            print("Identifiants chargés et valides.")
            return creds
        elif creds.expired and creds.refresh_token:
            print("Token expiré, actualisation en cours...")
            creds.refresh(google.auth.transport.requests.Request())
            save_credentials(creds)
            return creds
    except Exception as e:
        print(f"Erreur lors du chargement des identifiants : {e}")
        return None
    return None


def get_authenticated_service():
    print("Initialisation de l'authentification YouTube...")
    if not CLIENT_SECRETS_FILE.exists():
        print(f"Erreur : Le fichier '{CLIENT_SECRETS_FILE}' est manquant.")
        print("Veuillez placer votre fichier de secrets client OAuth2 dans la racine du projet.")
        return None

    # Essayer de charger des identifiants existants
    credentials = load_credentials()
    
    if not credentials:
        try:
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS_FILE), SCOPES)
            print("Ouverture du navigateur pour l'authentification OAuth2...")
            credentials = flow.run_local_server(port=0)
            print("Authentification réussie.")
            save_credentials(credentials)
        except Exception as e:
            print(f"Erreur lors de l'authentification : {e}")
            return None

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)


def initialize_upload(youtube, video_path, title, description):
    print(f"Préparation de l'upload pour la vidéo : {video_path.name}")
    tags = ["or-tools", "playwright", "solver", "puzzle"]
    puzzle_name = title.split(' ')[0].lower()
    tags.append(puzzle_name)

    body = dict(
        snippet=dict(
            title=title,
            description=description,
            tags=tags,
            categoryId="28"  # Science & Technology
        ),
        status=dict(
            privacyStatus="private"  # Ou "unlisted" / "public"
        )
    )

    insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=MediaFileUpload(str(video_path), chunksize=-1, resumable=True)
    )

    print(f"Début de l'upload de {video_path.name}...")
    response = None
    while response is None:
        status, response = insert_request.next_chunk()
        if status:
            print(f"Upload en cours... {int(status.progress() * 100)}%")

    print(f"Upload terminé ! ID de la vidéo : {response['id']}")
    print(f"URL : https://www.youtube.com/watch?v={response['id']}")
    return response['id']


def check_existing_videos_in_playlist(youtube, puzzle_name, playlist_id):
    print(f"Vérification dans la playlist ID '{playlist_id}' pour le puzzle '{puzzle_name}'...")
    try:
        # Lister les vidéos de la playlist
        existing_videos = []
        next_page_token = None

        while True:
            request = youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response.get("items", []):
                title = item["snippet"]["title"]
                video_id = item["snippet"]["resourceId"]["videoId"]
                # Regex : vérifie si le nom du puzzle est dans le titre
                if re.search(r'\b' + re.escape(puzzle_name) + r'\b', title, re.IGNORECASE):
                    existing_videos.append({"title": title, "id": video_id})

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        if existing_videos:
            print("\n⚠️  Vidéos similaires trouvées dans la playlist :")
            for v in existing_videos:
                print(f"  - {v['title']}")
                print(f"    https://www.youtube.com/watch?v={v['id']}")
            print("Ces vidéos semblent porter sur le même puzzle.")
            return existing_videos
        else:
            print("Aucune vidéo similaire trouvée dans la playlist.")
            return []

    except HttpError as e:
        print(f"Erreur lors de la vérification de la playlist : {e}")
        return []
    except Exception as e:
        print(f"Erreur inattendue lors de la vérification : {e}")
        return []


def add_video_to_playlist(youtube, video_id, playlist_id):
    print(f"Ajout de la vidéo {video_id} à la playlist...")
    try:
        youtube.playlistItems().insert(
            part="snippet",
            body=dict(
                snippet=dict(
                    playlistId=playlist_id,
                    resourceId=dict(
                        kind="youtube#video",
                        videoId=video_id
                    )
                )
            )
        ).execute()
        print(f"Vidéo ajoutée à la playlist avec succès !")
        print(f"URL de la playlist : https://www.youtube.com/playlist?list={playlist_id}")
        return True
    except HttpError as e:
        print(f"Erreur lors de l'ajout à la playlist : {e}")
        return False


def get_latest_video(video_dir="videos"):
    path = Path(video_dir)
    if not path.exists():
        return None
    videos = [f for f in path.iterdir() if f.suffix.lower() in ('.webm', '.mp4', '.mkv')]
    if not videos:
        return None
    return max(videos, key=lambda x: x.stat().st_mtime)


async def upload_video_file(video_path: Path, prompt_confirm=True, move_to_backup=True):
    if not check_dependencies():
        return False

    puzzle_name_raw = re.split(r'[_ ]', video_path.stem)[0].lower()
    title, description = await get_puzzle_metadata(video_path.stem)

    print("\n--- Résumé ---")
    print(f"Titre : {title}")
    print(f"Vidéo : {video_path.name}")
    print("-------------")

    if prompt_confirm:
        confirm = input("\nVoulez-vous uploader cette vidéo sur YouTube ? (o/n) : ")
        if confirm.lower() != 'o':
            print("Upload annulé.")
            return False

    youtube = get_authenticated_service()
    if not youtube:
        print("Impossible de s'authentifier à YouTube.")
        return False

    try:
        print(f"Vérification dans la playlist ID : {PLAYLIST_ID}")
        existing = check_existing_videos_in_playlist(youtube, puzzle_name_raw, PLAYLIST_ID)
        if existing:
            if prompt_confirm:
                confirm_continue = input("\n⚠️  Une vidéo similaire existe déjà dans la playlist. Continuer l'upload ? (o/n) : ")
                if confirm_continue.lower() != 'o':
                    print("Upload annulé.")
                    return False
            else:
                print("⏭️  Vidéo similaire existante ignorée (mode auto).")

        video_id = initialize_upload(youtube, video_path, title, description)
        print("\n=== Upload terminé avec succès ===")
        add_video_to_playlist(youtube, video_id, PLAYLIST_ID)

        if move_to_backup:
            try:
                BACKUP_DIR.mkdir(parents=True, exist_ok=True)
                dest = BACKUP_DIR / video_path.name
                shutil.move(str(video_path), str(dest))
                print(f"Vidéo déplacée vers {dest}")
            except Exception as e:
                print(f"Erreur lors du déplacement de la vidéo : {e}")
        return True

    except HttpError as e:
        print(f"\nUne erreur HTTP est survenue : {e.resp.status} {e.content}")
    except Exception as e:
        print(f"\nUne erreur est survenue lors de l'upload : {e}")
        import traceback
        traceback.print_exc()
    return False


async def main():
    print("=== PuzzleGames YouTube Uploader ===")
    print("Initialisation...\n")

    if not check_dependencies():
        return

    videos = get_video_files()
    selected = select_video(videos)
    if not selected:
        print("Fin du programme.")
        return

    await upload_video_file(selected)


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
