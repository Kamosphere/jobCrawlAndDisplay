/**
 * Created by Cary on 2016/12/10.
 */

//判定
if (typeof (salary) != "undefined" ){
    showBar();
    $("#display").ready(function(){delete salary;});
}
if (typeof (lan) != "undefined" ){
    var title = "语言热度";
    var desc = ['java','c++', 'python', 'javascript', 'php', 'c#', 'sql',  'android', 'ios', 'web'];
    showPie(title, desc, lan);
    $("#display").ready(function(){delete lan;});
}

if (typeof (education) != "undefined" ){
    var title = "学历分布";
    var desc = ['不限', '大专',  '本科', '硕士', '博士'];
    showRing(title, desc, education);
    $("#display").ready(function(){delete education;});
}

if (typeof (experience) != "undefined"){
    var title = "经验需求分布";
    var desc = ['1-3年', '3-5年',  '5-8年', '8-10年', '不限'];
    showPie(title, desc, experience);
    $("#display").ready(function(){delete experience;});
}

if (typeof (citys) != "undefined"){
    showChinaMap();
    $("#display").ready(function(){delete citys;});

}
if (typeof (ask) != "undefined"){
    showWordle();
    $("#display").ready(function(){delete ask;});
}
if (typeof (heat_lan) != "undefined"){
    showHeat();
   $("#display").ready(function(){delete heat_lan;});
}
