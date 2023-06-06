import auth
import os
from nostalgic import whitelist, asta_primesti

async def check_key(client, ctx, key, generated_key):
    lista_alba = whitelist("citeste")
    if ctx.author.id in lista_alba or auth.verify_key(key, generated_key) == False:
        print(f"{ctx.author} a incercat de pornit serverul, dar a gresit cheia de autentificare")
        await ctx.send(f"{ctx.author.mention} a incercat de pornit serverul, dar a gresit cheia de autentificare")
        await ctx.reply("Mananci cacat")
        asta_primesti(ctx.author.name)
        await ctx.reply(file=discord.File('cac.png'))
        os.remove("cac.png")
        return
    
    await ctx.send("Este ok. Te-ai autentificat cu succes sefule.")
    new_key = auth.generate_key()
    await send_key(client, key)
    return new_key
        
    
async def send_key(client, key):
    trusted = auth.retrieve_trustedman()
    trustedtrusted = client.get_user(trusted)
    await trustedtrusted.send(
        f"Aici este noua cheie : \n{auth.distribute_key(key)}"
    )