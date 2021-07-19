import abc
import logging
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class MyRush(metaclass=abc.ABCMeta):
    def __init__(self, url, driver=None, log_level=None):
        self.url = url
        if driver is None:
            self.wd = webdriver.Chrome()
        else:
            self.wd = webdriver.Chrome(driver)
        self._log_init(log_level)

    def _log_init(self, log_level):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(threadName)s [%(levelname)s] : %(message)s')
        self.logger = logging.getLogger(str(self))
        self.logger.setLevel(logging.INFO if log_level is None else log_level)

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
        time.sleep(60)

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


if __name__ == '__main__':
    tb = TaobaoRush('https://www.taobao.com')
    tb.url_test()
