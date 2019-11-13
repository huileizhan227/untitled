import os

def get_crash_log(log_path, file_coding):
    # file_name = os.path.basename(log_path)
    log = log_path + '\n'
    with open(log_path, 'rb') as file:
        line = file.readline().decode(file_coding)
        while line:
            line = file.readline().decode(file_coding)
            if (
                'beginning of crash' in line or
                ('AndroidRuntime' in line and 'com.transsnet.news.more' in line)
            ):
                log += line
                while line:
                    line = file.readline().decode(file_coding)
                    if line.strip() == '':
                        continue
                    elif 'AndroidRuntime' in line:
                        log += line
                    else:
                        line += '\n'
                        break
    return log

def get_all_crash_in_folder(log_folder, name_filter='logcat', file_coding='utf-8'):
    log = ''
    for dirpath, dirnames, filenames in os.walk(log_folder):
        for file_name in filenames:
            if name_filter not in file_name:
                continue
            log += '\n---------------------------\n'
            log += get_crash_log(os.path.join(dirpath, file_name), file_coding)
    return log

def to_file(log_folder, file_path):
    with open(file_path, 'w') as f:
        f.write(get_all_crash_in_folder(log_folder))

def collect_anr(log_folder, anr_folder, name_filter='monkey', file_coding='utf-8'):
    file_list = os.listdir(log_folder)
    if not os.path.exists(anr_folder):
        os.makedirs(anr_folder)
    for file_name in file_list:
        if name_filter not in file_name:
            continue
        file_path = os.path.join(log_folder, file_name)
        if not os.path.isfile(file_path):
            continue
        with open(file_path, 'rb') as file:
            raw = file.read().decode(file_coding)
        if 'ANR in com.transsnet.news' in raw:
            new_path = os.path.join(anr_folder, file_name)
            with open(new_path, 'wb') as file:
                file.write(raw.encode(file_coding))


if __name__ == "__main__":
    log = get_all_crash_in_folder('.', 'logcat')
    print(log)
