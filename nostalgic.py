import discord
import nostalgia
from discord.ext.commands import Bot as eu

talgic = eu(command_prefix="ALA MICU ")

@talgic.event
async def on_ready():
    print("Gattaaaa")

@talgic.command()
async def porneste(ctx):
    print(f"{ctx.author} a pornit serverul")
    await ctx.reply("Acum se va porni serverul sefule")
    nostalgia.start()
    await ctx.send(f"Sefu {ctx.author.mention} a pornit serverul")

@talgic.command()
async def porneste(ctx):
    print(f"{ctx.author} a oprit serverul")
    await ctx.reply("Acum se va opri serverul sefule")
    nostalgia.stop()
    await ctx.send(f"Sefu {ctx.author.mention} a oprit serverul")

@talgic.command()
async def informatii(ctx):
    print(f"{ctx.author} a cerut niste informatii despre server")
    await ctx.reply("Ai cerut niste informatii despre server sefule")
    informatii = nostalgia.get_servers_info()[2]
    await ctx.send(f"informatiile cerute: \n\tStatusul: {informatii['online']}\n\tjucatori: {informatii['players']}")


token = "AgR_CRISVf0pLEULp0k7Zfi53PDDkfH0ZqWl4K.dwOBsG.1MjNygDNzADO0UTO1QzN1UDO"[::-1]
talgic.run(token)