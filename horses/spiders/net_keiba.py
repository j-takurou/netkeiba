import scrapy, re
from horses.items import HorsesItem
import time
import datetime as dt


def get_url_from_month(ym):
    st_day = dt.datetime.strptime(ym, "%Y%m")
    if dt.datetime.weekday(st_day) not in [5, 6]:
        days = 5 - dt.datetime.weekday(st_day) # days to First Saturday
        url = (st_day + dt.timedelta(days=days)).strftime("%Y%m%d")
    else:
        url = st_day.strftime("%Y%m%d")
    return url
def get_previous_month(ym, diff_months):
    # diff_months
    st_day = dt.datetime.strptime(ym, "%Y%m")
    prev_month = st_day - dt.timedelta(days=1)
    return prev_month.strftime("%Y%m")

class KeibaSpider(scrapy.Spider):
    name = "keiba"
    count = 0
    ym = "202008"#引数設定できるのか？
    start_urls = [
        'https://db.netkeiba.com/?pid=race_search_detail'+f"&date={get_url_from_month(ym)}",
    ]

    def parse(self, response):
        
        for race_day_Selector in response.css('div.race_calendar a::attr(href)'):
            next_page = race_day_Selector.get()
            if re.match(string=next_page, pattern='/race/list/\d{8}/'):
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse_RaceList)
        # race calendarのracelistごとのscrapingが終わったら、次の月のページをcrawlする。
        # import pdb; pdb.set_trace()
        self.count += 1
        if self.count <= 2:#5ヶ月分取ってくる。
            import datetime as dt 
            import pdb; pdb.set_trace()
            for race_day_Selector in response.css('div.race_calendar a::attr(href)'):
                prev_m = get_previous_month(self.ym, self.count)
                extracted_link = re.findall(string=race_day_Selector.get(), pattern=f'{prev_m}[0-9][0-9]')
                if not extracted_link:
                    continue
                else:
                    with open(f"./log_{self.count}.log", "w") as f:
                        f.write("start scraping for previous month")
                    # ?pid=race_search_detail
                    next_page = extracted_link[0]
                    next_page = response.urljoin(next_page)
                    # Get next page and DO the same as self.parse did.
                    yield scrapy.Request(next_page, callback=self.parse)

    def parse_RaceList(self, response):
        # '/race/list/20200801/'
        # FROM race_list fc ::特定の日に開催されたレースの一覧リスト
        #   TO race_top_data_info fc ::特定の日に開催されたレース
        # "/race/202004020312/"
        # "/race/movie/202004020312/"にはクロールしない。
        # import pdb; pdb.set_trace()
        
        for RaceListSelector in response.css("div.race_list"):
            for RaceSelector in RaceListSelector.css("a::attr(href)"):
                # time.sleep(1)
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
                remove_html_tag = lambda text:re.sub(r'<[^>]*?>', ' ', text).strip()
                columns = [remove_html_tag(th.get()) for th in race_result[0].css("tr th")]

                # race_result[1:]:tr
                # elements of all horses
                #  race_result[1].css("td")
                results = []
                for tr in race_result[1:]:
                    results.append([remove_html_tag(td.get()) for td in tr.css("td")])
                
                result_dict["result_columns"] = columns
                result_dict["race_result"] = results

                return result_dict

                # [td.get() for td in race_result[1].css('td')]
        # Get Horse info

    def parse_Horse(self, response):
        pass
        # Profile of horses
        # class=db_prof_area_02
        # [remove_html_tag(t) for t in response.css("div.db_prof_area_02")[0].css("td").getall()] 
        # blood table
        # [remove_html_tag(t) for t in response.css("table.blood_table")[0].css("td").getall()]
