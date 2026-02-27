#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Python 3.4 compatible　（win7で動く）
"""
yt-dlp活用
sudo wget -O /usr/local/bin/yt-dlp \
https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp
② 実行権限
sudo chmod a+rx /usr/local/bin/yt-dlp
③ 確認
yt-dlp --version

sudo apt install ffmpeg
した上で

北京放送
最新の日替わりニュースと今週の２つの特番

NHK
https://www.nhk.or.jp/radionews/
と
https://www.bbc.com/audio/brand/p002vsmz
にアップロードされた最新を１つずつ
https://www.nhk.or.jp/radio/ondemand/detail.html?p=P1P796QWZ9_01
にアップロードされた最新と最新の過去をさかのぼって合計２つ

BBC　５分ニュースページ解析しDL　この.pyと同じフォルダーに配置されたBBCradiodownload_tool.pyを呼び出す

BBC RSS使用したGlobal News Podcast DL


以上をDLし/home/yuutarot/newsautoへ保存


ffmpeg -y -i m4a_path -vn -ab 192k mp3_path　.webmでも通用
"""

from __future__ import print_function
import os
import subprocess
import json
import urllib.request
import xml.etree.ElementTree as ET
import requests
import re
import time
import datetime



HOME_DIR = os.path.expanduser("~") #ターミナルで echo "$HOME"と同じものが入る
DOWNLOAD_DIR = os.path.join(HOME_DIR, "Downloads")
today = datetime.datetime.now().strftime("%y%m%d")
folder_name = "newsauto" + today # フォルダ名
SAVE_DIR = os.path.join(HOME_DIR, folder_name)

"""

"""
# RSSでDLできるBBCニュース
BBC_RSS = "https://podcasts.files.bbci.co.uk/p02nq0gn.rss"

# yt-dlpコマンドで自動DLできるサイトのリスト　（NHKはこの手法で簡単DL）
URLS = [
    # NHKニュース 最新1
    ("https://www.nhk.or.jp/radionews/", 1),
    
    #("https://www.nhk.or.jp/radio/ondemand/detail.html?p=P1P796QWZ9_01", 2),
]
# NHKオンデマンド 最新2   , 2)の２
URLS.append(
    ("https://www.nhk.or.jp/radio/ondemand/detail.html?p=P1P796QWZ9_01", 2)
)
# BBC Brief News,北京放送はページ解析の工夫で可能）


def get_bbc_latest_url(rss_address):
    try:
        xml_data = urllib.request.urlopen(rss_address).read()
        print(xml_data[:500])
        root = ET.fromstring(xml_data)
        item = root.find(".//item")   # ← ここ重要
        if item is None:
            print("item not found")
            return None
        enclosure = item.find(".//enclosure")
        if enclosure is None:
            print("enclosure not found")
            return None
        return enclosure.attrib.get("url")
    except urllib.error.HTTPError as e:
        print("BBC RSS 404 → skip:", rss_address)
        return None
    except Exception as e:
        print("BBC RSS error:", e)
        return None

#c 北京放送
def beijingfindanddownload_mp3(url):
    html = requests.get(url, timeout=20).text
    mp3URL_list = re.findall(r'https://[^"]+\.mp3', html)
    mp3URL_list = list(dict.fromkeys(mp3URL_list)) #重複除去
    print(mp3URL_list)
    print("１番ニュース、１１番経済、２１番目highway北京　それぞれ最新をDL")
    #time.sleep(15)
    
    if mp3URL_list:
        indexes = [0, 10, 20] # 取得したいインデックス
        targets = [] #DL用URL格納リスト定義
        for i in indexes: #リストの中身がそのまま iになる
            if len(mp3URL_list) > i: #len(mp3URL_list)は、通常５０くらいあるが、たとえば５まで（６つ）しかないと、i = 10が来たとき、条件ハズレでループ終了。次行エラー防止対策
                targets.append(mp3URL_list[i])
        #targets = mp3URL_list[:3]これだと最初の３つで最新ニュース３つDLされる
        print("北京放送DL開始")
        for mp3 in targets:
            run_yt(mp3, 1)
        return targets 
    else:
        print("北京放送DLありません")
        return None
    

def run_yt(url, count=1): #サイトから１つだけDLの場合をdefault指定、２項目は呼び出し側で省略可能
    #
    #c これはm4a形式
    cmd = [
        "yt-dlp",
        "--yes-playlist",
        "--playlist-end", str(count),
        "-P", SAVE_DIR,
        "--download-archive", os.path.join(SAVE_DIR, "archive.txt"),
        url
    ]
    """
    print("RUN:", " ".join(cmd))
    subprocess.call(cmd)
    #c DLしたてでmp3未変換の音声ファイル探す
    files = [
        os.path.join(SAVE_DIR, f)
        for f in os.listdir(SAVE_DIR)
        if f.lower().endswith((".m4a", ".webm"))
    ]
    #c 新しい順にcount数、そのパスを返す
    files.sort(key=os.path.getmtime, reverse=True)
    return files[:count]
    """
    try:これだと２つDLしたとき最新の１つしか変換できない
        return max(
            (os.path.join(SAVE_DIR, f)
            for f in os.listdir(SAVE_DIR)
            if f.lower().endswith((".m4a", ".webm"))),#２重括弧タプルリスト、１重だと２引数扱い
            key=os.path.getmtime
        )
    except ValueError:
        return None
    """

def download_if_valid(url, save_dir, label):
    if isinstance(url, str) and url.startswith("http"):
        filename = os.path.basename(url.split("?")[0])
        path = os.path.join(save_dir, filename)
        print(label + " download:", filename)
        urllib.request.urlretrieve(url, path)
        return path
    else:
        print(label + " invalid → skip")
        return None

def main():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    """   
    """
    # BBC brief News DL 別.py呼び出し
    print("BBC brief News")
    import BBCradiodownload_tool
    BBCradiodownload_tool.main()

    # BBC DL
    print("BBC Global News")
    bbc = get_bbc_latest_url(BBC_RSS)
    print("BBC URL:", bbc)
    download_if_valid(bbc, SAVE_DIR, "BBC")

    #c 北京
    #url = "https://japanese.cri.cn/2026/02/26/AUDI1772092655814577"
    print("北京放送")
    url = "https://japanese.cri.cn/radio/"
    beijingfindanddownload_mp3(url)
    
    # NHK DL　 URLSで指定したサイトから、指定個数分、DLしそれらをmp3変換したものも作成保存
    print("NHK")
    for url, count in URLS:
        paths = run_yt(url, count) #複数DLの場合あり
        if not paths:
            continue
        for m4a_path in paths:        
            # m4a_pathとして Noneを返してきたら、forへ戻る（continue）
            #c youtubeラジオは.webmが下りてくるがこれも以下で.mp3化作成保存できる
            mp3_path = os.path.splitext(m4a_path)[0] + ".mp3"
            # 同名mp3がすでにあればスキップ
            if os.path.exists(mp3_path):
                continue
            cmd = [
            "ffmpeg",
            "-y", # 同名mp3存在の場合上書き
            "-i", m4a_path,
            "-vn",
            "-ab", "96k",
            mp3_path
            ]
            subprocess.check_call(cmd) 


if __name__ == "__main__":
    print("radiodownload_tool　start")
    main()
    print("radiodownload_tool　終わり")
    import time
    print("15秒待機")
    time.sleep(15)
