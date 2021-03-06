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
            self.li = self.rawBody["li"]
        else:
            self.li = 0

    def sendChat(self, msg, extra, t):
        req = self.locoAgent.locoPacket.LocoRequest("WRITE", {
            "chatId": self.chatId,
            "extra": extra,
            "type": t,
            "msgId": time.time(),
            "msg": str(msg),
            "noSeen": False
        })
        return self.locoAgent.send_request(req).toJsonBody()

    def sendForwardChat(self, msg, extra, t):
        req = self.locoAgent.locoPacket.LocoRequest("FORWARD", {
            "chatId": self.chatId,
            "extra": extra,
            "type": t,
            "msgId": time.time(),
            "msg": str(msg),
            "noSeen": False
        })
        return self.locoAgent.send_request(req).toJsonBody()

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

    def sendReply(self, logId, message, tt, authorId, msg, t=1):
        return self.sendChat(msg, json.dumps({
            "attach_only": False,
            "attach_type": t,
            "mentions": [],
            "src_linkId": self.li,
            "src_logId": logId,
            "src_mentions": [],
            "src_message": message,
            "src_type": tt,
            "src_userId": authorId
        }), 26)

    def sendLongText(self, title, content, userId):
        path, key, url = self.kakaoTalkApi.upload(content.encode("utf-8"), "image/jpeg", userId)
        return self.sendForwardChat(title, json.dumps({
            "path": path,
            "k": key,
            "s": len(content),
            "cs": "",
            "sd": True
        }), 1)

    def getUserInfo(self, userId):
        req = self.locoAgent.locoPacket.LocoRequest("MEMBER", {
            "chatId": self.chatId,
            "memberIds": [userId]
        })
        return self.locoAgent.send_request(req).toJsonBody()

    def getChatInfo(self):
        req = self.locoAgent.locoPacket.LocoRequest("CHATINFO", {
            "chatId": self.chatId
        })
        return self.locoAgent.send_request(req).toJsonBody()

    def getLinkInfo(self):
        req = self.locoAgent.locoPacket.LocoRequest("INFOLINK", {
            "lis": [self.li]
        })
        return self.locoAgent.send_request(req).toJsonBody()

    def setMeta(self, t, content):
        req = self.locoAgent.locoPacket.LocoRequest("SETMETA", {
            "chatId": self.chatId,
            "type": t,
            "content": content
        })
        return self.locoAgent.send_request(req).toJsonBody()

    def kickMember(self, userId):
        if self.li:
            req = self.locoAgent.locoPacket.LocoRequest("KICKMEM", {
                "li": self.li,
                "c": self.chatId,
                "mid": userId
            })
            return self.locoAgent.send_request(req).toJsonBody()

    def hideMessage(self, logId, t):
        if self.li:
            req = self.locoAgent.locoPacket.LocoRequest("REWRITE", {
                "c": self.chatId,
                "li": self.li,
                "logId": logId,
                "t": t
            })
            return self.locoAgent.send_request(req).toJsonBody()

    def deleteMessage(self, logId):
        req = self.locoAgent.locoPacket.LocoRequest("DELETEMSG", {
            "chatId": self.chatId,
            "logId": logId
        })
        return self.locoAgent.send_request(req).toJsonBody()

    def getChatLogs(self, sincelogId):
        req = self.locoAgent.locoPacket.LocoRequest("MCHATLOGS", {
            "chatIds": [self.chatId],
            "sinces": [sincelogId]
        })
        return self.locoAgent.send_request(req).toJsonBody()
