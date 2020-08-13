# netkeiba

- Covid-19で無観客レースとなったことで、今まで活躍していた馬の調子に何かしらの影響を与えていないか？を検証するためにレース結果をscrapingするコード

- ```scrapy```を利用して実装する。

- https://qiita.com/kami634/items/55e49dad76396d808bf5
  この記事を参照＋documentationに記載されているtutorialから始めている。(quotes_spider.py etc)



## Memo:

- ```scrapy shell 'https://db.netkeiba.com/?pid=race_search_detail'```のようにdebugしながら実装することができてとても良い。
- parse -> 特定のlinkを指定して個別のparse methodを適用することが出来、crawlingの実装がとても容易に出来る。
