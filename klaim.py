import requests
import json
import time
import random
import base64
import os
import glob
import string
import asyncio
import aiohttp
from datetime import datetime
from itertools import cycle
from colorama import init, Fore, Style
from fake_useragent import UserAgent
from requests_html import HTMLSession
file_akun = 'initdata.txt'
file_vc_balapan = 'voucher_hamster_bike1.txt'
file_vc_train = 'voucher_train_miner1.txt'
file_vc_clone = 'voucher_clone_army1.txt'
file_vc_cube = 'voucher_chain_cube1.txt'
session = HTMLSession()
ua = UserAgent()
# Initialize colorama
init(autoreset=True)
def load_tokens(filename):
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []
def get_headers(token: str) -> dict:
    return {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': f'Bearer {token}',
        'Connection': 'keep-alive',
        'Origin': 'https://hamsterkombatgame.io',
        'Referer': 'https://hamsterkombatgame.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': ua.random
    }
def get_token(init_data_raw):
    url = 'https://api.hamsterkombatgame.io/auth/auth-by-telegram-webapp'
    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://hamsterkombatgame.io',
        'Referer': 'https://hamsterkombatgame.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': ua.random,
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    data = json.dumps({"initDataRaw": init_data_raw})
    res = session.post(url, headers=headers, data=data)
    if res.status_code == 200:
        return res.json()['authToken']
    else:
        error_data = res.json()
        if "invalid" in error_data.get("error_code", "").lower():
            print(Fore.LIGHTRED_EX + "\rFailed Get Token. Invalid init data", flush=True)
        else:
            print(Fore.LIGHTRED_EX + f"\rFailed Get Token. {error_data}", flush=True)
        return None
def authenticate(token):
    url = 'https://api.hamsterkombatgame.io/auth/me-telegram'
    headers = get_headers(token)
    response = session.post(url, headers=headers)
    return response
def klaim_voucher(token,pocer):
    url = 'https://api.hamsterkombatgame.io/clicker/apply-promo'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"promoCode": pocer})
    response = session.post(url, headers=headers, data=data)
    return response
