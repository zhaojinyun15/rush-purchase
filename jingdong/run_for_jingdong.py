import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def webdriver_test():
    wd = webdriver.Chrome()
    wd.get('https://www.jd.com/')
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
                wd.find_element_by_link_text("加入购物车").click()
                print('"加入购物车" success')
                break
            except NoSuchElementException:
                pass
        while True:
            try:
                wd.find_element_by_link_text("去购物车结算").click()
                print('"去购物车结算" success')
                break
            except NoSuchElementException:
                pass
        while True:
            try:
                wd.find_element_by_link_text("去结算").click()
                print('"去结算" success')
                break
            except NoSuchElementException:
                pass


if __name__ == '__main__':
    webdriver_test()

