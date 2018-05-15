# -*- coding: utf-8 -*-
from zhilian.items import ZhilianItem
from scrapy import Spider, Request
from bs4 import BeautifulSoup
import configparser
import os
import urllib.parse

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
        for i in range(1, 90):
            url = first_url + last_url + str(i)
            yield Request(url, self.parse)

    def parse(self, response):
        web_data = response.text
        soup = BeautifulSoup(web_data, 'lxml')
        job_name = soup.select("table.newlist > tr > td.zwmc > div > a:nth-of-type(1)")
        salary = soup.find_all('td', {'class': 'zwyx'})
        for name, salary in zip(job_name, salary):
            item = ZhilianItem()
            item["job_name"] = name.get_text()
            url = name.get('href')
            item["salary"] = salary.get_text()
            yield Request(url=url, meta={"item": item}, callback=self.parse_moive, dont_filter=True)

    def parse_moive(self, response):
        job_data = response.body
        job_soup = BeautifulSoup(job_data, 'lxml')
        item = response.meta['item']
        job_social = job_soup.find('div', {'class': 'terminalpage-main clearfix'})
        job_school = job_soup.find('div', {'class': 'cJobDetailInforWrap'})

        if job_social:
            item['link'] = response.url
            item['job_require'] = job_soup.find('div', {'class': 'tab-inner-cont'}).text
            item['address'] = job_soup.select('div.terminalpage-left strong')[1].text.strip()
            item['education'] = job_soup.select('div.terminalpage-left strong')[5].text.strip()
            item['experience'] = job_soup.select('div.terminalpage-left strong')[4].text.strip()
            item['company_name'] = job_soup.select('div.fixed-inner-box h2')[0].text
            item['company_size'] = job_soup.select('ul.terminal-ul.clearfix li strong')[8].text.strip()

        if job_school:
            item['link'] = response.url
            item['job_require'] = job_soup.find('p', {'class': 'mt20'}).text
            item['address'] = job_soup.find('li', {'id': 'currentJobCity'}).text.strip()
            item['education'] = '本科'
            item['experience'] = '不限'
            item['company_name'] = job_soup.find('li', {'id': 'jobCompany'}).text.strip()
            item['company_size'] = job_soup.select('li.cJobDetailInforWd2')[1].text.strip()

        yield item


