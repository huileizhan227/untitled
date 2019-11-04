import follow_main_page_test as follow

country = follow.get_country_by_oper_id(4)

follow.get_follow_info_list_by_country(country, 'tmp.csv')
