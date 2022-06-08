import discord
import random


async def play(ctx, shifumi_player):
    shifumi_list = ['pierre', 'ciseaux', 'feuille']

    if not shifumi_player in shifumi_list:
        embed = discord.Embed(title="", description="I don't recognize what did you play", color=discord.Color.red())
        return await ctx.send(embed=embed)

    shifumi_bot = shifumi_list[random.randint(0, 2)]

    if shifumi_bot == shifumi_player:
        embed = discord.Embed(title="", description="I play '" + shifumi_bot + "'\nIt's a draw",
                              color=discord.Color.lighter_grey())
        return await ctx.send(embed=embed)

    win = False
    if (shifumi_player == 'pierre' and shifumi_bot == 'ciseaux') or (
            shifumi_player == 'ciseaux' and shifumi_bot == 'feuille') or (
            shifumi_player == 'feuille' and shifumi_bot == 'pierre'):
        win = True

    if win:
        embed = discord.Embed(title="", description="I play '" + shifumi_bot + "'\nYou win!",
                              color=discord.Color.green())
        return await ctx.send(embed=embed)

    embed = discord.Embed(title="", description="I play '" + shifumi_bot + "'\nYou lose...", color=discord.Color.red())
    return await ctx.send(embed=embed)
