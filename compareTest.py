import pymongo
import time
import os
import sys
sys.path.append(r'C:\Users\lenovo\Desktop\毕业设计\code\app\mini_crawl')
from Toplist_song import Re_toplistSong
import matplotlib.pyplot as plt
# connect to database
client = pymongo.MongoClient()
db = client['crawl_data']

list_name = list(db['toplist'].find({}))
list_name.pop(20)
# begin crawl
begin_id = ''
time_list = []
for i in range(len(list_name)):
    time_dict = dict()
    time_dict['num'] = i+1
    begin_id += list_name[i]['id']

    # scrapy crawl
    time.sleep(3)
    start = time.time()
    run_str = r'cd C:\Users\lenovo\Desktop\毕业设计\code\app\crawler && scrapy crawl song'
    os.system(run_str + ' -a start_urls=' + begin_id + ' -s LOG_FILE=all.log')
    end = time.time()
    time_dict['scrapy'] = end - start

    # request crawl
    time.sleep(3)
    start = time.time()
    ts = Re_toplistSong(begin_id)
    ts.crawl()
    end = time.time()
    time_dict['request'] = end - start

    # add list
    time_list.append(time_dict)
    client['crawl_data']['compare_n'].insert_one(time_dict)
    print(time_dict)

    # update begin_id
    begin_id += '@'

#**************************************************
#  extract data from database and draw plot
#**************************************************
client = pymongo.MongoClient()
db = client['crawl_data']
result = list(db['compare_n'].find({}))

t_scrapy = []
t_request = []
num = []
for item in result:
    t_scrapy.append(item['scrapy'])
    t_request.append(item['request'])
    num.append(item['num'])

# gragh
plt.figure(figsize=(7,5))
plt.plot(num, t_scrapy, color = 'b', lw = 1.5, label = 'scrapy')
plt.plot(num, t_request, color = 'g', lw = 1.5, label = 'requests')
plt.xlabel('number of pages')
plt.ylabel('time (per second)')
plt.title('scrapy and requests compare')
plt.legend(loc = 0)
plt.show()

#***************************************************
#  calculate average seconds per page
#***************************************************
client = pymongo.MongoClient()
db = client['crawl_data']
result = list(db['compare_n'].find({}))

t_scrapy = 0
t_request = 0
for item in result:
    num = item['num']
    t_scrapy += item['scrapy'] / num
    t_request += item['request'] / num

t_scrapy = t_scrapy/29
t_request = t_request/29
print(t_scrapy)
print(t_request)