import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
from responce import get_response
import yt_dlp

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up bot
intents = discord.Intents.default()
intents.message_content = True  
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

reminders = {}  # Dictionary to track reminders

yt_dl_options = {"format": "bestaudio/best"}
ytdl = yt_dlp.YoutubeDL(yt_dl_options)
ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -filter:a "volume=0.25"'
}

voice_clients = {}

# -------------------- Bot Events -------------------- #

@bot.event
async def on_ready():
    print(f"{bot.user} is now running!")

@bot.event
async def on_member_join(member: discord.Member):
    channel = bot.get_channel(1346171356848590919) 
    if channel:
        await channel.send(f"Welcome {member.mention} to the server!")  

@bot.event
async def on_member_remove(member: discord.Member):
    channel = bot.get_channel(1346171484221210685)  
    if channel:
        await channel.send(f"{member.mention} has left the server.")
# -------------------- Poll Command -------------------- #

@bot.command()
async def poll(ctx, question: str, *options):
    """Create a poll with up to 10 options"""
    if not options:
        options = ["Yes", "No"]

    if len(options) > 10:
        await ctx.send("You can only have up to 10 options!")
        return

    poll_message = f"**{question}**\n"
    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    
    for i, option in enumerate(options):
        poll_message += f"{emojis[i]} {option}\n"

    poll = await ctx.send(poll_message)

    for i in range(len(options)):
        await poll.add_reaction(emojis[i])

# -------------------- Reminder Command -------------------- #
async def send_reminder(ctx, delay, reminder_message):
    await asyncio.sleep(delay)
    await ctx.send(f"{ctx.author.mention}, Reminder: {reminder_message}")

@bot.command()
async def remind(ctx, date_time: str, *, reminder_message: str):
    try:
        # Convert user input into a datetime object
        reminder_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M")
        now = datetime.now()

        # Calculate time difference
        delay = (reminder_time - now).total_seconds()

        if delay <= 0:
            await ctx.send("That time is in the past! Please set a future reminder.")
            return

        await ctx.send(f"Reminder set for {ctx.author.mention} at {date_time}: {reminder_message}")
        reminders[ctx.author.id] = asyncio.create_task(send_reminder(ctx, delay, reminder_message))
        # Wait for the reminder time
        await reminders[ctx.author.id]

    except ValueError:
        await ctx.send("Invalid format! Use: `YYYY-MM-DD HH:MM` (24-hour format)")

# -------------------- Cancel Reminder -------------------- #

@bot.command()
async def cancel_reminder(ctx):
    task = reminders.get(ctx.author.id)
    if task and not task.done():
        task.cancel()
        del reminders[ctx.author.id]
        await ctx.send(f"{ctx.author.mention}, your reminder has been canceled.")
    else:
        await ctx.send(f"{ctx.author.mention}, you don't have any active reminders.")

# -------------------- Voice Channel Join/Leave -------------------- #

@bot.command()
async def join(ctx):
    if ctx.author.voice: 
        channel = ctx.author.voice.channel
        if not ctx.guild.voice_client: 
            await channel.connect()
            await ctx.send(f"Joined {channel.name}")
        else:
            await ctx.send("I'm already connected to a voice channel!")
    else:
        await ctx.send("You're not in a Voice Channel!")

@bot.command()
async def leave(ctx):
    if ctx.guild.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Left the voice chat")
    else:
        await ctx.send("I'm not in a voice channel!")


# -------------------- Music Commands For Youtube -------------------- #

@bot.command()
async def play(ctx, url: str):
    #leave space between the url and !play
    try:
        # Join voice channel if not already connected
        if ctx.guild.id not in voice_clients or not ctx.voice_client:
            voice_client = await ctx.author.voice.channel.connect()
            voice_clients[ctx.guild.id] = voice_client
        else:
            voice_client = voice_clients[ctx.guild.id]

        # Download audio from YouTube
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        song = data['url']

        # Play the song
        player = discord.FFmpegOpusAudio(song, **ffmpeg_options)
        voice_client.play(player)
        
        await ctx.send(f"Now playing: {data['title']}")

    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command()
async def pause(ctx):
    try:
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Paused.")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command()
async def resume(ctx):
    try:
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Resumed.")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command()
async def stop(ctx):
    try:
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            del voice_clients[ctx.guild.id]
            await ctx.send("Stopped and left the voice channel.")
    except Exception as e:
        await ctx.send(f"Error: {e}")

#------------------------CLEAR-----------------------------#
@bot.command()
async def clear(ctx, limit: int = 5):
    await ctx.channel.purge(limit=limit)

@bot.command()
async def clear_all(ctx, limit: int = 100):
    for channel in ctx.guild.channels:
        if isinstance(channel, discord.TextChannel):
            try:
                await channel.purge(limit=limit)
            except Exception as e:  
                print(f"Error: {e}")

# -------------------- On Message Event -------------------- #

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    if message.content.startswith("!"):
        await bot.process_commands(message)
        return
    
    if(message.content==""):
        return
    
    if(message.content.startswith("?")):
        response = get_response(message.content)
        if response:
            await message.author.send(response)
            await message.channel.purge(limit=1)

    
    if message.content.startswith("~"):
        response = get_response(message.content)
        if response:
            await message.channel.send(response)

# -------------------- Run the Bot -------------------- #

bot.run(TOKEN)
