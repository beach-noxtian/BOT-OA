from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests, json


import errno
import os
import sys, random
import tempfile

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent,
)

app = Flask(__name__)

# Channel Access Token
auth_Token = "0lcg3ZYOuhGxczmYWWZb+R7LXHeCQAIm21/yur8nvbJWq7HHQ+S/NmnnAtYT3P8g8+z3UBl8ok/Rj6/mdXmYXVjSIjnlQ2j/QjS8Zfe0JbJKbldrE+EcRA9Tw7AORtRq0XzJB3nvY40OfH+IfFOZPFGUYhWQfeY8sLGRXgo3xvw="
client = LineBotApi(auth_Token)
# Channel Secret
handler = WebhookHandler('266e5489fc2b7e93fe1c49a35654c016')
#===========[ NOTE SAVER ]=======================
notes = {}

# Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text #simplify for receove message
    sender = event.source.user_id #get user_id
    gid = event.source.sender_id #get group_id
#=====[ LEAVE GROUP OR ROOM ]==========[ ARSYBAI ]======================
    if text == 'bye':
        if isinstance(event.source, SourceGroup):
            client.reply_message(
                event.reply_token, TextSendMessage(text='Leaving group'))
            client.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            client.reply_message(
                event.reply_token, TextSendMessage(text='Leaving group'))
            client.leave_room(event.source.room_id)
        else:
            client.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't leave from 1:1 chat"))
    elif text == "kickpart":
        groupId = event.source.group_id
        contactIds = "ue76ba731fe83a3e5af23eaa458157d5c"
        client.kickoutFromGroup(0, groupId, contactIds)
    elif text == "/test":
        client.reply_message(sender, TextSendMessage(text="Test pass"))
#===================================================
    elif 'gambar' in text:
        separate = text.split(" ")
        search = text.replace(separate[0] + " ","")
        r = requests.get("http://rahandiapi.herokuapp.com/imageapi?key=betakey&q={}".format(search))
        data = r.text
        data = json.loads(data)

        if data["result"] != []:
            items = data["result"]
            path = random.choice(items)
            a = items.index(path)
            b = len(items)

        image_message = ImageSendMessage(
            original_content_url=path,
            preview_image_url=path
        )

        client.reply_message(
            event.reply_token,
            image_message
        )

#=======================================================================================================================
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
