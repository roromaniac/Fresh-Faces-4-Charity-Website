import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from app.pages.credits import RAW_CREDITS_LIST
from dotenv import load_dotenv
load_dotenv()
import requests
import os

def get_base_images() -> None:
    """
    Download the Twitch profile image for each user in RAW_CREDITS_LIST['twitch_name'].
    Saves the images locally in an assets directory.
    """
    # Twitch API credentials (should be kept secret in production)
    client_id = os.getenv('TWITCH_PUBLIC_KEY')
    client_secret = os.getenv('TWITCH_PRIVATE_KEY')

    # Step 1: Get OAuth token from Twitch
    auth_url = 'https://id.twitch.tv/oauth2/token'
    auth_params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    auth_resp = requests.post(auth_url, params=auth_params)
    access_token = auth_resp.json().get('access_token', '')

    if not access_token:
        return

    # Step 2: Get user info from Twitch API
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}'
    }

    twitch_usernames = [x['twitch_name'] for x in RAW_CREDITS_LIST if x.get('twitch_name')]
    if not twitch_usernames:
        return

    logins = "&".join([f"login={name}" for name in twitch_usernames])
    url = f"https://api.twitch.tv/helix/users?{logins}"
    user_resp = requests.get(url, headers=headers)
    data = user_resp.json().get("data", [])
    credit_map = {c["twitch_name"].lower(): c for c in RAW_CREDITS_LIST if c.get('twitch_name')}

    for user in data:
        twitch_username = user.get('login')
        profile_url = user.get('profile_image_url')
        if not twitch_username or not profile_url:
            continue

        image = requests.get(profile_url)
        assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "assets"))
        os.makedirs(assets_dir, exist_ok=True)
        image_path = os.path.join(assets_dir, f"{twitch_username}.png")

        if not os.path.exists(image_path):
            with open(image_path, "wb") as f:
                f.write(image.content)
                # Optionally: credit_map[twitch_username]['image'] = image_path

get_base_images()
