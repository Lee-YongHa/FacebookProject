import json
import matplotlib.pyplot as plt
from matplotlib import font_manager
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np

def makePrint(p, data):
    absolute = int(round(p/100.*np.sum(data)))
    return "{:.2f}%\n({:d})".format(p, absolute)

with open("./data/news_data.json", "r", encoding='utf-8') as filedata:
    newsdata = json.loads(filedata.read())

# pubDate 기준으로 정렬
sorted_arr = sorted(newsdata, key=lambda x: (x['pubDate']))
# print(sorted_arr)

now = datetime.now()    # 현재
time_period = "year"
num = 3

if time_period == "day":
    before_time = now - relativedelta(days=num)   # num일 전
elif time_period == "week":
    before_time = now - relativedelta(weeks=num)   # num주 전
elif time_period == "month":
    before_time = now - relativedelta(months=num)   # num달 전
elif time_period == "year":
    before_time = now - relativedelta(years=num)   # num년 전

result = {"코로나":0, "올림픽":0, "폭염":0}
for i in result:
    for j in sorted_arr:
        if datetime.strptime(j['pubDate'], '%Y-%m-%d %H:%M:%S') < before_time:  # pubDate 키의 값을 datetime 형식으로 변환
            continue
        else:
            # print(j['pubDate'])
            if (i in j['title']) or (i in j['description']) :
                result[i] += j['title'].count(i)
                result[i] += j['description'].count(i)

    print("keyword : %s, count : %d" %(i, result[i]))

news_data = list(result.items())

fontLocation = r"C:\Windows\Fonts\malgun.ttf"
fontName = font_manager.FontProperties(fname=fontLocation).get_name()
plt.rc('font', family=fontName)

fig = plt.figure(figsize=(8,5)) # 캔버스 생성
fig.set_facecolor('white') # 캔버스 배경색을 하얀색으로 설정
ax = fig.add_subplot() # 프레임 생성

# labels = []
# frequency = []
# for x, y in news_data:
#     labels.append(x)
#     frequency.append(y)

pie = ax.pie([i[1] for i in news_data],
            startangle=90,
            counterclock=False,
            autopct=lambda p: makePrint(p, [i[1] for i in news_data]),
            wedgeprops=dict(width=1),
            colors=['lightskyblue', 'lightgreen', 'lightpink'])

ax.set_title("Keyword Count Pie Chart")

plt.legend(pie[0], [i[0] for i in news_data],
        title="Keyword",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1))
plt.text(0, -1.3, '기간 : %s ~ %s' % (before_time.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m-%d %H:%M:%S")), verticalalignment='bottom' , horizontalalignment='center', fontsize=9)
plt.show()