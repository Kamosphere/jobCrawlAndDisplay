# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from bs4 import BeautifulSoup as bs
from liepin import settings
import re
import pymysql
import hashlib
import os
fp_keyword = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../../keyword.txt')
fp_skill = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../../skill.txt')

class HtmlTagRemovePipeline(object):
    def process_item(self, item, spider):
        for key in item.keys():
            if not item[key].startswith('http'):
                item[key] = self.remove_tag(item[key])
        return item

    def remove_tag(self, raw):
        return bs(raw).text


class TransFormItemPipeline(object):
    def fileInput(self, filenames):
        myfile = open(filenames)
        filelines = myfile.readlines()
        lines = len(filelines)
        dicts = {}
        for line in filelines:
            line = line.strip('\n')
            dicts[line] = '0' * (len(dicts)) + '1' + '0' * (lines - 1 - len(dicts))
        return dicts

    def __init__(self, ):
        self.dict_keyword = self.fileInput(fp_keyword)
        self.dict_skill = self.fileInput(fp_skill)

    def process_item(self, item, spider):
        self.transform_education(item)
        self.transform_experience(item)
        self.transfrom_id(item)
        self.transfrom_salary(item)
        self.transform_companysize(item)
        self.transform_education(item)
        self.transform_dictdata(item, self.dict_keyword, 1)
        self.transform_dictdata(item, self.dict_skill, 2)
        return item

    def transform_education(self, item):
        if '大专' in item['education']:
            item['education'] = '大专'
        elif '本科' in item['education']:
            item['education'] = '本科'
        elif '硕士' in item['education']:
            item['education'] = '硕士'
        elif '博士' in item['education']:
            item['education'] = '博士'
        else:
            item['education'] = '不限'

    def transform_experience(self, item):
        pattern = re.compile('\d+')
        findyear = pattern.search(item['experience'])
        if findyear:
            item['experience'] = findyear.group()
        else:
            item['experience'] = '不限'

    def transfrom_id(self, item):
        idline = (item['job_name'] + item['company_name']).encode()
        item['id'] = hashlib.sha256(idline).hexdigest()

    def transfrom_salary(self, item):
        ptn_str = u'(\d+)-(\d+)万'
        ptn = re.compile(ptn_str)
        if ptn.match(item['salary']):
            gg = ptn.search(item['salary'])
            item['salary_min'] = gg.group(1)
            item['salary_max'] = gg.group(2)
        else:
            item['salary_min'] = 0
            item['salary_max'] = 0
        item['salary'] = round(
            float(item['salary_min']) + ((float(item['salary_max'])) - (float(item['salary_min'])) * 0.5))

    def transform_companysize(self, item):
        gm_str = item['company_size']
        gm_list = re.split('：', gm_str)
        if len(gm_list) > 1:
            item['company_size'] = gm_list[1]
        if '1-49人' in item['company_size']\
                or '50-99人' in item['company_size']:
            item['company_size'] = '1-99'
        elif '100-499人' in item['company_size']:
            item['company_size'] = '100-499'
        elif '500-999人' in item['company_size']:
            item['company_size'] = '500-999'
        elif '1000-2000人' in item['company_size']\
                or '2000-5000人' in item['company_size']\
                or '5000-10000人' in item['company_size']:
            item['company_size'] = '1000-9999'
        elif '10000人以上' in item['company_size']:
            item['company_size'] = '10000+'
        else:
            item['company_size'] = '保密'

    def transform_dictdata(self, item, dicts, flag):
        binput = 0
        for key, value in dicts.items():
            if key in item['job_require']:
                binput = binput | int(value, 2)
        boutput = str(bin(binput)[2:])
        if flag == 1:
            item['job_require_keyword'] = boutput
        elif flag == 2:
            item['job_require_skill'] = boutput


class LiepinPipeline(object):
    def __init__(self, ):
        self.conn = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWORD,
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            use_unicode=False)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        self.insertData(item)
        return item

    def insertData(self, item):
        sql1 = "insert into app_hireinfo(id,link,job_name,salary,company_name,job_require,address," \
               "experience,education,salary_min,salary_max,job_require_keyword,job_require_skill) " \
               "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        params1 = (
            item['id'], item['link'], item['job_name'], item['salary'], item['company_name'], item['job_require'],
            item['address'], item['experience'], item['education'], item['salary_min'], item['salary_max'],
            item['job_require_keyword'], item['job_require_skill'])
        self.cursor.execute(sql1, params1)
        sql2 = "insert into app_companyinfo(company_name,company_size) VALUES(%s,%s);"
        params2 = (item['company_name'], item['company_size'])
        self.cursor.execute(sql2, params2)
        self.conn.commit()
