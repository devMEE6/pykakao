import time
import hashlib
import requests
import json

class LocoChannelRes:
    def __init__(self, packet, locoAgent):
        self.locoAgent = locoAgent
        self.kakaoTalkApi = self.locoAgent.kakaoTalkApi.KakaoTalkApi()
        self.rawBody = packet.toJsonBody()
        self.chatId = self.rawBody["chatId"]

        if "li" in self.rawBody:
            self.linkId = self.rawBody["li"]
        else:
            self.linkId = 0

    def sendChat(self, msg, extra, t):
        req = self.locoAgent.locoPacket.LocoRequest("WRITE", {
            "chatId": self.chatId,
            "extra": extra,
            "type": t,
            "msgId": time.time(),
            "msg": str(msg),
            "noSeen": False
        })
        return self.locoAgent.send_request(req)

    def sendForwardChat(self, msg, extra, t):
        req = self.locoAgent.locoPacket.LocoRequest("FORWARD", {
            "chatId": self.chatId,
            "extra": extra,
            "type": t,
            "msgId": time.time(),
            "msg": str(msg),
            "noSeen": False
        })
        return self.locoAgent.send_request(req)

    def sendPhoto(self, data, height, width, userId):
        path, key, url = self.kakaoTalkApi.upload(data, "image/jpeg", userId)
        return self.sendForwardChat("", json.dumps({
            "thumbnailUrl": url,
            "thumbnailHeight": height,
            "thumbnailWidth": width,
            "url": url,
            "k": key,
            "cs": hashlib.sha1(data).hexdigest().upper(),
            "s": len(data),
            "w": width,
            "h": height,
            "mt": "image/jpeg"
        }), 2)
    
    def sendPhotoUrl(self, url, height, width, userId):
        r = requests.get(url)
        r.raise_for_status()
        data = r.content
        
        return self.sendPhoto(data, height, width, userId)

    def sendPhotoPath(self, path, height, width, userId):
        f = open(path, "rb")
        data = f.read()
        f.close()
        
        return self.sendPhoto(data, height, width, userId)
