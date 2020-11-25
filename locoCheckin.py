import locoAgent
import locoBooking
import locoPacket
import kakaoTalkApi

class LocoCheckin:
    def __init__(self):
        self.locoBookingData = locoBooking.LocoBooking().getLocoBookingData().toJsonBody()
        self.locoAgent = locoAgent.LocoAgent()
        self.kakaoTalkApi = kakaoTalkApi.KakaoTalkApi()
        
    def getLocoCheckinData(self):
        self.locoAgent.connect(self.locoBookingData["ticket"]["lsl"][0], self.locoBookingData["wifi"]["ports"][0])
        req = {
            "userId": 0,
            "os": self.kakaoTalkApi.agent,
            "ntype": 0,
            "appVer": self.kakaoTalkApi.version,
            "MCCMNC": "999",
            "lang": self.kakaoTalkApi.lang
        }
        req = locoPacket.LocoRequest("CHECKIN", req)
        res = self.locoAgent.send_request(req)
        return res.toJsonBody()
