import json
import locoPacket
import time

class LocoChatRes:
    def __init__(self, packet, channel):
        self.rawBody = packet.toJsonBody()
        self.channel = channel
        self.logId = self.rawBody["chatLog"]["logId"]
        self.type = self.rawBody["chatLog"]["type"]
        self.message = self.rawBody["chatLog"]["message"]
        self.msgId = self.rawBody["chatLog"]["msgId"]
        self.authorId = self.rawBody["chatLog"]["authorId"]
        
        try:
            if "attachment" in self.rawBody["chatLog"]:
                self.attachment = json.loads(self.rawBody["chatLog"]["attachment"])
            else:
                self.attachment = {}
        except:
            pass

        self.nickName = self.rawBody["authorNickname"]

    def replyChat(self, msg, extra, t):
        return self.channel.sendChat(msg, extra, t)

    def replyForwardChat(self, msg, extra, t):
        return self.channel.sendForwardChat(msg, extra, t)
    
    def replyText(self, msg):
        return self.replyChat(msg, '{}', 1)
    
    def replyPhoto(self, data, height, width):
        return self.channel.sendPhoto(data, height, width, self.authorId)
    
    def replyPhotoUrl(self, url, height, width):
        return self.channel.sendPhotoUrl(url, height, width, self.authorId)

    def replyPhotoPath(self, path, height, width):
        return self.channel.sendPhotoPath(path, height, width, self.authorId)

    def replyTemplate(self, template):
        return self.replyChat(template.getMessage(), template.getExtra(), template.getType())

    def delete(self):
        return self.channel.deleteMessage(self.logId)

    def hide(self):
        return self.channel.hideMessage(self.logId, self.type)
