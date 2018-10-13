#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @auther 牛润良
# 单个文件音频文件上传讯飞语音识别 iat
# 具体申请接口请查看https://www.xfyun.cn/
import base64
import hashlib
import json
import time

import requests

def main(file_address):
    f = open(file_address, 'rb')   
    file_content = f.read()
    base64_audio = base64.b64encode(file_content)
    body = {'audio': base64_audio}

    url = 'http://api.xfyun.cn/v1/service/v1/iat'
    api_key = 'bc3f4740f0b1b6567b75baab963e89d1'   # 如果出现ip错误，请将当前ip加入讯飞接口ip白名单中
    x_appid = '5b6a4117'                           # appid 讯飞接口权限码                      
    param = '{"engine_type":"sms16k","aue":"raw"}' #在此处修改识别类型 16K 8K

    x_param = base64.b64encode(param.encode())
    curTime = str(int(time.time()))
    w=api_key + curTime + x_param.decode()
    x_checksum = hashlib.md5(w.encode('utf-8')).hexdigest()
    x_header = {
            'X-Appid': x_appid,
            'X-CurTime':curTime,
            'X-Param': x_param,
            'X-CheckSum': x_checksum,
            'X-Client-IP':'210.47.7.163'
    }
    req = requests.post(url, data=body, headers=x_header)
    print (req.text.encode("ISO-8859-1").decode("utf-8"))

    result=json.loads(req.text)
    print(result)
    return

if __name__ == '__main__':
    file_address = "F:\\语音接口\\01.wav" #需要打开的文件与途径,上传该文件
    main(file_address)