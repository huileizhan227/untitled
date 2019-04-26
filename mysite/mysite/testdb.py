#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2018/11/19 15:38
#! @Auther : Yu Kunjiang
#! @File : testdb.py

from django.http import HttpResponse
from TestModel.models import Test

# 数据库操作
def testdb(request):
    test1 = Test(name='runoob')
    test1.save()
    return HttpResponse("<p.html>数据添加成功！</p.html>")

def testdb_get_data(request):
    # 初始化
    reponse = ""
    response1 = ""

    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
    list = Test.objects.all()

    # filter相当于SQL中的WHERE，可设置条件过滤结果
    response2 = Test.objects.filter(id=1)

    # 获取单个对象
    response3 = Test.objects.get(id=1)

    # 限制返回的数据 相当于 SQL 中的 OFFSET 0 LIMIT 2;
    Test.objects.order_by('name')[0:2]

    # 数据排序
    Test.objects.order_by("id")

    # 上面的方法可以连锁使用
    Test.objects.filter(name='runoob').order_by('id')

    # 输出所有数据
    for var in list:
        response1 += var.name + " "
    response = response1
    return HttpResponse("<p.html>" + response + "</p.html>")

def testdb_update(request):
    # 修改其中一个id=1的name字段，再save，相当于SQL中的UPDATE
    test1 = Test.objects.get(id=1)
    test1.name = 'Google'
    test1.save()
    #另一种方法
    Test.objects.filter(id=2).update(name="Baidu")
    # 修改所有的列
    Test.objects.all().update(name='Netease')

    return HttpResponse("<p.html>修改成功</p.html>")

def testdb_delete(request):
    test1 = Test.objects.get(id=1)
    test1.delete()
    # 另一种方法
    Test.objects.filter(id=2).delete()
    # 删除所有数据
    Test.objects.all().delete()
    return HttpResponse("<p.html>删除成功</p.html>")




