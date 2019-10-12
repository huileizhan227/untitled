import os
import time
import base64

def get_formated_time():
    """get formated time string

    use format: %Y%m%d.%H%M%S

    ex. 20190730.175907
    """
    return time.strftime('%Y%m%d.%H%M%S')

def base64_to_file(b64_raw, save_path):
    dir_name = os.path.dirname(save_path)
    if(not os.path.exists(dir_name)):
        os.makedirs(dir_name)
    b_data = base64.b64decode(b64_raw)
    with open(save_path, 'wb') as f:
        f.write(b_data)
