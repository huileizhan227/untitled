from django.db import models

# Create your models here.
class Publisher(models.Model):
    '''
    出版商 - 名称，地址，所在城市，省，国家，网站
    '''
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()
    def __unicode__(self):
        # unicode() 方法告诉Python如何将对象以unicode的方式显示出来
        return self.name

class Author(models.Model):
    '''
    作者 - 姓，名，email地址
    '''
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    def __unicode__(self):
        return u"{} {}".format(self.first_name, self.last_name)

class Book(models.Model):
    '''
    书籍 - 书名，作者（一个或多个作者，和作者是多对多的关联关系[many-to-many]），
    出版商（和出版商是一对多的关联关系[one-to-many]，也被称作外键[foreign key]），
    出版日期
    '''
    title = models.CharField(max_length=100)
    author = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)  #ForeignKey中需要加上on_delete=models.CASCADE
    publication_date = models.DateField()
    def __unicode__(self):
        return self.title


