import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "5784723595:AAEL26cA8Qbj-UcDeFoTquL3H-5bzrPxmAU")
API_ID = int(os.environ.get("API_ID", "23217719"))
API_HASH = os.environ.get("API_HASH", "03b3a05a0cf5601241463840ba9900d0")
AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "1983530070").split())
DATA_URL = os.environ.get("DATA_URL", "mongodb+srv://SAM:Flo@1303@cluster0.5nyz2uw.mongodb.net/?retryWrites=true&w=majority")
DATA_NAME = os.environ.get("DATA_NAME", "Music_downloder")
