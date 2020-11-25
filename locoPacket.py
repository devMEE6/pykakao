from bson import BSON as bson
import os
import io
import struct

class LocoPacket:
    def __init__(self, packetID = 0, status = 0, bodyType = 0, method = "", body = {}):
        self.packetID = packetID
        self.status = status
        self.bodyType = bodyType
        self.method = method
        self.body = bson.encode(body)
        self.bodyLength = len(self.body)

    def toLocoPacket(self):
        f = io.BytesIO()
        f.write(struct.pack("<I", self.packetID))
        f.write(struct.pack("<H", self.status))
        f.write(self.method.encode("utf-8"))
        f.write(b"\x00"*(11-len(self.method)))
        f.write(struct.pack("<b", self.bodyType))
        f.write(struct.pack("<i", self.bodyLength))
        f.write(self.body)
        
        return f.getvalue()

    def readLocoPacket(self, packet):
        self.packetID = struct.unpack("<I", packet[:4])[0]
        self.status = struct.unpack("<H", packet[4:6])[0]
        self.method = packet[6:17].decode().replace("\0", "")
        self.bodyType = struct.unpack("<b", packet[17:18])[0]
        self.bodyLength = struct.unpack("<i", packet[18:22])[0]
        self.body = packet[22:]

    def toEncryptedLocoPacket(self, crypto):
        iv = os.urandom(16)
        encrypted_packet = crypto.encrypt_aes(self.toLocoPacket(), iv)
        f = io.BytesIO()
        f.write(struct.pack("<I", len(encrypted_packet)+len(iv)))
        f.write(iv)
        f.write(encrypted_packet)

        return f.getvalue()

    def readEncryptedLocoPacket(self, packet, crypto):
        packetLen = struct.unpack(">I", packet[0:4])[0]
        iv = packet[4:20]
        data = packet[20:packetLen-16]
        dec = crypto.decrypt_aes(data, iv)

        try:
            self.readLocoPacket(dec)
        except Exception as e:
            print(str(e))

    def toJsonBody(self):
        return bson.decode(self.body)

class LocoRequest:
    def __init__(self, method = "", body = {}):
        self.method = method
        self.body = body
