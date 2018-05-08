import os
dirs = os.getcwd()
os.chdir(dirs+"\liepin")
os.system("scrapy crawl liepin -s CLOSESPIDER_TIMEOUT=600")

os.chdir(dirs+"\wuyou")
os.system("scrapy crawl wuyou -s CLOSESPIDER_TIMEOUT=600")

os.chdir(dirs+"\zhilian")
os.system("scrapy crawl zhilian -s CLOSESPIDER_TIMEOUT=600")

os.chdir(dirs+"\JobDisplay")
os.system("python manage.py runserver")
