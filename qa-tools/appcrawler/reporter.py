import os
import shutil

def report(report_folder):
    all_folder = os.path.join(report_folder, 'all')
    if os.path.exists(all_folder):
        raise Exception('{} already exists'.format(all_folder))
    dir_list = os.listdir(report_folder)
    os.makedirs(all_folder)
    for dir_name in dir_list:
        _folder = os.path.join(report_folder, dir_name)
        file_list = os.listdir(_folder)
        for file_name in file_list:
            file_path = os.path.join(_folder, file_name)
            if os.path.isfile(file_path) and file_path.endswith('.png'):
                new_file_name = '{}.{}'.format(dir_name, file_name)
                new_file_path = os.path.join(all_folder, new_file_name)
                shutil.copyfile(file_path, new_file_path)
