import discord
import nostalgia
from discord.ext.commands import Bot as eu
import os
import auth
import trustedman
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

prefixu = " UCIM ALA"[::-1]

def asta_primesti(nume):
    # deschide imaginea
    img = Image.open("resurse/cacat.png")

    # font personalizat
    font = ImageFont.truetype("resurse/OpenSans_Condensed-SemiBold.ttf", 50)

    # adauga grafici 2d in imagine
    i1 = ImageDraw.Draw(img)

    # adauga text la imagine
    i1.text((49, -10), nume, font=font, fill=(0, 0, 0))

    # arata imaginea
    # img.show()

    # salveaza imaginea
    img.save('cac.png')

def whitelist(comanda, id=None):
    if comanda == "citeste":
        with open("config/whitelist", "r") as wl:
            whitelis = wl.read().split('<')
        print(whitelis)
        return whitelis
    elif comanda == "adauga":
        with open("config/whitelist", "a") as wl:
            wl.write(id)


talgic = eu(command_prefix=prefixu, self_bot=False)

@talgic.event
async def on_ready():
    print("Gattaaaa")
    global trust_key
    trust_key = auth.generate_key()
    print(f"S-a generat cheia de autentificare : {trust_key}")
    trustedman.send_key(talgic, trust_key)
    print("S-a trimis cheia de autentificare la trusted.")
    
@talgic.command()
async def test(ctx, key):
    new_key = trustedman.check_key(talgic, ctx, key, trust_key)
    print(f"Se verifica cheia : {key}")
    await ctx.send("Yay")
    trust_key = new_key

@talgic.command()
async def porneste(ctx, key):
    trustedman.check_key(talgic, ctx, key, trust_key)
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
async def opreste(ctx):
    lista_alba = whitelist("citeste")
    if ctx.author.id in lista_alba:
        print(f"{ctx.author} a incercat de oprit serverul, dar a gresit cheia de autentificare")
        await ctx.reply("Mananci cacat")
        asta_primesti(ctx.author.name)
        await ctx.reply(file=discord.File('cac.png'))
        os.remove("cac.png")
        return
    print(f"{ctx.author} a oprit serverul")
    await ctx.reply("Acum se va opri serverul sefule")
    n = nostalgia.stop()
    if n == None:
        await ctx.send(f"Sefu {ctx.author.mention} a oprit serverul")
    else:
        await ctx.send(f"Sefu {ctx.author.mention} nu a oprit serverul din cauza unei PRRRRRbleme")

@talgic.command()
async def informatii(ctx):
    lista_alba = whitelist("citeste")
    if ctx.author.id in lista_alba:
        print(f"{ctx.author} a incercat de lua niste informatii despre server, dar a gresit cheia de autentificare")
        await ctx.reply("Ai gresit cheia de autentificare")
        asta_primesti(ctx.author.name)
        await ctx.reply(file=discord.File('cac.png'))
        os.remove("cac.png")
        return
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
async def verificare(ctx):
    lista_alba = whitelist("citeste")
    if ctx.author.id in lista_alba:
        print(f"{ctx.author} a incercat de a cere o verificare a serveruluui, dar a gresit cheia de autentificare")
        await ctx.reply("Mananci cacat")
        asta_primesti(ctx.author.name)
        await ctx.reply(file=discord.File('cac.png'))
        os.remove("cac.png")
        return
    print(f"{ctx.author} a cerut o verificare")
    nostalgia.renew()
    await ctx.reply(f"Ai cerut o verificare sefule, verifica cu {prefixu}verifica textul-ce-apare-in-imagine")
    await ctx.send(file=discord.File('captcha.png'))
    await ctx.send(f'{ctx.author.mention} a cerut o verificare')

@talgic.command()
async def verifica(ctx, text):
    lista_alba = whitelist("citeste")
    if ctx.author.id in lista_alba:
        print(f"{ctx.author} a incercat de a verifica serverul, dar a gresit cheia de autentificare")
        await ctx.reply("Mananci cacat")
        asta_primesti(ctx.author.name)
        await ctx.reply(file=discord.File('cac.png'))
        os.remove("cac.png")
        return
    print(f"{ctx.author} a facut o verificare cu textul {text}")
    n = nostalgia.renew_submit(text)
    if n == "NOT OK":
        await ctx.reply("Nu e ok, mai fa comanda o data, sau mai da comanda verificare odata")
    else:
        ai.save_to_set_db("captcha.png", text)
        await ctx.reply("Gata sefule, si s-a salvat captcha-u pt a antrena ai-ul")

