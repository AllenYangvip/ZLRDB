from django.db import models

# Create your models here.
class ZLInfo(models.Model):
    ''' 'name': name.get_text(),
    'company': company.get_text(),
    'salary': salary.get_text(),
    'location': location.get_text(),
    'time': time.get_text(),
    'zw_url': url1.get("href"),
    'cp_url': url2.get("href")'''
    name = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    salary = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    time = models.CharField(max_length=20)
    zw_url = models.CharField(max_length=50)
    cp_url = models.CharField(max_length=50)
    date = models.DateField(auto_now=True)

