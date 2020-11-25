import json
import locoPacket
import time

class LocoChatRes:
    def __init__(self, packet, locoAgent):
        self.rawBody = packet.toJsonBody()
        self.logId = self.rawBody["chatLog"]["logId"]
        self.type = self.rawBody["chatLog"]["type"]
        self.message = self.rawBody["chatLog"]["message"]
        self.msgId = self.rawBody["chatLog"]["msgId"]
        self.authorId = self.rawBody["chatLog"]["authorId"]
        self.chatId = self.rawBody["chatLog"]["chatId"]
        self.locoAgent = locoAgent
        
        try:
            if "attachment" in self.rawBody["chatLog"]:
                self.attachment = json.loads(self.rawBody["chatLog"]["attachment"])
            else:
                self.attachment = {}
        except:
            pass

        self.nickName = self.rawBody["authorNickname"]

    def replyChat(self, msg, extra, t):
        req = locoPacket.LocoRequest("WRITE", {
            "chatId": self.chatId,
            "extra": extra,
            "type": t,
            "msgId": time.time(),
            "msg": str(msg),
            "noSeen": False
        })
        return self.locoAgent.send_request(req)

    def replyText(self, msg):
        return self.replyChat(msg, '{}', 1)
