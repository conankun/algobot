import argparse
import asyncio
import os
import logging
import textwrap
import discord
from discord import Intents, Embed
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext, manage_commands
from discord_slash.utils.manage_commands import create_option
from parser.daily_problem_parser import DailyProblemParser
from parser.problem_parser import ProblemParser

parser = argparse.ArgumentParser(description="Fetch some configuration arguments.")
parser.add_argument('--token', dest='token', type=str, help='A string for the token of discord bot.', required=True)

args = parser.parse_args()

client = discord.Client()

token = args.token

bot = commands.Bot(command_prefix='/', intents=Intents.default())
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    """
    The method triggered when the bot initializes.
    """
    print(f'Logged in as the following user: {bot.user.name} ({bot.user.id})')

@slash.slash(
    name='problem', 
    description="Fetch the problem info", 
    options=[
        create_option(
            name='problem_name', 
            description='test', 
            option_type=3, 
            required=True,
       ) 
    ]
)
async def _problem(ctx: SlashContext, problem_name: str):
    problem_id = problem_name.lower().replace(' ', '-')
    metadata = ProblemParser.query(problem_id)
    if metadata is None:
        await ctx.reply('문제를 찾을 수 없습니다.')
    else:
        image = 'https://leetcode.com/static/images/LeetCode_Sharing.png'
        embed = Embed(
            title=f'{metadata["questionId"]}. {metadata["title"]}',
            description=textwrap.shorten(metadata['content'], width=100),
            url=metadata['url'],
            color=discord.Color.green())
        embed.set_thumbnail(url=image)
        embed.add_field(
            name='난이도', 
            value=metadata['difficulty'], 
            inline=True
        )
        embed.add_field(
            name='좋아요',
            value=metadata['likes'],
            inline=True
        )
        embed.add_field(
            name='싫어요',
            value=metadata['dislikes'],
            inline=True
        )
        embed.add_field(
            name='유료',
            value='O' if metadata['isPaidOnly'] else 'X',
            inline=True
        )
        embed.set_image(url=image)
        await ctx.reply(embed=embed)


@slash.slash(
    name='today', 
    description="Fetch the problem info of today's challenge", 
)
async def _today(ctx: SlashContext):
    metadata = DailyProblemParser.query()
    if metadata is None:
        await ctx.reply('문제를 찾을 수 없습니다.')
    else:
        image = 'https://leetcode.com/static/images/LeetCode_Sharing.png'
        embed = Embed(
            title=f'오늘의 문제: {metadata["questionId"]}. {metadata["title"]}',
            description=textwrap.shorten(metadata['content'], width=100),
            url=metadata['url'],
            color=discord.Color.blue())
        embed.set_thumbnail(url=image)
        embed.add_field(
            name='난이도', 
            value=metadata['difficulty'], 
            inline=True
        )
        embed.add_field(
            name='좋아요',
            value=metadata['likes'],
            inline=True
        )
        embed.add_field(
            name='싫어요',
            value=metadata['dislikes'],
            inline=True
        )
        embed.add_field(
            name='유료',
            value='O' if metadata['isPaidOnly'] else 'X',
            inline=True
        )
        embed.set_image(url=image)
        await ctx.reply(embed=embed)
@bot.event
async def on_command_error(ctx, error):
    logging.error(error)
    if isinstance(error, commands.CommandNotFound):
        await ctx.channel.send('명령어가 존재하지 않습니다.')
    else:
        await ctx.channel.send('명령어를 잘못 사용하셨습니다.')

@client.event
async def on_message(message):
    """
    The method triggered when the bot receives some message.
    """
    if message.author.bot:
        return None
    print('hi')

bot.run(token)
