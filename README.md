## Twitch VOD Clip Generator

## 動作サンプル

https://github.com/user-attachments/assets/c524a780-bba1-4202-8533-15f47cc89099

### 動作環境（テスト済み）
・OS：Windows11
・ブラウザ：Google Chrome

### 概要
Twitchのアーカイブ動画からコメント数を解析するPythonスクリプトです。

### インストール方法
1. distフォルダ下の.exeファイルをPCの任意の場所へダウンロード
2. .exeファイルを実行する

※WindowsによってPCが保護されましたが出てくる場合

![image](https://github.com/user-attachments/assets/90fcae84-2c98-420f-9a0d-3bda72d82542)

「詳細情報」をクリック

![image](https://github.com/user-attachments/assets/9740fe7e-7a60-46de-b042-894b72bcbb37)

「実行」をクリック

### 操作説明
1. ```アーカイブURLを入力:```  
→ TwitchアーカイブのURLをコピペ（例：https://www.twitch.tv/videos/xxxxxxxxx）
2. コメントの解析が始まります
3. ```集計間隔を入力してください（秒）（半角数字）```  
→ 何秒単位でコメントを集計するかを入力します。（3分単位で集計したい場合は `180` と入力）
4. コメント量の流れが棒グラフで出力されます。（サンプル↓）  
![image](https://github.com/user-attachments/assets/1b12ad3e-e9f2-48fe-bda6-72905a9b458b)

5. ```抽出する時間帯を選択しますか？(yes / no)```  
→ 特定の時間で絞り込みたい場合は `yes` を入力、絞り込まない場合は `no` を入力

---

> ```抽出する時間帯を選択しますか？(yes / no)``` で `yes` を入力した場合
6. ```開始時間を入力してください(hh:mm:ss)```  
→ 絞り込む開始時間を入力（例：00:10:00）

7. ```終了時間を入力してください(hh:mm:ss)```  
→ 絞り込む終了時間を入力（例：00:40:00）

8. 集計結果が表示されます。（サンプル↓）

```
hh:mm:ss : コメント数
0:33:00 : 84
0:18:00 : 64
0:24:00 : 52
0:27:00 : 43
0:21:00 : 42
0:39:00 : 33
0:12:00 : 31
0:36:00 : 29
0:30:00 : 25
0:15:00 : 22
```

9. ブラウザで開く
抽出したコメントランキングリストを上位から順番に開きます（デフォルトブラウザで開きます）  
全てのリストを開いた後、または `stop` と入力するとループを終了します。


10. ```もう一度集計しますか？(yes / no)```  
→ もう一度集計したい場合は `yes` 、 終了する場合は `no` を入力。

---

> ```抽出する時間帯を選択しますか？(yes / no)``` で `no` を入力した場合
6. ```抽出する時間数を入力してください（半角数字）```  
→ 全体からコメントの多い時間帯を、ここで入力した時間数分表示します。（ `10` と入力した場合のサンプル↓）

```
hh:mm:ss : コメント数
0:33:00 : 84
0:18:00 : 64
0:24:00 : 52
0:27:00 : 43
0:21:00 : 42
0:48:00 : 40
0:54:00 : 39
1:09:00 : 36
0:39:00 : 33
0:00:00 : 33
```

7. ブラウザで開く
抽出したコメントランキングリストを上位から順番に開きます（デフォルトブラウザで開きます）  
全てのリストを開いた後、または `stop` と入力するとループを終了します。

10. ```もう一度集計しますか？(yes / no)```  
→ もう一度集計したい場合は `yes` 、 終了する場合は `no` を入力。

# Lisence

This project is licensed under the MIT License, see the LICENSE.txt file for details