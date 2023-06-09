import os
if os.name == "nt":
    from pyngrok import ngrok
from pymongo import MongoClient

lk = "mongodb+srv://xalexclashroyale:canusmp@smp.j5jtcsr.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(lk)
db = client["smp"]
col = db["tunel"]


def start_tunnel():
    if os.name != "nt":
        print("Nu esti pe nogork")
        return
    tunnel : ngrok.NgrokTunnel = ngrok.connect()
    print(f"Gata sefu, tunelu e gata pe {tunnel.public_url}")
    tun = tunnel.public_url
    col.update_one({}, {"$set": {"tunel": tun}}, upsert=True)

def stop_tunnnel():
    if os.name != "nt":
        print("Nu esti pe nogork")
        return
    tunnels = ngrok.get_tunnels()
    tun = tunnels[0]
    ngrok.disconnect(tun)
    print("A cazut tunelu")

try:
    start_tunnel()
except KeyboardInterrupt:
    stop_tunnnel()
    exit(13)