import kakaoTalkApi
import locoAgent
import locoPacket
import locoCrypto
import locoCheckin
import packet.locoLoginList as locoLoginList
import talk.locoChatRes as locoChatRes
import talk.locoChannelRes as locoChannelRes
import gevent
import json

class LocoClient:
    def __init__(self, device_name = "UMJUNSIK", device_uuid = "VU1KVU5TSUs="):
        self.device_name = device_name
        self.device_uuid = device_uuid
        self.kakaoTalkApi = kakaoTalkApi.KakaoTalkApi(device_name, device_uuid)
        self.locoAgent = locoAgent.LocoAgent(True, self._onPacket)
        self.locoCrypto = locoCrypto.LocoCrypto()
        self.locoCheckinData = locoCheckin.LocoCheckin().getLocoCheckinData()
        
    def login(self, email, password):
        loginRes = json.loads(self.kakaoTalkApi.login(email, password))
        if loginRes["status"] == 0:
            self.accessKey = loginRes["access_token"]
            self.userId = loginRes["userId"]
            self.loginRes = loginRes
        else:
            print(loginRes)
            exit()
        self.locoAgent.connect(self.locoCheckinData["host"], self.locoCheckinData["port"])
        loginListReq = locoLoginList.LocoLoginListReq(self.device_uuid, self.accessKey)
        req = locoPacket.LocoRequest(loginListReq.Method(), loginListReq.toJsonBody())
        self.locoAgent.send_request(req)
        gevent.spawn(self.ping)
        gevent.event.Event().wait()
        
    def ping(self):
        while True:
            gevent.sleep(180)
            req = locoPacket.LocoRequest("PING", {})
            self.locoAgent.send_request(req)
            
    def _onPacket(self, packet):
        self.onPacket(packet)
        if packet.method == "MSG":
            channel = locoChannelRes.LocoChannelRes(packet, self.locoAgent)
            chat = locoChatRes.LocoChatRes(packet, channel)
            self.onMessage(chat)

        if packet.method == "DECUNREAD":
            channel = locoChannelRes.LocoChannelRes(packet, self.locoAgent)
            reader = channel.getUserInfo(packet.toJsonBody()["userId"])
            self.onMessageRead(channel, reader)

        if packet.method == "LOGINLIST":
            self.onReady()
            
    def onPacket(self, packet):
        pass

    def onMessage(self, chat):
        pass

    def onMessageRead(self, channel, reader):
        pass

    def onReady(self):
        pass
