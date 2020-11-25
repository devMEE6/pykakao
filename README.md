# pykakao
복사 붙여넣기의 결과물

# simple Bot
```python
import locoClient
import requests
from bs4 import BeautifulSoup

class MyClass(locoClient.LocoClient):
    def onReady(self):
        print("BOT START!")
    
    def onMessage(self, chat):
        if chat.message == "/코로나":
            html = requests.get("http://ncov.mohw.go.kr/").content
            soup = BeautifulSoup(html, "html.parser")
            a = soup.select("body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div.liveNum > ul > li:nth-child(1) > span.num")[0].text.split("(누적)")[1]
            b = soup.select("body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div.liveNum > ul > li:nth-child(2) > span.num")[0].text
            c = soup.select("body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div.liveNum > ul > li:nth-child(3) > span.num")[0].text
            d = soup.select("body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div.liveNum > ul > li:nth-child(4) > span.num")[0].text
            chat.replyText(f"누적 확진자: {a}\n격리해제: {b}\n격리중: {c}\n사망: {d}")
        
client = MyClass("deviceName", "deviceUUID")
client.login("emaail or phone number", "password")
```
