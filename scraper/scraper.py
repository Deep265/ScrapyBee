import scrapy
import pandas as pd
import csv
from scrapy.crawler import CrawlerProcess




class Writer:

    def __init__(self,file_name,cols):
        print("File Name in Writer :",file_name)
        file_name = file_name.split('/')[-1].split('.')[0]
        file_name = file_name+"_data.csv"
        self.file_name = "C:\\Users\\Vrushali\\PycharmProjects\\trial\\scrapybee\\media\\scraped_files\\"+file_name
        with open(self.file_name,"w",newline="",encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(cols)

    def data_writer(self,data):
        keys = list(data.keys())
        print(data.keys())
        with open(self.file_name,"a",newline="",encoding='utf-8') as f:
            writer = csv.DictWriter(f,keys)
            writer.writerow(data)

    def row_writer(self,data):
        with open(self.file_name, "a", newline="", encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(data)


class GeneralSpider(scrapy.Spider):
    name = "xpath_spider"

    def __init__(self,cols,xpaths,file_name):
        print(file_name,cols,xpaths)
        self.file_name = "C:\\Users\\Vrushali\\PycharmProjects\\trial\\scrapybee"+file_name
        self.cols = cols
        self.xpaths = xpaths
        self.writer = Writer(self.file_name,cols)

        print("Writing Completed")
        #self.writer = Writer("C:\\Users\\Vrushali\\PycharmProjects\\ScrapyBee\\scrapybee"+file_name,cols)

    def start_requests(self):
        df = pd.read_csv(self.file_name)
        print(len(df))
        for i in range(len(df)):
            yield scrapy.Request(df["Url"][i])

    def parse(self,response):
        data = {}
        for i in range(len(self.xpaths)):
            data[self.cols[i]] = response.xpath(self.xpaths[i]).get()

        self.writer.data_writer(data)
        print(data)

        #self.writer.data_writer(data)
        yield data


class run(scrapy.Spider):
    name = 'run'

    def start_requests(self):
        yield scrapy.Request('https://www.veromoda.in/241062702-night-sky')

    def parse(self,response):
        print("Runner Hello !!!!!!!!!!!!!!!!!")
        data = {}
        data['title'] = response.xpath('/html/body/div[4]/div[2]/div/div[1]/div[2]/div/h1/text()')
        yield data

# process = CrawlerProcess()
# process.crawl(run)
# process.start()



# process = CrawlerProcess()
# process.crawl(GeneralSpider,cols=['file'],xpaths=['/html/body/div[1]/div[4]/div[4]/div[2]/ul/li/div/div/div[2]/a'],file_name="C:\\Users\\Vrushali\\PycharmProjects\\ScrapyBee\\scrapybee\\media\\link_files\\links.csv")
# process.start()

class main_page_scraper(scrapy.Spider):
    name = "main_page"
    def __init__(self,cols,xpaths,file_name):
        self.file_name = "C:\\Users\\Vrushali\\PycharmProjects\\trial\\scrapybee" + file_name
        self.cols = cols
        self.xpaths = xpaths
        self.writer = Writer(self.file_name, cols)

    def start_requests(self):
        df = pd.read_csv(self.file_name)
        for i in range(len(df)):
            scrapy.Request(df['Url'][i])

    def parse(self, response):
        data = {}
        for i in range(len(self.xpaths)):
            data[self.cols[i]] = response.xpath.get(self.xpaths[i])
        j=0
        while True:
            try:
                collect_cols = []
                for i in range(len(self.cols)):
                    collect_cols.append(data[self.cols[i]][j])
                    j += 1
                self.writer.row_writer(collect_cols)
                yield collect_cols
            except:
                break



class JSON_Scraper(scrapy.Spider):
    name = "json"

    def __init__(self,file_name,cols,paths,all_products):
        self.file_name = file_name
        self.cols = cols
        self.paths = paths
        self.writer = Writer(file_name,cols)

    def start_requests(self):
        df = pd.read_csv(self.file_name)
        for i in range(len(df)):
            yield scrapy.Request(df['Url'][i])

    def parse(self,response):
        data = response.body()
        data_dict = {}

        for i in range(len(self.cols)):
            value = data
            for j in range(len(self.paths[i])): # self.paths is a 2D array
                value = value[self.paths[j]]

            data_dict[self.cols[i]] = value

    # Add the json keys to extract the data remaining