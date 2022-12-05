from pyrogram import Client
from pyrogram.raw.all import layer
from config import API_ID, API_HASH, BOT_TOKEN





class Musicdownloader(Client):

    def __init__(self):
        super().__init__(
            "Musicdownloader",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        await super().start()      
        me = await self.get_me()
        BOT_USERNAME = me.username
        BOT_NAME = me.first_name
        self.username = '@' + me.username
        print(f"{me.first_name} with  started on {me.username}.")
       
          

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped. Bye.")
        




app =  Musicdownloader()

print("bot successfully started")

app.run()


"""
admin commands
/send -  send the message to users
/send_groups - send the message to groups
/chatlist - get the group list in the bot server
/status- to tracjk the usres and groups count

 contact-  https://t.me/saranselva1
"""
