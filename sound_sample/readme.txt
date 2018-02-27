プログラム本体
sample_sw.py

・できること
１．岡氏制作のスイッチと連動（しているはず）
２．スイッチ１〜３をONにすると流星情報が再生される（はず）
　　※但し、１週間以内の日付がイベントデータに必要


・起動オプション
-g:GPIOを利用する（スイッチONで音声再生）
-s:サンプル音声を再生して終了
起動オプションなしの場合はcron用

【GPIOを使用する場合】
python sample_sw.py -g
GPIOで起動したらタワーLED（緑）が点灯（のはず）
各スイッチONでLEDが点灯（のはず）

【サンプル音声を再生して終了】
python sample_sw.py -s

【cron用】
python sample_sw.py

・必要なファイル
１．流星群イベントデータ：event.txt
　　sample_sw.pyと同じディレクトリに配置
２．ライブラリ（OpenJTalk）に必要なファイル
　　ラズパイにインストールして下さい。

使用するライブラリ
OpenJTalk

https://qiita.com/lutecia16v/items/8d220885082e40ace252

再生用スクリプト：say
使用例
say こんにちは。
で再生可能
sample_sw.pyプログラムはsayスクリプトを起動している
また、再生コマンドとして、aplayコマンドを使用しているため、音声ファイルはwavに変換

