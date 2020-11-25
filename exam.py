import locoClient
import attachment.easyCustomAttachment as easyCustomAttachment

class MyClass(locoClient.LocoClient):
    def onMessage(self, chat):
        if chat.message == "/안녕":
            chat.replyText("안녕")

        if chat.message == "/사진테스트":
            chat.replyPhotoUrl("https://i.ytimg.com/vi/mlVKclBXAOY/hqdefault.jpg", 100, 100)

        if chat.message == "/카링테스트":
            MessageInfo = easyCustomAttachment.MessageInfo()
            Content = easyCustomAttachment.FeedContent("안뇽", "테스트얌")
            Content.Buttons.append(easyCustomAttachment.Button("히히", "https://naver.com").Button)
            chat.replyTemplate(easyCustomAttachment.MessageTemplate(MessageInfo, Content))
            
    def onPacket(self, packet):
        print(packet.method)
        print(packet.toJsonBody())
        print("\n")
        
client = MyClass("", "")
client.login("", "")
