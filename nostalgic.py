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
    await ctx.send(f"informatiile cerute: \n\tStatusul: {informatii['online']}\n\tJucatori: {informatii['players']}")

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
        await ctx.reply("Nu e ok, mai fa comanda o data, sau mai da comanda verificare odata")
    else:
        await ctx.reply("Gata sefule")

@talgic.command()
async def stats(ctx):
    print(f"{ctx.author} a cerut informatiile serverului")
    sv_stats = nostalgia.get_servers_statistics()
    await ctx.reply("Ai cerut informatiile despre server")
    await ctx.reply(f"Uite informatiile cerute sefule:\n\tProcesoru: {sv_stats[0]}\n\tMemoria RAM: {sv_stats[1]}")
    await ctx.send(f"Sefu {ctx.author.mention} a cerut statistici despre server.")

@talgic.command()
async def reverificare(ctx):
    print(f"{ctx.author} a cerut o reverificare a serverului")
    nostalgia.resume()
    await ctx.reply(f"Ai cerut o reverificare sefule, reverifica cu {prefixu}reverifica textul-ce-apare-in-imagine")
    await ctx.send(file=discord.File('captcha.png'))
    await ctx.send(f'{ctx.author.mention} a cerut o reverificare')

@talgic.command()
async def reverifica(ctx, text):
    print(f"{ctx.author} a facut o reverificare cu textul {text}")
    n = nostalgia.resume_submit(text)
    if n == "NOT OK":
        await ctx.reply("Nu e ok, mai fa comanda o data, sau mai da comanda reverificare odata")
    else:
        await ctx.reply("Gata sefule")

@talgic.command()
async def restart(ctx):
    print(f"{ctx.author} a restartat serverul")
    await ctx.reply("Acum se va restarta serverul sefule")
    nostalgia.stop()
    await ctx.send(f"Sefu {ctx.author.mention} a restartat serverul")

token = "AgR_CRISVf0pLEULp0k7Zfi53PDDkfH0ZqWl4K.dwOBsG.1MjNygDNzADO0UTO1QzN1UDO"[::-1]

# talgic1 = talgic()
# talgic1.run(token)

talgic.run(token)