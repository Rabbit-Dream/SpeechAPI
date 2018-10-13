#!/usr/bin/env python
# coding=utf-8

import websocket
from websocket import ABNF
import json
import ssl
import uuid
# 具体申请接口请查看https://www.dui.ai/docs/ct_introduction
appid = '278574336' #填入产品Id
apikey = 'c59fb698738c4cd9af1238ce5241fc96' #填入apikey
url = 'ws://asr.dui.ai/runtime/v2/recognize?productId='+appid+'&apikey='+apikey
file_address = 'E:\\Users\\10178\\Desktop\\test\\01.wav' #wav文件的绝对路径

def on_message(ws, message):
    print(message)
    ws.close()

def on_open(ws):
    content={
    "context":{"productId":appid,"userId":"x","deviceName":"x","sdkName":"x"},
    "request":{"requestId":"x","audio":{"audioType":"wav","sampleRate":16000,"channel":1,"sampleBytes":2},"asr":{"enableVAD":True}}
    } 
    ws.send(json.dumps(content))
    with open(file_address, 'rb') as f:
        while True:
            data = f.read(3200)        #如果audioType是wav，此处需要修改为3200
            if data:
                ws.send(data, ABNF.OPCODE_BINARY)
            if len(data) < 3200:        #如果audioType是wav，此处需要修改为3200
                break
    ws.send('', ABNF.OPCODE_BINARY)

if __name__ == "__main__":
    ws = websocket.WebSocketApp(url,on_open = on_open,on_message = on_message)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})