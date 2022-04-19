import time
import random
import typing
from util import Option
from aiohttp import request
import discord
from discord.ext import commands
from discord_slash import manage_commands


def registerCommands(client, slash, guild_ids):
    def create_command(
            *,
            name: str = None,
            description: str = None,
            # guild_ids: list[int] = None,
            options: typing.List[dict] = None,
            default_permission: bool = True,
            permissions: dict = None,
            # usage: str = None,
            connector: dict = None,
            type_: str = 'both'):

        def wrapper(func):
            if type_ in ('both', 'slash'):
                slash.slash(
                    name=name,
                    guild_ids=guild_ids, 
                    description=description, 
                    options=options, 
                    default_permission=default_permission, 
                    permissions=permissions,
                    connector=connector)(func)
            
            if type_ in ('both', 'normal'):
                client.command(name=name, description=description)(func)
        
        return wrapper


    @create_command(name="ping", description="This is just a test command, nothing more.")
    async def ping(ctx: commands.Context):
        before = time.monotonic()
        msg = await ctx.send("Pong!")
        # await ctx.respond()
        ping = (time.monotonic() - before) * 1000
        
        await msg.edit(content=f"Pong! Bot Latency`{int(ping)}ms`\n"
                    f"API Latency `{int(ctx.bot.latency * 1000)}ms`")

    # @cog_ext.cog_slash(
    #     name='8ball',
    #     description='Uses AI to give you the best answers to your questions',
    #     options=[manage_commands.create_option(
    #         name='question',
    #         description='The question you want to ask.',
    #         option_type=3,
    #         required=True
    #     )],
    #     guild_ids=conf.guild_ids
    # )
    # @cooldown(2, 3, BucketType.channel)

    @create_command(name='8ball',
        description='Gives a random response to your "question"',
        options=[manage_commands.create_option(
            name='question',
            description='The question you want to ask.',
            option_type=Option.STRING,
            required=True
            )])
    async def eight_ball(ctx, *, question=None):
        colour_choices = [0x400000, 0x997379, 0xeb96aa, 0x4870a0, 0x49a7c3, 0x8b3a3a, 0x1e747c, 0x0000ff]
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Yes - definitely.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "You may rely on it.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Without a doubt.",
            "Cannot predict now.",
            "Don't count on it.",
            "My reply is no.",
            "Concentrate and ask again.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
            "Probably not",
            "There is a chance..."
            ]

        if question is not None:
            embed = discord.Embed(
                title='*The 8ball*',
                description=f'**{ctx.author}** asked a question.\n\n'
                            f'The question was: **{question}**\n\n\n'
                            f'{random.choice(responses)}',
                color=random.choice(colour_choices)
            )
            # await ctx.respond()
            await ctx.send(embed=embed)
        else:
            # await ctx.respond()
            await ctx.send('Ask me a question!')

    # 8ball: Error handling
    # @eight_ball.error
    # async def eight_ball_error(ctx, error):
    #     if isinstance(error, commands.CommandOnCooldown):
    #         await ctx.send(error)
    #     else:
    #         await ctx.send(f'An error occurred \n'
    #                        f'```\n{error}\n```\n'
    #                        f'Please check console for traceback.')
    #         raise error

    # Random quotes
    # @cog_ext.cog_slash(
    #     name='quotes',
    #     description='Sends a random quote',
    #     guild_ids=conf.guild_ids
    # )
    # @cooldown(1, 3, BucketType.channel)
    
    @create_command(name="quotes", description="Sends a random quote.")
    async def quotes(ctx):
        quotes_url = 'http://staging.quotable.io/random'

        async with request("GET", quotes_url, headers={}) as resp:
            if resp.status == 200:
                data = await resp.json()

                quote = data["content"]
                author = data["author"]

                # await ctx.respond()
                await ctx.send(f'```\n{quote}\n```\n**-{author}**')
            else:
                # await ctx.respond()
                await ctx.send(f"API seems down, says {resp.status} code")

    # Quotes: Error handling
    # @quotes.error
    # async def quotes_error(ctx, error):
    #     if isinstance(error, commands.CommandOnCooldown):
    #         await ctx.send(error)
    #     else:
    #         await ctx.send(f'An error occurred \n'
    #                        f'```\n{error}\n```\n'
    #                        f'Please check console for traceback.')
    #         raise error

    # @cog_ext.cog_slash(
    #     name='inspire',
    #     description='Sends inspirational image (generated by inspirobot, not me)',
    #     guild_ids=conf.guild_ids
    # )
    # @cooldown(1, 3, BucketType.channel)
    
    @create_command(name='inspire', description='Sends an "inspirational" image (generated by inspirobot)')
    async def inspire(ctx):
        inspire_url = 'https://inspirobot.me/api?generate=true'

        async with request("GET", inspire_url, headers={}) as resp:
            if resp.status == 200:
                data = await resp.text()

                e = discord.Embed(
                    title='inspire'
                )
                e.set_image(url=str(data))
                e.set_footer(text='generated by https://inspirobot.me')

                #await ctx.respond()
                await ctx.send(embed=e)
            else:
                # await ctx.respond()
                await ctx.send(f"API seems down, says {resp.status} code")

    # Random jokes
    # @cog_ext.cog_slash(
    #     name='joke',
    #     description='Sends a random joke',
    #     guild_ids=conf.guild_ids
    # )
    # @cooldown(1, 3, BucketType.channel)
    @create_command(name="joke", description="Sends a random joke (possibly unfunny).")
    async def jokes(ctx):
        colour_choices = [0x400000, 0x997379, 0xeb96aa, 0x4870a0, 0x49a7c3, 0x8b3a3a, 0x1e747c, 0x0000ff]
        jokes_url = 'https://official-joke-api.appspot.com/random_joke'

        async with request("GET", jokes_url, headers={}) as resp:
            if resp.status == 200:
                data = await resp.json()
                title = data["setup"]
                description = data["punchline"]

                embed = discord.Embed(
                    title=title,
                    description=description,
                    colour=random.choice(colour_choices)
                )
                # await ctx.respond()
                await ctx.send(embed=embed)
            else:
                # await ctx.respond()
                await ctx.send(f'The API seems down, say {resp.status}')

    # Jokes: Error handling
    # @jokes.error
    # async def jokes_error(ctx, error):
    #     if isinstance(error, commands.CommandOnCooldown):
    #         await ctx.send(error)
    #     else:
    #         await ctx.send(f'An error occurred \n'
    #                        f'```\n{error}\n```\n'
    #                        f'Please check console for traceback.')
    #         raise error

    # Random memes from the internet
    # @cog_ext.cog_slash(
    #     name='meme',
    #     description='Sends you a beautifully crafted meme',
    #     guild_ids=conf.guild_ids
    # )
    # @cooldown(1, 3, BucketType.channel)
    @create_command(name="meme", description="Sends a random meme (sfw).")
    async def meme(ctx):
        colour_choices = [0x400000, 0x997379, 0xeb96aa, 0x4870a0, 0x49a7c3, 0x8b3a3a, 0x1e747c, 0x0000ff]
        meme_url = "https://meme-api.herokuapp.com/gimme?nsfw=false"

        async with request("GET", meme_url, headers={}) as resp:
            if resp.status == 200:
                data = await resp.json()
                image_link = data["url"]
            else:
                image_link = None

        async with request("GET", meme_url, headers={}) as resp:
            if resp.status == 200:
                data = await resp.json()
                embed = discord.Embed(
                    title=data["title"],
                    url=image_link,
                    colour=random.choice(colour_choices)
                )
                if image_link is not None:
                    embed.set_image(url=image_link)
                    # await ctx.respond()
                    await ctx.send(embed=embed)

            else:
                # await ctx.respond()
                await ctx.send(f"The API seems down, says {resp.status}")

    # Memes: Error handling
    # @meme.error
    # async def meme_error(ctx, error):
    #     if isinstance(error, commands.CommandOnCooldown):
    #         await ctx.send(error)
    #     else:
    #         await ctx.send(f'An error occurred \n'
    #                        f'```\n{error}\n```\n'
    #                        f'Please check the console for traceback.')
    #         raise error

    # Programming jokes
    # @cog_ext.cog_slash(
    #     name='pjoke',
    #     description='Sends a programming related joke',
    #     guild_ids=conf.guild_ids
    # )
    # @cooldown(1, 3, BucketType.channel)
    @create_command(name="pjoke", description="Sends a programming related joke.")
    async def programming_jokes(ctx):
        colour_choices = [0x400000, 0x997379, 0xeb96aa, 0x4870a0, 0x49a7c3, 0x8b3a3a, 0x1e747c, 0x0000ff]
        jokes_url = 'https://official-joke-api.appspot.com/jokes/programming/random'

        async with request("GET", jokes_url, headers={}) as resp:
            if resp.status == 200:
                data = await resp.json()
                title = data[0]["setup"]
                description = data[0]["punchline"]

                embed = discord.Embed(
                    title=title,
                    description=description,
                    colour=random.choice(colour_choices)
                )
                # await ctx.respond()
                await ctx.send(embed=embed)
            else:
                # await ctx.respond()
                await ctx.send(f'The API seems down, say {resp.status}')


    @create_command(
        name='avatar',
        description='Shows the avatar of a specific user',
        options=[manage_commands.create_option(
            name='user',
            description="Which user's avatar you want",
            option_type=6,
            required=True
        )],
    )
    # @cooldown(1, 5, BucketType.channel)
    async def avatar(ctx, user: discord.User, override=None):
        # await ctx.respond()
        await ctx.send(content=f'{user.avatar_url}')

    # Avatar fetcher: Error handling
    # @avatar.error
    # async def avatar_error(self, ctx, error):
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         embed = discord.Embed(colour=0x0000ff)
    #         embed.set_image(url=f'{ctx.author.avatar_url}')
    #         await ctx.send(embed=embed)
    #     elif isinstance(error, commands.CommandOnCooldown):
    #         await ctx.send(error)
    #     else:
    #         await ctx.send(f'An error occurred \n'
    #                        f'```\n{error}\n```\n'
    #                        f'Please check console for traceback.')
    #         raise error

    # Userinfo
    @create_command(
        name='userinfo',
        description='Gives the info of a specific user',
        options=[manage_commands.create_option(
            name='user',
            description="Which user's info you want",
            option_type=6,
            required=True
        )],
    )
    # @cooldown(1, 5, BucketType.channel)
    async def userinfo(ctx, member):

        members = await ctx.guild.fetch_members().flatten()
        multiple_member_array = []

        if isinstance(member, discord.Member):
            for members_list in members:
                if member.name.lower() in members_list.name.lower():
                    multiple_member_array.append(members_list)
                else:
                    pass

        
        # await ctx.respond()
        
        if len(multiple_member_array) == 1:
            roles = []
            for role in multiple_member_array[0].roles:
                roles.append(role)

            embed = discord.Embed(
                colour=0x0000ff,
            )
            embed.set_author(name=f'User Info - {multiple_member_array[0]}')
            embed.set_thumbnail(url=multiple_member_array[0].avatar_url)

            embed.add_field(name='ID:', value=multiple_member_array[0].id)
            embed.add_field(name='Member Name:', value=multiple_member_array[0])
            embed.add_field(name='Member Nickname:', value=multiple_member_array[0].display_name)

            embed.add_field(name='Created at: ',
                            value=multiple_member_array[0].created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
            embed.add_field(name='Joined at:',
                            value=multiple_member_array[0].joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))

            if len(roles) == 1:
                embed.add_field(name=f'Roles ({len(roles) - 1})', value='**NIL**')
            else:
                embed.add_field(name=f'Roles ({len(roles) - 1})',
                                value=' '.join([role.mention for role in roles if role.name != '@everyone']))

            embed.add_field(name='Bot?', value=multiple_member_array[0].bot)

            await ctx.send(embed=embed)


        elif len(multiple_member_array) > 1:
            multiple_member_array_duplicate_array = []

            for multiple_member_array_duplicate in multiple_member_array:
                if len(multiple_member_array_duplicate_array) < 10:
                    multiple_member_array_duplicate_array.append(multiple_member_array_duplicate.name)
                else:
                    break

            embed = discord.Embed(
                title=f'Search for {member}\nFound multiple results (Max 10)',
                description='\n'.join(multiple_member_array_duplicate_array),
                colour=0x808080
            )
            await ctx.send(embed=embed)

        else:
            await ctx.send(f'The member `{member}` does not exist!')

    # Userinfo: Error handling
    # @userinfo.error
    # async def userinfo_error(self, ctx, error):
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         await ctx.send('```\n$userinfo {member_name}\n'
    #                        '          ^^^^^^^^^^^^^\nMissing Required Argument member_name\n```')
    #     elif isinstance(error, commands.CommandOnCooldown):
    #         await ctx.send(error)
    #     elif isinstance(error, discord.errors.Forbidden):
    #         await ctx.send('I am Forbidden from doing this command, please check if `server members intent` is enabled')
    #     else:
    #         await ctx.send(f'An error occurred \n'
    #                        f'```\n{error}\n```\n'
    #                        f'Please check the console for traceback.')
    #         raise error

    # Server info
    @create_command(
        name='serverinfo',
        description='Gives the info of the server',
    )
    # @cooldown(1, 5, BucketType.channel)
    async def serverinfo(ctx):
        bot_count = 0

        members = await ctx.guild.fetch_members().flatten()

        for people in members:
            if people.bot:
                bot_count += 1
            
        pass

        embed = discord.Embed(
            title=f'{ctx.guild.name} info',
            colour=0x0000ff
        )
        embed.set_thumbnail(url=ctx.guild.icon_url)

        embed.add_field(name='Owner name:', value=f'<@{ctx.guild.owner_id}>')
        embed.add_field(name='Server ID:', value=str(ctx.guild.id))

        embed.add_field(name='Server region:', value=ctx.guild.region)
        embed.add_field(name='Members:', value=str(ctx.guild.member_count))
        embed.add_field(name='bots:', value=str(bot_count))
        embed.add_field(name='Humans:', value=str(ctx.guild.member_count - bot_count))

        embed.add_field(name='Number of roles:', value=str(len(ctx.guild.roles)))
        embed.add_field(name='Number of boosts:', value=str(ctx.guild.premium_subscription_count))

        embed.add_field(name='Text Channels:', value=str(len(ctx.guild.text_channels)))
        embed.add_field(name='Voice Channels:', value=str(len(ctx.guild.voice_channels)))
        embed.add_field(name='Categories:', value=str(len(ctx.guild.categories)))

        embed.add_field(name='Created On:', value=ctx.guild.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))

        # await ctx.respond()
        await ctx.send(embed=embed)

    # Server info: Error handling
    # @serverinfo.error
    # async def serverinfo_error(self, ctx, error):
    #     if isinstance(error, commands.CommandOnCooldown):
    #         await ctx.send(error)
    #         raise error
    #     else:
    #         await ctx.send(f'An error occurred \n'
    #                        f'```\n{error}\n```\n'
    #                        f'Please check console for traceback.')
    #         raise error

    # Server count
    @create_command(
        name='servercount',
        description='Shows you how many servers the bot is in '
                    'and total number of members in those servers combined',
    )
    # @cooldown(1, 1, BucketType.channel)
    async def servercount(ctx):
        member_count = 0
        for guild in ctx.bot.guilds:
            member_count += guild.member_count

        # await ctx.respond()
        await ctx.send(
            f'Present in `{len(ctx.bot.guilds)}` servers, '
            f'moderating `{member_count}` members')

    # Server count: cooldown
    # @servercount.error
    # async def sc_error(self, ctx, error):
    #     if isinstance(error, commands.CommandOnCooldown):
    #         await ctx.send(error)
    #     else:
    #         await ctx.send(f'An error occurred \n'
    #                        f'```\n{error}\n```\n'
    #                        f'Please check console for traceback.')
    #         raise error

    # Prefix changer
    # @commands.command(name='prefix')
    # @cooldown(1, 5, BucketType.guild)
    # @commands.has_permissions(administrator=True)
    # async def prefix(self, ctx, prefix: str):
    #     if len(prefix) <= 4:
    #         if not any([c.isdigit() for c in prefix]):
    #             self.conf.set_prefix(ctx.guild.id, prefix)

    #             await ctx.send(f"Prefix of this server has been changed to **{prefix}** successfully!")
    #         else:
    #             await ctx.send("Integers are not allowed in prefixes")
    #     else:
    #         await ctx.send(f"A prefix must have only 4 or lesser characters, **{len(prefix)}** is not allowed")

    # # Prefix changer: Error handling
    # @prefix.error
    # async def prefix_error(self, ctx, error):
    #     if isinstance(error, commands.CommandOnCooldown):
    #         await ctx.send(error)
    #     elif isinstance(error, commands.CheckFailure):
    #         await ctx.send(f"Only administrators can use this command, {ctx.author.mention}")
    #     elif isinstance(error, commands.MissingRequiredArgument):
    #         prefix = self.conf.fetch_prefix(ctx.guild.id)

    #         await ctx.send(f"```\n{prefix}prefix <prefix>\n\n"
    #                        f"Missing required argument prefix\n```")
    #     else:
    #         await ctx.send(f'An error occurred \n'
    #                        f'```\n{error}\n```\n'
    #                        f'Please check console for traceback.')
    #         raise error


    @create_command(
        name="createembed",
        description="Creates an embed.",
        options=[
        manage_commands.create_option(
            name = "title",
            description = "the embed title",
            option_type = 3,
            required = True
        ),
        manage_commands.create_option(
            name='description',
            description='the embed description',
            option_type=3,
            required=True
        ),
        manage_commands.create_option(
            name='image',
            description='the embed image/thumbnail link',
            option_type=3,
            required=True
        ),
        manage_commands.create_option(
            name='color',
            description='the embed color in comma separated rgb format',
            option_type=3,
            required=True
        )],
    )
    async def createembed(ctx, *content):
        '''
        title |  | description | thumbnail | color
        '''
        print(content)
        lis = content
        colors = [int(x) for x in lis[3].split(",")]
        embed = discord.Embed(
            color=discord.Color.from_rgb(
                colors[0],
                colors[1],
                colors[2]),
            title=lis[0],
            description=lis[1]
        )
        embed.set_author(name=str(ctx.author)[:-5], icon_url=ctx.author.avatar_url)
        # embed.add_field(name=lis[1], value=lis[2])
        embed.set_image(url=lis[2])
        await ctx.send(embed=embed)

    @create_command(name='servertest', description='servertest', type_='normal')
    async def servertest(ctx):
        if ctx.author.id == 557933021844733963:
            print([guild.id for guild in ctx.bot.guilds])
