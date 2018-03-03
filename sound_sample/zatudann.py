import os
import requests
import pyaudio
import sys
import time
import wave
import json 
#device IDなどは関数で設定しないようにしていることに注意
def talk(message='こんにちは'):
#    os.system('/home/pi/nakayama/aquestalkpi/AquesTalkPi '+message + ' | aplay -Dhw:0,0')
    os.system('/home/pi/say '+message)
if __name__ == '__main__':
    chunk = 512
    chunk = 1024
    chunk = 2048
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
#    CHANNELS = 2
    #サンプリングレート、マイク性能に依存
    RATE =16000
#    RATE = 44100
    #録音時間
    RECORD_SECONDS = 3
     
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
    for i in range(0,int(RATE / chunk * RECORD_SECONDS)):
        data = stream.read(chunk)
        all.append(data)

    stream.close()
    data = b''.join(all)
    out = wave.open('mono.wav','w')
    out.setnchannels(CHANNELS) #mono
    out.setsampwidth(2) #16bits
    out.setframerate(RATE)
    out.writeframes(data)
    out.close()

    p.terminate()

path = "/home/pi/nakayama/aquestalkpi/mono.wav"
url = "https://api.apigw.smt.docomo.ne.jp/amiVoice/v1/recognize?APIKEY={}".format("395259795a76514538336a594b6d69423147646a376b32566f526b4632663632386e465876397856586336")
files = {"a": open(path, 'rb'), "v":"on"}
r = requests.post(url, files=files)
message = r.json()['text']
#しゃべった内容
print(message)

if "流星" in message or "流れ星" in message:
    print('start dust word process end')
# output file
    ff = open('./word.txt','w')
    ff.write(message + '\n')
    ff.close()
    sys.exit()


#以下雑談APIに出力されたテキストを渡す
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
talk(talk_message)
