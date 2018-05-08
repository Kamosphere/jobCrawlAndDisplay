# -*- coding: utf-8 -*-
from zhilian.items import ZhilianItem
from scrapy import Spider, Request
from bs4 import BeautifulSoup
import configparser
import os
import urllib.parse
import re

zhilian_config = configparser.ConfigParser()

fp = os.path.abspath(os.path.dirname(
    os.path.abspath(__file__)) + '/../../../keyword.cfg')
zhilian_config.read(fp, encoding="utf-8")
keyword = urllib.parse.quote(zhilian_config.get('search', 'keyword'))

class JobDetailSpider(Spider):
    name = 'zhilian'
    allowed_domains = ['www.zhaopin.com']
    start_urls = ['http://www.zhaopin.com/']

    def start_requests(self):
        first_url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E9%80%89%E6%8B%A9%E5%9C%B0%E5%8C%BA' \
                    '&kw= %wtf '.replace('%wtf', keyword)
        last_url = '&sm=0&isfilter=0&fl=489&isadv=0&sb=1&p='
        for i in range(1, 100):
            url = first_url + last_url + str(i)
            yield Request(url, self.parse)

    def parse(self, response):
        wbdata = response.text
        soup = BeautifulSoup(wbdata, 'lxml')
        job_name = soup.select("table.newlist > tr > td.zwmc > div > a:nth-of-type(1)")
        salary = soup.select("table.newlist > tr > td.zwyx")
        for name, salary in zip(job_name, salary):
            item = ZhilianItem()
            item["jobname"] = name.get_text()
            url = name.get('href')
            item["salary"] = salary.get_text()
        yield Request(url=url, meta={"item": item}, callback=self.parse_moive, dont_filter=True)

    def parse_moive(self, response):
        jobdata = response.body
        require_data = response.xpath(
            '//body/div[@class="terminalpage clearfix"]/div[@class="terminalpage-left"]/div[@class="terminalpage-main clearfix"]/div[@class="tab-cont-box"]/div[1]/p').extract()
        require_data_middle = ''
        for i in require_data:
            i_middle = re.sub(r'<.*?>', r'', i, re.S)
            require_data_middle = require_data_middle + re.sub(r'\s*', r'', i_middle, re.S)
        jobsoup = BeautifulSoup(jobdata, 'lxml')
        item = response.meta['item']
        listlink = response.xpath(
            "//link[@rel='canonical']/@href").extract()
        item['link'] = "".join(listlink).strip()
        item['job_require'] = require_data_middle
        item['address'] = jobsoup.select('div.terminalpage-left strong')[1].text.strip()
        item['education'] = jobsoup.select('div.terminalpage-left strong')[5].text.strip()
        item['experience'] = jobsoup.select('div.terminalpage-left strong')[4].text.strip()
        item['company_name'] = jobsoup.select('div.fixed-inner-box h2')[0].text
        item['company_size'] = jobsoup.select('ul.terminal-ul.clearfix li strong')[8].text.strip()
        yield item
