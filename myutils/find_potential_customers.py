#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2019/7/19 16:02
#! @Auther : Yu Kunjiang
#! @File : find_potential_customers.py

class VisitRecord():
    '''
    旅游记录
    找出那些去过普吉岛但没有去过新西兰的人

    针对某些无法放入集合或者字典的的对象，定义一个类，自定义__hash__和__eq__方法来实现
    '''

    def __init__(self,first_name, last_name, phone_number, date_visited):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.date_visited = date_visited

    def __hash__(self):
        return hash((self.first_name, self.last_name, self.phone_number))

    def __eq__(self, other):
        if isinstance(other, VisitRecord) and hash(other)==hash(self):
            return True
        return False

# 去过普吉岛的人员数据
users_visited_phuket = [
    {"first_name": "Sirena", "last_name": "Gross", "phone_number": "650-568-0388", "date_visited": "2018-03-14"},
    {"first_name": "James", "last_name": "Ashcraft", "phone_number": "412-334-4380", "date_visited": "2014-09-16"}
]

# 去过新西兰的人员数据
users_visited_nz = [
    {"first_name": "Justin", "last_name": "Malcom", "phone_number": "267-282-1964", "date_visited": "2011-03-13"},
    {"first_name": "Albert", "last_name": "Potter", "phone_number": "702-249-3714", "date_visited": "2013-09-11"},
    {"first_name": "James", "last_name": "Ashcraft", "phone_number": "412-334-4380", "date_visited": "2014-09-16"}
]

def find_potential_customers():
    # 返回类型：VisitRecord
    return set(VisitRecord(**r) for r in users_visited_phuket) - \
        set(VisitRecord(**r) for r in users_visited_nz)
customers = find_potential_customers()
for c in customers:
    print(c.first_name, c.last_name, c.phone_number, c.date_visited)