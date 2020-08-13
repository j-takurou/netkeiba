import scrapy

class KeibaSpider(scrapy.Spider):
    name = "keiba"
    start_urls = [
        'https://db.netkeiba.com/?pid=race_search_detail',
    ]

    def parse(self, response):
        for quote in response.css('div.race_calendar'):
            import pdb; pdb.set_trace()

            # yield {
            #     'text': quote.css('span.text::text').get(),
            #     'author': quote.css('small.author::text').get(),
            #     'tags': quote.css('div.tags a.tag::text').getall(),
            # }
            # FROM the main page 
            #   TO race_list fc
            # response.css('div.race_calendar')[0].css("a")
            #>>> response.css('div.race_calendar')[0].css("a::attr(href)")[0].get() 
            # '/?pid=race_search_detail&date=20190803'

            # FROM race_list fc ::特定の日に開催されたレースの一覧リスト
            #   TO race_top_data_info fc ::特定の日に開催されたレース

            # FROM race_top_data_info fc ::特定の日に開催されたレース
            #   TO race_table_01 nk_tb_common ::そのレース結果のHTMLテーブルタグ


        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)