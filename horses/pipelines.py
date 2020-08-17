# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class HorsesPipeline:
    def process_item(self, item, spider):
        # Validation of scraped Data
        # and pre-preprocessing
        # データによって渡すパイプラインの変え方を調べる。
        # ->単純に別のItemクラスを充てがえばいい気がしている。
        # tidied_result = {}
        # import pdb; pdb.set_trace()
        # columns = item["result_columns"]
        # race_result = item["race_result"]
        # for horse in race_result:
        #     for col in columns:
        #         tidied_result
        #         # TBD

        return item
    
