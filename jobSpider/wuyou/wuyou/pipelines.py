# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import re
from wuyou import settings
import hashlib


def stringProcess(src, dst):
    temp=src.replace(dst, '')
    arr=re.split('-', temp)
    return arr


class TransFormItemPipeline(object):
    def process_item(self, item, spider):
        self.transForm(item)
        return item

    def transForm(self, item):
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

        if '少于50人' in item['company_size']\
                or '50-150人' in item['company_size']:
            item['company_size'] = '1-99'
        elif '150-500人' in item['company_size']:
            item['company_size'] = '100-499'
        elif '500-1000人' in item['company_size']:
            item['company_size'] = '500-999'
        elif '1000-5000人' in item['company_size']\
                or '5000-10000人' in item['company_size']:
            item['company_size'] = '1000-9999'
        elif '10000人以上' in item['company_size']:
            item['company_size'] = '10000+'
        else:
            item['company_size'] = '保密'

        pattern = re.compile('\d+')
        findyear = pattern.search(item['experience'])
        if findyear:
            item['experience'] = findyear.group()
        else:
            item['experience'] = '不限'

        idline = (item['jobname'] + item['company_name']).encode()
        item['id'] = hashlib.sha256(idline).hexdigest()

        temp = item['salary']
        if temp.endswith('万/月'):
            arr1=stringProcess(temp,'万/月')
            item['salary_min'] = round(float(arr1[0]) * 12, 2)
            item['salary_max'] = round(float(arr1[1]) * 12, 2)
        elif temp.endswith('千/月'):
            arr2 = stringProcess(temp, '千/月')
            item['salary_min'] = round(float(arr2[0]) / 10 * 12, 2)
            item['salary_max'] = round(float(arr2[1]) / 10 * 12, 2)
        elif temp.endswith('万/年'):
            arr3 = stringProcess(temp, '万/年')
            item['salary_min'] = arr3[0]
            item['salary_max'] = arr3[1]
        elif temp.endswith('元/天'):
            arr4 = stringProcess(temp, '元/天')
            item['salary_min'] = round(float(arr4[0]) * 21 * 12 / 10000, 2)
            item['salary_max'] = round(float(arr4[1]) * 21 * 12 / 10000, 2)
        else:
            item['salary_min'] = 0
            item['salary_max'] = 0

        item['salary'] = round(float(item['salary_min'])+((float(item['salary_max']))-(float(item['salary_min']))*0.5))


class WuyouPipeline(object):
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
        sql1 = "insert into app_hireinfo(id,link,jobname,salary,company_name,job_require,address,experience,education,salary_min,salary_max) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        params1 = (
           item['id'], item['link'], item['jobname'], item['salary'], item['company_name'], item['job_require'],
           item['address'], item['experience'], item['education'], item['salary_min'], item['salary_max'])
        self.cursor.execute(sql1, params1)
        sql2 = "insert into app_companyinfo(company_name,company_size) VALUES(%s,%s);"
        params2 = (item['company_name'], item['company_size'])
        self.cursor.execute(sql2, params2)
        self.conn.commit()
