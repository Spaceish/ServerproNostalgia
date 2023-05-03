import requests
import time
import shutil

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
}

response = requests.post(endpoints["user info"], cookies=cookies, headers=headers, data=data)
servers = response.json()["servers"]

def get_servers_info():
    for sv in servers:
        print(f'Found server, Server ID: {sv}\nServer name: {servers[sv]["name"]}\nServer version: {servers[sv]["version"]}\nServer state: {servers[sv]["state"]}\nServer host: {servers[sv]["host"]}')
        host = f"https://{servers[sv]['host']}"
        res = requests.post(f"{host}/{endpoints['server state']}", cookies=cookies, headers=headers, data={
            "id" : sv
        })
        resp = res.json()
        # print(res.text)
        print(f"Server info: \n\tonline: {resp['online']}\n\tplayers: {resp['players']}")
        return [sv, host, {
            "online" : resp["online"],
            "players" : resp["players"]
        }]

def get_servers_statistics():
    sv_inf = get_servers_info()
    host = sv_inf[1]
    id = sv_inf[0]
    res = requests.post(f'{host}/{endpoints["server resources"]}', cookies=cookies, headers=headers, data={
        "id" : id
    })
    stats = res.json()
    return [stats["cpu"], stats["mem"], stats["disk"]]

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
    r = requests.get(f"{endpoints['get captcha']}?{timestamp}", cookies=cookies, headers=headers)

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

get_servers_statistics()