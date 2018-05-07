# coding: utf-8
from django.db import models


# 工作信息
class hireinfo(models.Model):
    objects = models.Manager()
    id = models.CharField(primary_key=True, max_length=100)  # id
    link = models.CharField(max_length=100)  # 网址
    jobname = models.CharField(max_length=50)  # 工作
    salary = models.CharField(max_length=20)  # 薪水
    salary_max = models.CharField(max_length=10)  # 薪水上限
    salary_min = models.CharField(max_length=10)  # 薪水下限
    company_name = models.CharField(max_length=100)  # 公司
    address = models.CharField(max_length=20)  # 工作地点
    experience = models.CharField(max_length=20) # 工作经验
    education = models.CharField(max_length=20)  # 学历
    job_require = models.CharField(max_length=1024)  # 工作描述


# 公司信息
class companyinfo(models.Model):
    objects = models.Manager()
    company_name = models.CharField(primary_key=True, max_length=100)  # 公司
    company_size = models.CharField(max_length=20)  # 公司规模

