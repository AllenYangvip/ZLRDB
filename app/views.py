from django.shortcuts import render,render_to_response,redirect,HttpResponse
from app import models
from app.core import zlinfo
import xlwt,datetime

# Create your views here.
info = []


def index(request):
    global info
    info = []
    if request.method == 'POST':
        data = []
        print("first data",data)
        zw = request.POST.get('zw')
        dd = request.POST.get('dd')

        print(zw,"----",dd)
        if dd == '':
            dd = '全国'
        page = 1
        info.append(zw)
        info.append(dd)
        if dd == '全国':
            print('全国范围')
            data = models.ZLInfo.objects.filter(name__icontains=zw)
        else:
            print('%s范围'%dd)
            data = models.ZLInfo.objects.filter(name__icontains=zw, location=dd)
        print("second data",data)
        if not data:
            if dd == '全国':
                print('======全国范围')
                data = zlinfo.main(zw, page)
            else:
                print('======%s范围' % dd)
                data = zlinfo.main(zw, page, dd)
            for item in data:
                dataobj = models.ZLInfo(name=item['name'], company=item['company'], salary=item['salary'],
                                        location=item['location'], time=item['time'], zw_url=item['zw_url'],
                                        cp_url=item['cp_url'])
                dataobj.save()
        print("----------------",data)
        return render(request, "infomation.html", {'querset': data})
    else:
        return render(request,"index.html")


def export(request):
    global info
    name = info[0]+"职位表"
    if info[1] == '全国':
        print('全国范围')
        data = models.ZLInfo.objects.filter(name__icontains=info[0])
    else:
        print('%s范围' % info[1])
        data = models.ZLInfo.objects.filter(name__icontains=info[0], location=info[1])
    print('111111111export data:',data)
    data_list = []
    headers = ['职位', '公司', '地点', '工资', '发布时间', '职位URL', '公司URL']
    # 格式化数据
    for i in data:
        row = []
        row.append(i.name)
        row.append(i.company)
        row.append(i.location)
        row.append(i.salary)
        row.append(i.time)
        row.append(i.zw_url)
        row.append(i.cp_url)
        data_list.append(row)
    print(data_list)
    # 实例化一个Workbook()对象(即excel文件)
    wbk = xlwt.Workbook()
    # 新建一个名为Sheet1的excel sheet。此处的cell_overwrite_ok =True是为了能对同一个单元格重复操作。
    sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
    j = 0
    for i in headers:
        sheet.write(0, j, i)
        j += 1
    i = 1
    for item in data_list:
        j = 0
        for initem in item:
            sheet.write(i, j, initem)
            j += 1
        i += 1
    wbk.save('111.xls')
    return HttpResponse("true")