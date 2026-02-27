BBCは英語、北京放送・NHKは日本語。NHKはニュースと国会中継。

２つのファイルを同一フォルダに配置してradiodownload_tool.pyを起動

止めたければ　Ctrl＋Cで終わる

準備としてyt-dlpやffmpegをDL

Preparation: download and install yt-dlp and ffmpeg.

sudo wget -O /usr/local/bin/yt-dlp \
https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp

sudo chmod a+rx /usr/local/bin/yt-dlp

sudo apt install ffmpeg

BBC is in English. Beijing Radio and NHK are in Japanese.
NHK includes news and Diet (parliament) broadcasts.

Place the two files in the same folder and run `radiodownload_tool.py`.
