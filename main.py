import os
from discord import activity
# import time
from discord.ext import commands
import discord
from discord_slash import SlashCommand
import discord_slash
from keep_alive import keep_alive
import cmds


client = commands.Bot(
    command_prefix='x.',
    case_insesetive=True,
    intents=discord.Intents(
        guilds=True,
        members=True,
        bans=False,
        emojis=False,
        integrations=False,
        webhooks=False,
        invites=False,
        voice_states=False,
        presences=False,
        messages=True,
        # guild_messages = True,
        # dm_messages = True,
        reactions=False,
        # guild_reactions = True,
        # dm_reactions = True,
        typing=True,
        # guild_typing = False,
        # dm_typing = False,
    ),
)

slash = SlashCommand(
    client,
    sync_commands=True,
    # sync_on_cog_reload=True
)

client.owner_id = 557933021844733963
guild_ids = [703540054169092217, 713107362763767929, 715847387230371901, 724361580698927418, 752177122998747199, 786648964874895381]


@client.event
async def on_ready():
    print("Ready!")
    await client.change_presence(
        activity=discord.Activity(
            name='x. or / commands',
            type=discord.ActivityType.listening),
        status=discord.Status.idle, afk=True)


cmds.registerCommands(client, slash, guild_ids)


keep_alive()
token = os.environ.get("TOKEN") 
client.run(token)
