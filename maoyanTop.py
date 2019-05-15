import requests
import re
import xlwt


def saveExcel(DATA):
    f = xlwt.Workbook(encoding='utf-8')
    sheet01 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)
    sheet01.write(0, 0, 'rank')
    sheet01.write(0, 1, "title")
    sheet01.write(0, 2, "actors")

    for i in range(len(DATA)):
        sheet01.write(i + 1, 0, DATA[i]['rank'])
        sheet01.write(i + 1, 1, DATA[i]['title'])
        sheet01.write(i + 1, 2, DATA[i]['actors'])
        print('p',end='')
    f.save("E:\\spider\\movieTop.xls")


def getPage(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(e)


def getInfo(page):
    items = re.findall('<i class="board-index board-index-(.*?)">.*?title="(.*?)".*?主演：(.*?)\n', page, re.S)
    for item in items:
        data = {}
        data['rank'] = item[0]
        data['title'] = item[1]
        data['actors'] = item[2]
        yield data


urls = ['https://maoyan.com/board/4?offset={}'.format(i * 10) for i in range(10)]

DATA = []
for url in urls:
    print(url)
    page = getPage(url)
    datas = getInfo(page)
    for data in datas:
        DATA.append(data)

print(DATA)
saveExcel(DATA)
