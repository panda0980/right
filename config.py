import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "5614754139:AAHic-ZQLWl5lt5SXF4MJLMY7IZXCp9xvzs")
API_ID = int(os.environ.get("API_ID", "11671320"))
API_HASH = os.environ.get("API_HASH", "8e409e260f1d80f0ead65da912ee07bb")
AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "1983530070").split())
DATA_URL = os.environ.get("DATA_URL", "mongodb+srv://panda:eGOv61gScegMQddj@cluster0.lilgk.mongodb.net/?retryWrites=true&w=majority")
DATA_NAME = os.environ.get("DATA_NAME", "Music_downloder")