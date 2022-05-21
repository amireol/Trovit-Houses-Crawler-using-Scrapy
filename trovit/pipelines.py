import csv
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class TrovitPipeline:

    def open_spider(self, spider):
        self.file = open('output.csv', 'w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['title', 'price', 'publish_time', 'address', 'link'])
        self.link, self.addr, self.price = [], [], []

    def process_item(self, item, spider):
        ada = ItemAdapter(item)
        # if (ada['link'] in self.link) and (ada['address'] in self.addr) and (ada['price'] in self.price):
        #     if self.addr.index(ada['address']) == self.price.index(ada['price']):
        #         raise DropItem('repeated ITEM')
        self.writer.writerow([ada['title'], ada['price'], ada['publish_time'], ada['address'], ada['link']])
        self.link.append(ada['link'])
        self.addr.append(ada['address'])
        self.price.append(ada['price'])
        return item

    def close_spider(self, spider):
        self.file.close()
        sort('output.csv')


def sort(file):

    def dic_check(date):
        if date not in dic:
            dic[date] = []

    file = open(file, 'r')
    reader = csv.reader(file)
    header = next(reader)
    items = []
    for item in reader:
        items.append(item)
    file.close()
    dic = {}

    for item in items:
        if '+ days' in item[2]:
            dic_check('44640')  # 31d*24h*60m
            dic['44640'].append(item)

        elif 'days' in item[2]:
            val = str(int(item[2].split()[0]) * 24 * 60)
            dic_check(val)
            dic[val].append(item)

        elif 'day' in item[2]:
            val = str(24 * 60)
            dic_check(val)
            dic[val].append(item)

        elif ' h ' in item[2]:
            spl = item[2].split()
            val = str(int(spl[0] * 60) + int(spl[2]))
            dic_check(val)
            dic[val].append(item)

    file = open('output.csv', 'w', newline='')
    writer = csv.writer(file)
    writer.writerow(header)
    for key in sorted(dic.keys()):
        for item in dic[key]:
            writer.writerow(item)
    file.close()
