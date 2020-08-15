# netkeiba

- Covid-19で無観客レースとなったことで、今まで活躍していた馬の調子に何かしらの影響を与えていないか？を検証するためにレース結果をscrapingするコード

- ```scrapy```を利用して実装する。

- https://qiita.com/kami634/items/55e49dad76396d808bf5
  この記事を参照＋documentationに記載されているtutorialから始めている。(quotes_spider.py etc)



## Memo:

- ```scrapy shell 'https://db.netkeiba.com/?pid=race_search_detail'```のようにdebugしながら実装することができてとても良い。
- parse -> 特定のlinkを指定して個別のparse methodを適用することが出来、crawlingの実装がとても容易に出来る。

> crawlingに必要なSelectorタグをcode内([net_keiba.py](https://github.com/Jumpo-523/netkeiba/blob/master/horses/spiders/net_keiba.py))整理している。
```python
# FROM the main page 
#   TO race_list fc
# response.css('div.race_calendar')[0].css("a")
#>>> response.css('div.race_calendar')[0].css("a::attr(href)")[0].get() 
# '/?pid=race_search_detail&date=20190803'

# FROM race_list fc ::特定の日に開催されたレースの一覧リスト
#   TO race_top_data_info fc ::特定の日に開催されたレース

# FROM race_top_data_info fc ::特定の日に開催されたレース
#   TO race_table_01 nk_tb_common ::そのレース結果のHTMLテーブルタグ
```

- next_pageのurlの渡し方を間違えていた。
- 動作確認未
8/15
- 次は、先月・先々月のデータを取得出来るようにする。