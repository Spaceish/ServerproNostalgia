import discord
import nostalgia
from discord.ext.commands import Bot as eu
import auth
import trustedman

prefixu = " UCIM ALA"[::-1]


talgic = eu(command_prefix=prefixu, self_bot=False)

@talgic.event
async def on_ready():
    print("Gattaaaa")
    trust_key = auth.generate_key()
    print(f"S-a generat cheia de autentificare : {trust_key}")
    await trustedman.send_key(talgic, trust_key)
    print("S-a trimis cheia de autentificare la trusted.")
    
@talgic.command()
async def test(ctx, key):
    print(f"Se verifica cheia : {key}")
    await ctx.send(f"Se verifica cheia : {key}")
    await trustedman.check_key(talgic, ctx, key)
    await ctx.send("Yay rezukltat")

@talgic.command()
async def porneste(ctx, key):
    if await trustedman.check_key(talgic, ctx, key, sup="de pornit serverul"): return
    print(f"{ctx.author} a pornit serverul")
    await ctx.reply("Acum se va porni serverul sefule")
    n = nostalgia.start()
    if n == None:
        await ctx.send(f"Sefu {ctx.author.mention} a pornit serverul")
    elif key == None:
        await ctx.send(f"Trebe cheia sefule {ctx.author.mention}")
    else:
        await ctx.send(f"Sefu {ctx.author.mention} nu a pornit serverul din cauza unei PRRRRRbleme")

@talgic.command()
async def opreste(ctx, key):
    if await trustedman.check_key(talgic, ctx, key, sup="de oprit serverul"): return
    print(f"{ctx.author} a oprit serverul")
    await ctx.reply("Acum se va opri serverul sefule")
    n = nostalgia.stop()
    if n == None:
        await ctx.send(f"Sefu {ctx.author.mention} a oprit serverul")
    else:
        await ctx.send(f"Sefu {ctx.author.mention} nu a oprit serverul din cauza unei PRRRRRbleme")

@talgic.command()
async def informatii(ctx, key):
    if await trustedman.check_key(talgic, ctx, key, sup="de a cere niste informatii despre server"): return
    print(f"{ctx.author} a cerut niste informatii despre server")
    await ctx.reply("Ai cerut niste informatii despre server sefule")
    info = nostalgia.get_servers_info()
    print(info)
    informatii = info[2]
    nume = info[3] if info[-1] == 1 else info[2]
    versiunea = info[4] if info[-1] == 1 else info[3]
    lumile = info[5] if info[-1] == 1 else "Nu se poate"
    try:
        await ctx.send(f"informatiile cerute: \n\tStatusul: {'Nu e pornit' if informatii['online'] == str(False) else 'Este pornit'}\n\tJucatori: {'nu e nimeni' if informatii['players'] == str(False) else informatii['players']}")
        await ctx.reply(f"Numele serverului: {nume}")
        await ctx.reply(f"Versiunea serverului: {versiunea}")
        await ctx.reply("Lumile serverului:")
    except:
        await ctx.reply("Trb reverificare")
    if type(lumile) == list:
        for lume in lumile:
            await ctx.reply(f"\n\t{lume}")
    elif type(lumile) == str:
        await ctx.reply(f'{lumile}')
    await ctx.send(f"Sefu {ctx.author.mention} a cerut niste informatii despre server")

@talgic.command()
async def verificare(ctx, key):
    if await trustedman.check_key(talgic, ctx, key, sup="de a cere o verificare despre server"): return
    print(f"{ctx.author} a cerut o verificare")
    nostalgia.renew()
    await ctx.reply(f"Ai cerut o verificare sefule, verifica cu {prefixu}verifica textul-ce-apare-in-imagine")
    await ctx.send(file=discord.File('captcha.png'))
    await ctx.send(f'{ctx.author.mention} a cerut o verificare')

