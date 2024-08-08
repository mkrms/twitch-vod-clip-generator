# MIT License

# Copyright (c) 2024 Niiyama Keisuke

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import requests
import time
import urllib.parse
import pprint
import numpy as np
import matplotlib.pyplot as plt
import re
import webbrowser


start = 0
comment_list = []
comment_data = []
comment_array = []

def input_video_url():
    url = input('アーカイブURLを入力: ')
    if ('https://www.twitch.tv/videos/' in url) == True:
        return url
    else:
        print("正しいURLを入力してください\n")
        time.sleep(0.5)
        return input_video_url()

# 秒 → hh:mm:ss 変換
def time_to_hhmmss(t):
    hours = int(t // 3600)
    minutes = int((t - hours * 3600) // 60)
    seconds = int(t - hours * 3600 - minutes * 60)
    return "{0}:{1:02}:{2:02}".format(hours, minutes, seconds)

# 秒 → hh"h"mm"m"ss"s" 変換

def time_to_link(t):
    hours = int(t // 3600)
    minutes = int((t - hours * 3600) // 60)
    seconds = int(t - hours * 3600 - minutes * 60)
    return "{0}h{1:02}m{2:02}s".format(hours, minutes, seconds)

# hh:mm:ss → 秒 変換
def time_to_seconds(t):
    time_array = t.split(":")
    hour = int(time_array[0]) * 3600
    minute = int(time_array[1]) * 60
    seconds = int(time_array[2])
    offset_seconds = (hour + minute + seconds)
    return offset_seconds

# count messages
def count_messages(data, start):
    for comment in data['comments']['edges']:
        if comment['node']['contentOffsetSeconds'] < start:
            continue
        comment_list.append(comment['node']['contentOffsetSeconds'])
        print("\r"+"集計中：", str(len(comment_list)), end="")

def input_interval():
    interval_seconds = input("集計間隔を入力してください（秒）（半角数字）: ")
    try:
        check_int = int(interval_seconds)
        print(check_int, "秒間隔でコメントを集計します")
        return check_int
    except ValueError:
        print("正しい数字を入力してください\n")
        time.sleep(0.5)
        return input_interval()

def input_start_time():
    match_pattern = "[0-2][0-9]:[0-5][0-9]:[0-5][0-9]"
    start_time = input("開始時間を入力してください(hh:mm:ss): ")
    match_obj = re.fullmatch((match_pattern), start_time)
    if match_obj == None:
        print("正しい開始時間を入力してください\n")
        return input_start_time()
    else:
        start_time_seconds = time_to_seconds(start_time)
        return start_time_seconds

def input_end_time():
    match_pattern = "[0-2][0-9]:[0-5][0-9]:[0-5][0-9]"
    end_time = input("終了時間を入力してください(hh:mm:ss): ")
    match_obj = re.fullmatch((match_pattern), end_time)
    if match_obj == None:
        print("正しい終了時間を入力してください\n")
        return input_start_time()
    else:
        end_time_seconds = time_to_seconds(end_time)
        return end_time_seconds

def analyze_comment_amount(unit_sec, start_time, end_time):
    sec=[]
    minute=[]
    val_sec = start_time
    val=start_time//60
    end_unit_time = (int(start_time) + int(unit_sec))
    while end_time > start_time:
        comment_unit = []
        for x in comment_list:
            if start_time < x <= end_unit_time:
                comment_unit.append(x)
        comment_data.append(len(comment_unit))
        start_time += unit_sec
        end_unit_time += unit_sec
        
        sec.append(val_sec)
        val_sec += unit_sec

        minute.append(val)
        val += unit_sec//60

    return comment_data, sec, minute

def select_again(comment_data, sec, UNIT_OF_SEC, video_url):
    is_again = input("もう一度集計しますか？(yes / no): ")
    if is_again == "yes":
        print("#########################")
        return analyze_comments(comment_data, sec, UNIT_OF_SEC, video_url)
    elif is_again == "no":
        pass
    else:
        print("yes または no を入力してください\n")
        return select_again(comment_data, sec, UNIT_OF_SEC, video_url)

def num_of_ext_time():
    ext_time = input("抽出する時間数を入力してください（半角数字）: ")
    try:
        check_int = int(ext_time)
        return check_int
    except ValueError:
        print("正しい時間数を入力してください")
        return num_of_ext_time()
    
def open_clip(sec, video_url):
    y=0
    link_len = len(sec)
    print("\n抽出した時間のURLを生成します。途中でやめる場合は'stop'と入力してください")
    for i in sec:
        query = time_to_link(i)
        time = time_to_hhmmss(i)
        print("開始時間：", time)
        link = video_url + '?t=' + query
        webbrowser.open(link,2,True)
        is_next = input("エンターキーで次のクリップを開きます\n")
        y +=1
        if y > link_len:
            break
        if is_next == 'stop':
            break


def analyze_comments(comment_data, sec, UNIT_OF_SEC, video_url):
    is_select_time_range = input("抽出する時間帯を選択しますか？(yes / no): ")

    if is_select_time_range == "yes":
        start_offset_seconds = input_start_time()
        end_offset_seconds = input_end_time()

        #sec から start_offset_secondsに対応する列番号を取得する
        start_index = np.where(start_offset_seconds <= sec)[0][0]
        #sec から end_offset_secondsに対応する列番号を取得する
        end_index = np.where(end_offset_seconds >= sec)[0][-1]
        #start_offset_secondsに対尾する列番号からend_offset_secondsに対応する列番号でcomment_list, secを絞り込む
        ext_sec_array = sec[start_index:(end_index+1)]
        ext_comment_data = comment_data[start_index:(end_index+1)]

        #配列の結合
        comment_array = np.stack((ext_sec_array,ext_comment_data))

        #降順でソート
        sorted_comment_array = comment_array[:, np.argsort(comment_array[1])[::-1]]
        many_comments_time = sorted_comment_array[0]
        many_comments_amount = sorted_comment_array[1]

        print("hh:mm:ss : コメント数")

        y=0
        for t in many_comments_time:
            print(time_to_hhmmss(t), ":", many_comments_amount[y])
            y+=1
        
        open_clip(many_comments_time, video_url)

        select_again(comment_data, sec, UNIT_OF_SEC, video_url)

    elif is_select_time_range == "no":
        comment_array = np.stack((sec,comment_data))
        sorted_comment_array = comment_array[:, np.argsort(comment_array[1])[::-1]]

        ext_time = num_of_ext_time()
        print("上位", ext_time, "を抽出します。\n")
        print("hh:mm:ss : コメント数")

        many_comments_time = sorted_comment_array[0][:ext_time]
        many_comments_amount = sorted_comment_array[1][:ext_time]
        y=0

        for t in many_comments_time:
            print(time_to_hhmmss(t), ":", many_comments_amount[y])
            y+=1
        
        open_clip(many_comments_time, video_url)
            
        select_again(comment_data, sec, UNIT_OF_SEC, video_url)
    else:
        print("yes または no を入力してください\n")
        return analyze_comments(comment_data, sec, UNIT_OF_SEC, video_url)
        

####################################################################

### main関数 ###

####################################################################

def main():
    # URL入力 ~ video_id 抽出
    video_url = input_video_url()
    parsed_url = urllib.parse.urlparse(video_url)
    video_id = parsed_url.path.split('/')[-1]

    #1回目のセッションスタート
    session = requests.Session()
    session.headers = { 'Client-ID': 'kd1unb4b3q4t58fwlpcbzcbnm76a8fp', 'content-type': 'application/json' }

    response = session.post(
        'https://gql.twitch.tv/gql',
        "[{\"operationName\":\"VideoCommentsByOffsetOrCursor\"," +
            "\"variables\":{\"videoID\":\"" + video_id + "\",\"contentOffsetSeconds\":" + str(start) + "}," +
            "\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"b70a3591ff0f4e0313d126c6a1502d79a1c02baebb288227c582044aa76adf6a\"}}}]",
        timeout=10)
    print("接続に成功しました\n")
    response.raise_for_status()
    data = response.json()

    count_messages(data[0]['data']['video'], start)

    cursor = None
    if data[0]['data']['video']['comments']['pageInfo']['hasNextPage']:
        cursor = data[0]['data']['video']['comments']['edges'][-1]['cursor']
        time.sleep(0.1)


    # session loop
    while cursor:
        response = session.post(
            'https://gql.twitch.tv/gql',
            "[{\"operationName\":\"VideoCommentsByOffsetOrCursor\"," +
                "\"variables\":{\"videoID\":\"" + video_id + "\",\"cursor\":\"" + cursor + "\"}," +
                "\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"b70a3591ff0f4e0313d126c6a1502d79a1c02baebb288227c582044aa76adf6a\"}}}]",
            timeout=10)
        response.raise_for_status()
        data = response.json()

        count_messages(data[0]['data']['video'], start)

        if data[0]['data']['video']['comments']['pageInfo']['hasNextPage']:
            cursor = data[0]['data']['video']['comments']['edges'][-1]['cursor']
            time.sleep(0.1)
        else:
            cursor = None

    print('\n総コメント数:', len(comment_list), "\n")

    UNIT_OF_SEC = input_interval()

    comment_data = np.array(analyze_comment_amount(UNIT_OF_SEC, 0,comment_list[-1])[0])
    sec = np.array(analyze_comment_amount(UNIT_OF_SEC, 0,comment_list[-1])[1])
    minute = np.array(analyze_comment_amount(UNIT_OF_SEC, 0, comment_list[-1])[2])

    print("コメント量の流れを表に出力します。")

    plt.bar(minute, comment_data, width=0.9)
    plt.title("Comment Amount in Twitch VOD")  
    plt.ylabel("Comment Amount")
    plt.xlabel("minute")
    plt.pause(0.1)

    analyze_comments(comment_data, sec, UNIT_OF_SEC, video_url)

    input("エンターキーを押すと終了します。")

if __name__ == "__main__":
    main()