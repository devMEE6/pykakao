from gevent import socket
import struct
from gevent.pool import Group
from gevent.queue import Queue

class TcpClient:
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._group = Group()
        self._send_buffer = Queue()
        self._recv_buffer = Queue()
        
    def connect(self, address):
        self._socket.connect(address)
        self._group.spawn(self._send_loop)
        self._group.spawn(self._recv_loop)

    def disconnect(self):
        self._group.kill()
        self._socket.close()
        self._group.join()

    def _recv_loop(self):
        encryptedBuffer = b""
        currentPacketSize = 0

        while True:
            recv = self._socket.recv(256)

            encryptedBuffer += recv

            if not currentPacketSize and len(encryptedBuffer) >= 4:
                currentPacketSize = struct.unpack("<I", encryptedBuffer[0:4])[0]
                
            if currentPacketSize:
                encryptedPacketSize = currentPacketSize+4
                
                if len(encryptedBuffer) >= encryptedPacketSize:
                    self._recv_buffer.put(encryptedBuffer[0:encryptedPacketSize])
                    encryptedBuffer = encryptedBuffer[encryptedPacketSize:]
                    currentPacketSize = 0

                    
    def _send_loop(self):
        while True:
            data = self._send_buffer.get()
            self._socket.sendall(data)

    def write(self, data):
        self._send_buffer.put(data)

    def get_packet(self):
        return self._recv_buffer.get()
