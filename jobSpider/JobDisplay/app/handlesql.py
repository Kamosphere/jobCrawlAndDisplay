
from django.db import connection, transaction
import json
import re


# sql语言帮助
class SqlHelper(object):
    # 元组向其他类型转换
    def tupleToOther(self, tup):
        for i in tup:
            if isinstance(i[0], int):
                return int(i[0])

    # 执行一条sql语句
    def executeSql(self, sql):
        with transaction.atomic():
            cursor = connection.cursor()
            cursor.execute(sql)
            raw = cursor.fetchall()
            return raw

    # 查询salary情况，返回相关结果
    def executeGroupSalary(self, args):
        # flag = 0（有上限有下限） flag=1(上限) flag=2(下限 ) flag=3(面议)
        def execute_salary(flag, args):
            if len(args) > 4 or len(args) < 0:
                return None
            if flag == 0:
                sql = "select count(link) from app_hireinfo where salary > %s and salary <= %s" % (args[0], args[1])
            elif flag == 1:
                sql = "select count(link) from app_hireinfo where salary <= %s " % (args[0])
            elif flag == 2:
                sql = "select count(link) from app_hireinfo where salary > %s" % (args[0])
            elif flag == 3:
                sql = "select count(link) from app_hireinfo where salary = 0"
            return self.executeSql(sql)
        ls = []
        for i in args:
            ls.append(self.tupleToOther(execute_salary(i[0], i[1:])))
        return ls

     # 关键字查询情况
    def executeGroupAsk(self, flag, args):
        la = []

        def executeLan(args):
            sql = "select count(jobname) from app_hireinfo where lower(job_require) like '%%%s%%'" % args.lower()
            return self.executeSql(sql)

        def executeKey(args):
            sql = "select count(jobname) from app_hireinfo where lower(job_require) like '%%%s%%'" % args.lower()
            return self.executeSql(sql)

        # 语言
        if 1 == flag:
            for i in args:
                la.append({"value": self.tupleToOther(executeLan(i)), "name": i})

        # 关建字
        if 2 == flag:
            for i in args:
                la.append({"value": self.tupleToOther(executeKey(i)), "name": i})
        return la

    # 城市查询情况
    def executeGroupCity(self, args):
        def executeCity(arg):
            sql = "select count(address) from app_hireinfo where address like '%%%s%%'" % arg
            return self.executeSql(sql)
        lc = []
        for i in args:
            lc.append({"value" : self.tupleToOther(executeCity(i)), "name" : i})
        return lc

    # 工作经验查询情况
    def executeGroupYear(self, args):
        def executeYear(args):
            if len(args)>1:
                sql = "select count(jobname) from app_hireinfo where experience >= %s and experience <= %s" % (
                    args[0], args[1])
            else:
                sql = "select count(jobname) from app_hireinfo where experience like '%%%s%%'" % args[0]
            return self.executeSql(sql)
        lc = []
        for i in args:
            lc.append({"value" : self.tupleToOther(executeYear(i)), "name" : i})
        return lc

    #学历查询情况
    def executeGroupEdu(self, args):
        def executeEdu(arg):
             sql = "select count(jobname) from app_hireinfo where education like '%%%s%%'" % arg
             return self.executeSql(sql)
        lc = []
        for i in args:
            lc.append({"value": self.tupleToOther(executeEdu(i)), "name": i})
        return lc

