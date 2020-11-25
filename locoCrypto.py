from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA1
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import construct
from Crypto.Signature import pss

import os
import io
import struct

class LocoCrypto:
    def __init__(self):
        self.aesKey = os.urandom(16)
        
    def encrypt_aes(self, data, iv):
        aesChiper = AES.new(self.aesKey, AES.MODE_CFB, iv, segment_size=128)
        return aesChiper.encrypt(data)

    def decrypt_aes(self, data, iv):
        aesChiper = AES.new(self.aesKey, AES.MODE_CFB, iv, segment_size=128)
        return aesChiper.decrypt(data)

    def encrypt_rsa(self, data):
        n = int("A44960441C7E83BB27898156ECB13C8AFAF05D284A4D1155F255CD22D3176CDE50482F2F27F71348E4D2EB5F57BF9671EF15C9224E042B1B567AC1066E06691143F6C50F88787F68CF42716B210CBEF0F59D53405A0A56138A6872212802BB0AEEA6376305DBD428831E8F61A232EFEDD8DBA377305EF972321E1352B5F64630993E5549C64FCB563CDC97DA2124B925DDEA12ADFD00138910F66937FAB68486AE43BFE203C4A617F9F232B5458A9AB409BAC8EDADEF685545F9B013986747737B3FD76A9BAC121516226981EA67225577D15D0F082B8207EAF7CDCB13123937CB12145837648C2F3A65018162315E77EAD2D2DD5986E46251764A43B9BA8F79", 16)
        e = int("3", 16)
        rsaKey = construct((n, e))
        
        rsaChiper = PKCS1_OAEP.new(key=rsaKey, hashAlgo=SHA1, mgfunc=lambda x, y: pss.MGF1(x, y, SHA1))
        return rsaChiper.encrypt(data)

    def getHandshakePacket(self):
        f = io.BytesIO()

        key = self.encrypt_rsa(self.aesKey)
        f.write(struct.pack("<I", len(key)))
        f.write(struct.pack("<I", 12))
        f.write(struct.pack("<I", 2))
        f.write(key)

        return f.getvalue()
