class TextDescFragment:
    def __init__(self, Text = "", Desc = ""):
        self.Text = Text
        self.Desc = Desc

    def toRawContent(self):
        obj = {"T": self.Text}
        if self.Desc:
            obj["D"] = self.Desc

        return obj
    
class URLFragment:
    def __init__(self, LinkWin = "", LinkMacOS = "", LinkAndroid = "", LinkIos = ""):
        self.LinkWin = LinkWin
        if not LinkMacOS:
            self.LinkMacOS = self.LinkWin
        else:
            self.LinkMacOS = LinkMacOS
        if not LinkAndroid:
            self.LinkAndroid = self.LinkWin
        else:
            self.LinkAndroid = LinkAndroid
        if not LinkIos:
            self.LinkIos = self.LinkWin
        else:
            self.LinkIos = LinkIos
        
    def toRawContent(self):
        obj = {}
        if self.LinkWin:
            obj["LPC"] = self.LinkWin
        if self.LinkMacOS:
            obj["LMO"] = self.LinkMacOS
        if self.LinkAndroid:
            obj["LCA"] = self.LinkAndroid
        if self.LinkIos:
            obj["LCI"] = self.LinkIos

        return obj

class ImageFragment:
    def __init__(self, Url = "", Width = 0, Height = 0, CropStyle = 1, IsLive = False, PlayTime = 0):
        self.Url = Url
        self.Width = Width
        self.Height = Height
        self.CropStyle = CropStyle
        self.IsLive = IsLive
        self.PlayTime = PlayTime

    def toRawContent(self):
        obj = {"THU": self.Url,
               "W": self.Width,
               "H": self.Height,
               "SC": self.CropStyle,
               "LI": self.IsLive,
               "PlayTime": self.PlayTime
               }

        return obj

class ButtonFragment:
    def __init__(self, Text = "", DisplayType = None, Link = None, Highlight = None):
        self.Text = Text
        self.DisplayType = DisplayType
        self.Link = Link
        self.Highlight = Highlight

    def toRawContent(self):
        obj = {"BU": {"T": self.Text}}
        if self.DisplayType:
            obj["BU"]["SR"] = self.DisplayType
        if self.Highlight:
            obj["BU"]["HL"] = self.Highlight
        if self.Link:
            obj["L"] = self.Link.toRawContent()

        return obj

class SocialFragment:
    def __init__(self, Like = 0, Comment = 0, Share = 0, View = 0, Subscriber = 0):
        self.Like = Like
        self.Comment = Comment
        self.Share = Share
        self.View = 0,
        self.Subscriber = 0

    def toRawContent(self):
        obj = {}
        if self.Like:
            obj["LK"] = self.Like
        if self.Comment:
            obj["CM"] = self.Comment
        if self.Share:
            obj["SH"] = self.Share
        if self.View:
            obj["VC"] = self.View
        if self.Subscriber:
            obj["SB"] = self.Subscriber

        return obj

class ProfileFragment:
    def __init__(self, TextDesc = TextDescFragment(), Link = None, Background = None, Thumbnail = None):
        self.TextDesc = TextDesc
        self.Link = Link
        self.Background = Background
        self.Thumbnail = Thumbnail

    def toRawContent(self):
        obj = {"TD": self.TextDsec.toRawContent()}
        if self.Link:
            obj["L"] = Link.toRawContent()
        if self.Background:
            obj["BG"] = self.Background.toRawContent()
        if self.Thumbnail:
            obj["TH"] = self.Thumbnail.toRawContent()

        return obj

