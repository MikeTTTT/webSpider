import time

import requests
import re
import xlwt

url = "https://www.lagou.com/jobs/positionAjax.json?city=%E5%B9%BF%E5%B7%9E&needAddtionalResult=false"

headers = {"Host": "www.lagou.com",
           "Referer": "https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?city=%E5%B9%BF%E5%B7%9E&cl=false&fromSearch=true&labelWords=&suginput=",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
           "X-Requested-With": "XMLHttpRequest"}


def getPage(url, i):
    data = {'first': 'false',
            'pn': i,
            'kd': '爬虫'}
    try:
        response = requests.get(url, data=data, headers=headers)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.json()
    except requests.ConnectionError as e:
        print(e)


def getInfo(json):
    json = json['content']['positionResult']['result']
    for item in json:
        info = {}
        info['companyId'] = item['companyId']
        info['companyFullName'] = item['companyFullName']
        info['cmpanyShortName'] = item['cmpanyShortName']
        info['district'] = item['district']
        info['positionName'] = item['positionName']
        info['salary'] = item['salary']
        info['workYear'] = item['workYear']
        info['city'] = item['city']
        info['companyLabelList'] = item['companyLabelList']
        yield info


def saveExcel(DATA):
    f = xlwt.Workbook(encoding='utf-8')
    sheet01 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)
    sheet01.write(0, 0, "companyId")
    sheet01.write(0, 1, "companyFullName")
    sheet01.write(0, 2, "cmpanyShortName")
    sheet01.write(0, 3, "district")
    sheet01.write(0, 4, "positionName")
    sheet01.write(0, 5, "salary")
    sheet01.write(0, 6, "workYear")
    sheet01.write(0, 7, "city")
    sheet01.write(0, 8, "companyLabelList")

    for i in range(len(DATA)):
        sheet01.write(i + 1, 0, DATA[i]['companyId'])
        sheet01.write(i + 1, 1, DATA[i]['companyFullName'])
        sheet01.write(i + 1, 2, DATA[i]['cmpanyShortName'])
        sheet01.write(i + 1, 3, DATA[i]['district'])
        sheet01.write(i + 1, 4, DATA[i]['positionName'])
        sheet01.write(i + 1, 5, DATA[i]['salary'])
        sheet01.write(i + 1, 6, DATA[i]['workYear'])
        sheet01.write(i + 1, 7, DATA[i]['city'])
        sheet01.write(i + 1, 8, DATA[i]['companyLabelList'])
        print('p', end='')
    f.save("E:\\spider\\laGou.xls")


Data = []
for i in range(1, 3):
    json = getPage(url, i)
    print(json)
    print('request:' + str(i) + url)
    time.sleep(2)
    datas = getInfo(json)
    for data in datas:
        Data.append(data)
saveExcel(Data)
