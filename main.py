import discord
from discord.ext import commands, tasks
from discord import app_commands
from messageHandler import get_message, postInfo

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='', intents=intents)

def start_message_listen(server_id ,channel_id):    
    @tasks.loop(seconds=2)
    async def messageLoop():
        message = await get_message("link", "1")
        if message["error"] != True:
            guild = bot.get_guild(server_id)
            if guild is None:
                print(f"Guild with ID {server_id} not found.")
                return
            
            channel = guild.get_channel(channel_id)
            if channel is None:
                print(f"Channel with ID {channel_id} not found or not accessible.")
                return
            
            await channel.send(f"{message['response']['message']}")
            
    if(messageLoop.is_running() != True):
        messageLoop.start()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)   
    
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(str(message.author) + ": " + str(message.content))

@bot.tree.command(name="set-responce-point")
async def set_responce_point(interaction: discord.Interaction):
    channelJSON = {"channelID" : str(interaction.channel_id)}
    res = await postInfo("server", str(interaction.guild_id), data=channelJSON)
    if(res["error"] != True):
        await interaction.response.send_message("Channel Set")
    else:
        await interaction.response.send_message(f"{res['response']}")
        
@bot.tree.command(name="start-link")
async def start_link(interaction: discord.Interaction):
    res = await get_message("server", str(interaction.guild_id))
    if(res["error"] != True):
        start_message_listen(interaction.guild_id, int(res['response']['channelID']))
        await interaction.response.send_message("Link Started")
    else:
        await interaction.response.send_message("Responce point not set")
    
@bot.tree.command(name="test")
async def test(interaction: discord.Interaction):
    channel_id = await get_message("server", str(interaction.guild_id))
    await interaction.response.send_message(f"{channel_id}")

bot.run("MTI3NDY3NjU4NjMwNTY4NzU3NQ.GAZSsu.U5ewAZ1mPtHwjjmBRp67jZ6fy8sjn-Fod6ldew")