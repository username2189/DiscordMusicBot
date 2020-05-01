import discord
import shutil
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os

BOT_PREFIX = '.'

bot = commands.Bot(command_prefix=BOT_PREFIX)


@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name + "\n")
    game = discord.Game("поиск дома")
    await bot.change_presence(activity=game)


@bot.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    """Подключиться к текущему голосовому каналу"""
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        return await voice.move_to(channel)

    await channel.connect()
    await ctx.send(f"Бот подключился к {channel}")
    print(f"Бот подключился к {channel}\n")


@bot.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    """Отключиться от текущего голосового канала"""
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"Бот оключился от {channel}")
        await ctx.send(f"Бот оключился от {channel}")
    else:
        print("Бот не находится в голосовом канале")
        await ctx.send("Бот не находится в голосовом канале")
        
        
@bot.command(pass_context=True, aliases=['pa', 'pau'])
async def pause(ctx):
    """Приостановить воспроизведение"""
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Пауза")
        voice.pause()
        await ctx.send("пауза")
    else:
        print("нечего ставить на паузу")
        await ctx.send("Нечего ставить на паузу")


@bot.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):
    """Продолжить воспроизведение"""
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("продолжение")
        voice.resume()
        await ctx.send("Продолжаю воспроизведение")
    else:
        print("ERROR")
        await ctx.send("ERROR")
        
        
@bot.command(pass_context=True, aliases=['v', 'vol'])
async def volume(ctx, volume: int):
    """Изменение громкости (.volume 50)"""
    if ctx.voice_client is None:
        return await ctx.send("Бот не находится в голосовом канале")

    print(volume/100)
    ctx.voice_client.source.volume = volume / 100
    await ctx.send(f"Громкость: {volume}%")


@bot.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):
    """Включить песню (.play youtubeURL)"""
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        print("ERROR: Что-то играет")
        await ctx.send("ERROR: Что-то играет")
        return

    await ctx.send("Начинаю загрузку...")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

        
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("выполнено"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Сейчас проигрывается: {nname[0]}")


b_token = os.environ.get('TOKEN')
bot.run(str(b_token))
