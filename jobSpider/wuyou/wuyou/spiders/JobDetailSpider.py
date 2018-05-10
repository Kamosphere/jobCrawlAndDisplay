# -*- coding: utf-8 -*-
import scrapy
from wuyou.items import WuyouItem
import re
from selenium import webdriver
import configparser
import os
import urllib.parse

wuyou_config = configparser.ConfigParser()
# Assuming it is at the same location
fp = os.path.abspath(os.path.dirname(
    os.path.abspath(__file__)) + '/../../../keyword.cfg')
wuyou_config.read(fp, encoding="utf-8")
keyword = urllib.parse.quote(wuyou_config.get('search', 'keyword'))

def clean_char(s):
    s = s.replace('\xa0', '')
    s = s.replace('\r', '')
    s = s.replace('\n', '')
    s = s.replace('\t', '')
    s = s.replace(' ', '')
    return s


class JobDetailSpider(scrapy.Spider):
    name = 'wuyou'
    allowed_domains = ['51job.com']
    start_urls = ['http://search.51job.com/jobsearch/search_result.php?fromJs=1&keyword= %s &keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9' % keyword]

    def parse(self, response):
        items = []
        # 选取每一个页面的职位信息
        for each in response.xpath('//div[@class="dw_table"]/div[@class="el"]'):
            # 创建对象
            item = WuyouItem()
            # 提取出相应的字段
            jobtitle = each.css('p>span>a::text').extract()
            link = each.xpath('p/span/a/@href').extract()
            company = each.css('span[class=t2]>a::text').extract()
            location = each.css('span[class=t3]::text').extract()
            money = each.css('span[class=t4]::text').extract()
            if len(money) == 0:
                money = ["null"]

            item['job_name'] = jobtitle[0].strip()
            item['link'] = link[0]
            item['company_name'] = company[0]
            item['address'] = location[0]
            item['salary'] = money[0]

            # 提取职位详情和公司详情
            yield scrapy.Request(item['link'], meta={'position': item}, callback=self.parse_position)

        # 获取当前页码
        now_pagenumber = response.xpath('//div[@class="dw_page"]/div[@class="p_box"]/div[@class="p_wp"]/div[@class="p_in"]/ul/li[@class="on"]/text()').extract()[0]
        url = 'http://search.51job.com/list/000000,000000,0000,00,9,99, %wtf ,2,'.replace('%wtf', keyword)+str(int(now_pagenumber)+1)+'.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
        print(now_pagenumber)
        # 判断是否到达尾页
        if response.xpath("//li[@class='bk'][last()]/a/@href"):
            # 发送下一页请求
            yield scrapy.Request(url=url, callback=self.parse)

    # 获取职位详情和公司详情函数
    def parse_position(self,response):
        item = response.meta['position']
        zhize_unit = response.css("div.tCompany_main > div:nth-child(2) > div")
        zhize_list=""
        zhize_firstlist = zhize_unit.xpath('./text()').extract()
        for selectorP in zhize_unit.css('p::text'):
            zhize_list=zhize_list+selectorP.extract()
        for selectorDiv in zhize_unit.css('div::text'):
            zhize_list = zhize_list + selectorDiv.extract()
        zhizefirst = "".join(zhize_firstlist)
        zhize = "".join(zhize_list)
        result_rnt = clean_char(zhizefirst)+clean_char(zhize)
        item['job_require'] = result_rnt
        piece = response.css('p.msg.ltype::text').extract()[0].split('|')
        clean = clean_char(piece[1])
        item['company_size'] = clean
        try:
            item['experience'] = response.css("div.tBorderTop_box.bt > div > div > span:nth-child(1)::text").extract()[0]
        except:
            item['experience'] = '经验不限'
        try:
            item['education'] = response.css("div.tBorderTop_box.bt > div > div > span:nth-child(2)::text").extract()[0]
        except:
            item['education'] = '不限'
        yield item
