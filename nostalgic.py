import discord
import nostalgia
from discord.ext.commands import Bot as eu

prefixu = " UCIM ALA"[::-1]

talgic = eu(command_prefix=prefixu, self_bot=True)

# command_prefix="ALA MICU "

# class talgic(discord.Client):
#     async def on_ready(self):
#         print('Gata baaa', self.user)

#     async def on_message(self, message):
#         # only respond to ourselves
#         # if message.author != self.user:
#         #     return

#         if message.content == f'{command_prefix}porneste':
#             # await message.channel.send('pong')
#             print(f"{message.author} a pornit serverul")
#             await message.channel.send("Acum se va porni serverul sefule")
#             nostalgia.start()
#             await message.channel.send(f"Sefu {message.author.mention} a pornit serverul")
#         if message.content == f"{command_prefix}opreste":
#                 print(f"{message.author} a oprit serverul")
#                 await message.channel.send("Acum se va opri serverul sefule")
#                 nostalgia.start()
#                 await message.channel.send(f"Sefu {message.author.mention} a oprit serverul")
#         if message.content == f"{command_prefix}informatii":
#                 print(f"{message.author} a cerut niste informatii despre server")
#                 await message.channel.send("Ai cerut niste informatii despre server sefule")
#                 informatii = nostalgia.get_servers_info()[2]
#                 await message.channel.send(f"informatiile cerute: \n\tStatusul: {informatii['online']}\n\tjucatori: {informatii['players']}")
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
async def opreste(ctx):
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

@talgic.command()
async def verificare(ctx):
    print(f"{ctx.author} a cerut o verificare")
    nostalgia.renew()
    await ctx.reply(f"Ai cerut o verificare sefule, verifica cu {prefixu}verifica textul-ce-apare-in-imagine")
    await ctx.send(file=discord.File('captcha.png'))
    await ctx.send(f'{ctx.author.mention} a cerut o verificare')

@talgic.command()
async def verifica(ctx, text):
    print(f"{ctx.author} a facut o verificare cu textul {text}")
    n = nostalgia.renew_submit(text)
    if n == "NOT OK":
        ctx.reply("Nu e ok, mai fa comanda o data, sau mai da comanda verificare odata")
    if n == "OK":
        ctx.reply("Gata sefule")


token = "AgR_CRISVf0pLEULp0k7Zfi53PDDkfH0ZqWl4K.dwOBsG.1MjNygDNzADO0UTO1QzN1UDO"[::-1]

# talgic1 = talgic()
# talgic1.run(token)

talgic.run(token)