import os
import sys
import time
import psutil
import random
import logging
import asyncio
from tasksio import TaskPool
from datetime import datetime
import discum
import warnings


warnings.filterwarnings("ignore", category=DeprecationWarning) 

class Scraper(object):

    def __init__(self, guild_id, channel_id, token):
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.token = token

        self.scraped = []

    def scrape(self):
        try:
            client = discum.Client(token=self.token, log=False)

            client.gateway.fetchMembers(self.guild_id, self.channel_id, reset=False, keep="all")

            @client.gateway.command
            def scraper(resp):
                try:
                    if client.gateway.finishedMemberFetching(self.guild_id):
                        client.gateway.removeCommand(scraper)
                        client.gateway.close()
                except Exception:
                    pass

            client.gateway.run()

            for user in client.gateway.session.guild(self.guild_id).members:
                self.scraped.append(user)

            client.gateway.close()
        except Exception:
            return
    
    def fetch(self):
        try:
            self.scrape()
            if len(self.scraped) == 0:
                return self.fetch()
            return self.scraped
        except Exception:
            self.scrape()
            if len(self.scraped) == 0:
                return self.fetch()
            return self.scraped

from aiohttp import ClientSession
from colorama import Fore


class Discord(object):
    def __init__(self):
        if sys.platform == "linux":
            self.clear = lambda: os.system("clear")
        else:
            self.clear = lambda: os.system("cls")

        self.clear()
        self.tokens = []

        self.guild_name = None
        self.guild_id = None
        self.channel_id = None

        filename = "mensagem.txt"
        infile = open(filename, "r")
        self.message = infile.read()

        try:
            for line in open("token.txt"):
                self.tokens.append(line.replace("\n", ""))
        except Exception:
            open("token.txt", "a ").close()

            print(f"   {Fore.YELLOW}Insira seus tokens em tokens.txt{Fore.RESET}")

            sys.exit()

        print(
            f"""{Fore.BLUE}


   ██╗      ██████╗ ███████╗██╗   ██╗    ██╗   ██╗███████╗███████╗██████╗     ██████╗ ██╗██╗   ██╗    ██╗   ██╗██████╗ 
   ██║     ██╔═══██╗██╔════╝╚██╗ ██╔╝    ██║   ██║██╔════╝██╔════╝██╔══██╗    ██╔══██╗██║██║   ██║    ██║   ██║╚════██╗
   ██║     ██║   ██║█████╗   ╚████╔╝     ██║   ██║███████╗█████╗  ██████╔╝    ██║  ██║██║██║   ██║    ██║   ██║ █████╔╝
   ██║     ██║   ██║██╔══╝    ╚██╔╝      ██║   ██║╚════██║██╔══╝  ██╔══██╗    ██║  ██║██║╚██╗ ██╔╝    ╚██╗ ██╔╝ ╚═══██╗
   ███████╗╚██████╔╝██║        ██║       ╚██████╔╝███████║███████╗██║  ██║    ██████╔╝██║ ╚████╔╝      ╚████╔╝ ██████╔╝
   ╚══════╝ ╚═════╝ ╚═╝        ╚═╝        ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝    ╚═════╝ ╚═╝  ╚═══╝        ╚═══╝  ╚═════╝ 
{Fore.RESET}"""
        )

        print(
            f"   [-] {Fore.YELLOW}A no total{Fore.RESET}{Fore.CYAN} %s {Fore.RESET}{Fore.YELLOW}token(s) na lista{Fore.RESET}\n"
            % (len(self.tokens))
        )

        self.invite = input(f"   [?] {Fore.YELLOW}Convite do Servidor:{Fore.RESET} ")

        try:
            self.delay = float(input(f"   [?] {Fore.YELLOW}Tempo:{Fore.RESET} "))
        except Exception:
            self.delay = 0

        print()

    def stop(self):
        process = psutil.Process(os.getpid())
        process.terminate()

    def nonce(self):
        date = datetime.now()
        unixts = time.mktime(date.timetuple())
        return str((int(unixts) * 1000 - 1420070400000) * 4194304)

    async def headers(self, token):
        async with ClientSession() as client:
            async with client.get("https://discord.com/app") as response:
                cookies = str(response.cookies)
                dcfduid = cookies.split("dcfduid=")[1].split(";")[0]
                sdcfduid = cookies.split("sdcfduid=")[1].split(";")[0]

        return {"Authorization": token,"accept": "*/*","accept-language": "en-US","connection": "keep-alive","cookie": "__dcfduid=%s; __sdcfduid=%s; locale=en-US" % (dcfduid, sdcfduid),"DNT": "1","origin": "https://discord.com","sec-fetch-dest": "empty","sec-fetch-mode": "cors","sec-fetch-site": "same-origin","referer": "https://discord.com/channels/@me","TE": "Trailers","User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36","X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAxIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDIiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6ODMwNDAsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9",}

    async def login(self, token: str):
        try:
            headers = await self.headers(token)
            async with ClientSession(headers=headers) as client:
                async with client.get(
                    "https://discord.com/api/v9/users/@me/library"
                ) as response:
                    if response.status == 200:
                        print(
                            f"   [L] {Fore.GREEN}Logado com sucesso no token{Fore.RESET} {Fore.CYAN}%s{Fore.RESET} "
                            % (token[:59])
                        )
                    if response.status == 401:
                        print(
                            f"   [X] {Fore.RED}Conta inválida %s{Fore.RESET}"
                            % (token[:59])
                        )
                        self.tokens.remove(token)
                    if response.status == 403:
                        print(
                            f"   [X] {Fore.RED}Conta bloqueada %s{Fore.RESET}"
                            % (token[:59])
                        )
                        self.tokens.remove(token)
                    if response.status == 429:
                        print(
                            f"   [-] {Fore.YELLOW}Ratelimited %s{Fore.RESET}"
                            % (token[:59])
                        )
                        time.sleep(self.delay)
                        await self.login(token)
        except Exception:
            await self.login(token)

    async def join(self, token: str):
        try:
            headers = await self.headers(token)
            async with ClientSession(headers=headers) as client:
                async with client.post(
                    "https://discord.com/api/v9/invites/%s" % (self.invite), json={}
                ) as response:
                    json = await response.json()
                    if response.status == 200:
                        self.guild_name = json["guild"]["name"]
                        self.guild_id = json["guild"]["id"]
                        self.channel_id = json["channel"]["id"]
                        print(
                            f"   [L] {Fore.GREEN}Encontrei o servidor %s {Fore.RESET}"
                            % (self.guild_name[:20])
                        )
                    elif response.status == 401:
                        print(
                            f"   [X] {Fore.RED}Conta inválida %s{Fore.RESET}"
                            % (token[:59])
                        )
                        self.tokens.remove(token)
                    elif response.status == 403:
                        print(
                            f"   [X] {Fore.RED}Conta bloqueada %s{Fore.RESET}"
                            % (token[:59])
                        )
                        self.tokens.remove(token)
                    elif response.status == 429:
                        print(
                            f"   [-] {Fore.YELLOW}Ratelimited %s{Fore.RESET}"
                            % (token[:59])
                        )
                        time.sleep(self.delay)
                        self.tokens.remove(token)
                    else:
                        self.tokens.remove(token)
        except Exception:
            await self.join(token)

    async def create_dm(self, token: str, user: str):
        try:
            headers = await self.headers(token)
            async with ClientSession(headers=headers) as client:
                async with client.post(
                    "https://discord.com/api/v9/users/@me/channels",
                    json={"recipients": [user]},
                ) as response:
                    json = await response.json()
                    if response.status == 200:
                        print(
                            f"   [V] {Fore.GREEN}Enviando mensagem para{Fore.RESET} {Fore.MAGENTA}%s{Fore.RESET}"
                            % (json["recipients"][0]["username"])
                        )
                        return json["id"]
                    elif response.status == 401:
                        print(
                            f"   [X] {Fore.RED}Token invalido %s{Fore.RESET}"
                            % (token[:59])
                        )
                        self.tokens.remove(token)
                        return False
                    elif response.status == 403:
                        print(
                            f"   [X] {Fore.RED}Erro ao enviar mensagem para{Fore.RESET}{Fore.MAGENTA} %s{Fore.RESET}"
                            % (token[:59])
                        )
                        self.tokens.remove(token)
                    elif response.status == 429:
                        print(
                            f"   [-] {Fore.YELLOW}Ratelimited %s{Fore.RESET}"
                            % (token[:59])
                        )
                        time.sleep(self.delay)
                        return await self.create_dm(token, user)
                    else:
                        return False
        except Exception:
            return await self.create_dm(token, user)

    async def direct_message(self, token: str, channel: str):
        try:
            headers = await self.headers(token)
            async with ClientSession(headers=headers) as client:
                async with client.post(
                    "https://discord.com/api/v9/channels/%s/messages" % (channel),
                    json={"content": self.message, "nonce": self.nonce(), "tts": False},
                ) as response:
                    json = await response.json()
                    if response.status == 200:
                        print(
                            f"   [V] {Fore.GREEN}Mensagem enviada com sucesso{Fore.RESET}"
                        )
                    elif response.status == 401:
                        print(
                            f"   [X] {Fore.RED}Token invalido %s{Fore.RESET}"
                            % (token[:59])
                        )
                        self.tokens.remove(token)
                        return False
                    elif response.status == 403 and json["code"] == 40003:
                        print(
                            f"   [-] {Fore.YELLOW}Ratelimited %s{Fore.RESET}"
                            % (token[:59])
                        )
                        time.sleep(self.delay)
                        await self.direct_message(token, channel)
                    elif response.status == 403 and json["code"] == 50007:
                        print(
                            f"   [!] {Fore.RED}O usuário desativou as mensagens diretas{Fore.RESET}"
                            % (token[:59])
                        )
                    elif response.status == 403 and json["code"] == 40002:
                        print(
                            f"   [X] {Fore.RED}Bloqueado %s{Fore.RESET}" % (token[:59])
                        )
                        self.tokens.remove(token)
                        return False
                    elif response.status == 429:
                        print(
                            f"   [!] {Fore.YELLOW}Ratelimited %s{Fore.RESET}"
                            % (token[:59])
                        )
                        time.sleep(self.delay)
                        await self.direct_message(token, channel)
                    else:
                        return False
        except Exception:
            await self.direct_message(token, channel)

    async def send(self, token: str, user: str):
        channel = await self.create_dm(token, user)
        if channel == False:
            return await self.send(random.choice(self.tokens), user)
        response = await self.direct_message(token, channel)
        if response == False:
            return await self.send(random.choice(self.tokens), user)

    async def start(self):
        if len(self.tokens) == 0:
            print(f"   [!] {Fore.YELLOW}Nenhum token carregado.{Fore.RESET}")
            sys.exit()

        async with TaskPool(1_000) as pool:
            for token in self.tokens:
                if len(self.tokens) != 0:
                    await pool.put(self.login(token))
                else:
                    self.stop()

        if len(self.tokens) == 0:
            self.stop()

        print()
        print(f"   [L] {Fore.YELLOW}Entrando no servidor{Fore.RESET}")
        print()

        async with TaskPool(1_000) as pool:
            for token in self.tokens:
                if len(self.tokens) != 0:
                    await pool.put(self.join(token))
                    if self.delay != 0:
                        await asyncio.sleep(self.delay)
                else:
                    self.stop()

        if len(self.tokens) == 0:
            self.stop()

        scraper = Scraper(
            token=self.tokens[0], guild_id=self.guild_id, channel_id=self.channel_id
        )
        self.users = scraper.fetch()

        print("")
        print(
            f"   [!] {Fore.GREEN}Acabei de encontrar{Fore.RESET}{Fore.CYAN} %s {Fore.RESET}{Fore.GREEN}membros para enviar mensagem.{Fore.RESET}"
            % (len(self.users))
        )
        print(f"   [L] {Fore.GREEN}Enviando mensagens.{Fore.RESET}")
        print("")

        if len(self.tokens) == 0:
            self.stop()

        async with TaskPool(1_000) as pool:
            for user in self.users:
                if len(self.tokens) != 0:
                    await pool.put(self.send(random.choice(self.tokens), user))
                    if self.delay != 0:
                        await asyncio.sleep(self.delay)
                else:
                    self.stop()


if __name__ == "__main__":
    client = Discord()
    asyncio.get_event_loop().run_until_complete(client.start())