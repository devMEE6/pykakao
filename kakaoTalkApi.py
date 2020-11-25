import requests
import hashlib

class KakaoTalkApi:
    def __init__(self, device_name = "UMJUNSIK", device_uuid = "VU1KVU5TSUs="):
        self.device_name = device_name
        self.device_uuid = device_uuid
        
        self.version = "3.1.7"
        self.lang = "ko"
        self.osVersion = "10.0"
        self.agent = "win32"

        self.authUserAgent = f"KT/{self.version} Wd/{self.osVersion} {self.lang}"
        self.authHeader = f"{self.agent}/{self.version}/{self.lang}"
        
    def login(self, email, password):
        r = requests.post("https://ac-sb-talk.kakao.com/win32/account/login.json", headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "A": self.authHeader,
            "X-VC": self.getXVC(email),
            "User-Agent": self.authUserAgent,
            "Accept": "*/*",
            "Accept-Language": self.lang
        }, data={
            "email": email,
            "password": password,
            "device_name": self.device_name,
            "device_uuid": self.device_uuid,
            "os_version": self.osVersion,
            "permanent": True,
            "forced": True
        })

        return r.content.decode()

    def upload(self, data, dataType, userId):
        r = requests.post("https://up-m.talk.kakao.com/upload", headers={
            "A": self.authHeader,
        }, data={
            "attachment_type": dataType,
            "user_id": userId,
        }, files={
            'attachment': data,
        })
        path = r.content.decode()
        key = path.replace('/talkm', "")
        url = f"https://dn-m.talk.kakao.com{path}"
        return path, key, url

    def getXVC(self, email, isFull=False):
        xvc = hashlib.sha512(f"HEATH|{self.authUserAgent}|DEMIAN|{email}|{self.device_uuid}".encode("utf-8")).hexdigest()
        if(isFull):
            return xvc
        return xvc[0:16]
