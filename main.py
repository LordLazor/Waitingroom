import discord
import asyncio
import json

def read_json():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config

def write_json_channel(config, channel_name):
    config['channel_name'] = channel_name
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)
        
def write_json_sound(config, sound_file_name):
    config['sound_file'] = sound_file_name
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

config = read_json()

status = discord.Status.dnd
activity = discord.Activity(type=discord.ActivityType.watching, name="/help for all commands")

intent = discord.Intents.default()
intent.message_content = True

bot = discord.Bot(intents=intent, status=status, activity=activity)

@bot.event
async def on_ready():
    print(f'{bot.user.name} ready!')

@bot.slash_command(description="Bot leaves channel currently playing in")
async def leave(ctx):
    for vc in bot.voice_clients:
        await vc.disconnect()
        await ctx.respond(f"Left the voice channel", ephemeral=True)

@bot.slash_command(description="Bot joins the voice channel given in config.json")
async def join(ctx):
    guild = ctx.guild
    
    await leave(ctx)

    for channel in guild.channels:
        if isinstance(channel, discord.VoiceChannel) and channel.name == config['channel_name']:
            voice_channel = await channel.connect()
            await ctx.respond(f"Playing sound on loop in channel **{channel.name}**", ephemeral=True)
                
            await asyncio.sleep(1)  # wait for the connection to be established

            async def play_sound(voice_channel, sound):
                
                if not voice_channel.is_connected():  # check the connection
                    return
                
                voice_channel.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=config['sound_file']))
                while voice_channel.is_playing():
                    await asyncio.sleep(1)
                await play_sound(voice_channel, sound)

            await play_sound(voice_channel, config['sound_file'])

            while voice_channel.is_playing():
                await asyncio.sleep(1)

            await voice_channel.disconnect()
            
def get_channels(ctx: discord.AutocompleteContext):
    return ['General', 'Waitingroom', 'Supportroom']

@bot.slash_command(description="Set the channel name for the bot to join")
async def set_channel(ctx, channel_name: discord.Option(str, autocomplete=get_channels)):
    write_json_channel(config, channel_name)
    
    await ctx.respond(f"Channel name set to **{channel_name}**", ephemeral=True)
    
def get_sounds(ctx: discord.AutocompleteContext):
    return ['sound.mp3', 'somesound.mp3', 'someothersound.mp3']

@bot.slash_command(description="Set the sound file for the bot to play")
async def set_sound(ctx, sound_file: discord.Option(str, autocomplete=get_sounds)):
    write_json_sound(config, sound_file)
    await ctx.respond(f"Sound file set to **{sound_file}**", ephemeral=True)
    
@bot.slash_command(description="Get developers socials")
async def socials(ctx):
    embed = discord.Embed(
        title="Socials", 
        description="Socials of LordLazor", 
        color=discord.Color.blue())
    
    embed.add_field(name="GitHub", value="[Click me](https://www.github.com/LordLazor)", inline=False)
    embed.add_field(name="LinkedIn", value="[Click me](https://www.linkedin.com/lazar-konstantinou-99901a2b0)", inline=False)
    embed.add_field(name="Codedex", value="[Click me](https://www.codedex.io/@lordlazor)", inline=False)
    
    await ctx.respond(embed=embed, ephemeral=True)
    
@bot.slash_command(description="List of all features")
async def help(ctx):
    embed = discord.Embed(
        title="Help", 
        description="List of all features", 
        color=discord.Color.blue())
    
    embed.add_field(name="/socials", value="Get developers socials", inline=False)
    embed.add_field(name="/join", value="Bot joins the voice channel given in config.json", inline=False)
    embed.add_field(name="/leave", value="Leaves channel currently looping in", inline=False)
    embed.add_field(name="/set_channel", value="Set the channel name for the bot to join", inline=False)
    embed.add_field(name="/set_sound", value="Set the sound file for the bot to play on repeat", inline=False)
    
    embed.set_thumbnail(url=ctx.author.avatar.url)
    
    embed.set_footer(text="Final Project for Codedex by LordLazor")
    
    await ctx.respond(embed=embed, ephemeral=True)

bot.run(config['token'])