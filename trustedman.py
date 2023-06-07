import auth
import discord
from PIL import Image
from PIL import ImageDraw
import os
from PIL import ImageFont

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

async def check_key(client, ctx, key, sup="test"):
    flag = auth.verify_key(key)
    if flag == False:
        print(f"{ctx.author} a incercat {sup}, dar a gresit cheia de autentificare")
        await ctx.send(f"{ctx.author.mention} a incercat {sup}, dar a gresit cheia de autentificare")
        await ctx.reply("Mananci cacat")
        asta_primesti(ctx.author.name)
        await ctx.reply(file=discord.File('cac.png'))
        os.remove("cac.png")
        await ctx.send(f"Cheia anterioara a fost {auth.load_key()}, s-a generat una noua")
        new_key = auth.generate_key()
        await send_key(client, new_key)
        return
    else:
        await ctx.send("Este ok. Te-ai autentificat cu succes sefule.")
        await ctx.send(f"Cheia anterioara a fost {auth.load_key()}, s-a generat una noua")
        new_key = auth.generate_key()
        await send_key(client, new_key)
        # return new_key
        
    
async def send_key(client, key):
    trusted = auth.retrieve_trustedman()
    trustedtrusted = client.get_user(trusted)
    await trustedtrusted.send(
        f"Aici este noua cheie : \n{key}"
    )