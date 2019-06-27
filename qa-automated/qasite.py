import os
import time
import requests

from config.config_main import UPLOAD_URL

def upload_report(file, report_type, project_name, build_id):
    """upload report

    args:
    - file: report file.
    - report_type: 
        - 0: AUTOMATION
        - 1: PERFORMANCE
    - project_name: project name.
    - build_id: build id.
    """
    for i in range(3):
        if not os.path.exists(file):
            raise Exception('file does not exist')
        
        data = {
            'report_type': report_type,
            'project_name': project_name,
            'build_id': build_id
        }
        files = {'file': file}
        
        response = requests.post(UPLOAD_URL, data=data, files=files)
        status_code = response.status_code
        if status_code != 200:
            print('upload report failed: {}, retrying'.format(status_code))
            time.sleep(10)
            continue
        else:
            return True
    return False