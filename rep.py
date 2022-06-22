from .. import loader, utils
from telethon import events
import random

class ReputationMod(loader.Module):
    """Reputation of users"""
    strings = {"name": "Reputation"}
    template = "<b>%s</b> » <a href=tg://user?id=%s>%s</a> — <b>%s</b> ♥️\n"
    loading = ["😸", "😼", "🧐", "🐈", "🦊", "🦋", "🐍", "🍀", "⚡️", "🌼"]
  
    async def client_ready(self, client, db):
        self.db = db
        self.client = client

        client.add_event_handler(self.on_rep_change, events.NewMessage)
        client.add_event_handler(self.on_user_join, events.ChatAction)
        self.me = await client.get_me()
        
    @loader.ratelimit
    async def repcmd(self, message):
        args = utils.get_args_raw(message).split(" ", maxsplit=2)
        user = await self.client.get_entity(message.sender_id)

        if not user.bot:
            if not args[0]:
                number = self.db.get("Reputation", str(message.sender_id), 0)
                await message.reply(f"<b>{user.first_name}</b>, your reputation: <b>{number}</b> ❤️")
            elif args[0] == "top":
                users = self.db["Reputation"]
                top = ""
                load = await message.reply("<b>Loading... </b>" + random.choice(self.loading))
                for n, i in enumerate(sorted(users.items(), key=lambda x: x[1])[::-1]):
                    if n == 10: break
                    user = await self.client.get_entity(int(i[0]))
                    top +=  self.template % (n + 1, user.id, user.first_name, i[1])
                await load.edit(top)
        if message.sender_id == self.me.id:
            if args[0] == "getdb":
                users = self.db["Reputation"]
                await message.edit(f"<code>{users}</code>")
            elif args[0] == "set":
                if message.is_reply:
                    reply = await message.get_reply_message()
                    self.db.set("Reputation", str(reply.sender_id), int(args[1]))
                else:
                    self.db.set("Reputation", str(args[1]), int(args[2]))
                await message.edit(f"The user's reputation " + (f"<b>{reply.sender_id}</b>" if message.is_reply else f"<b>{args[1]}</b>") + " was successfully changed to " + (f"<b>{args[1]}</b>" if message.is_reply else f"<b>{args[2]}</b>"))

    async def on_rep_change(self, message):
        if message.is_reply and not message.is_private:
            reply = await message.get_reply_message()
            user = await self.client.get_entity(reply.sender_id)
            
            number = self.db.get("Reputation", str(reply.from_id.user_id), 0)
            if message.from_id.user_id != reply.from_id.user_id:
                if not user.bot:
                    if message.text == "+":
                        number += 1
                        self.db.set("Reputation", str(reply.from_id.user_id), number)
                        await message.reply(f"Like! You have increased the reputation of the user <b>{user.first_name}</b>.\nNow its reputation is: <b>{number}</b> ❤️")
                    elif message.text == "-":
                        number -= 1
                        self.db.set("Reputation", str(reply.from_id.user_id), number)
                        await message.reply(f"Dislike! You have decreased the reputation of the user <b>{user.first_name}</b>.\nNow its reputation is: <b>{number}</b> 💔")
            elif message.text == "+" or message.text == "-":
                    await message.reply("You can't change your reputation!")    

    async def on_user_join(self, message):
        if message.user_joined or message.user_added:
            user = await message.get_user()
            chat = await message.get_chat()
            if user.id != self.me.id:
                number = self.db.get("Reputation", str(user.id), 0)
                return await message.reply(f"<b>{user.first_name}</b>, welcome to chat <b>{chat.title}</b>!" + (f"\n\nYour reputation: <b>{number}</b> ❤️" if number != 0 else " "))