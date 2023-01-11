from os import system , mkdir
from os.path import isdir
from random import randint
import cv2
import base64

try:
    from requests import Session
except ModuleNotFoundError:
    system("pip install requests")
    from requests import Session
try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    system("pip install bs4")
    from bs4 import BeautifulSoup
try:
    from anticaptchaofficial.imagecaptcha import *
except ModuleNotFoundError:
    system("pip3 install anticaptchaofficial")
    from anticaptchaofficial.imagecaptcha import *

class Charge:
    def __init__(self , apikey=None , proxy=None):
        self.session = Session()
        self.key = apikey
        self.solver = imagecaptcha()
        self.proxy = {"http" : proxy , "https" : proxy}
    def makecharge(self , code , count):
        self.data = {
                "card" : str(code),
                "quantity" : str(count),
                "email" : "mrnull@gmail.com",
                "phoneNumber" : "09051142536",
                "selectedBankId" : "2",
                "gateway" : "21",
            }
        self.resp = self.session.post("http://www.mihancharge.com/pay" , json=self.data , proxies=self.proxy, timeout=10).content
        self.parser = BeautifulSoup(self.resp , "html.parser")
        return self.parser.find_all("input")[1].get("value") 
    def getcapcha(self , refid):
        self.resp = self.session.get(f"https://bpm.shaparak.ir/pgwchannel/captchaimg.jpg?RefId={refid}&r={randint(00000, 99999)}" , proxies=self.proxy , timeout=10).content
        with open(f"captcha.jpg" , "wb") as f:
            f.write(self.resp)
            f.close()
        self.solver.set_verbose(1)
        self.solver.set_key(self.key)
        return self.solver.solve_and_return_solution(file_path=f"captcha.jpg")
    def getcapcha2(self , refid):
        self.resp = self.session.get(f"https://bpm.shaparak.ir/pgwchannel/captchaimg.jpg?RefId={refid}&r={randint(00000, 99999)}" , proxies=self.proxy , timeout=10).content
        with open(f"captcha.jpg" , "wb") as f:
            f.write(self.resp)
            f.close()
    def sendotp(self , refid , pan , capcha):
        self.headers = {
                'Accept':'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language':'en-US,en;q=0.9',
                'Connection':'keep-alive',
                'Content-Type':'application/json',
                'Host':'bpm.shaparak.ir',
                'Origin':'https://bpm.shaparak.ir',
                'Referer':f'https://bpm.shaparak.ir/pgwchannel/payment.mellat?RefId={refid}',
                'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
                'sec-ch-ua-mobile':'?0',
                'sec-ch-ua-platform':'"Windows"',
                'Sec-Fetch-Dest':'empty',
                'Sec-Fetch-Mode':'cors',
                'Sec-Fetch-Site':'same-origin',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
                'X-Requested-With':'XMLHttpRequest',
            }
            
        return self.session.post(f"https://bpm.shaparak.ir/pgwchannel/otp-request.mellat?RefId={refid}" , headers=self.headers , json={"pan" : str(pan) , "selectedPanIndex":-1 , "captcha":str(capcha)} , proxies=self.proxy , timeout=10).json()
    def pay(self , refid , pan , cvv2 , y , m , pin , capcha):
        self.url = f"https://bpm.shaparak.ir/pgwchannel/sale.mellat?RefId={refid}"
        self.headers = {
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.9',
            'Connection':'keep-alive',
            'Content-Type':'application/json',
            'Host':'bpm.shaparak.ir',
            'Origin':'https://bpm.shaparak.ir',
            'Referer':f'https://bpm.shaparak.ir/pgwchannel/payment.mellat?RefId={refid}',
            'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'"Windows"',
            'Sec-Fetch-Dest':'empty',
            'Sec-Fetch-Mode':'cors',
            'Sec-Fetch-Site':'same-origin',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
        }
            
        self.data = {
            "pan" : str(pan),
            "selectedPanIndex" : "-1",
            "pin": str(pin),
            "cvv2": str(cvv2),
            "expireMonth" : str(m),
            "expireYear":str(y),
            "captcha":str(capcha),
            "payerId" : "null",
            "email":"",
            "savePan":"false",
        }

        self.resp1 = self.session.post(self.url , headers=self.headers , json=self.data , proxies=self.proxy , timeout=10)
        if self.resp1.json()["status"] == "OK":
            self.headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Cache-Control": "max-age=0",
                    "Connection": "keep-alive",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Host": "bpm.shaparak.ir",
                    "Origin": "https://bpm.shaparak.ir",
                    "Referer": "https://bpm.shaparak.ir/pgwchannel/payment.mellat?RefId={}".format(refid),
                    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": "Windows",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-User": "?1",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36",
                }
            self.resp2 = self.session.post(f"https://bpm.shaparak.ir/pgwchannel/result.mellat?RefId={refid}" , headers = self.headers , cookies=self.resp1.cookies.get_dict() , proxies=self.proxy)
            self.parser = BeautifulSoup(self.resp2.content , "html.parser")
            self.refid = refid
            self.ResCode = self.parser.find_all("input")[1].get("value")
            self.SaleOrderId = self.parser.find_all("input")[2].get("value")
            self.SaleReferenceId = self.parser.find_all("input")[3].get("value")
            self.CardHolderInfo = self.parser.find_all("input")[4].get("value")
            self.CardHolderPan = self.parser.find_all("input")[5].get("value")
            self.FinalAmount = self.parser.find_all("input")[6].get("value")
            self.url = "http://www.mihancharge.com/PaymentHandler/Mellat.aspx"
            self.data = {
                    "RefId" : self.refid,            
                    "ResCode" : self.ResCode,
                    "SaleOrderId" : self.SaleOrderId,
                    "SaleReferenceId" : self.SaleReferenceId,
                    "CardHolderInfo" : self.CardHolderInfo,
                    "CardHolderPan" : self.CardHolderPan,
                    "FinalAmount" : self.FinalAmount,
                }
            self.headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Cache-Control": "max-age=0",
                    "Connection": "keep-alive",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Host": "www.mihancharge.com",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36",
                    }
            self.resp3 = self.session.post(self.url , headers=self.headers , data=self.data , allow_redirects=True , proxies=self.proxy , timeout=10)
            self.parser = BeautifulSoup(self.resp3.content , "html.parser")
            self.allcodes = self.parser.find_all(class_="chargeCode")
            self.codes = []
            for i in range(0 , len(self.allcodes)):
                temp = ""
                parser = BeautifulSoup(str(self.allcodes[i]) , "html.parser")
                for j in range(0 , 4):
                    temp = temp + str(parser.find_all("span")[j]).split('<span style="margin-left: 2px;">')[1].split("</span>")[0].split("\r\n")[1].split()[0] + "-"
                self.codes.append(str(temp))
            self.serials = []
            self.allserials = self.parser.find_all(class_="serial")
            for i in range(0 , len(self.allserials)):
                self.serials.append(str(str(self.allserials[i]).split('<td class="serial">')[1].split("</td>")[0].split("\r\n")[1].split()[0]))
            self.allamounts = self.parser.find_all(class_="chargeAmount")
            self.amounts = []
            for i in range(0 , len(self.allamounts)):
                self.amounts.append(str(str(self.allamounts[i]).split('<td class="chargeAmount">')[1].split("</td>")[0].split("\r\n")[1].split()[0]))
            self.alltypes = self.parser.find_all(class_="cardType")
            self.types = []
            for i in range(0 , len(self.alltypes)):
                self.types.append(str(str(self.alltypes[i]).split('<td class="cardType">')[1].split("</td>")[0].split("\r\n")[1].split()[2]))
            
            return {"status" : "ok" , "description" : "transaction success" , "charges" : {"codes" : self.codes , "types" : self.types , "amounts" : self.amounts , "serials" : self.serials}}
        else:
            return self.resp1.json()


        