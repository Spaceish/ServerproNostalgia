import requests

site = "http://localhost:3000"

def post_key(key):
    payload = {
        "key" : str(key)
    }
    endpoint = f"{site}/key"
    requests.post(url=endpoint, params=payload)
    print("S-a postat cheiea pe site")

def get_key():
    endpoint = f"{site}/key-rec"
    r = requests.get(url=endpoint)
    key = r.json()
    print(key)

def main():
    print("[1] POST KEY\n[2] GET KEY")
    op = int(input("OP >.< "))
    if op == 1:
        print("POSTING KEY")
        k = str(input("Enter a new testing key to post >.< "))
        post_key(k)
        print("Done")
    else:
        print("GETTING KEY")
        get_key()
        print("Done")

while True:
    main()