class BaseOnSqlHelper(object):
    # 配置你想要获取的信息
    def __init__(self):
        self.sqlHelper = SqlHelper()
        # flag = 0（有上限有下限） flag=1(上限) flag=2(下限 ) flag=3(面议)
        self.salary = [[0, 0.1, 5], [0, 5, 10], [0, 10, 15], [0, 15, 20], [0, 20, 25], [0, 25, 30], [0, 30, 35], [0, 35, 40],  [2, 40], [3]]
        self.lan = ['java','c++', 'python', 'javascript', 'php', 'c#', 'sql',  'android', 'ios', 'web']
        self.app_citys = ['武汉', '广州', '北京', '深圳', '上海', '天津', '重庆', '石家庄', '沈阳', '哈尔滨', '杭州',
             '福州', '济南','成都', '昆明', '兰州', '南宁', '银川', '长春', '南京', '合肥', '南昌',
             '郑州' , '长沙','海口','贵阳', '西安', '呼和浩特', '拉萨', '乌鲁木齐']
        self.keyWords = ['人工智能', '大数据','云计算', '物联网', '数据挖掘', '机器学习', '区块链','算法','嵌入式',
                         '态度认真', '责任', '执行力', '吃苦耐劳', '团队', '进取心', '管理能力', '沟通', '协调',
                         '压力', '测试', '硬件', '安全', '架构', '高并发', '多线程', '分布式', '核心'
                         ]
        self.education = ['不限', '大专',  '本科', '硕士', '博士']
        self.experience = [[1, 3], [3, 5], [5, 8], [8, 10], ['不限']]
    # 二维元祖转换列表
    def tuple_to_list(self, tuples):
        ls = []
        for i in tuples:
            if isinstance(i[0], int):
                ls.append(int(i[0]))
        return ls

    # 拿到薪水值
    def getSalary(self):
        return self.sqlHelper.executeGroupSalary(self.salary)

    # 拿到语言值
    def getLan(self):
        return self.sqlHelper.executeGroupAsk(1, self.lan)

    # 拿到城市值
    def getCity(self):
        return self.sqlHelper.executeGroupCity(self.app_citys)

    # 拿到关键字
    def getKeyWords(self):
        return self.sqlHelper.executeGroupAsk(2, self.keyWords)

    # 拿到教育情况
    def getEducation(self):
        return self.sqlHelper.executeGroupEdu(self.education)

    # 拿到工作经验
    def getExperience(self):
        return self.sqlHelper.executeGroupYear(self.experience)

    # 二维元祖转换为字典列表
    def tuple_dict_list(self, tuples):
        ls = []
        #注意 ，要与getSearchData一一对应
        keys = ['link', 'jobname', 'salary_min', 'salary_max', 'company_name', 'address', 'education', 'experience']
        for tuple in tuples:
            ls.append({keys[0]:tuple[0],keys[1]:tuple[1],keys[2]:tuple[2],keys[3]:tuple[3]
                          ,keys[4]:tuple[4],keys[5]:tuple[5],keys[6]:tuple[6],keys[7]:tuple[7]})
        return ls
    # 搜索函数
    def getSearchData(self, key):
        # 一次查询限制返回100条
        sql = "select link, jobname, salary_min, salary_max, company_name, address, education, experience " \
              "from app_hireinfo where lower(jobname) like '%%%%%s%%%%'  order by jobname desc limit 500" % key.lower()
        result = self.tuple_dict_list(self.sqlHelper.executeSql(sql))

        return result

    # 将城市需求结果以字典列表形式返回
    def city_list_dict(self, ll, app_citys):
        la = []
        for i in range(len(app_citys)):
            la.append({'name' : app_citys[i], 'value' : ll[i]})
        return la


    # 不同语言在各个城市之间的需求
    def getLanEachOfCity(self, key, app_citys):
        la = []
        l = {"c++" : u'c\+\+', "java" : 'java',"python":'python',"php": 'php',"c#":'c\#', "sql":'sql',
             "android":'android', "ios":'ios', "web" : 'web',"javascript":'javascript'
        }
        analyse = {
            'java' : '由于Java语言开发的电商平台具有安全性高、结构合理，高效、稳定、扩展性强，支持高并发量、采用集群式部署等特点，在开发方面相对于其他编程语言具有天然的优势，所以电商平台基本都是由Java开发而成。也许未来 Java 不是最有前景的语言，但是 Java 在未来很长一段时间内都会是不可或缺的语言，相关的工作岗位也自然一直有需求，而且 Java 语言的易学性也很高，适合新手。',
            'sql' : 'SQL是存储，检索和操作数据库中数据的标准查询语言。在技术上，它算不上编程语言，因为缺少循环和其他基本功能，但像PL / SQL这样的扩展已经添加了其中一些。 SQL在工作中需求非常高！',
            'python' : 'AI兴起，Python开始大热。Python是一种用于 Web 开发的通用编程语言，也是软件开发人员的支持语言。 它可广泛用于科学计算，数据挖掘和机器学习。人工智能大量依赖数据，而Python 在数据分析、数据挖掘方面实用性非常的强。机器学习开发人员的持续增长和职位需求可能正在推动Python的普及。',
            'javascript' : '超过 80％ 的开发者和 95％ 的网站都使用 JavaScript 来实现页面上的动态逻辑。 随着物联网和移动设备越来越流行，React 和 AngularJS 等 JavaScript前端框架具有巨大的未来潜力，所以我们可能很快就会看到 JavaScript 的普及。',
            'c++' : '作为老一辈语言 —— C语言的延伸， C++通常用于系统/应用软件，游戏开发，驱动程序，客户端服务器应用程序和嵌入式固件。许多程序员发现 C++ 比 Python 或 JavaScript 等语言更复杂，学习和使用起来也更困难，但它仍然在许多大型企业的遗留系统中使用。 ',
            'c#' : 'C＃是Microsoft设计的面向对象的编程语言，可以在微软的.NET平台上运行，并且比微软以前的语言更快更简单。像C++一样，C＃在视频游戏开发中被大量使用，所以任何有志的视频游戏开发者都应该好好学习这两门语言。',
            'web' : '随着互联网的告诉发展，广大的用户对于用户体验的不断提升，web前端对于整个IT行业的重视程度还在继续处于上升的趋势。web前端开发逐渐成为互联网时代软件产品研发中不可缺少的一部分，充当着重要的角色.',
            'android':'整体来说，Android开发领域趋于成熟稳定，已经走出了之前开荒的飞速成长时期。移动互联网整体仍在以相对很快的速度在成长，相应的技术需求也在持续。app的进化会对技术人员提出更高的要求。移动平台的延伸（VR，可穿戴，物联网，智能家居等）都在萌芽和创新尝试的阶段，也许几年内移动平台就会延伸到更大的领域。',
            'php':'从各个招聘网站的数据上来看PHP开发的职位非常多，薪资水平也非常不错。实际在中小企业、互联网创业公司PHP的市场地位是高于 Java 的。PHP 语言入门简单，容易掌握，程序健壮性好，不容易出现像 Java 、 C++ 等其他语言那样复杂的问题，如内存泄漏和 Crash ，跟踪调试相对轻松很多。',
            'ios': '国内对iOS开发这一领域还处在初级阶段，由于iOS入门门槛高，许多开发人才并没有过系统iOS学习，企业招聘到合适人才也是难上加难。如今传统行业，智能家居、游戏行业及汽车行业等，都将基于iOS系统开发进行转型，并逐渐走进人们的生活，可以预见未来几年，iOS开发人才市场仍旧会呈现供不应求的趋势。'
        }
        value = str()
        flag = True
        for x in l:
            if re.search(l[x], key, re.I):
                flag = False
                value = analyse[x]
        if flag:
            value = '在目前的行业发展状况来看，在近十年中，国内发展呈增长趋势，各大中小型企业的需求日益增长，要有很好的项目经验，对于这个行业，要有全局认识，工作选择的机会就越大。'
        # 没有勾选任何城市
        if len(app_citys) < 1:
            app_citys = ['北京', '上海', '广州', '深圳']
            for city in app_citys:
                sql = "select count(jobname) from app_hireinfo where lower(jobname) like '%%%s%%' and address like '%%%s%%'" % (key.lower(), city)
                la.append(self.sqlHelper.tupleToOther(self.sqlHelper.executeSql(sql)))
            best_city = app_citys[la.index(max(la))]
            return json.dumps(self.city_list_dict(la, app_citys)), best_city, value
        else:
            for city in app_citys:
                sql = "select count(jobname) from app_hireinfo where lower(jobname) like '%%%s%%' and address like '%%%s%%'" % (key.lower(), city)
                la.append(self.sqlHelper.tupleToOther(self.sqlHelper.executeSql(sql)))
            best_city = app_citys[la.index(max(la))]
            return json.dumps(self.city_list_dict(la, app_citys)), best_city, value