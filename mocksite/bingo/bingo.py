#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2019/1/10 15:07
#! @Auther : Yu Kunjiang
#! @File : bingo.py
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
import time
import requests
import logging

def bingo(request):
    return render(request, 'bingo.html')