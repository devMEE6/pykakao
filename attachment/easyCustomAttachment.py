import attachment.customAttachment as customAttachment
import json

class MessageInfo:
    def __init__(self, Type = "Feed", Url = "https://github.com/magenta1028/pykakao", FeedMessage = "Hello, World!"):
        self.Type = Type
        self.Url = Url
        self.FeedMessage = FeedMessage
        self.CustomInfo = customAttachment.CustomInfo(self.FeedMessage, self.Type, "plusfriend_bot", self.Url, "6.4.5", "6.4.5", "2.6.1", "2.3.5", None, None, None, None, False)

class FeedContent:
    def __init__(self, Text = "", Desc = ""):
        self.Text = Text
        self.Desc = Desc
        self.TextDesc = customAttachment.TextDescFragment(self.Text, self.Desc)
        self.Buttons = []
        self.Photos = []
        
class Button:
    def __init__(self, ButtonText = "", Url = ""):
        self.ButtonText = ButtonText
        self.Url = Url
        self.Button = customAttachment.ButtonFragment(ButtonText, "both", customAttachment.URLFragment(Url))

class Photo:
    def __init__(self, Url = "", Width = 0, Height = 0):
        self.Url = Url
        self.Width = Width
        self.Height = Height
        self.Photo = customAttahment.ImageFragment(self.Url, self.Width, self.Height)
        
class MessageTemplate:
    def __init__(self, MessageInfo, FeedContent):
        self.MessageInfo = MessageInfo
        self.FeedContent = FeedContent
        self.Attachment = customAttachment.CustomAttachment(MessageInfo.CustomInfo, customAttachment.CustomFeedContent(FeedContent.TextDesc, 0, FeedContent.Buttons, FeedContent.Photos))

    def getMessage(self):
        return self.MessageInfo.FeedMessage

    def getExtra(self):
        return json.dumps(self.Attachment.toJsonAttachment())

    def getType(self):
        return 71