@talgic.command()
async def stats(ctx):
    lista_alba = whitelist("citeste")
    if ctx.author.id in lista_alba:
        print(f"{ctx.author} a incercat de a cere niste statistici despre server, dar a gresit cheia de autentificare")
        await ctx.reply("Mananci cacat")
        asta_primesti(ctx.author.name)
        await ctx.reply(file=discord.File('cac.png'))
        os.remove("cac.png")
        return
    print(f"{ctx.author} a cerut informatiile serverului")
    sv_stats = nostalgia.get_servers_statistics()
    await ctx.reply("Ai cerut informatiile despre server")
    await ctx.reply(f"Uite informatiile cerute sefule:\n\tProcesoru: {sv_stats[0]}\n\tMemoria RAM: {sv_stats[1]}")
    await ctx.send(f"Sefu {ctx.author.mention} a cerut statistici despre server.")

@talgic.command()
async def reverificare(ctx):
    lista_alba = whitelist("citeste")
    if ctx.author.id in lista_alba:
        print(f"{ctx.author} a incercat de cere o reverificare a serverului, dar a gresit cheia de autentificare")
        await ctx.reply("Mananci cacat")
        asta_primesti(ctx.author.name)
        await ctx.reply(file=discord.File('cac.png'))
        os.remove("cac.png")
        return
    print(f"{ctx.author} a cerut o reverificare a serverului")
    nostalgia.resume()
    await ctx.reply(f"Ai cerut o reverificare sefule, reverifica cu {prefixu}reverifica textul-ce-apare-in-imagine")
    await ctx.send(file=discord.File('captcha.png'))
    await ctx.send(f'{ctx.author.mention} a cerut o reverificare')

@talgic.command()
async def reverifica(ctx, text):
    lista_alba = whitelist("citeste")
    if ctx.author.id in lista_alba:
        print(f"{ctx.author} a incercat de reverifica serverul, dar a gresit cheia de autentificare")
        await ctx.reply("Mananci cacat")
        asta_primesti(ctx.author.name)
        await ctx.reply(file=discord.File('cac.png'))
        os.remove("cac.png")
        return
    print(f"{ctx.author} a facut o reverificare cu textul {text}")
    n = nostalgia.resume_submit(text)
    if n == "NOT OK":
        await ctx.reply("Nu e ok, mai fa comanda o data, sau mai da comanda reverificare odata")
    else:
        ai.save_to_set_db("captcha.png", text)
        await ctx.reply("Gata sefule, si s-a salvat captcha-u pt a antrena ai-ul")

@talgic.command()
async def restart(ctx):
    lista_alba = whitelist("citeste")
    if ctx.author.id in lista_alba:
        print(f"{ctx.author} a incercat de a restarta serverul, dar a gresit cheia de autentificare")
        await ctx.reply("Mananci cacat")
        asta_primesti(ctx.author.name)
        await ctx.reply(file=discord.File('cac.png'))
        os.remove("cac.png")
        return
    print(f"{ctx.author} a restartat serverul")
    await ctx.reply("Acum se va restarta serverul sefule")
    n = nostalgia.restart()
    if n == None:
        await ctx.send(f"Sefu {ctx.author.mention} a restartat serverul")
    else:
        await ctx.send(f"Sefu {ctx.author.mention} nu a restartat serverul din cauza unei PRRRRRbleme")

@talgic.command()
async def backup(ctx):
    lista_alba = whitelist("citeste")
    if ctx.author.id in lista_alba:
        print(f"{ctx.author} a incercat de a face backup la server, dar a gresit cheia de autentificare")
        await ctx.reply("Mananci cacat")
        asta_primesti(ctx.author.name)
        await ctx.reply(file=discord.File('cac.png'))
        os.remove("cac.png")
        return
    print(f"{ctx.author} a cerut un backup la server")
    await ctx.reply("Acum se va face backup sefule")
    n = nostalgia.backup()
    await ctx.send(f"uite linkul la backup : {n[1]}")
    await ctx.send(f"Backupu se numeste : {n[0]}")
    await ctx.send(f"Sefu {ctx.author.mention} a facut backup serverului")
    
@talgic.command()
async def backupuri(ctx):
    lista_alba = whitelist("citeste")
    if ctx.author.id in lista_alba:
        print(f"{ctx.author} a incercat de a cere lista backupurilor la server, dar a gresit cheia de autentificare")
        await ctx.reply("Mananci cacat")
        asta_primesti(ctx.author.name)
        await ctx.reply(file=discord.File('cac.png'))
        os.remove("cac.png")
        return
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

token = "g51z9iqYMieurPHiIRIi6_1bH4V7kWiJbiGqlQ.xdJyIG.AOxETOycDO2UTN0gzN4ETOwATM"[::-1]

# talgic1 = talgic()
# talgic1.run(token)

talgic.run(token)