/**
 * Created by Cary on 2016/12/10.
 */

//判定
if (typeof (salary) != "undefined" ){
    showBar();
    $("#display").ready(function(){delete salary;});
}
if (typeof (lan) != "undefined" ){
    var title = "技能热度";
    showPie(title, lan);
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
    showPie(title, experience);
    $("#display").ready(function(){delete experience;});
}

if (typeof (companysize) != "undefined"){
    var title = "公司规模分布";
    var desc = ['1-99', '100-499',  '500-999', '1000-9999', '10000+', '保密'];
    showRose(title, desc, companysize);
    $("#display").ready(function(){delete companysize;});
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
