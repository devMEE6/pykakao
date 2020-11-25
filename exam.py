import locoClient

class MyClass(locoClient.LocoClient):
    def onMessage(self, chat):
        if chat.message == "/안녕":
            print(chat.replyText("안녕").toJsonBody())

client = MyClass("", "")
client.login("", "")
