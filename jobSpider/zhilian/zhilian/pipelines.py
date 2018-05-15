# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import re
import hashlib
from twisted.enterprise import adbapi
import os
import copy
fp_keyword = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../../keyword.txt')
fp_skill = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../../skill.txt')


class TransFormItemPipeline(object):
    def fileInput(self, file_name):
        input_file = open(file_name)
        file_lines = input_file.readlines()
        lines = len(file_lines)
        dicts = {}
        for line in file_lines:
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
        find_year = pattern.search(item['experience'])
        if find_year:
            item['experience'] = find_year.group()
        else:
            item['experience'] = '不限'

    def transfrom_id(self, item):
        id_line = (item['job_name'] + item['company_name']).encode()
        item['id'] = hashlib.sha256(id_line).hexdigest()

    def transfrom_salary(self, item):
        ptn_str = u'(\d+)-(\d+)'
        ptn = re.compile(ptn_str)
        if ptn.match(item['salary']):
            gg = ptn.search(item['salary'])
            item['salary_min'] = round(float(gg.group(1)) * 12 / 10000, 2)
            item['salary_max'] = round(float(gg.group(2)) * 12 / 10000, 2)
        else:
            item['salary_min'] = 0
            item['salary_max'] = 0
        item['salary'] = round(
            float(item['salary_min']) + ((float(item['salary_max'])) - (float(item['salary_min'])) * 0.5))

    def transform_companysize(self, item):
        if '20人以下' in item['company_size']\
                or '20-99人' in item['company_size']:
            item['company_size'] = '1-99'
        elif '100-499人' in item['company_size']:
            item['company_size'] = '100-499'
        elif '500-999人' in item['company_size']:
            item['company_size'] = '500-999'
        elif '1000-9999人' in item['company_size']:
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
        bin_output = str(bin(binput)[2:])
        if flag == 1:
            item['job_require_keyword'] = bin_output
        elif flag == 2:
            item['job_require_skill'] = bin_output


class ZhilianPipeline(object):
    def __init__(self, db_pool):
        self.db_pool = db_pool

    @classmethod
    def from_settings(cls, settings):
        db_params = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )
        db_pool = adbapi.ConnectionPool("pymysql", **db_params)
        return cls(db_pool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        async_item = copy.deepcopy(item)
        query_job = self.db_pool.runInteraction(self.insertjobData, async_item)
        query_job.addErrback(self.handle_error, item, spider)  # 处理异常
        query_company = self.db_pool.runInteraction(self.insertcompanyData, async_item)
        query_company.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def insertjobData(self, cursor, item):
        sql = "insert into app_hireinfo(id,link,job_name,salary,company_name,job_require,address," \
               "experience,education,salary_min,salary_max,job_require_keyword,job_require_skill) " \
               "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        params = (
            item['id'], item['link'], item['job_name'], item['salary'], item['company_name'], item['job_require'],
            item['address'], item['experience'], item['education'], item['salary_min'], item['salary_max'],
            item['job_require_keyword'], item['job_require_skill'])
        cursor.execute(sql, params)

    def insertcompanyData(self, cursor, item):
        sql = "insert into app_companyinfo(company_name,company_size) VALUES(%s,%s);"
        params = (item['company_name'], item['company_size'])
        cursor.execute(sql, params)
