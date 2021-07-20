import datetime

from webdriver_rush import JingdongRush

if __name__ == '__main__':
    url = r'the goods page you want to purchase'
    ref_time = datetime.datetime.strptime('2020-01-01 12:00:00', '%Y-%m-%d %H:%M:%S')
    thread_num = 10

    for i in range(thread_num):
        ref_time = ref_time + datetime.timedelta(seconds=0.1)
        jd = JingdongRush(url=url, ref_time=ref_time, thread_name=f'thread_{i}')
        jd.start()
