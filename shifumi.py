import discord
import random


async def play(ctx, shifumi_player):
    shifumi_list = ['pierre', 'ciseaux', 'feuille']

    if not shifumi_player in shifumi_list:
        embed = discord.Embed(title="", description="I don't recognize what did you play", color=discord.Color.red())
        return await ctx.send(embed=embed)

    shifumi_player_key = shifumi_list.index(shifumi_player)

    shifumi_bot_key = random.randint(0, 2)
    shifumi_bot = shifumi_list[shifumi_bot_key]

    result = shifumi_player_key - shifumi_bot_key

    if result == 0:
        embed = discord.Embed(title="", description="I play '" + shifumi_bot + "'\nIt's a draw",
                              color=discord.Color.lighter_grey())
        return await ctx.send(embed=embed)

    if result in [-1, 2]:
        embed = discord.Embed(title="", description="I play '" + shifumi_bot + "'\nYou win!",
                              color=discord.Color.green())
        return await ctx.send(embed=embed)

    embed = discord.Embed(title="", description="I play '" + shifumi_bot + "'\nYou lose...", color=discord.Color.red())
    return await ctx.send(embed=embed)
