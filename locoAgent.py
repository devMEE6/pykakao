import tcpClient
import locoCrypto
import locoPacket
import struct
import gevent
from gevent.event import AsyncResult

class LocoAgent:
    def __init__(self, usesClient = False, onPacket = None, handler = None):
        self.tcpClient = tcpClient.TcpClient()
        self.locoCrypto = locoCrypto.LocoCrypto()
        self.packet_processor = gevent.spawn(self._process_packet)
        self.packetHandler = {}
        self.currentpacketID = 0
        self.usesClient = usesClient
        self.onPacket = onPacket
        self.handler = handler

        self.__processingBuffer = b""
        self.__processingHeader = b""
        self.__processingSize = 0
        
    def _process_packet(self):
        tcp = self.tcpClient
        buf = b""

        while True:
            buf += tcp.get_packet()
            packet = locoPacket.LocoPacket()
            packet.readEncryptedLocoPacket(buf, self.locoCrypto)
            buf = buf[struct.unpack(">I", buf[0:4])[0]+4:]

            if packet.packetID in self.packetHandler:
                self.packetHandler[packet.packetID].set(packet)
            if self.usesClient and self.onPacket:
                gevent.spawn(self.onPacket, packet)
            if self.handler and packet.method in self.handler:
                gevent.spawn(self.handler[packet.method][1], self.handler[packet.method][0](packet, self))
            
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
