import csv
from django.shortcuts import render,reverse,HttpResponse,HttpResponseRedirect,get_object_or_404
import scrapy
import pandas as pd
from .models import Links
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# from .scraper import GeneralSpider,Writer
# Scrapy imports
# from scrapers.scrapers.spiders import General
# from scrapers.scrapers import settings
from scrapy.cmdline import execute
from scrapy.utils.project import get_project_settings
from . import scraper
from scrapy.crawler import CrawlerProcess
import mimetypes

# Scrapy crawler runner
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor,defer
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
# Create your views here.
def get_csv(request,pk):
    """
    Stores the csv file in the database with the user key and then returns the latest file

    :param request:
    :param pk:
    :return:
    """
    if request.method == "POST":
        file = request.FILES.get("csv")
        user = get_object_or_404(User,pk=pk)
        save_file = Links(user=user,file=file)
        save_file.save()
        print("saveeeeddddd")
        return HttpResponseRedirect(reverse('scraper:result',args=[pk]))
    return render(request,'get_csv1.html')

def just_stop():
    print("I am Done with this scraper")
    return "OK"


# Scrapy Crawler Runner
configure_logging()
runner = CrawlerRunner(get_project_settings())
@defer.inlineCallbacks
def crawl(cols,xpath,file):
    yield runner.crawl(scraper.GeneralSpider,cols=cols,xpaths=xpath,file_name=file)
    reactor.stop()


def scrape(request,pk):
    user = get_object_or_404(User,pk=pk)
    file = Links.objects.filter(user=user)
    file = file[len(file)-1]
    print(file)
    print(file.file.url)
    if request.method == "POST":
        n_xpaths = request.POST.get("numofquestions")
        xpath_type = request.POST.get("xpath_type")
        cols = []
        xpath = []
        for i in range(int(n_xpaths)):
            col_name = request.POST.get("col" + str(i))
            xpath_value = request.POST.get("xpath" + str(i))
            cols.append(col_name)
            xpath.append(xpath_value)


        print(xpath)
        print(cols)

        # process = CrawlerProcess()
        # process.crawl(scraper.GeneralSpider,cols=cols, xpaths=xpath,file_name=file.file.url)
        # process.start()
        # test = scraper.GeneralSpider(cols=cols,xpaths=xpath,file_name=file.file.url)
        # test.runner()
        # process = CrawlerProcess()
        # process.crawl(scraper.GeneralSpider, cols=cols,
        #               xpaths=xpath,
        #               file_name=file.file.url)
        # process.start()
        # configure_logging()
        # test = CrawlerRunner()
        # test.crawl(scraper.GeneralSpider,cols=cols,xpaths=xpath,file_name=file.file.url)
        # reactor.stop()
        # reactor.run()
        # crawl(cols,xpath,file.file.url)


        # if xpath_type == "list":
        #     runner.crawl(scraper.GeneralSpider,cols=cols,xpaths=xpath,file_name=file.file.url)
        # else:
        #     runner.crawl(scraper.main_page_scraper, cols=cols, xpaths=xpath, file_name=file.file.url)
        runner.crawl(scraper.GeneralSpider, cols=cols, xpaths=xpath, file_name=file.file.url)
        print(file.file.url)
        d = runner.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
        file_name = file.file.url.split('/')[-1].split('.')[0]
        file_name = file_name + "_data.csv"
        filepath = "C:\\Users\\Vrushali\\PycharmProjects\\trial\\scrapybee\\media\\scraped_files\\"+file_name
        # Open the file for reading content
        path = open(filepath, 'r')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % file_name
        return response

        # return HttpResponse("Passed !!!!!!! <a href='{file}' download=> Download</a>".format(file="C:\\Users\\Vrushali\\PycharmProjects\\trial\\scrapybee\\media\\scraped_files\\"+file_name))
    return render(request,'result1.html',context={'file':file})














