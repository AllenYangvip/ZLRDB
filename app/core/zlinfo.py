#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Allen Yang
import requests
from bs4 import BeautifulSoup
import urllib.parse
from app import models
data_list=[]
def get_zhaopin(page, zhiwei, jl):
    """
    :param page:显示的页数用户需要搜索几页就搜索几页默认为5
    :param zhiwei: 用户搜索的职位
    :param jl: 针对的搜索范围例：全国、北京、上海、杭州
    :return:
    """
    global data_list
    url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl={0}&kw={1}&p={2}'.format(jl,zhiwei,page)
    print (url)
    print("第{0}页".format(page))
    wbdata = requests.get(url).content

    soup = BeautifulSoup(wbdata,'lxml')
    job_name = soup.select("table.newlist > tr > td.zwmc > div > a")
    gsmc = soup.select("table.newlist > tr > td.gsmc  > a")
    zwurl = soup.find_all("a", attrs={"style": "font-weight: bold"})
    salarys = soup.select("table.newlist > tr > td.zwyx")
    locations = soup.select("table.newlist > tr > td.gzdd")
    times = soup.select("table.newlist > tr > td.gxsj > span")
    # 将得出的公司名称再次过滤以获取url
    soup2 = BeautifulSoup(str(gsmc),'lxml')
    gsurl=soup2.find_all("a", attrs={"target":"_blank"})
    # print(gsurl[0].get("href"))
    # print "职位：{0}  工资：{1} 地点：{2} 时间：{3} URL：{4}".format(job_name,salarys,locations,times,base_url)


    for name,company, salary, location, time, url1 ,url2  in zip(job_name, gsmc, salarys, locations, times, zwurl,gsurl):
        data = {
            'name': name.get_text(),
            'company' : company.get_text(),
            'salary': salary.get_text(),
            'location': location.get_text(),
            'time': time.get_text(),
            'zw_url': url1.get("href"),
            'cp_url': url2.get("href")
            # '职位': name.get_text(),
            # '公司':company.get_text(),
            # '工资': salary.get_text(),
            # '地点': location.get_text(),
            # '时间': time.get_text(),
            # '职位URL': url1.get("href"),
            # '公司URL': url2.get("href")


        }
        if data['name'] != '' and data['name'] != '\xa0' and data['company'] != ''and data['company'] != '\xa0'and data['salary']!= '' and data['location']!= '' and data['zw_url']!= '' and data['cp_url']!= '':
            data_list.append(data)
def main(zw, item=5, dd='全国'):
    """
        This function was interface for users.The can use this fuction to get the recruitment infomation
        that they wanted.
    :param zw:搜索的职位
    :param item:搜索的页数
    :param dd:针对的地址范围
    :return:
    """
    global data_list
    data_list = []
    try:
        new_zw = urllib.parse.quote(zw) # 采用Python3 urllib中的parse.quote 将搜索职位进行转换
        if int(item) < 1:
            item = 1
    except Exception as e:
        item = 1
    for i in range(1, item+1):
            get_zhaopin(i, new_zw,dd)
    return data_list

if __name__ == '__main__':
    main('C++', 1,'北京')