#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2018/12/3 14:36
#! @Auther : Yu Kunjiang
#! @File : forms.py

from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    email = forms.EmailField(required=False, label='Your e-mail address')            #非必填项
    message = forms.CharField(widget=forms.Textarea)    #变成一个textarea

    def clean_message(self):
        '''
        Django的form系统自动寻找匹配的函数方法，该方法名称以clean_开头，并以字段名称结束。 如果有这样的方法，它将在校验时被调用。
        '''
        message = self.cleaned_data['message']
        num_of_words = len(message.split())
        if num_of_words<4:
            raise forms.ValidationError("Not enough words!")
        return message
