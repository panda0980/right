import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "1983530070").split())
DATA_URL = os.environ.get("DATA_URL")
DATA_NAME = os.environ.get("DATA_NAME", "Music_downloder")
