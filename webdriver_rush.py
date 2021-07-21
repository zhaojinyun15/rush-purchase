import abc
import datetime
import logging
import threading
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver import DesiredCapabilities, ActionChains

import log_factory


class MyRush(threading.Thread, metaclass=abc.ABCMeta):
    def __init__(self, my_conf, thread_name=None):
        super().__init__()
        self.url = my_conf['url']
        self.ref_time = datetime.datetime.strptime(my_conf['ref_time_str'], '%Y-%m-%d %H:%M:%S')
        self.advance_time = self.ref_time - datetime.timedelta(minutes=1)
        self.account = my_conf.get('account')
        self.password = my_conf.get('password')
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
        self.chains = ActionChains(self.wd)

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
        # this code block can skip the slide verification!!!
        self.wd.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": '''
                    Object.defineProperty(navigator, 'webdriver', {
                      get: () => undefined
                    })
                  '''
        })
        self.wd.get('https://login.taobao.com/member/login.jhtml?')
        if self.account is None or self.password is None:
            self.logger.warning('account or password missing! please login by hand!')
            super(TaobaoRush, self).login()
        else:
            account_frame = self.wd.find_element_by_id('fm-login-id')
            account_frame.send_keys(self.account)
            password_frame = self.wd.find_element_by_id('fm-login-password')
            password_frame.send_keys(self.password)
            time.sleep(1)
            """
            # deal with slider
            try:
                # if has slider  //*[@id='nc_2_n1z']
                slider = self.wd.find_element_by_xpath("//*[@id='nc_2_n1z']")
                # drag the slider
                self.chains.drag_and_drop_by_offset(slider, 258, 0).perform()
                time.sleep(0.5)
                # release the slider
                self.chains.release().perform()
            except (NoSuchElementException, WebDriverException) as e:
                self.logger.warning('verification code slider does not work')
            """
            self.wd.find_element_by_xpath("//button[@class='fm-button fm-submit password-login']").click()
            self.logger.info('login success')

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
        self.wd.get('https://passport.jd.com/new/login.aspx?')
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
