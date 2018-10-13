#!/usr/bin/python
# -*- coding: UTF-8 -*-

import base64
import json
import os
import requests

# 具体申请接口请查看http://ai.baidu.com/docs#/Begin/top
client_id ='2X7C7Q0jbQQuGsURUQIlTo3H'                   # API Key
client_secret ='qnmPylZ7HjVjobcfRtCYrQwzznVmxeuS'       # Secret Key

def Switch(wav_Path,save_dir_Path,txt_name):

    f = open(wav_Path, 'rb')   
    speech = base64.b64encode(f.read()).decode('utf8')

    get_token_url = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials'+'&client_id='+client_id+'&client_secret='+client_secret
    # 鉴权认证机制获取 Access Token
    token = json.loads(requests.post(get_token_url).text)["access_token"]

    lens = os.path.getsize(wav_Path)
    headers = { 'Content-Type' : 'application/json'} 
    url = "https://vop.baidu.com/server_api"
    data={
        "format":"wav",
        "rate":"16000",
        "dev_pid":"1536",
        "cuid":"wate_play",
        "channel":1,
        "speech":speech,
        "len":lens,
        "token":token,
    }

    res = requests.post(url,json.dumps(data),headers)
    Result = json.loads(res.text)
    print(Result)
    if 'result' in Result.keys():
        result_str = "".join(Result['result'])
        # result_text = result_str.encode("ISO-8859-1").decode("utf-8")
        file_text = open(save_dir_Path + "/" + txt_name + ".txt","w",encoding='utf-8')
        file_text.write(result_str+"\n")
        file_text.close()

def main():
    dir_Path = r"F:\录音分割结果\录音数据备份\20180906"
    save_Path = r"F:\语音分割文本\录音数据备份\20180906"
    for root1, dirs1, files1 in os.walk(dir_Path):
        for name in dirs1:
            for root2, dirs2, files2 in os.walk(os.path.join(root1,name)):
                save_dir_Path = os.path.join(save_Path,name)
                if not os.path.exists(save_dir_Path):
                    os.mkdir(save_dir_Path)
                for file in files2:
                    # print(os.path.join(root2,file))
                    wav_Path = os.path.join(root2,file)
                    file_name = "".join(file.split("."))
                    try:
                        Switch(wav_Path,save_dir_Path,file_name)
                    except BaseException as s:
                        print('Error:',s)

if __name__ == '__main__':
    main() 
