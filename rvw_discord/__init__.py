TOKEN = '---------------'

import discord
from discord import channel
from discord.ext import commands
from discord.utils import get

import random

intents = discord.Intents.all()
intents.reactions = True
intents.members = True
intents.guilds = True

owner = '--------'


class WolfHelper(discord.Client):
    async def reset(self):
        canal = self.get_channel(891414194803572787)
        await canal.purge(limit=100)
        # self.get_emoji()
        emb = discord.Embed(title='Selecteaza-ti rolul in echipa!',description="Apasa pe reactia cu numarul corespunzator rolului tau in echipa!\n\n1️⃣ - Voluntar\n2️⃣ - Programator\n3️⃣ - Mecanic\n4️⃣ - Design 3D\n5️⃣ - Media",color=discord.Colour.red())
        msg = await canal.send(embed=emb)
        await msg.add_reaction("1️⃣")
        await msg.add_reaction("2️⃣")
        await msg.add_reaction("3️⃣")
        await msg.add_reaction("4️⃣")
        await msg.add_reaction("5️⃣")
        emb = discord.Embed(title='Schimba-ti nickname-ul ca sa stim cine esti', description="Scrie in chat !nume <numele tau intreg>", color=discord.Colour.red())
        msg = await canal.send(embed=emb)

    async def on_ready(self):
        print('Bot inregistrat cu id-ul {0}!'.format(self.user))
        # await self.reset()
        

    async def on_message(self, message):
        if message.content.startswith("!"):
            if "nume" in message.content:
                if ' ' in message.content:
                    membru = message.author
                    splits = message.content.split(" ")
                    nume = ""
                    for i in range(1, len(splits)):
                        nume += message.content.split(" ")[i]+" "
                    nume = nume.strip().lower().title()
                    await membru.edit(nick=nume)
                await message.channel.purge(limit=1)
                return
            if str(message.author) == owner:
                if "clear" in message.content:
                    lim = 1
                    if ' ' in message.content:
                        try:
                            lim = int(message.content.split(" ")[1])
                        except:
                            lim=0
                    lim+= 1
                    await message.channel.purge(limit=lim)
                if "reset" in message.content and message.channel.id == 891414194803572787:
                    await self.reset()

    async def on_raw_reaction_add(self, payload):
        user = client.get_user(payload.user_id)
        guild = client.get_guild(payload.guild_id)
        print(user, payload.emoji)
        if payload.channel_id == 891414194803572787 and not str(user) == "Wolf Helper#9563":
            gasit = False
            if str(payload.emoji) == "1️⃣":
                rol = get(guild.roles, name="Voluntar")
                gasit=True
            if str(payload.emoji) == "2️⃣":
                rol = get(guild.roles, name="Programator")
                gasit=True
            if str(payload.emoji) == "3️⃣":
                rol = get(guild.roles, name="Mecanic")
                gasit=True
            if str(payload.emoji) == "4️⃣":
                rol = get(guild.roles, name="Designer")
                gasit=True
            if str(payload.emoji) == "5️⃣":
                rol = get(guild.roles, name="Media")
                gasit=True

            if gasit:
                if len(payload.member.roles) > 1:
                    await payload.member.send("Ai deja rolul de "+payload.member.roles[1].name+".\nDaca ai gresit rolul, contacteaza un administrator/membru din board.")
                else:
                    await payload.member.add_roles(rol)
                    await payload.member.send("Rolul \""+rol.name+"\" ti-a fost atribuit")


client = WolfHelper(intents=intents)

client.run(TOKEN)