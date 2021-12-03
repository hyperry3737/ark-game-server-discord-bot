import a2s
import discord
import asyncio
from discord import player
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument
from time import strftime,gmtime

intents = discord.Intents.default()

client = commands.Bot(command_prefix='!', intents=intents)

#------
TOKEN = "" #봇 토큰
#------

async def GetA2SInfo(address:str,port:int):
    try:
        return(await a2s.ainfo((address,port),timeout=1.5))
    except:
        return 0

async def GetA2SPlayers(address:str,port:int):
    try:
        return(await a2s.aplayers((address,port),timeout=1.5))
    except:
        return 0

async def GetA2SRules(address:str,port:int):
    try:
        return(await a2s.arules((address,port),timeout=1.5))
    except:
        return 0

def AddPlayerToList(playerInfo): #공백 제외 처리 안 함
    if (playerInfo.name == ""):
        return "NeedStrip" #NeedStrip 기준으로 공백 닉네임 제거
    else:
        duration:str = str(strftime("%H:%M:%S", gmtime(round(int(playerInfo.duration)))))
        return f"+ {duration} | {playerInfo.name}"

@client.event
async def on_ready():
    print(f"{client.user} is ready!")

@client.command()
async def server_scan(ctx,address:str=None,port:int=None):
    if (address == None or port == None):
        await ctx.send("오류: 인자 누락") #discord.ext.commands.errors.MissingRequiredArgument 예외 처리 실패
        return

    rules,info,players = await asyncio.gather(
        GetA2SRules(address,port),
        GetA2SInfo(address,port),
        GetA2SPlayers(address,port)
    )
    
    if (rules == 0 or info == 0 or players == 0):
        await ctx.send("오류: 서버 스캔 실패")
        return

    header:str = f'```ahk\n"Server Name" : "{info.server_name}"\n"Map Name" : "{info.map_name}"\n"Player Count" : "{info.player_count}/{info.max_players}"```'
    playerList:list = list(map(AddPlayerToList,players))
    body:str = "```diff\n{0}```".format('\n'.join(playerList)).replace("NeedStrip\n","")

    await ctx.send(header)
    await ctx.send(body)

client.run(TOKEN)