@talgic.command()
async def verifica(ctx, text, key):
    if await trustedman.check_key(talgic, ctx, key, sup="de a verifica despre server"): return
    print(f"{ctx.author} a facut o verificare cu textul {text}")
    n = nostalgia.renew_submit(text)
    if n == "NOT OK":
        await ctx.reply("Nu e ok, mai fa comanda o data, sau mai da comanda verificare odata")
    else:
        await ctx.reply("Gata sefule")

@talgic.command()
async def stats(ctx, key):
    if await trustedman.check_key(talgic, ctx, key, sup="de a cere niste statistici despre server"): return
    print(f"{ctx.author} a cerut informatiile serverului")
    sv_stats = nostalgia.get_servers_statistics()
    await ctx.reply("Ai cerut informatiile despre server")
    await ctx.reply(f"Uite informatiile cerute sefule:\n\tProcesoru: {sv_stats[0]}\n\tMemoria RAM: {sv_stats[1]}")
    await ctx.send(f"Sefu {ctx.author.mention} a cerut statistici despre server.")

@talgic.command()
async def reverificare(ctx, key):
    if await trustedman.check_key(talgic, ctx, key, sup="de a cere o reverificare despre server"): return
    print(f"{ctx.author} a cerut o reverificare a serverului")
    nostalgia.resume()
    await ctx.reply(f"Ai cerut o reverificare sefule, reverifica cu {prefixu}reverifica textul-ce-apare-in-imagine")
    await ctx.send(file=discord.File('captcha.png'))
    await ctx.send(f'{ctx.author.mention} a cerut o reverificare')

@talgic.command()
async def reverifica(ctx, text, key):
    if await trustedman.check_key(talgic, ctx, key, sup="de a reverifica serverul"): return
    print(f"{ctx.author} a facut o reverificare cu textul {text}")
    n = nostalgia.resume_submit(text)
    if n == "NOT OK":
        await ctx.reply("Nu e ok, mai fa comanda o data, sau mai da comanda reverificare odata")
    else:
        await ctx.reply("Gata sefule")

@talgic.command()
async def restart(ctx, key):
    if await trustedman.check_key(talgic, ctx, key, sup="de a da restart la server") == False: return
    print(f"{ctx.author} a restartat serverul")
    await ctx.reply("Acum se va restarta serverul sefule")
    n = nostalgia.restart()
    if n == None:
        await ctx.send(f"Sefu {ctx.author.mention} a restartat serverul")
    else:
        await ctx.send(f"Sefu {ctx.author.mention} nu a restartat serverul din cauza unei PRRRRRbleme")

@talgic.command()
async def backup(ctx, key):
    if await trustedman.check_key(talgic, ctx, key, sup="de a face backup la server"): return
    print(f"{ctx.author} a cerut un backup la server")
    await ctx.reply("Acum se va face backup sefule")
    n = nostalgia.backup()
    await ctx.send(f"uite linkul la backup : {n[1]}")
    await ctx.send(f"Backupu se numeste : {n[0]}")
    await ctx.send(f"Sefu {ctx.author.mention} a facut backup serverului")
    
@talgic.command()
async def backupuri(ctx, key):
    if await trustedman.check_key(talgic, ctx, key, sup="de a cere niste backupuri despre server"): return
    print(f"{ctx.author} a cerut lista backupurilor la server")
    await ctx.reply("Acum se va lua lista backupurilor sefule")
    n = nostalgia.retrieve_backups()
    backupur = str()
    for backup in n:
        backupur += f'''
            Numele Backupului : {backup["numele"]},
            Data Backupului: {backup["ora in stampila"]},
            Linkul Backupului: {backup["link"]}
        ''' + '\n'
    await ctx.reply(backupur)
    await ctx.send(f"Sefu {ctx.author.mention} a cerut lista backupurilor serverului")

token = "AdRkdzHocM3GS8qtOBWeLBCSnxtxyTOXVOYrOp.NjIDnG.AOxETOycDO2UTN0gzN4ETOwATM"[::-1]

# talgic1 = talgic()
# talgic1.run(token)

talgic.run(token)