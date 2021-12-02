import a2s
import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument

intents = discord.Intents.default()

client = commands.Bot(command_prefix='!', intents=intents)

#------
TOKEN = "" #봇 토큰
#------

def GetA2SInfo(address:str,port:int):
    try:
        return(a2s.info((address,port),timeout=1.5))
    except:
        return 0

def GetA2SPlayers(address:str,port:int):
    try:
        return(a2s.players((address,port),timeout=1.5))
    except:
        return 0

def GetA2SRules(address:str,port:int):
    try:
        return(a2s.rules((address,port),timeout=1.5))
    except:
        return 0

@client.event
async def on_ready():
    print(f"{client.user} is ready!")

@client.command()
async def server_scan(ctx,address:str=None,port:int=None):
    if (address == None or port == None):
        await ctx.send("오류: 인자 누락") #discord.ext.commands.errors.MissingRequiredArgument 예외 처리 실패
        return
    await ctx.send(GetA2SInfo(address,port))
    await ctx.send(GetA2SPlayers(address,port))
    await ctx.send(GetA2SRules(address,port))

client.run(TOKEN)