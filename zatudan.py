#雑談プログラム
import os
import requests
import pyaudio
import sys
import time
import wave
import json 

#音声合成処理関数。AquesTalkに処理を渡す。
#device IDやサウンドカードIDは毎回確認する必要あり
def talk(message='こんにちは'):
    os.system('/home/pi/aquestalkpi/AquesTalkPi '+message + ' | aplay -Dhw:1,0')

#main処理
#録音処理。音声レートがマイク性能に依存しているが、pulseaudioを利用して16000Hzでも問題ないようにした
if __name__ == '__main__':
    chunk = 512
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    #サンプリングレート、マイク性能に依存
    RATE =16000
    #録音時間
    RECORD_SECONDS = 5
     
    #pyaudio
    p = pyaudio.PyAudio()
    #マイク0番を設定
    input_device_index = 0
    #マイクからデータ取得
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = chunk)
    all = []
    for i in range(0,int(RATE / chunk * 5)):
        data = stream.read(chunk)
        all.append(data)

    stream.close()
    data = b''.join(all)
    out = wave.open('mono.wav','w')
    out.setnchannels(1) #mono
    out.setsampwidth(2) #16bits
    out.setframerate(RATE)
    out.writeframes(data)
    out.close()

    p.terminate()

#録音した音声をテキストに変換処理
path = "/home/pi/aquestalkpi/mono.wav"
url = "https://api.apigw.smt.docomo.ne.jp/amiVoice/v1/recognize?APIKEY={}".format("395259795a76514538336a594b6d69423147646a376b32566f526b4632663632386e465876397856586336")
files = {"a": open(path, 'rb'), "v":"on"}
r = requests.post(url, files=files)
message = r.json()['text']

#変換後のテキストを一応出力
print(message)


#雑談APIにテキストを渡す
url = "https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue?APIKEY={}".format("395259795a76514538336a594b6d69423147646a376b32566f526b4632663632386e465876397856586336")
payload = {
  "utt": message,
  "context": "",
  "nickname": "光",
  "nickname_y": "ヒカリ",
  "sex": "女",
  "bloodtype": "B",
  "birthdateY": "1997",
  "birthdateM": "5",
  "birthdateD": "30",
  "age": "16",
  "constellations": "双子座",
  "place": "東京",
  "mode": "dialog",
}
r = requests.post(url, data=json.dumps(payload))
print (r.json()['utt'])
talk_message=r.json()['utt']

#音声合成処理に雑談APIが出力したテキストを渡す
talk(talk_message)
