import discord
from discord.ext import commands
import datetime

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = 'BOT TOKEN HERE' #Bot Token
MASTER_CHANNEL_ID = 'LOGGING CHANNEL HERE' #Channel ID
LOG_CHANNEL_IDS = [CHANNEL 1, CHANNEL 2] # Channel ID
message_log = {}  

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id in LOG_CHANNEL_IDS:
        master_channel = bot.get_channel(MASTER_CHANNEL_ID)
        
        embed = discord.Embed(
            title=f"{message.author.name} {datetime.datetime.utcnow().strftime('%m/%d/%Y %I:%M %p')}",
            color=discord.Color.red()
        )
        embed.add_field(name="Message:", value=message.content, inline=True)
        embed.add_field(name="ID:", value=str(message.id), inline=True)
        embed.add_field(name="User:", value=message.author.mention, inline=True)
        embed.add_field(name="Channel:", value=f"<#{message.channel.id}> - `#{message.channel.name}`", inline=True)
        embed.add_field(name="Server:", value=f"{message.guild.id} - `{message.guild.name}`", inline=True)
        embed.add_field(name="Time:", value=f"<t:{int(message.created_at.timestamp())}:R>", inline=True)
        embed.set_footer(text=f"Message sent by {message.author}")
        embed.set_thumbnail(url=message.author.avatar.url)

        log_message = await master_channel.send(embed=embed)
        message_log[message.id] = log_message.id  

    await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    if message.channel.id in LOG_CHANNEL_IDS:
        master_channel = bot.get_channel(MASTER_CHANNEL_ID)
        log_message_id = message_log.get(message.id)
        
        if log_message_id:
            log_message = await master_channel.fetch_message(log_message_id)
            delete_embed = discord.Embed(
                title="Message Deleted",
                color=discord.Color.red(),
                description=f"**User:** {message.author.mention}\n**Message:** {message.content}\n**Deleted By:** {message.author.mention}"
            )
            await log_message.reply(embed=delete_embed)

@bot.event
async def on_message_edit(before, after):
    if after.channel.id in LOG_CHANNEL_IDS:
        master_channel = bot.get_channel(MASTER_CHANNEL_ID)
        log_message_id = message_log.get(after.id)

        if log_message_id:
            log_message = await master_channel.fetch_message(log_message_id)
            edit_embed = discord.Embed(
                title=f"Message Edited by {after.author.name} {datetime.datetime.utcnow().strftime('%m/%d/%Y %I:%M %p')}",
                color=discord.Color.blue()
            )
            edit_embed.add_field(name="Original Message:", value=before.content, inline=True)
            edit_embed.add_field(name="Edited Message:", value=after.content, inline=True)
            edit_embed.add_field(name="ID:", value=str(after.id), inline=True)
            edit_embed.add_field(name="User:", value=after.author.mention, inline=True)
            edit_embed.add_field(name="Channel:", value=f"<#{after.channel.id}> - `#{after.channel.name}`", inline=True)
            edit_embed.add_field(name="Server:", value=f"{after.guild.id} - `{after.guild.name}`", inline=True)
            edit_embed.add_field(name="Time:", value=f"<t:{int(after.created_at.timestamp())}:R>", inline=True)
            edit_embed.set_footer(text=f"Message edited by {after.author}")
            edit_embed.set_thumbnail(url=after.author.avatar.url)

            await master_channel.send(embed=edit_embed)

@bot.event
async def on_voice_state_update(member, before, after):
    master_channel = bot.get_channel(MASTER_CHANNEL_ID)
    
    if before.channel is None and after.channel is not None:

        embed = discord.Embed(
            title="Voice Channel Update",
            color=discord.Color.green(),
            description=f"**User:** {member.mention}\n**Action:** Joined voice channel\n**Channel:** {after.channel.name}"
        )
        embed.set_thumbnail(url=member.avatar.url)
        await master_channel.send(embed=embed)
    elif before.channel is not None and after.channel is None:

        embed = discord.Embed(
            title="Voice Channel Update",
            color=discord.Color.red(),
            description=f"**User:** {member.mention}\n**Action:** Left voice channel\n**Channel:** {before.channel.name}"
        )
        embed.set_thumbnail(url=member.avatar.url)
        await master_channel.send(embed=embed)
    elif before.channel is not None and after.channel is not None and before.channel != after.channel:

        embed = discord.Embed(
            title="Voice Channel Update",
            color=discord.Color.orange(),
            description=f"**User:** {member.mention}\n**Action:** Switched voice channel\n**From:** {before.channel.name}\n**To:** {after.channel.name}"
        )
        embed.set_thumbnail(url=member.avatar.url)
        await master_channel.send(embed=embed)

bot.run(TOKEN)
