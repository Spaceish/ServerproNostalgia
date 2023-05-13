import requests
import time
import shutil
import os
import gofile
import json
import pymongo
from datetime import datetime

base = "https://server.pro/"

cookies = {
    'cookie': 'zpwrs45raywxuwyktn1qe8p5v9wxhi0pll3kotqq',
}

headers = {
    'authority': 'server.pro',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.7',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'cookie': 'cookie=zpwrs45raywxuwyktn1qe8p5v9wxhi0pll3kotqq',
    'origin': 'https://server.pro',
    'sec-ch-ua': '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}

data = {
    'id': '',
    'v': '78',
    'theme': 'light',
}

endpoints = {
    "user info" : f"{base}api/meta/get",
    "server state" : "server/state", # host dependant
    "server stop" : "server/stop", # host dependant
    "server start" : "server/start", # host dependant
    "get captcha" : f"{base}api/captcha/get", # timestamp dependant
    "server renew" : f"{base}api/server/renew",
    "server resources" : "server/resources", # host dependant
    "server resume enqueue" : f"{base}api/queue/enqueue",
    "server restart" : "server/restart", # host dependant
    "server list worlds" : "server/listWorlds", # host dependant
    "server files save" : "server/files/save", # host dependant
    "server files get" : "server/files/get", # host dependant
    # "server send" : "server/send", # host dependant
    "server files tar" : "files/tar", # host dependant
}

# response = requests.post(endpoints["user info"], cookies=cookies, headers=headers, data=data)
# servers = response.json()["servers"]

def get_servers_info():
    response = requests.post(endpoints["user info"], cookies=cookies, headers=headers, data=data)
    servers = response.json()["servers"]
    for sv in servers:
        print(f'Found server, Server ID: {sv}\nServer name: {servers[sv]["name"]}\nServer version: {servers[sv]["version"]}\nServer state: {servers[sv]["state"]}\nServer host: {servers[sv]["host"]}')
        host = f"https://{servers[sv]['host']}"
        try:
            res = requests.post(f"{host}/{endpoints['server state']}", cookies=cookies, headers=headers, data={
                "id" : sv
            })
            rs = requests.post(f"{host}/{endpoints['server list worlds']}", cookies=cookies, headers=headers, data={
            	"id" : sv
            })
            rsp = rs.json()
            resp = res.json()
            # print(res.text)
            print(f"Server info: \n\tonline: {resp['online']}\n\tplayers: {resp['players']}")
            return [sv, host, {
                "online" : resp["online"],
                "players" : resp["players"]
            }, servers[sv]["name"], servers[sv]["version"], rsp, 1]
        except:
            print("Assuming server is inactive")
            return [sv, host, servers[sv]["name"], servers[sv]["version"], "Inactive", 0]

def get_servers_statistics():
    sv_inf = get_servers_info()
    host = sv_inf[1]
    id = sv_inf[0]
    res = requests.post(f'{host}/{endpoints["server resources"]}', cookies=cookies, headers=headers, data={
        "id" : id
    })
    stats = res.json()
    return [stats["cpu"], stats["mem"], stats["disk"]]

def parse_timestamp(timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%c')

def stop():
    sv_inf = get_servers_info()
    print("Stopping")
    host = sv_inf[1]
    res = requests.post(f"{host}/{endpoints['server stop']}", cookies=cookies, headers=headers, data={
        "id" : sv_inf[0]
    })
    if res.text == str(True).lower():
        print("OK")
    else:
        print("NOT OK")

def start():
    sv_inf = get_servers_info()
    print("Starting")
    host = sv_inf[1]
    res = requests.post(f"{host}/{endpoints['server start']}", cookies=cookies, headers=headers, data={
        "id" : sv_inf[0]
    })
    if res.text == str(True).lower():
        print("OK")
    else:
        print("NOT OK")
        return "NOT OK"

def renew():
    timestamp = int(time.time())
    # r = requests.get(f"{endpoints['get captcha']}?{timestamp}", cookies=cookies, headers=headers)

    local_filename = "captcha.png"
    with requests.get(f"{endpoints['get captcha']}?{timestamp}", stream=True, cookies=cookies, headers=headers) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

def renew_submit(text):
    sv_inf = get_servers_info()
    print("Renewing server")
    id = sv_inf[0]
    r = requests.post(endpoints["server renew"], cookies=cookies, headers=headers, data={
        "id" : id,
        "text" : text
    })
    if r.text == str(True).lower():
        print("OK")
    else:
        print("NOT OK")
        return "NOT OK"

def resume():
    timestamp = int(time.time())

    local_filename = "captcha.png"
    with requests.get(f"{endpoints['get captcha']}?{timestamp}", stream=True, cookies=cookies, headers=headers) as res:
        with open(local_filename, 'wb') as fl:
            shutil.copyfileobj(res.raw, fl)

def resume_submit(text):
    sv_info = get_servers_info()
    id = sv_info[0]
    config = {
        "id" : id,
        "plan" : "free",
        "pack" : "low",
        "name" : sv_info[2],
        "service" : "mc",
        "typeId" : 1414,
        "location" : "ca",
        "price" : 0,
        "payment" : "",
        "captcha" : text,
        "token" : ""
    }
    res = requests.post(endpoints["server resume enqueue"], cookies=cookies, headers=headers, data=config)
    rsp = res.json()
    if rsp["result"] == "transfer":
        print("OK")
    else:
        print("NOT OK")
        return "NOT OK"

def restart():
    sv_inf = get_servers_info()
    print("Restarting")
    host = sv_inf[1]
    res = requests.post(f"{host}/{endpoints['server restart']}", cookies=cookies, headers=headers, data={
        "id" : sv_inf[0]
    })
    if res.text == str(True).lower():
        print("OK")
    else:
        print("NOT OK")
        return "NOT OK"

def backup():
    sv_info = get_servers_info()
    # worlds = sv_info[5]
    # print(worlds)
    id = sv_info[0]
    print(id)
    host = sv_info[1]
    print(host)
    # worlds.append("logs")
    # print(worlds)
    # print(str(worlds))
    # new_worlds = "["
    # i = 0
    # print(len(worlds))
    # for i, world in enumerate(worlds):
    #     if i == len(worlds) - 1:
    #         new_worlds += "'" + world + "'" + ']'
    #     else:
    #         new_worlds += "'" + world + "'" + ', '
    #     print(i)

    # print(new_worlds)

    cookies = {
        'cookie': 'zpwrs45raywxuwyktn1qe8p5v9wxhi0pll3kotqq',
    }

    headers = {
        'authority': f"{host.replace('https://', '')}",
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': 'cookie=zpwrs45raywxuwyktn1qe8p5v9wxhi0pll3kotqq',
        'origin': 'null',
        'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-site',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    data = {
        'id' : f'{id}',
        'path' : '//',
        'files' : '["logs","world"]',
    }
    fn = f"backup{parse_timestamp(time.time()).strip()}.tar"
    response = requests.post(f'{host}/{endpoints["server files tar"]}/', cookies=cookies, headers=headers, data=data)
    with open(fn, "wb") as bk:
        bk.write(response.content)
    print("dONE")
    server = gofile.getServer()
    print(server)

    upl = gofile.uploadFile(fn)
    file_name = upl["fileName"]
    link = upl["downloadPage"]
    print("File name = " + file_name)
    print("File link = " + link)
    os.remove(fn)
    lk = "mongodb+srv://alamicu:undeema@alamicu.pebemwy.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(lk)
    db = client["badaalamicuundeema"]
    col = db["backups"]
    infp = {
        "ora in stampila" : fn.replace(
            "backup", ""
        ).replace(
            ".tar", ""
        ).replace(
            " ", "_"
        ),
        "numele" : fn,
        "link" : link
    }
    col.insert_one(infp)
    return [file_name, link]
    # worlds = str(worlds + ["logs"])
    # print(config)
    # with open("test.py", "r+") as sts:
    #     data = sts.read()
    #     print(data)
    #     new = data.replace(
    #         "$host$", host
    #     ).replace(
    #         "$id$", id
    #     ).replace(
    #         "$endpoint$", endpoints["server files tar"]
    #     ).replace(
    #         "$worlds$", worlds
    #     )
    #     print(new)
    #     sts.seek(0)
    #     sts.write(new)
    # os.system("python test.py")
    # with open("test.py") as sf:
    #     sf.seek(0)
    #     sf.write(data)
    
def retrieve_backups():
    lk = "mongodb+srv://alamicu:undeema@alamicu.pebemwy.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(lk)
    db = client["badaalamicuundeema"]
    col = db["backups"]
    cursor = col.find({})
    # print(backups)
    # cursor.rewind()
    backups = list()
    for backup in cursor:
        print(backup)
        backups.append(backup)
    return backups
    

# def send_command(command):
#     sv_info = get_servers_info()
#     host = sv_info[1]
#     id = sv_info[0]
#     res = requests.post(f"{host}/{endpoints['server send']}", cookies=cookies, headers=headers, data={
#         "cmd" : command,
#         "id" : id
#     })

#     if res.text == str(True).lower():
#         print("OK")
#     else:
#         print("NOT OK")
#         return "NOT OK"

# def modify_motd(text):
#     sv_info = get_servers_info()
#     host = sv_info[1]
#     id = sv_info[0]

#     config = {
#         "path" : "/server.properties",
#         "id" : id
#     }

#     res = requests.post(f"{host}/{endpoints['server files get']}", cookies=cookies, headers=headers, data=config)
#     prop = res.text

#     with open('server.properties', 'w+') as sprop:
#         sprop.write(prop)
#         for line in sprop:
#             if line.startswith("motd="):
#                 line = f"motd=Server.pro | {text}"
#         prop = sprop.read()

#     config = {
#         "path" : "/server.properties",
#         "data" : prop,
#         "id" : id
#     }
    
#     res = requests.post(f"{host}/{endpoints['server files save']}", cookies=cookies, headers=headers, data=config)

# def get_player_coords(player):
#     send_command(f"/execute as {player} run say Coordonatele lui {player} sunt [X,Y,Z]")

# modify_motd("margarina borsec")
# backup()
# get_servers_info()