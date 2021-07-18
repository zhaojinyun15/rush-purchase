import sys
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def webdriver_test():
    wd = webdriver.Chrome()
    wd.get('https://www.taobao.com/')
    time.sleep(300)


def login():
    print('Please login in 60 seconds!')
    time.sleep(60)


def run(url):
    wd = webdriver.Chrome()
    wd.get(url)
    login()
    while True:
        while True:
            try:
                wd.find_element_by_link_text("立即购买").click()
                print('"立即购买" success')
                break
            except NoSuchElementException:
                pass
        while True:
            try:
                wd.find_element_by_class_name('go-btn').click()
                print('"提交订单" success')
                break
            except NoSuchElementException:
                pass


if __name__ == '__main__':
    webdriver_test()

