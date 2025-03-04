import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up bot
intents = discord.Intents.default()
intents.message_content = True  
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

reminders = {}  # Dictionary to track reminders

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

@bot.command()
async def remind(ctx, date_time: str, *, reminder_message: str):
    """
    Set a reminder using date-time format.
    Example: !remind "2025-03-05 14:30" Take a break!
    """
    try:
        # Convert user input into a datetime object
        reminder_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M")
        now = datetime.now()

        # Calculate time difference
        delay = (reminder_time - now).total_seconds()

        if delay <= 0:
            await ctx.send("⏰ That time is in the past! Please set a future reminder.")
            return

        await ctx.send(f"✅ Reminder set for {ctx.author.mention} at {date_time}: {reminder_message}")

        # Wait for the reminder time
        await asyncio.sleep(delay)
        await ctx.send(f"⏰ {ctx.author.mention}, Reminder: {reminder_message}")

    except ValueError:
        await ctx.send("❌ Invalid format! Use: `YYYY-MM-DD HH:MM` (24-hour format)")

# -------------------- Cancel Reminder -------------------- #

@bot.command()
async def cancel_reminder(ctx):
    """Cancel all reminders (if implemented in the future)"""
    await ctx.send(f"{ctx.author.mention}, this feature is not yet implemented!")

# -------------------- Voice Channel Join/Leave -------------------- #

@bot.command()
async def join(ctx):
    if ctx.author.voice: 
        channel = ctx.author.voice.channel
        if not ctx.guild.voice_client: 
            await channel.connect()
            await ctx.send(f"🎤 Joined {channel.name}")
        else:
            await ctx.send("I'm already connected to a voice channel!")
    else:
        await ctx.send("You're not in a Voice Channel!")

@bot.command()
async def leave(ctx):
    if ctx.guild.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("🔇 Left the voice chat")
    else:
        await ctx.send("I'm not in a voice channel!")

# -------------------- On Message Event -------------------- #

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    if message.content.startswith("!"): 
        await bot.process_commands(message)
        return

    print(f"[{message.channel}] {message.author}: {message.content}") 
    
    await bot.process_commands(message)

# -------------------- Run the Bot -------------------- #

bot.run(TOKEN)
