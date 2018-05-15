# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.views.decorators.cache import cache_page
import json
from .handlesql import BaseOnSqlHelper
# Create your views here.

helper = BaseOnSqlHelper()


# 转换不能传输到html中的字符
def url_replace(input_key):
    keyword = input_key
    keyword = keyword.replace('+', '%2B')
    keyword = keyword.replace('#', '%23')
    keyword = keyword.replace('?', '%3F')
    keyword = keyword.replace('&', '%26')
    keyword = keyword.replace('=', '%3D')
    return keyword


def index(request):
    ctx = {}
    return render(request, 'index.html', ctx)


@csrf_exempt
def display(request):
    ctx = {}
    if request.is_ajax():
        val = request.POST.get('choose')
        if val in 'salary':
            salary = helper.getSalary()
            ctx['salary'] = salary
        if val in 'lan':
            lan = helper.getLan()
            ctx['lan'] = lan
        if val in 'ask':
            ask = helper.getKeyWords()
            ctx['ask'] = ask
        if val in 'citys':
            citys = helper.getCity()
            ctx['citys'] = citys
        if val in 'education':
            education = helper.getEducation()
            ctx['education'] = education
        if val in 'experience':
            experience = helper.getExperience()
            ctx['experience'] = experience
        if val in 'companysize':
            companysize = helper.getCompanysize()
            ctx['companysize'] = companysize
    else:
        salary = helper.getSalary()
        ctx['salary'] = salary
    return render(request, 'display.html', ctx)


def search(request):
    limit = 10        # 每页显示的记录数
    ctx = {}
    if request.GET.get('search'):
        keyword = request.GET.get('search')
    else:
        keyword = 'java'
    paginator = Paginator(helper.getSearchData(keyword), limit)
    page = request.GET.get('page')
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    ctx['result'] = result
    ctx['keyword'] = url_replace(keyword)
    return render(request, 'search.html', ctx)


def analyse(request):
    ctx = {}
    citys = []
    if request.GET.get('beijing'):
        citys.append(u'北京')
    if request.GET.get('wuhan'):
        citys.append(u'武汉')
    if request.GET.get('shanghai'):
        citys.append(u'上海')
    if request.GET.get('guangzhou'):
        citys.append(u'广州')
    if request.GET.get('hangzhou'):
        citys.append(u'杭州')
    if request.GET.get('jinan'):
        citys.append(u'济南')
    if request.GET.get('shenzheng'):
        citys.append(u'深圳')
    if request.GET.get('nanjing'):
        citys.append(u'南京')
    if request.GET.get('hefei'):
        citys.append(u'合肥')
    if request.GET.get('changsha'):
        citys.append(u'长沙')
    if request.GET.get('chengdu'):
        citys.append(u'成都')
    if request.GET.get('xian'):
        citys.append(u'西安')
    if request.GET.get('shenyang'):
        citys.append(u'沈阳')
    if request.GET.get('dalian'):
        citys.append(u'大连')
    if request.GET.get('haerbin'):
        citys.append(u'哈尔滨')
    if request.GET.get('changchun'):
        citys.append(u'长春')

    if request.GET.get('search'):
        search_key = request.GET.get('search')
    else:
        search_key = 'java'

    heat_lan, best_city, value = helper.getLanEachOfCity(search_key, citys)
    ctx['heat_lan'] = heat_lan
    ctx['title'] = json.dumps(search_key)
    ctx['best_city'] = best_city
    ctx['analyse'] = value
    return render(request, 'analyse.html', ctx)
