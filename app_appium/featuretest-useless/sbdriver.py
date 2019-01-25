import unittest
import time
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException

class SbDriver(unittest.TestCase):
    @classmethod
    def init_driver(cls, ip="localhost", version=""):
        if(not hasattr(SbDriver, "driver")):
            opts = {
                "platformName": "Android",
                "platformVersion": version,
                "deviceName": "Android",
                "appPackage": "com.sportybet.android",
                "appActivity": "com.sportybet.android.home.MainActivity",
                "automationName": "appium",
                "autoGrantPermissions": "true"
            }
            url = "http://{}:4723/wd/hub".format(ip)
            cls.driver = webdriver.Remote(url, opts)
            cls.driver.implicitly_wait(10)
        return cls.driver
    
    @classmethod
    def click(cls, e_id):
        try:
            el = cls.driver.find_element_by_id(e_id)
        except NoSuchElementException:
            return False
        el.click()
        return True
    
    @classmethod
    def set_value(cls, e_id, value):
        try:
            el = cls.driver.find_element_by_id(e_id)
        except NoSuchElementException:
            return False
        el.set_value(value)
        time.sleep(1)
        cls.try_hide_keyboard()
        return True
    
    @classmethod
    def get_bottom_els(cls):
        try:
            el_bottom = cls.driver.find_element_by_id("android:id/tabs")
        except NoSuchElementException:
            return []
        els = el_bottom.find_elements_by_class_name(
            "android.widget.RelativeLayout"
        )
        return els

    @classmethod
    def try_hide_keyboard(cls):
        try:
            cls.driver.hide_keyboard()
        except:
            pass
    
    @classmethod
    def back(cls):
        cls.driver.press_keycode(4)
    
    @classmethod
    def set_country(cls, country="ke"):
        if(country == "ke"):
            cls.phone = "0792338137"
            region_text = "Kenya"
        elif(country == "ng"):
            cls.phone = "8146610183"
            region_text = "Nigeria"
        elif(country == "gh"):
            cls.phone = "240087457"
            region_text = "Ghana"
        cls.pwd = "qwe123"
        els = cls.get_bottom_els()
        els[-1].click()
        time.sleep(5) #wait for deposit pop
        cls.click("com.sportybet.android:id/general")
        
        el = cls.driver.find_element_by_id("com.sportybet.android:id/country")
        if(el.text == region_text):
            # back to homepage
            cls.back()
            time.sleep(1)
            els[0].click()
        else:
            ##
            el = cls.driver.find_element_by_id(
                "com.sportybet.android:id/change_region"
            )
            el.click()
            resource_id = "com.sportybet.android:id/{}".format(country)
            try:
                cls.click(resource_id)
                time.sleep(10)
                cls.click("com.sportybet.android:id/skip")
            except NoSuchElementException:
                return False
        return True

    # @classmethod
    # def login(cls):
    #     SbDriver.init_driver()
    #     SbDriver.click("com.sportybet.android:id/login")
    #     SbDriver.set_value("com.sportybet.android:id/mobile", "")
