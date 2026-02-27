#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
以下python3.4対応でscriptお願いします
https://www.bbc.co.uk/programmes/p002vsmz/episodes/player
このサイトのソースを調べ、””で囲まれてhttps://www.bbc.co.uk/programmesで始まるという条件を満たす文字列をさがし、上から３つ目のを取得
例：https://www.bbc.co.uk/programmes/w172zwx4jg6w2yw

上記文字列のサイトへ行く
このサイトのソースを調べ、
””で囲まれてmp3を含む条件を満たす最初の文字列を取得
例：（httpsを含まないものが見つかる）
//open.live.bbc.co.uk/mediaselector/6/redir/version/2.0/mediaset/audio-nondrm-download/proto/https/vpid/w1msl7hzs9953ll.mp3
その文字列の先頭に「https:」を付け加えた新たな文字列を作成

その作成した文字列のサイトへ行く。自動DLが始まり
/home/yuutarot/Downloads　に保存されるので、ここで最新のファイルを探し、/home/yuutarot/newsautoへコピーする。


"""



import re
import urllib.request
import os
import shutil
import datetime

BASE_URL = "https://www.bbc.co.uk/programmes/p002vsmz/episodes/player"
DOWNLOAD_DIR = "/home/yuutarot/Downloads"
HOME_DIR = os.path.expanduser("~") #ターミナルで echo "$HOME"と同じものが入る
DOWNLOAD_DIR = os.path.join(HOME_DIR, "Downloads")
#日付を260227方式で取得しnewsautoの末尾へくっつけ、これをHOME_DIR にあるフォルダ名とし、そのパスをSAVE_DIRに代入
today = datetime.datetime.now().strftime("%y%m%d")
folder_name = "newsauto" + today # フォルダ名新生
SAVE_DIR = os.path.join(HOME_DIR, folder_name)



def get_html(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", "ignore")


def find_3rd_programme(html):
    hits = re.findall(r'"(https://www\.bbc\.co\.uk/programmes[^"]+)"', html)
    if len(hits) < 3:
        return None
    return hits[2]


def find_first_mp3(html):
    hits = re.findall(r'"([^"]*mp3[^"]*)"', html)
    if not hits:
        return None
    return hits[0]


def download(url, folder):
    name = url.split("/")[-1]
    path = os.path.join(folder, name)

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        with open(path, "wb") as f:
            f.write(r.read())

    return path


def latest_file(folder):
    files = []
    for f in os.listdir(folder):
        p = os.path.join(folder, f)
        if os.path.isfile(p):
            files.append((os.path.getmtime(p), p))
    if not files:
        return None
    files.sort(reverse=True)
    return files[0][1]


def main():
    print("start")

    # ① 最初ページ
    html1 = get_html(BASE_URL)

    # ② programmes 3番目
    programme_url = find_3rd_programme(html1)
    if not programme_url:
        print("programme url not found")
        return

    print("programme:", programme_url)

    # ③ そのページ
    html2 = get_html(programme_url)

    # ④ mp3
    mp3_part = find_first_mp3(html2)
    if not mp3_part:
        print("mp3 not found")
        return

    # ⑤ https:付加
    if mp3_part.startswith("//"):
        mp3_url = "https:" + mp3_part
    else:
        mp3_url = mp3_part

    print("mp3:", mp3_url)

    # ⑥ DL
    download(mp3_url, DOWNLOAD_DIR)

    # ⑦ 最新ファイル
    newest = latest_file(DOWNLOAD_DIR)
    if not newest:
        print("latest file not found")
        return

    print("latest:", newest)

    # ⑧ コピー
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    dst = os.path.join(SAVE_DIR, os.path.basename(newest))
    shutil.copy(newest, dst)

    print("copied:", dst)



if __name__ == "__main__":
    main()
    print("BBCradiodownload_tool　終わり")
    import time
    print("15秒待機")
    time.sleep(15)
