import abc
import datetime
import logging
import threading
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import DesiredCapabilities

import log_factory


class MyRush(threading.Thread, metaclass=abc.ABCMeta):
    def __init__(self, my_conf, thread_name=None):
        super().__init__()
        self.url = my_conf['url']
        self.ref_time = datetime.datetime.strptime(my_conf['ref_time_str'], '%Y-%m-%d %H:%M:%S')
        self.advance_time = self.ref_time - datetime.timedelta(minutes=1)
        if thread_name is not None:
            self.setName(thread_name)

        # create a webdriver
        self._web_driver_init(my_conf.get('driver'))

        # create a logger
        self._log_init(my_conf.get('log_level'))

    def _web_driver_init(self, driver):
        # set options
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # options.add_experimental_option('prefs', {"profile.managed_default_content_settings.images": 2})
        # set page load strategy
        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities["pageLoadStrategy"] = "normal"
        if driver is None:
            self.wd = webdriver.Chrome(options=options, desired_capabilities=desired_capabilities)
        else:
            self.wd = webdriver.Chrome(executable_path=driver, options=options,
                                       desired_capabilities=desired_capabilities)

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
        login_time = 180
        self.logger.info(f'Please login in {login_time} seconds!')
        time.sleep(login_time)

    def _wait(self):
        self.logger.info('wait until advance time')
        self.logger.info(f'ref_time: {str(self.ref_time)}')
        self.logger.info(f'advance_time: {str(self.advance_time)}')
        while True:
            now = datetime.datetime.now()
            if now >= self.advance_time:
                break
            self.logger.debug('now < advance_time')
        self.logger.info('now time is greater than advance_time')

    @abc.abstractmethod
    def run(self):
        pass


class TaobaoRush(MyRush):
    def login(self):
        super(TaobaoRush, self).login()

    def run(self):
        self.login()
        self._wait()
        while True:
            try:
                self.wd.get(self.url)
                self.wd.find_element_by_link_text("立即购买").click()
                self.logger.info('"立即购买" success')
                break
            except NoSuchElementException:
                self.logger.debug('"立即购买" failed')
        while True:
            try:
                self.wd.find_element_by_class_name('go-btn').click()
                self.logger.info('"提交订单" success')
                break
            except NoSuchElementException:
                self.logger.debug('"提交订单" failed')
        while True:
            pass


class JingdongRush(MyRush):
    def login(self):
        self.wd.get('https://www.jd.com/')
        self.wd.find_element_by_link_text("你好，请登录").click()
        super(JingdongRush, self).login()

    def run(self):
        self.login()
        self._wait()
        while True:
            try:
                self.wd.get(self.url)
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


if __name__ == '__main__':
    # tb = TaobaoRush('https://www.taobao.com')
    # tb.url_test()
    # jd = JingdongRush('https://www.jd.com/', '2021-07-20 21:31:00')
    # jd.url_test()
    pass
