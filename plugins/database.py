import datetime
import motor.motor_asyncio 

 
class Database:
    def __init__(self, uri,  database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.users = self.db.users
        self.groups = self.db.groups

    def new_user(self, id, name):
        return dict(id=id, 
        name=name, 
        join_date=datetime.date.today().isoformat())

    async def add_user(self, id, name):
        user = self.new_user( id, name)
        await self.users.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.users.find_one({'id':int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.users.count_documents({})
        return count

    async def get_all_users(self):
        return self.users.find({})

    async def delete_user(self, user_id):
        await self.users.delete_many({'id': int(user_id)})

    def new_group(self, id, title):
        return dict(id=id, title=title, chat_status=dict(is_disabled=False, reason=""))
       
    async def is_group_exist(self, id):
        group = await self.groups.find_one({'id':int(id)})
        return bool(group)
        
    async def add_chat(self, chat, title):
        chat = self.new_group(chat, title)
        await self.groups.insert_one(chat)
    async def get_chat(self, chat):
        chat = await self.groups.find_one({'id':int(chat)})
        if not chat:
            return False
        else:
            return chat.get('chat_status')
    
    async def re_enable_chat(self, id):
        chat_status=dict(is_disabled=False, reason="")
        await self.groups.update_one({'id': int(id)}, {'$set': {'chat_status': chat_status}})
    
    async def disable_chat(self, chat, reason="No Reason"):
        chat_status=dict(is_disabled=True, reason=reason)
        await self.groups.update_one({'id': int(chat)}, {'$set': {'chat_status': chat_status}})
   
    async def total_chat_count(self):
        count = await self.groups.count_documents({})
        return count    

    async def get_all_chats(self):
        return self.groups.find({})