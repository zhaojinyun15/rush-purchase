import time

from selenium import webdriver

from taobao import run_for_taobao


def webdriver_test():
    wd = webdriver.Chrome('/opt/homebrew/bin/chromedriver')
    # wd.get("https://www.tmall.com")
    wd.get("https://m.tb.cn/h.4CUZbB4?sm=de32de")
    # time.sleep(20)
    # wd.find_element_by_id('J_LinkBuy').click()
    wd.find_element_by_link_text("立即购买").click()
    time.sleep(0.01)
    wd.find_element_by_class_name('go-btn').click()
    time.sleep(60)

    # print('++++++++++++++')
    # print(wd.find_element_by_class_name("大会员"))
    # print(wd.find_element_by_name("大会员"))
    # wd.find_element_by_name("22bfbf13")
    # wd.find_element_by_id("22bfbf13")
    # wd.find_element_by_id('data-v-22bfbf13').click()
    # wd.find_element_by_link_text("请登录").click()
    # time.sleep(30)

    # wd.find_elements_by_class_name('name')


if __name__ == '__main__':
    run_for_taobao.webdriver_test()
