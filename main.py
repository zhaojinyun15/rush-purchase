import conf
from webdriver_rush import JingdongRush, TaobaoRush


def run_jd(my_conf):
    thread_num = my_conf['thread_num']
    for i in range(thread_num):
        jd = JingdongRush(my_conf, f'thread_{i}')
        jd.start()


def run_tb(my_conf):
    thread_num = my_conf['thread_num']
    for i in range(thread_num):
        tb = TaobaoRush(my_conf, f'thread_{i}')
        tb.start()


if __name__ == '__main__':
    # run jingdong or taobao
    run_jd(conf.JINGDONG_CONF)
    # run_tb(conf.TAOBAO_CONF)
