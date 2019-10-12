country_name_dict = {
    '1': 'KE',
    '2': 'NG',
    '3': 'EG',
    '5': 'ZA',
    '8': 'GH',
    '9': 'UG',
}

country_lang_dict = {
    '1': ['en'],
    '3': ['ar'],
    '2': ['en'],
    '5': ['en'],
    '8': ['en'],
    '9': ['en'],
}

oper_list = [1, 2, 3, 5, 8, 9] # 当前可用的所有oper id
auto_oper_list = [1, 2, 3, 5, 8, 9] # 系统可以自动选择国家的oper id

def get_country_name_by_oper_id(oper_id):
    return country_name_dict.get(str(oper_id), 'None')
