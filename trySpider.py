import re

data='<p class="name"><a href="/films/1215919" title="印度合伙人" data-act="boarditem-click" data-val="{movieId:1215919}">印度合伙人</a></p><p class="star">主演：阿克谢·库玛尔,拉迪卡·艾普特,索娜姆·卡普尔<p class="name"><a href="/films/123" title="龙猫" data-act="boarditem-click" data-val="{movieId:123}">龙猫</a></p><p class="star">主演：帕特·卡洛尔,蒂姆·达利,丽娅·萨隆加</p>'

# 下面定义正则表达式的时候，一定要把前后字符都定义好
# findall函数中，括号里的正则才会匹配
# 正则中使用？会匹配最近的符合条件的字符串
result = re.findall('title="(.*?)".*?主演：(.*?)<', data, re.S)
for (movie, star) in result:
    print("电影名：", movie, "主演：", star)
# print(result)
