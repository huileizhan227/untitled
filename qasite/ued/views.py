import os
import sys
import shutil
import zipfile
import logging
import urllib.parse

from . import unzip
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.http import Http404

UED_ROOT = os.path.join(settings.MEDIA_ROOT, 'ued')
UED_TMP_PATH = os.path.join(UED_ROOT, 'tmp')
UED_CONTENT_PATH = os.path.join(UED_ROOT, 'content')
UED_CONTENT_RELATIVE_PATH = 'ued/content'

logger = logging.getLogger('django')

def index(request):
    # debug: encoding
    logger.debug('sys.getdefaultencoding(): {}'.format(sys.getdefaultencoding()))
    logger.debug('sys.getfilesystemencoding(): {}'.format(sys.getfilesystemencoding()))

    context = None
    if os.path.exists(UED_CONTENT_PATH) and os.path.isdir(UED_CONTENT_PATH):
        platforms = os.listdir(UED_CONTENT_PATH)
        context = {'platform_list': platforms}
    return render(request, 'ued/index.html', context=context)


def platform(request, platform_name):
    platform_name = urllib.parse.unquote(platform_name)
    platform_path = os.path.join(UED_CONTENT_PATH, platform_name)
    if not os.path.exists(platform_path):
        raise Http404()
    version_list = os.listdir(platform_path)
    context = {
        'platform_name': platform_name,
        'version_list': version_list
    }
    return render(request, 'ued/platform.html', context=context)

def detail(request, platform_name, version):
    platform_name = urllib.parse.unquote(platform_name)
    version = urllib.parse.unquote(version)
    doc_path = os.path.join(UED_CONTENT_PATH, platform_name, version, 'index.html')
    doc_relative_path = os.path.join(
        UED_CONTENT_RELATIVE_PATH, platform_name, version, 'index.html'
    )
    if not os.path.exists(doc_path):
        raise Http404()
    fs = FileSystemStorage()
    doc_url = fs.url(doc_relative_path)
    context = {
        'platform_name': platform_name,
        'version': version,
        'doc_url': doc_url
    }
    return render(request, 'ued/detail.html', context=context)

def upload(request):
    if request.method == 'GET':
        raise Http404()
    zip_file = request.FILES['file']
    platform = request.POST['platform']
    version = request.POST['version']
    platform = platform.replace(' ', '_')
    version = version.replace(' ', '_')

    fs = FileSystemStorage(UED_TMP_PATH)
    file_name = fs.save(zip_file.name, zip_file)
    zip_path = os.path.join(UED_TMP_PATH, file_name)
    
    ued_version_path = os.path.join(UED_CONTENT_PATH, platform, version)
    if os.path.exists(ued_version_path):
        shutil.rmtree(ued_version_path)
    unzip.unzip_file_with_encoding(zip_path, ued_version_path)
    ued_folder = ''
    for folder, sub_folders, sub_files in os.walk(ued_version_path):
        for sub_file in sub_files:
            if sub_file == 'index.html':
                ued_folder = folder
    if ued_folder and ued_folder != ued_version_path:
        for name_ in os.listdir(ued_folder):
            path_ = os.path.join(ued_folder, name_)
            shutil.move(path_, ued_version_path)

    shutil.rmtree(UED_TMP_PATH)
    return HttpResponse('upload success')

def reset(request):
    if request.method == 'GET':
        raise Http404()
    if os.path.exists(UED_CONTENT_PATH):
        shutil.rmtree(UED_CONTENT_PATH)
    return HttpResponse('ok')
