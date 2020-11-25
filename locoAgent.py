import tcpClient
import locoCrypto
import locoPacket
import kakaoTalkApi
import struct
import gevent
from gevent.event import AsyncResult

class LocoAgent:
    def __init__(self, usesClient = False, onPacket = None):
        self.tcpClient = tcpClient.TcpClient()
        self.locoCrypto = locoCrypto.LocoCrypto()
        self.packet_processor = gevent.spawn(self._process_packet)
        self.packetHandler = {}
        self.currentpacketID = 0
        self.usesClient = usesClient
        self.onPacket = onPacket
        self.locoPacket = locoPacket
        self.kakaoTalkApi = kakaoTalkApi
        
        self.__processingBuffer = b""
        self.__processingHeader = b""
        self.__processingSize = 0
        
    def _process_packet(self):
        tcp = self.tcpClient
        encryptedPacket = b""

        while True:
            encryptedPacket = tcp.get_packet()
            iv = encryptedPacket[4:20]
            body = encryptedPacket[20:]

            self.__processingBuffer += self.locoCrypto.decrypt_aes(body, iv)
            
            if not self.__processingHeader and len(self.__processingBuffer) >= 22:
                self.__processingHeader = self.__processingBuffer[0:22]
                self.__processingSize = struct.unpack("<i", self.__processingHeader[18:22])[0] + 22

            if self.__processingHeader:
                if len(self.__processingBuffer) >= self.__processingSize:
                    packet = locoPacket.LocoPacket()
                    packet.readLocoPacket(self.__processingBuffer)
                    
                    if packet.packetID in self.packetHandler:
                        self.packetHandler[packet.packetID].set(packet)
                    if self.usesClient and self.onPacket:
                        gevent.spawn(self.onPacket, packet)

                    self.__processingBuffer = self.__processingBuffer[self.__processingSize:]
                    self.__processingHeader = b""

    def _next_packetID(self):
        packetID = self.currentpacketID
        self.currentpacketID += 1
        return packetID
    
    def connect(self, host, port):
        self.tcpClient.connect((host, port))
        self.handshake()
        
    def handshake(self):
        self.tcpClient.write(self.locoCrypto.getHandshakePacket())

    def send_request(self, request):
        packetID = self._next_packetID()
        packet = locoPacket.LocoPacket(packetID, 0, 0, request.method, request.body)
        self.packetHandler[packetID] = AsyncResult()
        self.tcpClient.write(packet.toEncryptedLocoPacket(self.locoCrypto))
        result = self.packetHandler[packetID].get()
        del self.packetHandler[packetID]
        return result
