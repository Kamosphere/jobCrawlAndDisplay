# -*- coding: utf-8 -*-
import pdb
import scrapy
import configparser
import os
import urllib.parse
from scrapy import Request
from liepin.items import LiepinItem

liepin_config = configparser.ConfigParser()
# Assuming it is at the same location
fp = os.path.abspath(os.path.dirname(
    os.path.abspath(__file__)) + '/../../../keyword.cfg')
liepin_config.read(fp, encoding="utf-8")


class JobDetailSpider(scrapy.Spider):
    name = 'liepin'
    allowed_domains = ['liepin.com']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        keyword = urllib.parse.quote(liepin_config.get('search', 'keyword'))
        url = 'https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&d_sfrom=search_fp&key= %s ' % keyword
        yield Request(url, headers=self.headers)

    def parse(self, response):
        jobs_xpath = '/html/body[@id="sojob"]//div[@class="sojob-item-main clearfix"]'
        for sel in response.xpath(jobs_xpath):
            job = sel.xpath('div[@class="job-info"]')
            job_detail_url = job.xpath(
                'h3/a/@href').extract_first(default='Null').strip()
            if job_detail_url != 'Null':
                if job_detail_url.startswith('http'):
                    yield Request(job_detail_url, headers=self.headers)
                elif job_detail_url.startswith('/'):
                    yield Request('%s%s' % ('https://www.liepin.com', job_detail_url), headers=self.headers)
            # 产生下一页地址
            next_xpath = '//div[@class="pagerbar"]/a[@class="current"]/following-sibling::a[1]'
            # 下一页不是disable了，说明还没头
            if response.xpath(next_xpath + '/text()').extract_first().strip() != u'下一页':
                yield Request('https://www.liepin.com' + response.xpath(next_xpath + '/@href').extract_first().strip(), headers=self.headers)

        one_job = "/html/body/div[@id='job-view-enterprise']"
        if response.xpath(one_job):
            item = LiepinItem()
            listlink = response.xpath(
                "//link[@rel='canonical']/@href").extract()
            item['link'] = "".join(listlink).strip()
            item['jobname'] = response.xpath(
                "/html//div[@id='job-view-enterprise']//div[@class='title-info']/h1/text()").extract_first().strip()
            item['salary'] = response.xpath(
                "/html//p[@class='job-item-title']/text()").extract_first().strip()
            item['address'] = response.xpath(
                "/html//div[@class='job-title-left']/p[@class='basic-infor']/span[1]/a/text()").extract_first().strip()
            item['education'] = response.xpath(
                "/html//div[@class='job-qualifications']/span[1]/text()").extract_first().strip()
            item['experience'] = response.xpath(
                "/html//div[@class='job-qualifications']/span[2]/text()").extract_first().strip()
            item['job_require'] = response.xpath(
                "/html//div[@class='about-position']/div[@class='job-item main-message job-description'][1]/div[@class='content content-word']").extract_first().strip()
            item['company_size'] = response.xpath(
                "//ul[@class='new-compintro']/li[2]/text()").extract_first().strip()
            item['company_name'] = response.xpath(
                "/html//div[@class='title-info']/h3/a/text()").extract_first().strip()
            yield item

        one_hunter_job = "/html/body/div[@id='job-hunter']"
        if response.xpath(one_hunter_job):
            item = LiepinItem()
            jobnameraw=response.xpath(
                "/html/body/div[@id='job-hunter']/div[@class='wrap clearfix']/div[@class='clearfix content']/div[@class='main ']/div[@class='about-position']/div[@class='title']/div[@class='title-info']/h1/text()").extract_first()
            if jobnameraw is None:
                jobnameraw = response.xpath(
                    "/html/body/div[@id='job-hunter']/div[@class='wrap clearfix']/div[@class='clearfix content']/div[@class='main']/div[@class='about-position']/div[@class='title']/div[@class='title-info ']/h1/text()").extract_first()
            item['jobname'] = jobnameraw.strip()
            item['salary'] = response.xpath(
                "/html/body/div[@id='job-hunter']//"
                "p[@class='job-main-title']/text()").extract_first().strip()
            item['education'] = response.xpath(
                "/html/body/div[@id='job-hunter']//div[@class='resume clearfix']/span[1]/text()").extract_first().strip()
            item['experience'] = response.xpath(
                "/html/body/div[@id='job-hunter']//div[@class='resume clearfix']/span[2]/text()").extract_first().strip()
            item['job_require'] = response.xpath(
                "/html/body/div[@id='job-hunter']//div[@class='content content-word']").extract_first().strip()
            yield item
