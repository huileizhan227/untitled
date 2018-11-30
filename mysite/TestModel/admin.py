from django.contrib import admin
from TestModel.models import Test, Contact, Tag

# Register your models here.
#admin.site.register([Test, Contact, Tag])
#admin.site.register(Test)

#使用内联显示，让 Tag 附加在 Contact 的编辑页面上显示
class TagInline(admin.TabularInline):
    model = Tag

class ContactAdmin(admin.ModelAdmin):
    #fields = ('name', 'email')      #fields定义了要显示的字段
    inlines = [TagInline]       #inline
    list_display = ('name', 'age', 'email')     #list
    search_fields = ('name','email')    #搜索功能
    fieldsets = (
        ['Main', {'fields':('name', 'email')}],         #展示的属性
        ['Advance', {'classes':('collapse',), 'fields':('age',)}]   #隐藏的属性
    )

class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')

admin.site.register(Contact, ContactAdmin)  #add时隐藏age项
admin.site.register(Test, TestAdmin)