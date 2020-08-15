import scrapy, re
from horses.items import HorsesItem

class KeibaSpider(scrapy.Spider):
    name = "keiba"
    start_urls = [
        'https://db.netkeiba.com/?pid=race_search_detail',
    ]

    def parse(self, response):
        for race_day_Selector in response.css('div.race_calendar a::attr(href)'):
            
            next_page = race_day_Selector.get()
            if re.match(string=next_page, pattern='/race/list/\d{8}/'):
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse_RaceList) 
    def parse_RaceList(self, response):
        # '/race/list/20200801/'
        # FROM race_list fc ::特定の日に開催されたレースの一覧リスト
        #   TO race_top_data_info fc ::特定の日に開催されたレース
        # "/race/202004020312/"
        # "/race/movie/202004020312/"にはクロールしない。
        # import pdb; pdb.set_trace()
        for RaceListSelector in response.css("div.race_list"):
            for RaceSelector in RaceListSelector.css("a::attr(href)"):
                next_page = RaceSelector.get()
                if "movie" not in next_page:
                    next_page = response.urljoin(next_page)
                    yield scrapy.Request(next_page, callback=self.parse_Race)

    def parse_Race(self, response):
        # import pdb; pdb.set_trace()
        # FROM race_top_data_info fc ::特定の日に開催されたレース
        #   TO race_table_01 nk_tb_common ::そのレース結果のHTMLテーブルタグ
        response = response.replace(body=response.body.replace(b'<br>', b''))
        # Raceの基礎情報
        # 2歳未勝利,芝右1500m / 天候 : 晴 / 芝 : 良 / 発走 : 09:50など、
        result_dict = HorsesItem()
        result_dict["base_info"] =\
            response.css("div.data_intro")[0].css("diary_snap_cut span")[0].get()

        for table in response.css("table"):
            if "race_table_" in table.attrib["class"]:
                race_result = table.css("tr")
                # race_result[0]:th
                remove_html_tag = lambda text:re.sub(r'<[^>]*?>', ' ', text)
                columns = [remove_html_tag(th.get()) for th in race_result[0].css("tr th")]

                # race_result[1:]:tr
                # elements of all horses
                #  race_result[1].css("td")
                results = []
                for tr in race_result[1:]:
                    results.append([remove_html_tag(td.get()).strip() for td in tr.css("td")])
                
                result_dict["result_columns"] = columns
                result_dict["race_result"] = results

                return result_dict

                # [td.get() for td in race_result[1].css('td')]   
