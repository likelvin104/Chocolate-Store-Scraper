# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import psycopg2

class ChocolatescraperPipeline:
    def process_item(self, item, spider):
        return item

class PriceToUSDPipeline:
    gpbToUsdRate = 1.3

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('price'):
            floatPrice = float(adapter['price'])
            adapter['price'] = floatPrice * self.gpbToUsdRate
            return item
        else:
            raise DropItem(f"Missing price in {item}")
        
class DuplicatesPipeline:
    def __init__(self):
        self.name_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter['name'] in self.name_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.name_seen.add(adapter['name'])
            return item
    
class SavingToPostgreSQLPipeline():
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.connection = psycopg2.connect(
            host="db.vruwmdtksafafixuegxc.supabase.co",
            database="postgres",
            user="postgres",
            password="vay9drh*vqn8fwg3AEZ")
        self.curr = self.connection.cursor()

    def process_item(self, item, spider):
        self.store_item(item)
        return item
    
    def store_item(self, item):
        try:
            self.curr.execute("""INSERT INTO "CHOCOLATE" VALUES ('{}', {}, '{}')""".format(item['name'], item['price'], item['url']))
        except BaseException as e:
            print(e)
        self.connection.commit()