def main():
    print_welcome_message()
    print(Fore.LIGHTGREEN_EX + "Bot dijalankan....")
    init_data = load_tokens(file_akun)
    token_cycle = cycle(init_data)
    token_dict = {}  # Dictionary to store successful tokens
    while True:
        init_data_raw = next(token_cycle)
        token = token_dict.get(init_data_raw)
        if token:
            print(Fore.LIGHTRED_EX + f"\n\n\n\rAkun: Diulang", flush=True)
        else:
            token = get_token(init_data_raw)
            # print(token)
            if token:
                token_dict[init_data_raw] = token
                print(Fore.LIGHTGREEN_EX + f"\n\n\rAkun: Aktif", flush=True)
            else:
                print(Fore.LIGHTRED_EX + f"\rBeralih ke akun selanjutnya\n", flush=True)
                continue  # Lanjutkan ke iterasi berikutnya jika gagal mendapatkan token
        response = authenticate(token)
        ## TOKEN AMAN
        if response.status_code == 200:
            user_data = response.json()
            username = user_data.get('telegramUser', {}).get('username', 'Username Kosong')
            firstname = user_data.get('telegramUser', {}).get('firstName', 'Kosong')
            lastname = user_data.get('telegramUser', {}).get('lastName', 'Kosong')
            print(Fore.LIGHTYELLOW_EX + f"~~~~~~~~[{Fore.LIGHTWHITE_EX} {username} | {firstname} {lastname} {Fore.LIGHTYELLOW_EX}]~~~~~~~~\n")
			# Balap Sepeda
            vsukses = 0
            for x in range(4):
                count = x + 1
                with open(file_vc_balapan, "r") as myfile:
                    pocer = myfile.readline().strip('\n')
                print(Fore.BLUE + f"\r[ Bike   ] : VC-{count}: {pocer}             ", flush=True)
                response = klaim_voucher(token,pocer)
                if response.status_code == 200:
                    print(Fore.LIGHTGREEN_EX + f"\r[ Bike   ] : VC-{count} berhasil diklaim", flush=True)
                    with open(file_vc_balapan, "r") as myfile:
                        rows = myfile.readlines()[1:]
                    with open(file_vc_balapan, "w") as myfile:
                        for item in rows:
                            myfile.write(item)
                            vsukses += 1
                    time.sleep(1)
                elif response.status_code == 400:
                    print(Fore.LIGHTRED_EX + f"\r[ Bike   ] : VC-{count} gagal diklaim", flush=True)
                else:
                    print(Fore.LIGHTRED_EX + f"\r[ Bike   ] : Gagal ambil status server...", flush=True)
                count += 1
            print(Fore.LIGHTCYAN_EX + f"\r[ Bike	] : Berhasil Klaim {vsukses} voucher", flush=True)
			# Train Miner
            vsukses = 0
            for x in range(4):
                count = x + 1
                with open(file_vc_train, "r") as myfile:
                    pocer = myfile.readline().strip('\n')
                print(Fore.BLUE + f"\r[ Train   ] : VC-{count}: {pocer}             ", flush=True)
                response = klaim_voucher(token,pocer)
                if response.status_code == 200:
                    print(Fore.LIGHTGREEN_EX + f"\r[ Train   ] : VC-{count} berhasil diklaim", flush=True)
                    with open(file_vc_train, "r") as myfile:
                        rows = myfile.readlines()[1:]
                    with open(file_vc_train, "w") as myfile:
                        for item in rows:
                            myfile.write(item)
                            vsukses += 1
                    time.sleep(1)
                elif response.status_code == 400:
                    print(Fore.LIGHTRED_EX + f"\r[ Train   ] : VC-{count} gagal diklaim", flush=True)
                else:
                    print(Fore.LIGHTRED_EX + f"\r[ Train   ] : Gagal ambil status server...", flush=True)
                count += 1
            print(Fore.LIGHTCYAN_EX + f"\r[ Train	] : Berhasil Klaim {vsukses} voucher", flush=True)
			# Clone Army
            vsukses = 0
            for x in range(4):
                count = x + 1
                with open(file_vc_clone, "r") as myfile:
                    pocer = myfile.readline().strip('\n')
                print(Fore.BLUE + f"\r[ Clone   ] : VC-{count}: {pocer}             ", flush=True)
                response = klaim_voucher(token,pocer)
                if response.status_code == 200:
                    print(Fore.LIGHTGREEN_EX + f"\r[ Clone   ] : VC-{count} berhasil diklaim", flush=True)
                    with open(file_vc_clone, "r") as myfile:
                        rows = myfile.readlines()[1:]
                    with open(file_vc_clone, "w") as myfile:
                        for item in rows:
                            myfile.write(item)
                            vsukses += 1
                    time.sleep(1)
                elif response.status_code == 400:
                    print(Fore.LIGHTRED_EX + f"\r[ Clone   ] : VC-{count} gagal diklaim", flush=True)
                else:
                    print(Fore.LIGHTRED_EX + f"\r[ Clone   ] : Gagal ambil status server...", flush=True)
                count += 1
            print(Fore.LIGHTCYAN_EX + f"\r[ Clone	] : Berhasil Klaim {vsukses} voucher", flush=True)
            # Cube
            vsukses = 0
            for x in range(4):
                count = x + 1
                with open(file_vc_cube, "r") as myfile:
                    pocer = myfile.readline().strip('\n')
                print(Fore.BLUE + f"\r[ Cube   ] : VC-{count}: {pocer}             ", flush=True)
                response = klaim_voucher(token,pocer)
                if response.status_code == 200:
                    print(Fore.LIGHTGREEN_EX + f"\r[ Cube   ] : VC-{count} berhasil diklaim", flush=True)
                    with open(file_vc_cube, "r") as myfile:
                        rows = myfile.readlines()[1:]
                    with open(file_vc_cube, "w") as myfile:
                        for item in rows:
                            myfile.write(item)
                            vsukses += 1
                    time.sleep(1)
                elif response.status_code == 400:
                    print(Fore.LIGHTRED_EX + f"\r[ Cube   ] : VC-{count} gagal diklaim", flush=True)
                else:
                    print(Fore.LIGHTRED_EX + f"\r[ Cube   ] : Gagal ambil status server...", flush=True)
                count += 1
            print(Fore.LIGHTCYAN_EX + f"\r[ Cube	] : Berhasil Klaim {vsukses} voucher", flush=True)
            print(Fore.LIGHTYELLOW_EX + "\r=================================================")
        ## TOKEN MATI        
        elif response.status_code == 401:
            error_data = response.json()
            if error_data.get("error_code") == "NotFound_Session":
                print(Fore.LIGHTRED_EX + f"=== [ Token Invalid {token} ] ===")
                token_dict.pop(init_data_raw, None)  # Remove invalid token
                token = None  # Set token ke None untuk mendapatkan token baru di iterasi berikutnya
            else:
                print(Fore.LIGHTRED_EX + "Authentication failed with unknown error")
        else:
            print(Fore.LIGHTRED_EX + f"Error with status code: {response.status_code}")
            token = None  # Set token ke None jika terjadi error lain
        time.sleep(1)
def print_welcome_message():
    print(Fore.LIGHTYELLOW_EX + "\n\rRecode By Una Davina ( https://t.me/unadavina )")
    print(Fore.LIGHTGREEN_EX + "\n=============================================")
if __name__ == "__main__":
    main()