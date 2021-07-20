import abc
import datetime
import logging
import threading
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import log_factory


class MyRush(threading.Thread, metaclass=abc.ABCMeta):
    def __init__(self, url, ref_time, thread_name, driver=None, log_level=None):
        super().__init__()
        self.url = url
        self.ref_time = ref_time
        self.setName(thread_name)

        # create a webdriver
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # options.add_experimental_option('prefs', {"profile.managed_default_content_settings.images": 2})
        if driver is None:
            self.wd = webdriver.Chrome(options=options)
        else:
            self.wd = webdriver.Chrome(executable_path=driver, options=options)

        # create a logger
        self._log_init(log_level)

    def _log_init(self, log_level):
        self.logger = logging.getLogger(str(self))
        self.logger.setLevel(logging.INFO if log_level is None else log_level)
        self.logger.addHandler(log_factory.h1)
        self.logger.addHandler(log_factory.h2)

    def __del__(self):
        pass

    def wd_quit(self):
        self.wd.quit()

    def url_test(self):
        self.wd.get(self.url)
        self.logger.info('url test success')
        time.sleep(300)

    def login(self):
        self.logger.info('Please login in 60 seconds!')
        time.sleep(120)

    @abc.abstractmethod
    def run(self):
        pass


class TaobaoRush(MyRush):
    def login(self):
        super(TaobaoRush, self).login()

    def run(self):
        self.wd.get(self.url)
        self.login()
        while True:
            while True:
                try:
                    self.wd.find_element_by_link_text("立即购买").click()
                    self.logger.info('"立即购买" success')
                    break
                except NoSuchElementException as e:
                    self.logger.debug('"立即购买" failed')
                    self.logger.debug(e.stacktrace)
            while True:
                try:
                    self.wd.find_element_by_class_name('go-btn').click()
                    self.logger.info('"提交订单" success')
                    break
                except NoSuchElementException as e:
                    self.logger.debug('"提交订单" failed')
                    self.logger.debug(e.stacktrace)


class JingdongRush(MyRush):
    def run(self):
        self.wd.get(self.url)
        self.login()
        self._check_ref_time(self.ref_time)
        self.wd.get(self.url)
        while True:
            try:
                self.wd.find_element_by_link_text("加入购物车").click()
                self.logger.info('"加入购物车" success')
                break
            except NoSuchElementException:
                self.logger.debug('"加入购物车" failed')
        while True:
            try:
                self.wd.find_element_by_link_text("去购物车结算").click()
                self.logger.info('"去购物车结算" success')
                break
            except NoSuchElementException:
                self.logger.debug('"去购物车结算" failed')
        while True:
            try:
                self.wd.find_element_by_link_text("去结算").click()
                self.logger.info('"去结算" success')
                break
            except NoSuchElementException:
                self.logger.debug('"去结算" failed')
        while True:
            try:
                self.wd.find_element_by_id('order-submit').click()
                self.logger.info('"提交订单" success')
                break
            except NoSuchElementException:
                self.logger.debug('"提交订单" failed')
        while True:
            pass

    def _check_ref_time(self, ref_time):
        self.logger.info(f'ref_time: {str(ref_time)}')
        while True:
            now = datetime.datetime.now()
            if now >= ref_time:
                break
            self.logger.debug('now < ref_time')
        self.logger.info('now time is greater than ref_time')


if __name__ == '__main__':
    # tb = TaobaoRush('https://www.taobao.com')
    # tb.url_test()
    jd = JingdongRush('https://www.jd.com/', '2021-07-20 21:31:00')
    jd.url_test()
