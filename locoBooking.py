import kakaoTalkApi
import locoPacket
import ssl
import socket

class LocoBooking:
    def __init__(self):
        self.kakaoTalkApi = kakaoTalkApi.KakaoTalkApi()
        
    def getLocoBookingData(self):
        req = {
            "MCCMNC": "999",
            "os": self.kakaoTalkApi.agent,
            "model": ""
        }
        context = ssl.create_default_context()

        with socket.create_connection(("booking-loco.kakao.com", 443)) as sock:
            with context.wrap_socket(sock, server_hostname = "booking-loco.kakao.com") as ssock:
                packet = locoPacket.LocoPacket(1, 0, 0, "GETCONF", req)
                ssock.write(packet.toLocoPacket())
                data = ssock.recv(4096)
                recvPacket = locoPacket.LocoPacket()
                recvPacket.readLocoPacket(data)
                return recvPacket
