import kakaoTalkApi
import locoAgent
import locoPacket
import locoCrypto
import locoCheckin
import locoLoginListReq
import locoChatRes
import gevent
import json

class LocoClient:
    def __init__(self, device_name = "UMJUNSIK", device_uuid = "VU1KVU5TSUs="):
        self.device_name = device_name
        self.device_uuid = device_uuid
        self.kakaoTalkApi = kakaoTalkApi.KakaoTalkApi(device_name, device_uuid)
        self.locoAgent = locoAgent.LocoAgent(True, self.onPacket, {"MSG": [locoChatRes.LocoChatRes, self.onMessage]})
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
        self.locoAgent.connect(self.locoCheckinData["host"], self.locoCheckinData["port"])
        loginListReq = locoLoginListReq.LocoLoginListReq(self.device_uuid, self.accessKey)
        req = locoPacket.LocoRequest(loginListReq.Method(), loginListReq.toJsonBody())
        self.locoAgent.send_request(req)
        gevent.spawn(self.ping)
        gevent.event.Event().wait()
        
    def ping(self):
        while True:
            gevent.sleep(180)
            req = locoPacket.LocoRequest("PING", {})
            self.locoAgent.send_request(req)
            
    def onPacket(self, packet):
        pass

    def onMessage(self, packet):
        pass