class CustomFeedContent:
    def __init__(self, TextDesc = TextDescFragment(), ButtonStyle = 0, ButtonList = [], ThumbnailList = [], ExtraThumbCount = 0, TextLink = None, FullText = True, Link = None, Profile = None, Social = None):
        self.TextDesc = TextDesc
        self.ButtonStyle = ButtonStyle
        self.ButtonList = ButtonList
        self.ThumbnailList = ThumbnailList
        self.ExtraThumbCount = ExtraThumbCount
        self.TextLink = TextLink
        self.FullText = FullText
        self.Link = Link
        self.Profile = Profile
        self.Social = Social

    def toRawContent(self):
        textItem = {}
        textItem["TD"] = self.TextDesc.toRawContent()
        if self.TextLink:
            textItem["L"] = self.TextLink.toRawContent()
        if type(self.FullText) == bool:
            textItem["FT"] = self.FullText
        obj = {"TI": textItem,
               "BUT": self.ButtonStyle
               }
        if self.ExtraThumbCount:
            obj["THC"] = self.ExtraThumbCount
        thumbList = []
        for thumb in self.ThumbnailList:
            thumbList.append(thumb.toRawContent())
        obj["THL"] = thumbList
        buttonList = []
        for btn in self.ButtonList:
            buttonList.append(btn.toRawContent())
        obj["BUL"] = buttonList
        if self.Link:
            obj["L"] = self.Link.toRawContent()
        if self.Profile:
            obj["PR"] = self.Profile.toRawContent()
        if self.Social:
            obj["SO"] = self.Social.toRawContent()

        return obj

class CustomInfo:
    def __init__(self, Message = "", Type = "Feed", ServiceId = "", ProviderId = "", AndroidVersion = "", IosVersion = "", WinVersion = "", MacVersion = "", ServiceSettings = None, ServiceNickname = "", ServiceIcon = "", ServiceLink = URLFragment, Link = URLFragment, BigChat = True, Secure = False, KakaoVerified = False, CanForward = True, Ref = "", Ad = False):
        self.Message = Message
        self.Type = Type
        self.ServiceId = ServiceId
        self.ProviderId = ProviderId
        self.AndroidVersion = AndroidVersion
        self.IosVersion = IosVersion
        self.WinVersion = WinVersion
        self.MacVersion = MacVersion
        self.ServiceSettings = ServiceSettings
        self.ServiceNickname = ServiceNickname
        self.ServiceIcon = ServiceIcon
        self.ServiceLink = ServiceLink
        self.Link = Link
        self.BigChat = BigChat
        self.Secure = Secure
        self.KakaoVerified = KakaoVerified
        self.CanForward = CanForward
        self.Ref = Ref
        self.Ad = Ad

    def toRawContent(self):
        obj = {"ME": self.Message,
               "TP": self.Type,
               "SID": self.ServiceId,
               "DID": self.ProviderId,
               "VA": self.AndroidVersion,
               "VI": self.IosVersion,
               "VW": self.WinVersion,
               "VM": self.MacVersion
               }
        if self.ServiceSettings:
            obj["SST"] = self.ServiceSettings.toRawContent()
        if self.ServiceNickname:
            obj["SNM"] = self.ServiceNickname
        if self.ServiceIcon:
            obj["SIC"] = self.ServiceIcon
        if self.Secure:
            obj["LOCK"] = self.Secure
        if self.BigChat:
            obj["BC"] = self.BigChat
        if self.CanForward:
            obj["FW"] = self.CanForward
        if self.KakaoVerified:
            obj["KV"] = self.KakaoVerified
        if self.Ad:
            obj["AD"] = self.Ad
        if self.Ref:
            obj["RF"] = self.Ref
        if self.Link:
            obj["L"] = self.Link.toRawContent()
        if self.ServiceLink:
            obj["SL"] = self.ServiceLink.toRawContent()

        return obj
    
class CustomAttachment:
    def __init__(self, Info = CustomInfo(), Content = None, LinkInfo = None):
        self.Info = Info
        self.Content = Content
        self.LinkInfo = None

    def toJsonAttachment(self):
        obj = {"P": self.Info.toRawContent()}
        if self.Content:
            obj["C"] = self.Content.toRawContent()
        if self.LinkInfo:
            obj["K"] = self.LinkInfo.toRawContent()

        return obj
