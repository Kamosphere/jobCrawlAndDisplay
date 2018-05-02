# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-11 09:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hireinfo',
            name='address',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='hireinfo',
            name='company_size',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='hireinfo',
            name='education',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='hireinfo',
            name='experience',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='hireinfo',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='hireinfo',
            name='jobname',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='hireinfo',
            name='salary',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='hireinfo',
            name='salary_max',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='hireinfo',
            name='salary_min',
            field=models.CharField(max_length=10),
        ),
    ]