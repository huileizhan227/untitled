import zipfile
import getopt
import shutil
import sys
import os

def unzip_file_with_encoding(from_file, to_path, zip_encoding='cp437'):
    sys_encoding = sys.getdefaultencoding()
    if not os.path.exists(from_file):
        raise ValueError('{} not exists.'.format(from_file))
    if os.path.exists(to_path):
        raise ValueError('{} exists.'.format(to_path))
    os.makedirs(to_path)
    with zipfile.ZipFile(from_file, 'r') as zip_ref:
        for info in zip_ref.filelist:
            name = info.filename
            new_name = name.encode(zip_encoding).decode(sys_encoding)
            new_name = new_name.replace('/', os.sep).replace('?','_')
            new_path = os.path.join(to_path, new_name)
            if new_path.endswith(os.sep):
                os.makedirs(new_path)
                continue
            with open(new_path, 'wb') as new_file:
                with zip_ref.open(name) as file:
                    shutil.copyfileobj(file, new_file)

def unzip_file(input, output):
    '''Unzip file.
    Args:
        input (str): Zip file.
        output (str): Target directory.
    '''
    with zipfile.ZipFile(input, 'r') as zip:
        zip.extractall(output)

def zip_file(directory, output):
    '''Create a zip file.
    Args:
        directory (str): Directory to be compressed.
        output (str): Output file .zip.
    '''
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk(directory):
            for file in files:
                filename = os.path.join(root, file)
                if os.path.isfile(filename):
                    arcname = os.path.join(os.path.relpath(root, directory), file)
                    zip.write(filename, arcname)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('at least 2 args needed')
    opts, args = getopt.getopt(sys.argv[1:], shortopts='e')
    with_encode = False
    for opt, value in opts:
        if opt == '-e':
            with_encode = True
    path1 = args[0]
    path2 = args[1]
    if os.path.isdir(path1):
        zip_file(path1, path2)
    elif with_encode:
        print('unzip with encoding')
        unzip_file_encoding(path1, path2)
    else:
        unzip_file(path1, path2)
