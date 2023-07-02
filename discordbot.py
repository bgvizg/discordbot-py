import nextcord
import asyncio
from datetime import datetime, timedelta
import a2s
from nextcord.ext import tasks
import time
from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
import os
load_dotenv()

# 디스코드 클라이언트 객체 생성
client = nextcord.Client()

# 특정 채널 ID
channel_id = 1124982022302093502

# 채널 객체 가져오기
channel = None
message = None

# 디스코드 봇이 준비되었을 때 실행되는 이벤트 핸들러
@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    
    # 채널 객체 설정
    global channel
    channel = client.get_channel(channel_id)
    
    # 메시지 전송
    global message
    message = await channel.send(result())
    
    # 주기적으로 메시지 수정하는 작업 시작
    update_time.start()

# 현재 시간을 문자열로 반환하는 함수
address = "121.147.111.167"
ports = [27029,27030,27031,27032,27033,27034,27035,27036,27037,27038,27039,27040]
Red = "\033[31m"
BrightRed = "\033[91m"
Green = "\033[32m"
Cyan = "\033[36m"
Purple = "\033[95m"
Yellow = "\033[33m"
Suffix = "\033[0m"

def result():
    result = "```ansi\n"
    sumPlayerCount = 0
    now = datetime.now()
    result +=Green + "서버 조회 시각 : " + str(now.strftime('%Y-%m-%d %H:%M:%S.%f')) + Suffix + "\n"
    result +="\n"
    result +="―――――――――――――― 서버 리스트 ――――――――――――――\n"
    result +="\n"
    start = time.time()
    for port in ports:
        try:
            #서버 조회
            players = a2s.players((address,port))
            mapColor = Cyan
            if (port == 27039):
                mapColor = Purple

            #플레이어 조회
            certainPlayer = []
            for player in players:
                playerColor = ""
                if (player.duration > 5400): #1시간 30분 이상 접속 유저 표시
                    playerColor = Yellow
                if (port == 27039): #에버 접속 유저 표시
                    playerColor = Red
                if len(str(player.name)) != 0:
                    sumPlayerCount += 1
                    certainPlayer.append(playerColor + "  - " + player.name + " | " + str(timedelta(seconds=player.duration)) + Suffix + "\n")

            cuertainPlayerMsg = "".join(certainPlayer)
            playerListMsg = f"\n + 플레이어 리스트 {BrightRed}[{len(certainPlayer)}명]{Suffix}\n{cuertainPlayerMsg}\n"

            #메시지 출력
            result +=f"{mapColor}" + a2s.info((address,port)).server_name + Suffix
            result +=playerListMsg
        except:
            result +=Red + "! 서버를 찾을 수 없음" + Suffix + " | " + address + ":" + str(port) + "\n"
    end = time.time()
    nextTime = now + timedelta(seconds=10 + end-start)
    result +=f"―――――――――――――― ∑ 플레이어 {BrightRed}[{sumPlayerCount}명]{Suffix} ――――――――――――――"
    result +="\n\n"
    result +="\033[32m다음 서버 조회 시각 : " + str(nextTime) + "\033[0m"
    result +="```"
    return result

# 10초마다 메시지를 수정하는 작업
@tasks.loop(seconds=10)
async def update_time():
    if message:
        await message.edit(content=result())

# 봇 실행
bot_token = "MTEyNTA0MjAzNDYyMTgxNjg5Mw.Gd6GJL.ipsNFd0e3pYvFdsRuFbxQ6eq6MqG3zMXnhr0ro"
client.run(bot_token)
