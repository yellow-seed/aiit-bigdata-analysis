#
# python3 Feeds_1.py
#
import pandas as pd
import feedparser
import re

def get_feeds(n, url):
    """
    urlから取得したフィードをリストにして返す。
    """
    print('URL #{} {}'.format(n, url), flush=True)
    # 初期化
    feeds = []
    # urlからフィードを取得
    try:
        f = feedparser.parse(url)
        if f.bozo != 0 and f.bozo != True:
            print('Error(bozo) url:', url, flush=True)
            return feeds
    except:
        print('Error(exception) url:', url, flush=True)
        return feeds
    # f.entries 内の各要素について処理
    # - title: タイトル
    # - summary, description: 内容
    for e in f.entries:
        # タイトル
        if 'title' in e:
            title = e.title
        else:
            title = ''

        # 内容：summary または description
        if 'summary' in e:
            body = e.summary
        elif 'description' in e:
            body = e.description
        else:
            body = ''

        # title と body の両方が空ならば追加しない
        if title == '' and body == '':
            continue

        # HTML 形式の場合があるため <...> を削除
        body = re.compile(r'<[^>]+>').sub('', body)
        # feeds に URL, タイトル、内容 を追加
        # - body.strip(): 先頭、末尾の改行・空白文字を削除
        feeds.append([url, title, body.strip()])

    return feeds

def write_feeds(feedlist, output):
    """
    feedlistに記載のURLからフィードを取得し、CSV形式でoutputファイルに書き出す。
    outputファイルが既にあれば、読み込み、重複排除を行う。
    """
    try:
        # outputファイル（CSV形式）から読み込み
        df = pd.read_csv(output)
    except:
        # outputファイルがなかった場合、DataFrameを作成
        df = pd.DataFrame([], columns=['url', 'title', 'summary'])

    # feedlistに記載のURLからフィードを取得
    urls = [line.strip() for line in open(feedlist)]
    for i, url in enumerate(urls):
        feeds = get_feeds(i, url)
        df = pd.concat([df, pd.DataFrame(feeds, columns=['url', 'title', 'summary'])])

    # 重複排除
    df = df.drop_duplicates()
    # CSV形式でoutputファイルに書き出し
    df.to_csv(output, index=False)

write_feeds('feedlist_en.txt', 'output_en.csv')
write_feeds('feedlist_jp.txt', 'output_jp.csv')
