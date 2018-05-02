from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
import json
from .handlesql import BaseOnSqlHelper
# Create your views here.

helper = BaseOnSqlHelper()

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
    else:
        salary = helper.getSalary()
        ctx['salary'] = salary
    return render(request, 'display.html', ctx)

def about(request):
    ctx = {}
    return render(request, 'about.html', ctx)

def search(request):
    limit = 10        #每页显示的记录数
    ctx = {}
    if request.GET.get('search'):
        search = request.GET.get('search')
        paginator = Paginator(helper.getSearchData(search), limit)
    else:
        paginator = Paginator(helper.getSearchData('java'), limit)
    page = request.GET.get('page')
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    ctx['result'] = result
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
        search = request.GET.get('search')
        heat_lan,best_city, value = helper.getLanEachOfCity(search, citys)
        ctx['heat_lan'] = heat_lan
        ctx['best_city'] = best_city
        ctx['title'] = json.dumps(search)
        ctx['analyse'] = value
    else:
        search = 'java'
        heat_lan,best_city,value = helper.getLanEachOfCity(search, citys)
        ctx['heat_lan'] = heat_lan
        ctx['title'] = json.dumps(search)
        ctx['best_city'] = best_city
        ctx['analyse'] = value
    return render(request, 'analyse.html', ctx)