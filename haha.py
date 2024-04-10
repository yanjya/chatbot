import os
from fastapi import FastAPI, Request
from linebot.v3.webhook import WebhookParser
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ReplyMessageRequest,
    PushMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)   
import line_response_genai as ai
import tea_link as tea
channel_secret = os.getenv('Line_Channel_Secret')
channel_access_token = os.getenv('LINE_Channel_Access_Token')


configuration = Configuration(
    access_token=channel_access_token
)

app = FastAPI()
async_api_client = AsyncApiClient(configuration)
line_bot_api = AsyncMessagingApi(async_api_client)
parser = WebhookParser(channel_secret)



@app.post("/webhooks/line")
async def handle_callback(request: Request):
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = await request.body()
    body = body.decode()

    events = parser.parse(body, signature)


    for event in events:
        print(event)
        if event.message.text == '薰薰':
            await line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text= 'good day, 有什麼心事都可以跟我分享❤️',quoteToken=event.message.quote_token)]
                )
            )
        if event.message.text == '你還健在嗎':
            await line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text= '洗勒靠邀喔，幹拎九喇錒',quoteToken=event.message.quote_token)]
                )
            )
        if event.message.text[0] == '#':
            text=ai.get_answer(str(event.message.text))
            print('response message: ',text)
            product_link = tea.check_tea_link(text)
            await line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=text,quoteToken=event.message.quote_token)]
                )
            )

    return 'OK'

